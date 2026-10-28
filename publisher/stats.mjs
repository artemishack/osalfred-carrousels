// Collecte des statistiques des posts publiés (Instagram + Facebook) et écriture dans Notion.
// Appelé par index.mjs après la publication. Tolérant : une métrique refusée par Meta est ignorée.
//
// Rythme : stories toutes les heures pendant 24 h (Meta les efface ensuite),
// autres posts toutes les 6 h pendant 30 jours.

const HOUR = 3600e3;

export async function collectStats({ notion, graph, log, deadline, dry }) {
  if (Date.now() > deadline) return;
  const since = new Date(Date.now() - 30 * 24 * HOUR).toISOString();
  const res = [];
  let cursor;
  do {
    const j = await notion(`databases/${process.env.NOTION_DB_ID}/query`, "POST", {
      filter: { and: [
        { property: "Statut", select: { equals: "Publié" } },
        { property: "Publié le", date: { on_or_after: since } },
        { property: "Réseau", select: { does_not_equal: "TikTok" } },
      ] },
      start_cursor: cursor, page_size: 100,
    });
    res.push(...j.results);
    cursor = j.has_more ? j.next_cursor : undefined;
  } while (cursor);

  const now = Date.now();
  const due = res.filter((p) => {
    const pr = p.properties;
    const type = pr["Type"]?.select?.name;
    const pub = Date.parse(pr["Publié le"]?.date?.start || 0);
    const last = Date.parse(pr["Stats MAJ le"]?.date?.start || 0) || 0;
    if (type === "Story") return now - pub < 24 * HOUR && now - last > HOUR;
    return now - last > 6 * HOUR;
  });
  if (!due.length) return;
  log(`Stats : ${due.length} post(s) à mettre à jour`);

  for (const p of due) {
    if (Date.now() > deadline) { log("Stats : temps écoulé, suite au prochain passage"); break; }
    const pr = p.properties;
    const reseau = pr["Réseau"]?.select?.name;
    const type = pr["Type"]?.select?.name;
    const ref = (pr["Réf. publication"]?.rich_text || []).map((x) => x.plain_text).join("");
    if (!ref || ref.startsWith("container:")) continue;
    try {
      const s = reseau === "Instagram" ? await igStats(graph, ref, type) : await fbStats(graph, ref, type);
      const inter = (s.likes || 0) + (s.comments || 0) + (s.shares || 0) + (s.saves || 0);
      const base = s.reach || s.views || 0;
      const props = {
        "Stats MAJ le": { date: { start: new Date().toISOString() } },
      };
      const put = (k, v) => { if (Number.isFinite(v)) props[k] = { number: Math.round(v * 100) / 100 }; };
      put("Vues", s.views); put("Portée", s.reach); put("Likes", s.likes); put("Commentaires", s.comments);
      put("Partages", s.shares); put("Enregistrements", s.saves); put("Durée moy. (s)", s.avgWatch);
      if (base) put("Engagement %", (inter / base) * 100);
      if (dry) { log("DRY stats", ref, s); continue; }
      await notion(`pages/${p.id}`, "PATCH", { properties: props });
      log(`  stats ${reseau} ${type} ${ref} : vues ${s.views ?? "?"}, portée ${s.reach ?? "?"}, interactions ${inter}`);
    } catch (e) {
      log("  stats impossibles", ref, e.message);
      // on marque quand même la date pour ne pas réessayer en boucle
      if (!dry) await notion(`pages/${p.id}`, "PATCH", { properties: { "Stats MAJ le": { date: { start: new Date().toISOString() } } } }).catch(() => {});
    }
  }
}

// Une métrique à la fois : si Meta en refuse une, les autres passent quand même.
async function metrics(graph, id, list, extra = {}) {
  const out = {};
  try {
    const j = await graph(`${id}/insights`, { metric: list.join(","), ...extra }, "GET");
    for (const m of j.data || []) out[m.name] = m.values?.[0]?.value ?? m.total_value?.value;
    return out;
  } catch {
    for (const m of list) {
      try {
        const j = await graph(`${id}/insights`, { metric: m, ...extra }, "GET");
        const d = j.data?.[0];
        if (d) out[d.name] = d.values?.[0]?.value ?? d.total_value?.value;
      } catch { /* métrique indisponible pour ce type de média */ }
    }
    return out;
  }
}

async function igStats(graph, id, type) {
  if (type === "Story") {
    const m = await metrics(graph, id, ["views", "reach", "replies", "shares", "total_interactions"]);
    return { views: m.views, reach: m.reach, comments: m.replies, shares: m.shares };
  }
  const list = ["views", "reach", "likes", "comments", "shares", "saved", "total_interactions"];
  if (type === "Reel") list.push("ig_reels_avg_watch_time");
  const m = await metrics(graph, id, list);
  return {
    views: m.views, reach: m.reach, likes: m.likes, comments: m.comments, shares: m.shares, saves: m.saved,
    avgWatch: m.ig_reels_avg_watch_time != null ? m.ig_reels_avg_watch_time / 1000 : undefined,
  };
}

async function fbStats(graph, id, type) {
  if (type === "Reel") {
    const v = {};
    try {
      const j = await graph(`${id}/video_insights`, {}, "GET");
      for (const d of j.data || []) v[d.name] = d.values?.[0]?.value;
    } catch { /* pas d'accès aux insights vidéo */ }
    let f = {};
    try { f = await graph(id, { fields: "likes.summary(true).limit(0),comments.summary(true).limit(0)" }, "GET"); } catch {}
    return {
      views: v.blue_reels_play_count ?? v.fb_reels_total_plays, reach: v.post_impressions_unique,
      likes: f.likes?.summary?.total_count, comments: f.comments?.summary?.total_count,
      avgWatch: v.post_video_avg_time_watched != null ? v.post_video_avg_time_watched / 1000 : undefined,
    };
  }
  if (type === "Story") return {}; // Meta n'expose pas les stats des stories Facebook de page de façon fiable
  let f = {};
  try { f = await graph(id, { fields: "reactions.summary(true).limit(0),comments.summary(true).limit(0),shares" }, "GET"); } catch {}
  const m = await metrics(graph, id, ["post_media_view", "post_impressions_unique", "post_total_media_view_unique"]);
  return {
    views: m.post_media_view, reach: m.post_total_media_view_unique ?? m.post_impressions_unique,
    likes: f.reactions?.summary?.total_count, comments: f.comments?.summary?.total_count, shares: f.shares?.count,
  };
}
