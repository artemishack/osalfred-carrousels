# Robot de publication OS Alfred

Lit la base Notion « Planning réseaux OS Alfred » et publie sur Instagram et Facebook via l'API officielle Meta.
Tourne en cron toutes les 5 minutes sur Railway (`railway.json`). Aucune dépendance (Node 20+).

Variables : `NOTION_TOKEN`, `NOTION_DB_ID`, `META_PAGE_TOKEN`, `FB_PAGE_ID`, `IG_USER_ID` (optionnel : `GRAPH_VERSION`, `DRY_RUN=1`).

Statuts : Programmé → En cours → (Traitement pour les vidéos longues à traiter) → Publié, ou Erreur avec le message.
Les lignes TikTok sont ignorées (publication via TikTok Studio).
