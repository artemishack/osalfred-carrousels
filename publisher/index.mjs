// Robot de publication OS Alfred : lit la base Notion « Planning réseaux » et publie sur Instagram / Facebook
// via l'API officielle Meta (Graph API). Pensé pour tourner en cron toutes les 5 min (Railway ou GitHub Actions).
// Aucune dépendance : Node 18+ (fetch natif).
//
// Variables d'environnement :
//   NOTION_TOKEN     jeton de l'intégration Notion (secret_… / ntn_…)
//   NOTION_DB_ID     id de la base « Planning réseaux »
//   META_PAGE_TOKEN  jeton de page Facebook longue durée (n'expire pas)
//   FB_PAGE_ID       id de la page Facebook
//   IG_USER_ID       id du compte Instagram professionnel (instagram_business_account)
//   GRAPH_VERSION    optionnel, défaut v26.0
//   DRY_RUN=1        optionnel : affiche ce qui serait publié sans rien publier

import { collectStats } from "./stats.mjs";

const env = process.env;
const GV = env.GRAPH_VERSION || "v26.0";
const G = `https://graph.facebook.com/${GV}`;
const DRY = env.DRY_RUN === "1";
const NOTION_V = "2022-06-28";
const MAX_RUN_MS = 4 * 60 * 1000; // on rend la main avant le cron suivant

const t0 = Date.now();
const log = (...a) => console.log(new Date().toISOString(), ...a);
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

for (const k of ["NOTION_TOKEN", "NOTION_DB_ID", "META_PAGE_TOKEN"]) {
  if (!env[k]) { console.error(`Variable manquante : ${k}`); process.exit(1); }
}

// ---------------------------------------------------------------- Notion
async function notion(path, method = "GET", body) {
  const r = await fetch(`https://api.notion.com/v1/${path}`, {
    method,
    headers: { Authorization: `Bearer ${env.NOTION_TOKEN}`, "Notion-Version": NOTION_V, "Content-Type": "application/json" },
    body: body ? JSON.stringify(body) : undefined,
  });
  const j = await r.json();
  if (!r.ok) throw new Error(`Notion ${r.status} : ${j.message || JSON.stringify(j)}`);
  return j;
}

const txt = (p) => (p?.rich_text || p?.title || []).map((x) => x.plain_text).join("");
const sel = (p) => p?.select?.name || p?.status?.name || "";

async function duePages() {
  const nowIso = new Date().toISOString();
  const res = [];
  let cursor;
  do {
    const j = await notion(`databases/${env.NOTION_DB_ID}/query`, "POST", {
      filter: { or: [
        { and: [ { property: "Statut", select: { equals: "Programmé" } }, { property: "Date", date: { on_or_before: nowIso } },
                 { property: "Réseau", select: { does_not_equal: "TikTok" } } ] },
        { property: "Statut", select: { equals: "Traitement" } },
      ] },
      sorts: [{ property: "Date", direction: "ascending" }],
      start_cursor: cursor,
      page_size: 50,
    });
    res.push(...j.results);
    cursor = j.has_more ? j.next_cursor : undefined;
  } while (cursor);
  return res;
}

async function setStatus(pageId, statut, extra = {}) {
  const props = { Statut: { select: { name: statut } } };
  if (extra.erreur !== undefined) props["Erreur"] = { rich_text: [{ text: { content: String(extra.erreur).slice(0, 1900) } }] };
  if (extra.ref !== undefined) props["Réf. publication"] = { rich_text: [{ text: { content: String(extra.ref).slice(0, 1900) } }] };
  if (statut === "Publié") props["Publié le"] = { date: { start: new Date().toISOString() } };
  if (DRY) return log("DRY statut", pageId, statut, extra);
  await notion(`pages/${pageId}`, "PATCH", { properties: props });
}

