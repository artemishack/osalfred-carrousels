# Audit avant publication (copywriting + Méthode 21)

À appliquer à **tout post non publié** (lignes Notion `Programmé` / `À valider`, posts Metricool programmés ou en brouillon), à chaque passage de la boucle, avant l'étape « Programmer ». Mis en place le 17/11/2026.

## Brief de référence (condition deck court)

- **Cible** : patron du second œuvre ou dirigeant de TPE, non-tech, 30-55 ans, qui fait sa gestion le soir.
- **Désir n° 1** : récupérer ses soirées sans perdre d'argent. **Douleur n° 1** : devis, relances, factures faits à 22 h.
- **Niveau de conscience** : 1 à 2 (trafic froid). Donc : on réveille le problème avec une scène vécue, on ne présente pas l'offre en premier. CTA léger (commenter KIT, enregistrer, répondre à une question).
- **Émotion dominante** : Facile (« ça part tout seul »), soutenue par Sûr. Intensité subtile : cible méfiante envers le marketing.
- **Preuves** : aucune preuve client publiable. Donc pas de chiffre de résultat ; un chiffre = un exemple de calcul présenté comme tel.

## Grille de notation (/10, moyenne des 8 critères)

| # | Critère | 10/10 quand… |
|---|---|---|
| 1 | Hook verbal / 1re ligne | Ouvre sur une **scène vécue + enjeu** (« 22 h, encore sur tes mails »), soulève une question, sans interjection (« Attention. », « Sérieux ? », « Stop. ») |
| 2 | Hook textuel et visuel | Texte à l'écran dès la **1re image**, lisible sans le son ; un élément visuel qui intrigue |
| 3 | Promesse | Une seule idée, crédible, le lecteur sait ce qu'il obtient |
| 4 | Rétention | Blocs de 10 s max, un retournement (« Et le pire ? ») avant chaque décrochage, promesse tenue à la fin |
| 5 | Légende | Ne **répète pas** la slide 1 ou le hook : elle ajoute la scène, donne la réponse en clair, finit par une question facile |
| 6 | CTA | Un seul. Carrousel : « enregistre-le » (signal mesuré). Reel : KIT en commentaire ou diagnostic. Jamais juste avant la révélation |
| 7 | Clarté (CUB) | Rien de confus, d'incroyable ou d'ennuyeux ; mots de la cible ; phrases courtes |
| 8 | Conformité | Règles de fond de BOUCLE.md (pas de faux chiffre, pas de prix, « OS Alfred »…) |

- **< 6** : réécrire (légende, et média si le défaut est dans la vidéo). **6 à 7,5** : corriger la légende. **> 7,5** : ne pas toucher.
- Écrire la note et la cause dans `Diagnostic`, incrémenter `Version`, remplir `Accroche`.
- Hashtags : 4 maximum, ciblés métier (pas #tpe #pme #entrepreneur génériques).

## Ce qu'on a le droit de modifier

- **Légendes et titres** d'un post `Programmé` : oui, directement (c'est une correction, pas un nouveau post).
- **Média** d'un post `Programmé` : coupe d'interjection (`studio/motion/hookcut.sh`) oui ; refonte visuelle complète → nouvelle ligne `À valider`, Matisse choisit.
- **Posts d'un test en cours** (journal des tests) : ne rien changer d'autre que la variable testée.
- **Stories** : images sans texte de légende ; elles s'auditent sur l'image seule (lisibilité, une idée, question en story 3).

## Modèle de script reel (Méthode 21)

```
HOOK TEXTUEL (1re image) · HOOK VISUEL · HOOK SONORE
HOOK VERBAL (scène + enjeu) → HANDCUFFER (« reste 10 secondes… »)
DÉVELOPPEMENT 1 (≤ 10 s) → TURNAROUND (« Et le pire ? ») → DÉVELOPPEMENT 2
CONCLUSION (promesse tenue) → CTA unique
QUESTIONS OUVERTES dans la tête du spectateur : 1) … 2) …
```
Si un bloc n'ouvre aucune question, le réécrire.

## Motion : règles retenues des skills de référence

Sources lues le 17/11 : charlie947/motion-graphics-skills, heygen-com/hyperframes, lottiefiles/motion-design-skill, whaleyxbt/claude-motion, delphi-ai/animate-skill, Barty-Bart/motion-graphics, AbubakrChan/product-launch-motion, motiondivision/motion.

- **HTML piloté par `render(t)`**, capture image par image (Playwright) puis ffmpeg : rendu déterministe. C'est le principe de HyperFrames et de claude-motion, déjà celui de nos moteurs.
- **Entrées** en ease-out fort (équivalent `cubic-bezier(.16,1,.3,1)`), **sorties 2 fois plus courtes** que les entrées.
- **Ressorts** à dépassement minimal pour les objets qui tombent ; pas de bounce, pas de glow, pas de dégradé sur texte, pas d'effet machine à écrire.
- **Une seule couleur d'accent** (#0066FF). Fond : nuit → bleu (retournement) → neige (solution).
- **Un objet qui se transforme** plutôt que des coupes (les cartes de tâches tombent, orbitent, puis rentrent dans l'outil).
- **Chaque animation suit un mot** de la voix (timings des mots dans `audio*/rNN.json`).
- **Sous-titres mot à mot** obligatoires, au-dessus de la zone de légende ; mot clé en bleu.
- **Zone sûre** : rien d'important à moins de 70 px des bords ni sous y = 1500.
- Audio masterisé à **−14 LUFS**, whoosh discret sur chaque impact.
- **Planche de contrôle** (`render8.py shots`) à regarder avant tout rendu complet.

## 3D

- `studio/motion/engine8.html` + `render8.py` : scène three.js (téléphone, cartes, tuile outil), ombres douces, caméra animée, textes DOM par-dessus. Rendu logiciel, environ 15 min pour 22 s à 30 i/s.
- **Moteur de référence depuis le 17/11 : `studio/motion/engine9.html` + `render9.py`** (style « téléphone en verre », inspiration fournie par Matisse) : studio clair, iPhone 3D debout, écran en texture canvas, pastilles de verre dépoli qui sortent de l'écran sur chaque mot, caméra en poussée continue, fin sur téléphone noir avec logo. Un seul objet (le téléphone) du début à la fin. Rendu logiciel : environ 30 min pour 22 s. `engine8` (cartes à plat) a été jugé « pas beau » : ne plus l'utiliser.
- **Blender** (connecteur du PC de Matisse) : utilisable seulement si Blender est ouvert avec l'add-on MCP démarré. Le 17/11 il n'était pas joignable (« Cannot connect to Blender at localhost:9876 »). Si un rendu Blender est voulu : le signaler à Matisse dans le compte rendu, ne pas bloquer la boucle.

## Organisation (template « organisation méthode 21 »)

Le kanban fourni par Matisse suit les étapes : NICHE → idées vidéo → VEILLE HEBDOMADAIRE → WRITING → TOURNAGE → MONTAGE → programmation → ANALYSE → DATABASE, avec une fiche « Vidéo repérée » (créateur, lien, sujet, pourquoi elle attire, adaptation). Correspondance avec notre base : `À valider` = WRITING/MONTAGE terminés, `Programmé` = programmation, `Publié` + stats = ANALYSE, `Diagnostic`/journal des tests = DATABASE. La veille hebdomadaire (3 vidéos repérées dans la niche, fiche remplie) est à ajouter au compte rendu du lundi.
