# Boucle d'amélioration du contenu OS Alfred

Mode d'emploi suivi chaque semaine par la tâche planifiée « Analyse contenu OS Alfred ».
Objectif : mesurer, comprendre, corriger, republier, jusqu'à trouver ce qui prend auprès des patrons du second œuvre.

## 0. Préparer l'atelier (session neuve)

```bash
cd /home/claude && git clone https://github.com/artemishack/osalfred-carrousels.git
cp -r osalfred-carrousels/studio/carrousel /home/claude/carrousel
cp -r osalfred-carrousels/studio/motion /home/claude/motion
pip install --break-system-packages pillow numpy 2>/dev/null
```
Playwright + Chromium sont déjà installés. ffmpeg : `which ffmpeg` (sinon `apt-get install -y ffmpeg` ou `pip install imageio-ffmpeg`).

## 1. Collecter

- **Instagram / Facebook** : base Notion « Planning réseaux OS Alfred » (`collection://58692b99-555b-415e-8c33-23ad9a4d16a2`). Le robot Railway remplit seul Vues, Portée, Likes, Commentaires, Partages, Enregistrements, Durée moy. (s), Engagement %. Lire toutes les lignes `Statut = Publié` des 28 derniers jours (SQL).
- **TikTok** : Metricool (brandId 7552451), `getAnalyticsAvailableMetrics` puis `getAnalyticsDataByMetrics` sur TikTok pour les posts publiés. Écrire les chiffres dans des lignes Notion `Réseau = TikTok`, `Statut = Publié` (créer la ligne si elle n'existe pas).
- Remplir `Sujet` et `Accroche` (première ligne de la légende ou titre TikTok) quand c'est vide.

## 2. Mesurer (par format, jamais tous formats mélangés)

| Format | Signal principal | Signal secondaire |
|---|---|---|
| Reel | Vues ÷ abonnés (portée hors abonnés) et Durée moy. ÷ durée du reel (rétention) | Partages + Enregistrements |
| Carrousel | (Enregistrements + Partages) ÷ Portée | Commentaires ÷ Portée |
| Story | Portée story 3 ÷ story 1 (combien restent jusqu'au bout) | Réponses |

Classer chaque post en **haut / milieu / bas tiers** de son format. Ne rien conclure sur un post de moins de 48 h ni sur un échantillon de moins de 5 posts par format : le noter « à confirmer ».

## 3. Diagnostiquer (une cause principale par post faible)

| Symptôme | Cause probable | Correction |
|---|---|---|
| Peu de vues, bonne rétention chez ceux qui regardent | Accroche ou couverture | Réécrire les 2 premières secondes / la slide 1 : chiffre concret, situation vécue, question qui pique |
| Vues correctes, rétention faible | Milieu trop long ou trop abstrait | Couper, une idée par plan, exemple chantier concret |
| Bonne rétention, zéro interaction | CTA ou question finale faible | Question fermée facile à répondre, ou « écris KIT » |
| Carrousel vu mais pas enregistré | Pas assez « outil » | Ajouter une liste, un modèle de message, un calcul à garder |
| Tout bas sur un créneau | Heure / jour | Tester un autre créneau (une seule variable à la fois) |
| Un sujet bat tous les autres | Sujet porteur | Décliner ce sujet sous 2 nouveaux angles |

Écrire le diagnostic dans la colonne `Diagnostic` du post (1 phrase : cause + correction).

## 4. Décider

- **Gagnants (haut tiers)** : garder le format et le sujet, produire 2 déclinaisons (nouvel angle, même promesse).
- **Perdants (bas tiers)** : produire une version corrigée (`Version` + 1) qui ne change **qu'un seul élément** (accroche OU structure OU CTA OU créneau), pour savoir ce qui a joué.
- **Milieu** : ne rien toucher, laisser tourner.
- Tenir le **journal des tests** (page Notion « Journal des tests contenu ») : hypothèse, changement, résultat la semaine suivante, conclusion. Une hypothèse confirmée 2 fois devient une règle de la charte ci-dessous.

## 5. Produire

- Carrousels : `studio/carrousel` (data.py / build_all.py / engine.py), 1080×1350, charte Montserrat + Inter, bleu #0066FF, nuit #0B132B.
- Reels : `studio/motion` (scripts7.py → voix ElevenLabs « Raphael », `creative_list_voices` pour l'id → getvoice7.sh → reels7.py / render7.py, moteur engine5.html avec zone sûre). Structure Hook → Contexte → Re-hook → Réponse → CTA, tutoiement, résultat concret.
- Pousser les médias dans le repo (`reels-v9/`, `v3/…`) puis utiliser les URL jsDelivr `https://cdn.jsdelivr.net/gh/artemishack/osalfred-carrousels@main/…`.

**Règles de fond (non négociables)** : zéro faux chiffre, faux témoignage ou fausse stat ; pas de prix ; jamais « maintenance incluse », « le code vous appartient à 100 % », « sans frais mensuels » ; « OS Alfred » dans les textes ; pas de Wasquehal ; pas de liste d'outils techniques. Un chiffre = un calcul exemple présenté comme tel.

## 6. Programmer

- IG + FB : lignes Notion avec le statut défini dans la tâche planifiée (`À valider` ou `Programmé`). Le robot ne publie que `Programmé`.
- TikTok : Metricool, **20 posts maximum par mois** au total. Remplacer les moins bons brouillons par les nouvelles versions, garder l'étalement sur le mois, reels 18 h / carrousels 10 h en semaine, 10 h le week-end.
- Ne jamais toucher à ce qui est déjà publié.

## 7. Rendre compte

Créer une page Notion « Analyse contenu — semaine du JJ/MM » sous la base : top 3 / flop 3 par format, causes, ce qui a été corrigé, ce qui est programmé, tests en cours. Puis envoyer à Matisse un résumé de 5 lignes maximum.

## Charte apprise (règles confirmées par les tests)

_Vide pour l'instant. Ajouter ici chaque règle confirmée 2 fois, avec la date._