// ---------------------------------------------------------------- Meta
async function graph(path, params = {}, method = "POST") {
  const body = new URLSearchParams({ ...params, access_token: env.META_PAGE_TOKEN });
  const url = method === "GET" ? `${G}/${path}?${body}` : `${G}/${path}`;
  const r = await fetch(url, method === "GET" ? {} : { method, body });
  const j = await r.json();
  if (!r.ok || j.error) throw new Error(`Meta ${r.status} : ${j.error?.message || JSON.stringify(j)}`);
  return j;
}

const isVideo = (u) => /\.(mp4|mov)(\?|$)/i.test(u);

// Instagram : attend qu'un conteneur vidéo soit prêt. Renvoie "FINISHED", "IN_PROGRESS" (on reprendra plus tard) ou lève une erreur.
async function igWait(containerId, maxMs) {
  const end = Date.now() + maxMs;
  for (;;) {
    const s = await graph(containerId, { fields: "status_code,status" }, "GET");
    if (s.status_code === "FINISHED") return "FINISHED";
    if (s.status_code === "ERROR" || s.status_code === "EXPIRED") throw new Error(`Instagram : traitement vidéo ${s.status_code} ${s.status || ""}`);
    if (Date.now() > end) return "IN_PROGRESS";
    await sleep(8000);
  }
}

async function igPublish(containerId) {
  const p = await graph(`${env.IG_USER_ID}/media_publish`, { creation_id: containerId });
  return p.id;
}

async function igCreate(type, media, caption) {
  const ig = env.IG_USER_ID;
  if (!ig) throw new Error("IG_USER_ID manquant");
  if (type === "Carrousel") {
    if (media.length < 2) throw new Error("Carrousel : 2 médias minimum");
    const children = [];
    for (const u of media.slice(0, 10)) {
      const c = await graph(`${ig}/media`, isVideo(u) ? { media_type: "VIDEO", video_url: u, is_carousel_item: "true" } : { image_url: u, is_carousel_item: "true" });
      if (isVideo(u)) await igWait(c.id, 120000);
      children.push(c.id);
    }
    return (await graph(`${ig}/media`, { media_type: "CAROUSEL", children: children.join(","), caption })).id;
  }
  const u = media[0];
  if (type === "Reel") return (await graph(`${ig}/media`, { media_type: "REELS", video_url: u, caption, share_to_feed: "true" })).id;
  if (type === "Story") return (await graph(`${ig}/media`, isVideo(u) ? { media_type: "STORIES", video_url: u } : { media_type: "STORIES", image_url: u })).id;
  // Post simple
  return (await graph(`${ig}/media`, isVideo(u) ? { media_type: "REELS", video_url: u, caption } : { image_url: u, caption })).id;
}

// Facebook (page)
async function fbReel(u, description) {
  const page = env.FB_PAGE_ID;
  const start = await graph(`${page}/video_reels`, { upload_phase: "start" });
  const up = await fetch(`https://rupload.facebook.com/video-upload/${GV}/${start.video_id}`, {
    method: "POST", headers: { Authorization: `OAuth ${env.META_PAGE_TOKEN}`, file_url: u },
  });
  const uj = await up.json();
  if (!up.ok || uj.success === false) throw new Error(`Facebook upload reel : ${JSON.stringify(uj)}`);
  await graph(`${page}/video_reels`, { upload_phase: "finish", video_id: start.video_id, video_state: "PUBLISHED", description });
  return start.video_id;
}

async function fbStory(u) {
  const page = env.FB_PAGE_ID;
  if (!isVideo(u)) {
    const ph = await graph(`${page}/photos`, { url: u, published: "false" });
    return (await graph(`${page}/photo_stories`, { photo_id: ph.id })).post_id || ph.id;
  }
  const start = await graph(`${page}/video_stories`, { upload_phase: "start" });
  const up = await fetch(`https://rupload.facebook.com/video-upload/${GV}/${start.video_id}`, {
    method: "POST", headers: { Authorization: `OAuth ${env.META_PAGE_TOKEN}`, file_url: u },
  });
  if (!up.ok) throw new Error(`Facebook upload story : ${await up.text()}`);
  const fin = await graph(`${page}/video_stories`, { upload_phase: "finish", video_id: start.video_id });
  return fin.post_id || start.video_id;
}

async function fbPublish(type, media, caption) {
  const page = env.FB_PAGE_ID;
  if (!page) throw new Error("FB_PAGE_ID manquant");
  if (type === "Reel") return fbReel(media[0], caption);
  if (type === "Story") return fbStory(media[0]);
  if (type === "Carrousel" || media.length > 1) {
    const ids = [];
    for (const u of media.slice(0, 10)) ids.push((await graph(`${page}/photos`, { url: u, published: "false" })).id);
    const params = { message: caption };
    ids.forEach((id, i) => (params[`attached_media[${i}]`] = JSON.stringify({ media_fbid: id })));
    return (await graph(`${page}/feed`, params)).id;
  }
  const u = media[0];
  if (isVideo(u)) return (await graph(`${page}/videos`, { file_url: u, description: caption })).id;
  return (await graph(`${page}/photos`, { url: u, caption })).post_id;
}

// ---------------------------------------------------------------- Boucle
async function handle(page) {
  const p = page.properties;
  const titre = txt(p["Titre"]);
  const reseau = sel(p["Réseau"]);
  const type = sel(p["Type"]);
  const statut = sel(p["Statut"]);
  const caption = txt(p["Légende"]);
  const media = txt(p["Médias"]).split(/\s+/).map((s) => s.trim()).filter(Boolean);
  const ref = txt(p["Réf. publication"]);
  log(`→ ${reseau} ${type} « ${titre} » (${statut})`);

  if (!media.length) throw new Error("Aucun média");
  if (DRY) return log("DRY", { reseau, type, media, caption: caption.slice(0, 80) });

  if (reseau === "Instagram") {
    // Reprise d'un conteneur vidéo encore en traitement au passage précédent
    let container = statut === "Traitement" && ref.startsWith("container:") ? ref.slice(10) : null;
    if (!container) {
      await setStatus(page.id, "En cours");
      container = await igCreate(type, media, caption);
    }
    const needsWait = type === "Reel" || (type === "Story" && isVideo(media[0])) || (type === "Post" && isVideo(media[0]));
    if (needsWait) {
      const left = Math.max(30000, MAX_RUN_MS - (Date.now() - t0) - 30000);
      if ((await igWait(container, left)) !== "FINISHED") {
        await setStatus(page.id, "Traitement", { ref: `container:${container}` });
        return log("  vidéo encore en traitement, reprise au prochain passage");
      }
    }
    const id = await igPublish(container);
    await setStatus(page.id, "Publié", { ref: id, erreur: "" });
    return log("  publié IG", id);
  }

  if (reseau === "Facebook") {
    if (statut === "Traitement") return; // pas de reprise côté FB
    await setStatus(page.id, "En cours");
    const id = await fbPublish(type, media, caption);
    await setStatus(page.id, "Publié", { ref: id, erreur: "" });
    return log("  publié FB", id);
  }

  throw new Error(`Réseau non géré : ${reseau}`);
}

let pages;
try { pages = await duePages(); }
catch (e) { console.error("Lecture Notion impossible :", e.message); process.exit(1); }
log(`${pages.length} élément(s) à traiter`);
let errors = 0;
for (const page of pages) {
  if (Date.now() - t0 > MAX_RUN_MS) { log("Temps écoulé, la suite au prochain passage"); break; }
  try { await handle(page); }
  catch (e) {
    errors++;
    log("  ERREUR", e.message);
    try { await setStatus(page.id, "Erreur", { erreur: e.message }); } catch (e2) { log("  impossible d'écrire l'erreur dans Notion", e2.message); }
  }
}
try { await collectStats({ notion, graph, log, deadline: t0 + MAX_RUN_MS, dry: DRY }); }
catch (e) { log("Stats : erreur", e.message); }
log(`Terminé${errors ? ` avec ${errors} erreur(s)` : ""}`);
process.exit(0);
