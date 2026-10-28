"""Reels v7 — pubs Hook → Contexte → Re-hook → Réponse → CTA. Moteur engine5. W(i) = début du mot i."""
SNOW, INK, BLUE, ICE = "#f4faff", "#0b132b", "#0066ff", "#e0f2fe"

def kit_end(W, i0, iBtn, END, dark=False):
    c = "white" if dark else "ink"
    return [
        dict(k="txt", lines=["Les messages,", "{blue}offerts."], c=c, s=128, align="c", y=250, at=W(i0), out=W(iBtn) - .05, om="up"),
        dict(k="kit", x=300, y=560, w=480, h=680, at=W(i0) + .3, flip=.45, out=END - 2.3, om="up"),
        dict(k="txt", lines=["Écris « KIT »", "en commentaire."], c=c, s=110, align="c", y=250, at=W(iBtn), out=None),
        dict(k="btn", t="Écris « KIT » en commentaire", bg=BLUE if dark else INK, x=92, y=1340, w=896, at=W(iBtn) + .1),
        dict(k="lock", dark=dark, y=600, at=END - 2.1, tag="osalfred.com/kit"),
    ]

def r01(W, END):
    return dict(slug="r01-devis-silence", ground=SNOW, grid="dots",
      bg=[dict(t=W(9) - .12, c=INK, x=540, y=900, dark=True, grid="none", d=.45),
          dict(t=W(27) - .12, c=BLUE, x=540, y=900, dark=True, grid="dots", d=.4),
          dict(t=W(42) - .15, c=SNOW, x=540, y=1000, grid="dots", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK (texte présent dès l'image 0)
        dict(k="txt", t="Stop.", s=330, align="c", y=700, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Tes devis", "{blue}sans réponse ?"], s=140, align="c", y=330, at=W(1), out=W(9) - .1, om="up"),
        dict(k="card", av="DM", t="Devis Martin", b="Sans réponse", x=110, y=820, w=860, at=W(2), out=W(9) - .1),
        dict(k="card", av="DD", t="Devis Dubois", b="Sans réponse", x=110, y=990, w=860, at=W(4), out=W(9) - .1),
        dict(k="card", av="DL", t="Devis Leroy", b="Sans réponse", x=110, y=1160, w=860, at=W(6), out=W(9) - .1),
        # CONTEXTE (nuit)
        dict(k="num", **{"from": 1300}, to=1367, pre="", dur=.9, s=230, c="white", align="c", y=330, at=W(9), out=W(17) - .1, fmt="h"),
        dict(k="txt", t="Envoyé.", c="white", s=120, align="c", y=700, at=W(14), out=W(17) - .1, om="up"),
        dict(k="dots", x=430, y=1000, at=W(17), stop=W(19) + .3, out=W(27) - .12),
        dict(k="txt", lines=["Puis…", "{blue}plus rien."], c="white", s=150, align="c", y=330, at=W(17), out=W(27) - .12, om="up"),
        dict(k="txt", lines=["Tu n'oses pas relancer.", "Ou tu oublies."], c="white", s=70, align="c", y=1200, at=W(20), out=W(27) - .12, om="up"),
        # RE-HOOK (bleu)
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(27), out=W(30) - .05),
        dict(k="strk", t="Refusé", c="white", s=170, y=600, at=W(30), cut=W(36) + .1, out=W(38) - .05, om="up"),
        dict(k="txt", t="Oublié.", c="white", s=230, align="c", y=900, mode="punch", at=W(38), out=W(42) - .15),
        # RÉPONSE (neige)
        dict(k="lock", y=560, at=W(42) - .1, sp=1.9, tag="Ton majordome digital", out=W(45) + .05, om="shrink"),
        dict(k="txt", lines=["Relancé", "{blue}tout seul."], s=150, align="c", y=300, at=W(45), out=W(56) - .05, om="up"),
        dict(k="tl", x=170, y=1060, w=740, at=W(45) + .1, draw=1.1, out=W(63) - .1, om="shrink", pts=[
             dict(x=0, d="J0", l="Devis envoyé", at=W(45) + .1),
             dict(x=45, d="J+3", l="Relance 1", at=W(52), env=1),
             dict(x=100, d="J+7", l="Relance 2", at=W(55), env=1)]),
        dict(k="txt", lines=["Toi, tu n'y", "penses {blue}plus."], s=140, align="c", y=300, at=W(56), out=W(63) - .1, om="up"),
        dict(k="chip", t="✓ Relance envoyée", c="green", x=330, y=1400, at=W(57), out=W(63) - .1),
        # CTA
        *kit_end(W, 63, 70, END),
      ])

def diag_end(W, i0, iR, END, ask, dark=False):
    """CTA diagnostic : « Décris ton problème sur osalfred.com » (i0) puis « reçois ta feuille de route sous 48 h » (iR)."""
    c = "white" if dark else "ink"
    return [
        dict(k="txt", lines=["Décris", "{blue}ton problème."], c=c, s=130, align="c", y=270, at=W(i0), out=W(iR) - .05, om="up"),
        dict(k="bub", x=130, y=760, w=820, at=W(i0) + .2, td=1.3, out=W(iR) - .05, t=ask, meta="Ton message · osalfred.com"),
        dict(k="txt", lines=["Ta feuille de route", "{blue}sous 48 h."], c=c, s=108, align="c", y=270, at=W(iR), out=None),
        dict(k="btn", t="Décris ton problème · osalfred.com", bg=BLUE if dark else INK, x=92, y=1340, w=896, at=W(iR) + .1),
        dict(k="lock", dark=dark, y=600, at=END - 2.1, tag="osalfred.com"),
    ]

def r02(W, END):
    nodes = [dict(cx=540, cy=640, t="Tu saisis le client", ic="✎", at=W(54), hot=W(54)),
             dict(cx=540, cy=900, t="Devis à jour", ic="✓", at=W(58), hot=W(58) + .2),
             dict(cx=540, cy=1160, t="Facture à jour", ic="✓", at=W(60), hot=W(60) + .2),
             dict(cx=540, cy=1420, t="Tableau à jour", ic="✓", at=W(62) - .1, hot=W(62) + .1)]
    return dict(slug="r02-excel-soirees", ground=INK, dark=True, grid="lines", glow="rgba(0,102,255,.22)",
      bg=[dict(t=W(32) - .12, c=BLUE, x=540, y=900, dark=True, grid="dots", d=.4),
          dict(t=W(45) - .15, c="#e8f2fd", x=540, y=1000, grid="hex", d=.5)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Stop.", c="white", s=330, align="c", y=700, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Tes soirées", "{blue}sur Excel ?"], c="white", s=150, align="c", y=600, at=W(1), out=W(8) - .08, om="up"),
        # CONTEXTE
        dict(k="txt", lines=["Trois fichiers.", "{blue}Chaque semaine."], c="white", s=110, align="c", y=300, at=W(8), out=W(25) - .1, om="up"),
        dict(k="card", av="XL", t="Devis_2026.xlsx", b="À recopier", cc="ink", x=110, y=760, w=860, at=W(9), out=W(25) - .1),
        dict(k="card", av="XL", t="Factures_v3.xlsx", b="À recopier", cc="ink", x=110, y=930, w=860, at=W(13), out=W(25) - .1),
        dict(k="card", av="XL", t="Suivi_semaine.xlsx", b="À remettre à jour", cc="red", x=110, y=1100, w=860, at=W(18), out=W(25) - .1),
        dict(k="txt", lines=["Les mêmes infos,", "recopiées"], c="white", s=110, align="c", y=330, at=W(25), out=W(32) - .12, om="up"),
        dict(k="num", **{"from": 1}, to=3, pre="× ", dur=.8, s=380, c="blue", align="c", y=760, at=W(27), out=W(32) - .12),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(32), out=W(35) - .05),
        dict(k="txt", lines=["Tu gardes", "tes habitudes."], c="white", s=130, align="c", y=420, at=W(35), out=W(40) - .05, om="up"),
        dict(k="card", av="XL", t="Ton fichier", b="Tes habitudes", cc="green", x=110, y=900, w=860, at=W(36), out=W(40) - .05),
        dict(k="txt", lines=["Et tu ne recopies", "{blue}plus rien."], c="white", s=120, align="c", y=420, at=W(40), out=W(45) - .15, om="up"),
        dict(k="strk", t="Recopier", c="white", s=170, y=900, at=W(40) + .1, cut=W(43), out=W(45) - .15),
        # RÉPONSE
        dict(k="lock", y=560, at=W(45) - .1, sp=1.9, tag="Ton majordome digital", out=W(48) + .05, om="shrink"),
        dict(k="txt", lines=["Ton fichier devient", "{blue}un outil simple."], s=110, align="c", y=300, at=W(48), out=W(54) - .05, om="up"),
        dict(k="chip", t="Tes colonnes. Ta logique.", c="blue", x=300, y=760, at=W(50), out=W(54) - .05),
        dict(k="txt", t="Saisis {blue}une fois.", s=120, align="c", y=300, at=W(54), out=W(63) - .1, om="up"),
        dict(k="flow", at=W(54) - .1, out=W(63) - .1, nodes=nodes, links=[[0, 1, W(58) - .3], [1, 2, W(60) - .3], [2, 3, W(62) - .35]],
             tok=[dict(n=0, t=W(57)), dict(n=1, t=W(58)), dict(n=2, t=W(60)), dict(n=3, t=W(62))]),
        # CTA
        *diag_end(W, 63, 68, END, "Je recopie mes devis et mes factures dans trois fichiers, chaque semaine."),
      ])

ALL = {"r01": r01, "r02": r02}

def r03(W, END):
    items = [dict(t="Relancer les devis", at=W(16)), dict(t="Relancer les factures", at=W(19)),
             dict(t="Caler les rendez-vous", at=W(22)), dict(t="Répondre aux questions", sm="Toujours les mêmes", at=W(25)),
             dict(t="Faire le point", sm="Chaque semaine", at=W(29))]
    done = [dict(n="✓", t=x["t"], at=W(46) + .1 + j * .14) for j, x in enumerate(items)]
    return dict(slug="r03-cinq-taches", ground=SNOW, grid="lines",
      bg=[dict(t=W(35) - .12, c=INK, x=540, y=900, dark=True, grid="none", d=.45),
          dict(t=W(43) - .15, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.45),
          dict(t=W(55) - .12, c=INK, x=540, y=1300, dark=True, grid="lines", d=.5)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", lines=["Écoute", "bien."], s=250, align="c", y=560, mode="punch", at=-.3, out=W(2) - .02, od=.12),
        dict(k="txt", lines=["{blue}5 tâches", "volent tes soirées."], s=108, align="c", y=300, at=W(2), out=W(16) - .1, om="up"),
        dict(k="num", **{"from": 1080}, to=1320, dur=1.4, fmt="h", s=230, align="c", y=760, at=W(7), out=W(16) - .1),
        dict(k="chip", t="Encore à la main", c="red", x=350, y=1080, at=W(12), out=W(16) - .1),
        # CONTEXTE : la liste
        dict(k="steps", y=330, gap=240, dim=True, at=W(16) - .05, out=W(35) - .12, items=items),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(35), out=W(38) - .05),
        dict(k="txt", lines=["Aucune ne demande", "{blue}ton expertise."], c="white", s=96, align="c", y=330, at=W(38), out=W(43) - .15, om="up"),
        dict(k="num", **{"from": 5}, to=0, suf=" / 5", dur=.9, s=300, c="blue", align="c", y=780, at=W(39), out=W(43) - .15),
        # RÉPONSE
        dict(k="lock", dark=True, y=560, at=W(43) - .1, sp=1.9, tag="Ton majordome digital", out=W(46) + .05, om="shrink"),
        dict(k="txt", lines=["Elles tournent", "toutes seules."], c="white", s=130, align="c", y=270, at=W(46), out=W(50) - .05, om="up"),
        dict(k="steps", c="white", y=700, gap=170, at=W(46), out=W(50) - .05, items=done),
        dict(k="txt", lines=["Tu récupères", "tes soirées."], c="white", s=130, align="c", y=270, at=W(50), out=W(55) - .12, om="up"),
        dict(k="num", **{"from": 1320}, to=1110, dur=1.0, fmt="h", s=260, c="white", align="c", y=760, at=W(51), out=W(55) - .12),
        dict(k="chip", t="Soirée libre", c="green", x=400, y=1100, at=W(52), out=W(55) - .12),
        # CTA
        *kit_end(W, 55, 62, END, dark=True),
      ])
ALL["r03"] = r03

def r04(W, END):
    nodes = [dict(cx=540, cy=640, t="Facture envoyée", sm="Jour J", ic="€", at=W(44), hot=W(44)),
             dict(cx=540, cy=920, t="Rappel courtois", sm="Avant l'échéance", ic="✉", at=W(47), hot=W(48)),
             dict(cx=540, cy=1200, t="Message ferme", sm="Et poli, si besoin", ic="!", at=W(51), hot=W(53))]
    return dict(slug="r04-facture-impayee", ground="#e8f2fd", grid="hex",
      bg=[dict(t=W(25) - .12, c=INK, x=540, y=900, dark=True, grid="lines", d=.45),
          dict(t=W(38) - .15, c=SNOW, x=540, y=1000, grid="lines", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Sérieux ?", s=210, align="c", y=720, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Il te doit de l'argent,", "et c'est {blue}toi qui es gêné ?"], s=84, align="c", y=300, at=W(1), out=W(13) - .08, om="up"),
        dict(k="morph", at=W(1), doc=dict(t="Facture n°118", s=44), out=W(13) - .08, kf=[
             dict(t=W(1), x=310, y=1900, w=460, h=560, r=28, bg="#ffffff"),
             dict(t=W(1) + .7, x=310, y=700, w=460, h=560, r=28, bg="#ffffff", d=.7)]),
        dict(k="chip", t="En attente", c="red", x=400, y=1300, at=W(6), out=W(13) - .08),
        # CONTEXTE
        dict(k="txt", t="Tu attends.", s=150, align="c", y=330, at=W(13), out=W(15) - .05, om="up"),
        dict(k="arc", x=390, y=820, w=300, h=300, at=W(13) + .1, out=W(25) - .12),
        dict(k="txt", lines=["Tu ne veux pas", "{blue}froisser."], s=130, align="c", y=300, at=W(15), out=W(20) - .05, om="up"),
        dict(k="txt", lines=["Tu espères", "que ça {blue}arrive."], s=130, align="c", y=300, at=W(20), out=W(25) - .12, om="up"),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(25), out=W(28) - .05),
        dict(k="txt", lines=["Pas relancée ?", "{blue}Payée en dernier."], c="white", s=110, align="c", y=300, at=W(28), out=W(38) - .15, om="up"),
        dict(k="card", av="1", t="Le fournisseur", b="Payé", cc="green", x=110, y=760, w=860, at=W(30), out=W(38) - .15),
        dict(k="card", av="2", t="Le loyer", b="Payé", cc="green", x=110, y=930, w=860, at=W(32), out=W(38) - .15),
        dict(k="card", av="3", t="Ta facture", b="En dernier", cc="red", x=110, y=1100, w=860, at=W(35), out=W(38) - .15),
        # RÉPONSE
        dict(k="lock", y=560, at=W(38) - .1, sp=1.9, tag="Ton majordome digital", out=W(41) + .05, om="shrink"),
        dict(k="txt", lines=["La relance,", "{blue}prévue dès l'envoi."], s=100, align="c", y=270, at=W(41), out=W(57) - .05, om="up"),
        dict(k="flow", at=W(44) - .1, out=W(63) - .1, nodes=nodes, links=[[0, 1, W(47) - .3], [1, 2, W(51) - .3]],
             tok=[dict(n=0, t=W(45)), dict(n=0, t=W(47) - .3), dict(n=1, t=W(48)), dict(n=1, t=W(51) - .3), dict(n=2, t=W(53))]),
        dict(k="txt", lines=["Payé, sans", "{blue}courir après."], s=120, align="c", y=270, at=W(57), out=W(63) - .1, om="up"),
        dict(k="chip", t="✓ Facture payée", c="green", x=340, y=1440, at=W(59), out=W(63) - .1),
        # CTA
        *kit_end(W, 63, 70, END),
      ])
ALL["r04"] = r04

def r05(W, END):
    hs = [62, 40, 78, 30, 55, 88, 35, 70, 45]
    used = {2, 5, 7}
    bars = [dict(h=h, v="", l="Utilisé" if j in used else "", d=j not in used, at=W(2) + j * .1) for j, h in enumerate(hs)]
    return dict(slug="r05-logiciel-trois-boutons", ground="#e8f2fd", grid="dots",
      bg=[dict(t=W(27) - .12, c=INK, x=540, y=900, dark=True, grid="lines", d=.45),
          dict(t=W(38) - .15, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.45),
          dict(t=W(59) - .12, c=INK, x=540, y=1300, dark=True, grid="lines", d=.5)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Attends.", s=220, align="c", y=720, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Un logiciel entier,", "{blue}3 boutons utilisés ?"], s=96, align="c", y=300, at=W(1), out=W(10) - .08, om="up"),
        dict(k="bars", x=120, y=700, w=840, h=560, at=W(2) - .05, out=W(10) - .08, bars=bars),
        # CONTEXTE
        dict(k="txt", lines=["Tu paies.", "{blue}Chaque mois."], s=130, align="c", y=300, at=W(10), out=W(14) - .05, om="up"),
        dict(k="txt", lines=["Des fonctions", "{blue}jamais ouvertes."], s=120, align="c", y=300, at=W(14), out=W(21) - .05, om="up"),
        dict(k="txt", lines=["Et pour le reste,", "tu {blue}contournes."], s=120, align="c", y=300, at=W(21), out=W(27) - .12, om="up"),
        dict(k="card", av="€", t="Abonnement", b="Chaque mois", cc="ink", x=110, y=760, w=860, at=W(11), out=W(27) - .12),
        dict(k="card", av="⚙", t="Fonctions", b="Jamais ouvertes", cc="red", x=110, y=930, w=860, at=W(15), out=W(27) - .12),
        dict(k="card", av="↺", t="Le reste", b="Contourné", cc="red", x=110, y=1100, w=860, at=W(22), out=W(27) - .12),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(27), out=W(30) - .05),
        dict(k="txt", lines=["Ce que tu cherches", "est souvent {blue}simple."], c="white", s=100, align="c", y=330, at=W(30), out=W(38) - .15, om="up"),
        dict(k="strk", t="Usine à gaz", c="white", s=150, y=820, at=W(31), cut=W(36), out=W(38) - .15),
        # RÉPONSE
        dict(k="lock", dark=True, y=560, at=W(38) - .1, sp=1.9, tag="Ton majordome digital", out=W(41) + .05, om="shrink"),
        dict(k="txt", lines=["On part de ta façon", "de {blue}travailler."], c="white", s=100, align="c", y=270, at=W(41), out=W(49) - .05, om="up"),
        dict(k="steps", c="white", y=700, gap=180, at=W(42), out=W(56) - .05, items=[
             dict(t="Tes étapes", at=W(43)), dict(t="Tes documents", at=W(45)), dict(t="Tes habitudes", at=W(47))]),
        dict(k="txt", lines=["L'outil fait", "{blue}exactement ça."], c="white", s=120, align="c", y=270, at=W(49), out=W(56) - .05, om="up"),
        dict(k="chip", t="✓ Construit pour toi", c="green", x=320, y=1300, at=W(51), out=W(56) - .05),
        dict(k="txt", lines=["Rien", "de plus."], c="white", s=220, align="c", y=640, mode="punch", at=W(56), out=W(59) - .12),
        # CTA
        *diag_end(W, 59, 64, END, "J'utilise trois boutons de mon logiciel, et je contourne tout le reste.", dark=True),
      ])
ALL["r05"] = r05

def r06(W, END):
    return dict(slug="r06-ia-mails", ground=INK, dark=True, grid="dots", glow="rgba(0,102,255,.22)",
      bg=[dict(t=W(29) - .12, c=SNOW, x=540, y=900, grid="lines", d=.45),
          dict(t=W(41) - .15, c="#e8f2fd", x=540, y=1000, grid="hex", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Stop.", c="white", s=330, align="c", y=700, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Le même mail,", "{blue}tous les jours ?"], c="white", s=130, align="c", y=300, at=W(1), out=W(9) - .08, om="up"),
        dict(k="bub", x=130, y=800, w=820, at=W(2), td=1.6, out=W(9) - .08, t="Bonjour, suite à notre échange, je vous envoie comme convenu…", meta="Tapé à la main · encore"),
        # CONTEXTE
        dict(k="txt", lines=["Tout ça,", "{blue}à la main."], c="white", s=130, align="c", y=300, at=W(9), out=W(23) - .08, om="up"),
        dict(k="card", av="CR", t="Compte rendu", b="À taper", cc="ink", x=110, y=760, w=860, at=W(9) + .1, out=W(23) - .08),
        dict(k="card", av="DV", t="Devis", b="À partir des notes", cc="ink", x=110, y=930, w=860, at=W(12), out=W(23) - .08),
        dict(k="card", av="RC", t="Réponse client", b="À rédiger", cc="red", x=110, y=1100, w=860, at=W(19), out=W(23) - .08),
        dict(k="txt", lines=["Des heures de frappe,", "{blue}chaque semaine."], c="white", s=90, align="c", y=300, at=W(23), out=W(29) - .12, om="up"),
        dict(k="cal", x=92, y=720, w=896, h=460, pct=72, at=W(23) + .05, fill=W(24), out=W(29) - .12),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", s=150, align="c", y=420, mode="punch", at=W(29), out=W(32) - .05),
        dict(k="txt", lines=["Tout ça peut se préparer", "{blue}pendant que tu bosses."], s=78, align="c", y=330, at=W(32), out=W(41) - .15, om="up"),
        dict(k="dots", x=430, y=900, at=W(33), out=W(41) - .15),
        # RÉPONSE
        dict(k="lock", y=560, at=W(41) - .1, sp=1.9, tag="Ton majordome digital", out=W(44) + .05, om="shrink"),
        dict(k="txt", t="L'IA {blue}prépare.", s=150, align="c", y=280, at=W(44), out=W(51) - .05, om="up"),
        dict(k="bub", x=130, y=640, w=820, at=W(45), td=1.1, out=W(57) - .1, t="Bonjour M. Martin, voici le compte rendu de notre rendez-vous d'hier.", meta="Brouillon préparé · à relire"),
        dict(k="card", av="DV", t="Devis n°215", b="Brouillon prêt", cc="blue", x=110, y=1080, w=860, at=W(49), out=W(57) - .1),
        dict(k="txt", lines=["Toi, tu relis.", "{blue}Tu valides."], s=130, align="c", y=270, at=W(51), out=W(57) - .1, om="up"),
        dict(k="chip", t="✓ Validé et envoyé", c="green", x=320, y=1320, at=W(56), out=W(57) - .1),
        # CTA
        *diag_end(W, 57, 62, END, "Je passe des heures à écrire les mêmes mails et comptes rendus."),
      ])
ALL["r06"] = r06

def r07(W, END):
    return dict(slug="r07-site-clients", ground=SNOW, grid="dots",
      bg=[dict(t=W(8) - .12, c=INK, x=540, y=900, dark=True, grid="lines", d=.45),
          dict(t=W(24) - .12, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.4),
          dict(t=W(35) - .15, c=SNOW, x=540, y=1000, grid="dots", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", lines=["Question", "simple."], s=200, align="c", y=600, mode="punch", at=-.3, out=W(2) - .02, od=.12),
        dict(k="txt", lines=["Ton site t'apporte", "{blue}des clients ?"], s=110, align="c", y=300, at=W(2), out=W(8) - .08, om="up"),
        dict(k="morph", at=W(2), doc=dict(t="tonsite.fr", s=44), out=W(8) - .08, kf=[
             dict(t=W(2), x=290, y=1900, w=500, h=600, r=28, bg="#ffffff"),
             dict(t=W(2) + .7, x=290, y=700, w=500, h=600, r=28, bg="#ffffff", d=.7)]),
        # CONTEXTE
        dict(k="txt", lines=["Il affiche", "{blue}ton numéro."], c="white", s=130, align="c", y=300, at=W(8), out=W(14) - .05, om="up"),
        dict(k="chip", t="☎ 06 ·· ·· ·· ··", c="ink", x=330, y=800, at=W(10), out=W(16) - .08),
        dict(k="txt", t="Et il {blue}attend.", c="white", s=140, align="c", y=300, at=W(14), out=W(16) - .08, om="up"),
        dict(k="txt", lines=["Les questions arrivent", "{blue}en plein chantier."], c="white", s=86, align="c", y=300, at=W(16), out=W(24) - .12, om="up"),
        dict(k="card", av="☎", t="Appel entrant", b="Tu es sur le chantier", cc="red", x=110, y=760, w=860, at=W(18), out=W(24) - .12),
        dict(k="card", av="☎", t="Appel entrant", b="Encore une question", cc="red", x=110, y=930, w=860, at=W(20), out=W(24) - .12),
        dict(k="card", av="☎", t="Appel manqué", b="Pas rappelé", cc="red", x=110, y=1100, w=860, at=W(22), out=W(24) - .12),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(24), out=W(27) - .05),
        dict(k="txt", lines=["Il pourrait trier", "{blue}à ta place."], c="white", s=120, align="c", y=300, at=W(27), out=W(35) - .15, om="up"),
        dict(k="card", av="✓", t="Demande sérieuse", b="Pour toi", cc="green", x=110, y=820, w=860, at=W(29), out=W(35) - .15),
        dict(k="card", av="?", t="Question simple", b="Réponse auto", cc="ink", x=110, y=990, w=860, at=W(31), out=W(35) - .15),
        # RÉPONSE
        dict(k="lock", y=560, at=W(35) - .1, sp=1.9, tag="Ton majordome digital", out=W(38) + .05, om="shrink"),
        dict(k="txt", lines=["Ton site", "{blue}fait le tri."], s=140, align="c", y=270, at=W(38), out=W(53) - .1, om="up"),
        dict(k="steps", y=640, gap=200, dim=True, at=W(40) - .05, out=W(53) - .1, items=[
             dict(t="Répond aux questions", at=W(40)), dict(t="Propose un créneau", at=W(43)), dict(t="Te fait un résumé", sm="Chaque matin", at=W(47))]),
        dict(k="bub", x=130, y=1260, w=820, at=W(49), td=1.0, out=W(53) - .1, t="Résumé du matin : demandes triées, créneaux proposés.", meta="Ton site · 8 h"),
        # CTA
        *diag_end(W, 53, 58, END, "Mon site affiche mon numéro, et je réponds à tout au téléphone."),
      ])
ALL["r07"] = r07


def _bl(line):
    if not line.startswith("{blue}"): return line
    return " ".join("{blue}" + w.replace("{blue}", "") for w in line.split(" "))

def blueline(c):
    """« {blue} » en début de ligne = toute la ligne en bleu."""
    for e in c["els"]:
        if e.get("k") == "txt":
            if "lines" in e: e["lines"] = [_bl(l) for l in e["lines"]]
            if "t" in e: e["t"] = _bl(e["t"])

def r08(W, END):
    nodes = [dict(cx=540, cy=620, t="Appel manqué", ic="☎", at=W(45), hot=W(45)),
             dict(cx=540, cy=860, t="SMS dans la minute", sm="Envoyé tout seul", ic="✉", at=W(49), hot=W(50)),
             dict(cx=540, cy=1100, t="Il décrit son besoin", sm="Via un lien", ic="✎", at=W(54), hot=W(56)),
             dict(cx=540, cy=1340, t="Tu rappelles", sm="Avec toutes les infos", ic="✓", at=W(61), hot=W(62))]
    return dict(slug="r08-appel-manque", ground=BLUE, dark=True, grid="dots",
      bg=[dict(t=W(12) - .12, c=INK, x=540, y=900, dark=True, grid="lines", d=.45),
          dict(t=W(32) - .12, c=SNOW, x=540, y=1000, grid="lines", d=.45),
          dict(t=W(42) - .15, c="#e8f2fd", x=540, y=1000, grid="hex", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", lines=["Le téléphone", "sonne."], c="white", s=150, align="c", y=600, mode="punch", at=-.3, out=W(3) - .02, od=.12),
        dict(k="txt", lines=["Combien de clients", "tu perds ?"], c="white", s=110, align="c", y=300, at=W(3), out=W(12) - .08, om="up"),
        dict(k="card", av="☎", t="Appel manqué", b="Client potentiel", cc="red", x=110, y=800, w=860, at=W(7), out=W(12) - .08),
        # CONTEXTE
        dict(k="txt", lines=["Tu es en", "{blue}rendez-vous."], c="white", s=130, align="c", y=300, at=W(12), out=W(19) - .05, om="up"),
        dict(k="txt", lines=["Tu rappelles", "{blue}deux heures après."], c="white", s=110, align="c", y=300, at=W(19), out=W(25) - .05, om="up"),
        dict(k="num", **{"from": 840}, to=960, dur=1.0, fmt="h", s=260, c="white", align="c", y=760, at=W(20), out=W(25) - .05),
        dict(k="txt", t="Trop tard.", c="white", s=200, align="c", y=600, mode="punch", at=W(25), out=W(32) - .12),
        dict(k="chip", t="Il a appelé le suivant", c="red", x=290, y=950, at=W(27), out=W(32) - .12),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", s=150, align="c", y=420, mode="punch", at=W(32), out=W(35) - .05),
        dict(k="txt", lines=["Tu étais juste occupé", "à {blue}bien travailler."], s=92, align="c", y=420, at=W(35), out=W(42) - .15, om="up"),
        # RÉPONSE
        dict(k="lock", y=560, at=W(42) - .1, sp=1.9, tag="Ton majordome digital", out=W(45) + .05, om="shrink"),
        dict(k="txt", lines=["Chaque appel manqué", "{blue}reçoit un SMS."], s=86, align="c", y=250, at=W(45), out=W(61) - .05, om="up"),
        dict(k="flow", at=W(45) - .1, out=W(67) - .1, nodes=nodes, links=[[0, 1, W(49) - .3], [1, 2, W(54) - .3], [2, 3, W(61) - .3]],
             tok=[dict(n=0, t=W(46)), dict(n=1, t=W(50)), dict(n=2, t=W(56)), dict(n=3, t=W(62))]),
        dict(k="txt", lines=["Tu rappelles", "{blue}avec les infos."], s=110, align="c", y=250, at=W(61), out=W(67) - .1, om="up"),
        # CTA
        *diag_end(W, 67, 72, END, "Je rate des appels en rendez-vous, et je rappelle trop tard."),
      ])
ALL["r08"] = r08

def r09(W, END):
    nodes = [dict(cx=540, cy=640, t="M. Martin", sm="Saisi une fois", ic="✎", at=W(48)),
             dict(cx=290, cy=980, t="Devis", ic="✓", at=W(53)), dict(cx=790, cy=980, t="Facture", ic="✓", at=W(53) + .2),
             dict(cx=290, cy=1240, t="Agenda", ic="✓", at=W(54) + .1), dict(cx=790, cy=1240, t="Suivi", ic="✓", at=W(55))]
    return dict(slug="r09-saisie-unique", ground=SNOW, grid="hex",
      bg=[dict(t=W(32) - .12, c=INK, x=540, y=900, dark=True, grid="lines", d=.45),
          dict(t=W(44) - .15, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.45),
          dict(t=W(59) - .12, c=INK, x=540, y=1300, dark=True, grid="lines", d=.5)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", lines=["Compte", "bien."], s=250, align="c", y=560, mode="punch", at=-.3, out=W(2) - .02, od=.12),
        dict(k="txt", lines=["Le même client,", "tapé {blue}combien de fois ?"], s=96, align="c", y=300, at=W(2), out=W(11) - .08, om="up"),
        dict(k="num", **{"from": 1}, to=4, pre="× ", dur=.9, s=380, c="blue", align="c", y=720, at=W(9) - .2, out=W(11) - .08),
        # CONTEXTE
        dict(k="txt", lines=["Partout,", "{blue}à la main."], s=130, align="c", y=300, at=W(11), out=W(22) - .05, om="up"),
        dict(k="card", av="DV", t="Devis · M. Martin", b="Saisi", cc="ink", x=110, y=640, w=860, at=W(13), out=W(32) - .12),
        dict(k="card", av="FA", t="Facture · M. Martin", b="Saisi", cc="ink", x=110, y=810, w=860, at=W(16), out=W(32) - .12),
        dict(k="card", av="AG", t="Agenda · M. Martin", b="Saisi", cc="ink", x=110, y=980, w=860, at=W(18), out=W(32) - .12),
        dict(k="card", av="SV", t="Suivi · M. Martain", b="Faute de frappe", cc="red", x=110, y=1150, w=860, at=W(20), out=W(32) - .12),
        dict(k="txt", lines=["4 fois la même info.", "{blue}4 chances d'erreur."], s=92, align="c", y=300, at=W(22), out=W(32) - .12, om="up"),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(32), out=W(35) - .05),
        dict(k="txt", lines=["C'est souvent la cause", "de tes {blue}erreurs", "{blue}de facturation."], c="white", s=92, align="c", y=330, at=W(35), out=W(44) - .15, om="up"),
        dict(k="chip", t="Facture à refaire", c="red", x=340, y=900, at=W(41), out=W(44) - .15),
        # RÉPONSE
        dict(k="lock", dark=True, y=560, at=W(44) - .1, sp=1.9, tag="Ton majordome digital", out=W(47) + .05, om="shrink"),
        dict(k="txt", lines=["Tu saisis", "{blue}une fois."], c="white", s=140, align="c", y=270, at=W(47), out=W(52) - .05, om="up"),
        dict(k="flow", at=W(48) - .1, out=W(59) - .12, lc="#ffffff", nodes=nodes, links=[[0, 1, W(52) + .1], [0, 2, W(52) + .25], [0, 3, W(53) + .1], [0, 4, W(54)]]),
        dict(k="txt", lines=["L'info circule", "{blue}toute seule."], c="white", s=130, align="c", y=270, at=W(52), out=W(59) - .12, om="up"),
        # CTA
        *diag_end(W, 59, 64, END, "Je tape les mêmes infos client dans quatre outils différents.", dark=True),
      ])
ALL["r09"] = r09

def r10(W, END):
    return dict(slug="r10-marge-reelle", ground=INK, dark=True, grid="lines", glow="rgba(0,102,255,.22)",
      bg=[dict(t=W(10) - .12, c="#e8f2fd", x=540, y=900, grid="hex", d=.45),
          dict(t=W(26) - .12, c=INK, x=540, y=1000, dark=True, grid="lines", d=.45),
          dict(t=W(39) - .15, c=SNOW, x=540, y=1000, grid="dots", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Attention.", c="white", s=200, align="c", y=720, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Ta {blue}vraie marge", "sur ton dernier projet ?"], c="white", s=90, align="c", y=600, at=W(1), out=W(10) - .08, om="up"),
        # CONTEXTE (exemple chiffré)
        dict(k="tag", t="Exemple", c="l", align="c", y=260, at=W(10), out=W(26) - .12),
        dict(k="eq", x=92, y=380, w=896, at=W(10), out=W(26) - .12, om="up", rows=[
             dict(l="Prix de vente", n=5000, suf=" €", at=W(10) + .1),
             dict(l="Achats", n=1500, pre="− ", suf=" €", at=W(20)),
             dict(l="Ton temps", n=2000, pre="− ", suf=" €", at=W(23)),
             dict(l="Ce qui reste", n=1500, **{"from": 5000}, suf=" €", tot=True, at=W(24) + .3)]),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(26), out=W(29) - .05),
        dict(k="txt", lines=["Découverte", "chez le comptable,", "{blue}des mois plus tard."], c="white", s=88, align="c", y=330, at=W(29), out=W(39) - .15, om="up"),
        dict(k="tl", x=170, y=900, w=740, at=W(30), draw=1.6, out=W(39) - .15, om="shrink", pts=[
             dict(x=0, d="Début", l="Projet signé", at=W(30)), dict(x=45, d="Fin", l="Projet livré", at=W(32)),
             dict(x=100, d="Bilan", l="Trop tard", o=1, at=W(35))]),
        # RÉPONSE
        dict(k="lock", y=560, at=W(39) - .1, sp=1.9, tag="Ton majordome digital", out=W(42) + .05, om="shrink"),
        dict(k="txt", lines=["Ta marge,", "{blue}pendant le projet."], s=110, align="c", y=270, at=W(42), out=W(48) - .05, om="up"),
        dict(k="ring", x=340, y=620, w=400, h=400, at=W(43), to=30, suf=" %", ns=104, dur=1.2, arc=.3, out=W(53) - .1),
        dict(k="tag", t="Exemple", c="l", align="c", y=1050, at=W(44), out=W(53) - .1),
        dict(k="txt", lines=["Quand tu peux", "{blue}encore agir."], s=120, align="c", y=270, at=W(48), out=W(53) - .1, om="up"),
        dict(k="tl", x=170, y=1300, w=740, at=W(48), draw=1.0, out=W(53) - .1, om="shrink", pts=[
             dict(x=0, d="Début", l="Devis signé", at=W(48)), dict(x=50, d="Ici", l="Tu ajustes", at=W(50)),
             dict(x=100, d="Fin", l="Marge tenue", at=W(52))]),
        # CTA
        *diag_end(W, 53, 58, END, "Je ne connais ma vraie marge qu'au bilan, chez le comptable."),
      ])
ALL["r10"] = r10

def r11(W, END):
    return dict(slug="r11-logiciel-placard", ground="#e8f2fd", grid="dots",
      bg=[dict(t=W(8) - .12, c=SNOW, x=540, y=900, grid="lines", d=.45),
          dict(t=W(22) - .12, c=INK, x=540, y=1000, dark=True, grid="lines", d=.45),
          dict(t=W(34) - .15, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.45),
          dict(t=W(53) - .12, c=INK, x=540, y=1300, dark=True, grid="lines", d=.5)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Avoue.", s=280, align="c", y=700, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Ton dernier logiciel,", "{blue}au placard ?"], s=98, align="c", y=300, at=W(1), out=W(8) - .08, om="up"),
        dict(k="morph", at=W(1), doc=dict(t="Nouveau logiciel", s=40), out=W(8), kf=[
             dict(t=W(1), x=290, y=1900, w=500, h=600, r=28, bg="#ffffff"),
             dict(t=W(1) + .7, x=290, y=700, w=500, h=600, r=28, bg="#ffffff", d=.7),
             dict(t=W(8) - .1, x=440, y=1500, w=200, h=240, r=20, bg="#ffffff", rot=-12, op=0, d=.6, e="ant")]),
        # CONTEXTE
        dict(k="txt", t="Trois semaines.", s=120, align="c", y=300, at=W(8), out=W(22) - .12, om="up"),
        dict(k="steps", y=620, gap=260, dim=True, at=W(8), out=W(22) - .12, items=[
             dict(t="On essaie", sm="Semaine 1", at=W(8) + .1), dict(t="On contourne", sm="Semaine 2", at=W(13)),
             dict(t="Retour au papier", sm="Semaine 3", at=W(17))]),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(22), out=W(25) - .05),
        dict(k="txt", t="Le problème ?", c="white", s=120, align="c", y=330, at=W(25), out=W(34) - .15, om="up"),
        dict(k="strk", t="Ton équipe", c="white", s=150, y=600, at=W(27), cut=W(31) + .1, out=W(34) - .15),
        dict(k="txt", lines=["C'était", "{blue}l'outil."], c="white", s=200, align="c", y=860, mode="punch", at=W(32), out=W(34) - .15),
        # RÉPONSE
        dict(k="lock", dark=True, y=560, at=W(34) - .1, sp=1.9, tag="Ton majordome digital", out=W(37) + .05, om="shrink"),
        dict(k="txt", lines=["On part de", "{blue}tes habitudes."], c="white", s=130, align="c", y=270, at=W(37), out=W(42) - .05, om="up"),
        dict(k="txt", lines=["L'outil", "{blue}s'y adapte."], c="white", s=140, align="c", y=270, at=W(42), out=W(46) - .05, om="up"),
        dict(k="steps", c="white", y=700, gap=170, at=W(38), out=W(53) - .12, items=[
             dict(n="✓", t="Tes étapes", at=W(39)), dict(n="✓", t="Tes mots", at=W(41)), dict(n="✓", t="Ton rythme", at=W(43))]),
        dict(k="txt", lines=["Ton équipe", "{blue}l'adopte."], c="white", s=140, align="c", y=270, at=W(46), out=W(53) - .12, om="up"),
        dict(k="chip", t="✓ Il lui ressemble", c="green", x=340, y=1300, at=W(50), out=W(53) - .12),
        # CTA
        *diag_end(W, 53, 58, END, "On a acheté un logiciel, mais l'équipe est revenue au papier.", dark=True),
      ])
ALL["r11"] = r11

def r12(W, END):
    return dict(slug="r12-semaine-vacances", ground=INK, dark=True, grid="dots", glow="rgba(0,102,255,.22)",
      bg=[dict(t=W(9) - .12, c=SNOW, x=540, y=900, grid="lines", d=.45),
          dict(t=W(23) - .12, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.4),
          dict(t=W(37) - .15, c="#e8f2fd", x=540, y=1000, grid="hex", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Imagine.", c="white", s=215, align="c", y=720, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Tu pars", "{blue}une semaine."], c="white", s=140, align="c", y=300, at=W(1), out=W(6) - .05, om="up"),
        dict(k="num", **{"from": 1}, to=7, pre="Jour ", dur=1.0, s=200, c="white", align="c", y=800, at=W(2), out=W(9) - .08),
        dict(k="txt", lines=["Ton entreprise", "{blue}s'arrête ?"], c="white", s=130, align="c", y=300, at=W(6), out=W(9) - .08, om="up"),
        # CONTEXTE
        dict(k="txt", lines=["Pendant", "ton absence…"], s=130, align="c", y=300, at=W(9), out=W(23) - .12, om="up"),
        dict(k="card", av="DV", t="Les devis", b="En attente", cc="ink", x=110, y=760, w=860, at=W(10), out=W(23) - .12),
        dict(k="card", av="☎", t="Les clients", b="Rappellent", cc="ink", x=110, y=930, w=860, at=W(13), out=W(23) - .12),
        dict(k="card", av="?", t="Le dernier fichier", b="Introuvable", cc="red", x=110, y=1100, w=860, at=W(15), out=W(23) - .12),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(23), out=W(26) - .05),
        dict(k="strk", t="Ton équipe", c="white", s=150, y=420, at=W(26), cut=W(30), out=W(32) - .05),
        dict(k="txt", lines=["Tout est", "{blue}dans ta tête."], c="white", s=150, align="c", y=700, mode="punch", at=W(32), out=W(37) - .15),
        # RÉPONSE
        dict(k="lock", y=560, at=W(37) - .1, sp=1.9, tag="Ton majordome digital", out=W(40) + .05, om="shrink"),
        dict(k="txt", lines=["Tes process,", "{blue}écrits et outillés."], s=100, align="c", y=270, at=W(40), out=W(46) - .05, om="up"),
        dict(k="steps", y=640, gap=200, dim=False, at=W(41), out=W(55) - .1, items=[
             dict(n="✓", t="Qui fait quoi", at=W(42)), dict(n="✓", t="Où est chaque fichier", at=W(43)),
             dict(n="✓", t="Les modèles prêts", at=W(45))]),
        dict(k="txt", lines=["Chacun sait", "{blue}quoi faire."], s=130, align="c", y=270, at=W(46), out=W(50) - .05, om="up"),
        dict(k="txt", lines=["Et toi,", "{blue}tu pars vraiment."], s=110, align="c", y=270, at=W(50), out=W(55) - .1, om="up"),
        dict(k="chip", t="✓ Tout tourne sans toi", c="green", x=300, y=1300, at=W(52), out=W(55) - .1),
        # CTA
        *diag_end(W, 55, 60, END, "Quand je ne suis pas là, tout s'arrête : tout est dans ma tête."),
      ])
ALL["r12"] = r12

def r13(W, END):
    return dict(slug="r13-par-ou-commencer", ground=BLUE, dark=True, grid="dots",
      bg=[dict(t=W(12) - .12, c=INK, x=540, y=900, dark=True, grid="lines", d=.45),
          dict(t=W(19) - .12, c=SNOW, x=540, y=1000, grid="lines", d=.45),
          dict(t=W(33) - .15, c="#e8f2fd", x=540, y=1000, grid="hex", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Stop.", c="white", s=330, align="c", y=700, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Tu veux automatiser,", "{blue}mais par où", "{blue}commencer ?"], c="white", s=92, align="c", y=520, at=W(1), out=W(12) - .08, om="up"),
        # CONTEXTE
        dict(k="txt", lines=["Tout te semble", "{blue}urgent."], c="white", s=130, align="c", y=300, at=W(12), out=W(16) - .05, om="up"),
        dict(k="card", av="DV", t="Les devis", b="Urgent", cc="red", x=110, y=700, w=860, at=W(13), out=W(19) - .12),
        dict(k="card", av="FA", t="Les factures", b="Urgent", cc="red", x=110, y=870, w=860, at=W(14), out=W(19) - .12),
        dict(k="card", av="PL", t="Le planning", b="Urgent", cc="red", x=110, y=1040, w=860, at=W(15), out=W(19) - .12),
        dict(k="txt", lines=["Et rien", "{blue}n'avance."], c="white", s=130, align="c", y=300, at=W(16), out=W(19) - .12, om="up"),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", s=150, align="c", y=420, mode="punch", at=W(19), out=W(22) - .05),
        dict(k="txt", lines=["Automatiser un process", "{blue}mal pensé…"], s=88, align="c", y=330, at=W(22), out=W(27) - .05, om="up"),
        dict(k="txt", lines=["…c'est faire des erreurs", "{blue}plus vite."], s=84, align="c", y=330, at=W(27), out=W(33) - .15, om="up"),
        dict(k="race", x=92, y=820, w=896, at=W(27) + .1, out=W(33) - .15, lanes=[
             dict(l="À la main", t="Erreurs", c="#b9c4d6", reach=.35, dur=1.3),
             dict(l="Automatisé sans plan", t="Erreurs, plus vite", c="#e5484d", reach=1, dur=.9)]),
        # RÉPONSE
        dict(k="lock", y=560, at=W(33) - .1, sp=1.9, tag="Ton majordome digital", out=W(36) + .05, om="shrink"),
        dict(k="txt", lines=["D'abord, on cartographie", "{blue}tes tâches."], s=80, align="c", y=270, at=W(36), out=W(44) - .05, om="up"),
        dict(k="ring", x=340, y=620, w=400, h=400, at=W(40), to=30, suf=" min", ns=78, dur=1.2, arc=.5, out=W(44) - .05),
        dict(k="txt", lines=["Puis ta feuille de route,", "{blue}dans l'ordre."], s=86, align="c", y=270, at=W(44), out=W(53) - .1, om="up"),
        dict(k="steps", y=640, gap=220, at=W(45), out=W(53) - .1, items=[
             dict(t="Ce qui te coûte le plus", at=W(45) + .1), dict(t="Ce qui est simple", at=W(48)), dict(t="Le reste, ensuite", at=W(51))]),
        # CTA
        *diag_end(W, 53, 58, END, "Je veux automatiser, mais je ne sais pas par quoi commencer."),
      ])
ALL["r13"] = r13

def r14(W, END):
    nodes = [dict(cx=540, cy=640, t="Prévu dans le devis", ic="✎", at=W(38)),
             dict(cx=540, cy=920, t="Demandé à la signature", ic="€", at=W(42)),
             dict(cx=540, cy=1200, t="Relancé tout seul", ic="✉", at=W(47))]
    return dict(slug="r14-acompte", ground=SNOW, grid="lines",
      bg=[dict(t=W(8) - .12, c="#e8f2fd", x=540, y=900, grid="hex", d=.45),
          dict(t=W(23) - .12, c=INK, x=540, y=1000, dark=True, grid="lines", d=.45),
          dict(t=W(33) - .15, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.45),
          dict(t=W(50) - .12, c=INK, x=540, y=1300, dark=True, grid="lines", d=.5)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", t="Sérieux ?", s=210, align="c", y=720, mode="punch", at=-.3, out=W(1) - .02, od=.12),
        dict(k="txt", lines=["Encore un projet", "{blue}sans acompte ?"], s=120, align="c", y=300, at=W(1), out=W(8) - .08, om="up"),
        dict(k="morph", at=W(1), doc=dict(t="Devis signé", s=44), out=W(8) - .08, kf=[
             dict(t=W(1), x=310, y=1900, w=460, h=540, r=28, bg="#ffffff"),
             dict(t=W(1) + .7, x=310, y=700, w=460, h=540, r=28, bg="#ffffff", d=.7)]),
        dict(k="chip", t="Acompte : aucun", c="red", x=370, y=1290, at=W(5), out=W(8) - .08),
        # CONTEXTE
        dict(k="txt", lines=["Le client", "est {blue}sympa."], s=140, align="c", y=300, at=W(8), out=W(15) - .05, om="up"),
        dict(k="bub", x=130, y=760, w=820, at=W(11), td=1.0, out=W(15) - .05, t="Pas de souci, je vous règle à la fin !", meta="Le client · promis"),
        dict(k="txt", lines=["Puis le projet", "{blue}glisse."], s=140, align="c", y=300, at=W(15), out=W(19) - .05, om="up"),
        dict(k="txt", lines=["Et le paiement", "{blue}recule."], s=140, align="c", y=300, at=W(19), out=W(23) - .12, om="up"),
        dict(k="tl", x=170, y=900, w=740, at=W(15) + .1, draw=1.6, out=W(23) - .12, om="shrink", pts=[
             dict(x=0, d="Début", l="Projet lancé", at=W(15) + .1), dict(x=45, d="Prévu", l="Paiement", at=W(18)),
             dict(x=100, d="?", l="Paiement repoussé", o=1, at=W(21))]),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(23), out=W(26) - .05),
        dict(k="txt", lines=["Un acompte rassure", "{blue}aussi ton client."], c="white", s=96, align="c", y=300, at=W(26), out=W(33) - .15, om="up"),
        dict(k="card", av="✓", t="Toi", b="Tu démarres serein", cc="green", x=110, y=800, w=860, at=W(27), out=W(33) - .15),
        dict(k="card", av="✓", t="Ton client", b="Le projet est calé", cc="green", x=110, y=970, w=860, at=W(30), out=W(33) - .15),
        # RÉPONSE
        dict(k="lock", dark=True, y=560, at=W(33) - .1, sp=1.9, tag="Ton majordome digital", out=W(36) + .05, om="shrink"),
        dict(k="txt", lines=["L'acompte,", "{blue}prévu d'avance."], c="white", s=120, align="c", y=270, at=W(36), out=W(50) - .12, om="up"),
        dict(k="flow", at=W(38) - .1, out=W(50) - .12, lc="#ffffff", nodes=nodes, links=[[0, 1, W(42) - .3], [1, 2, W(47) - .3]]),
        # CTA
        *kit_end(W, 50, 57, END, dark=True),
      ])
ALL["r14"] = r14

def r15(W, END):
    return dict(slug="r15-vingt-deux-heures", ground=INK, dark=True, grid="lines", glow="rgba(0,102,255,.22)",
      bg=[dict(t=W(13) - .12, c=SNOW, x=540, y=900, grid="dots", d=.45),
          dict(t=W(32) - .12, c=BLUE, x=540, y=1000, dark=True, grid="dots", d=.4),
          dict(t=W(41) - .15, c="#e8f2fd", x=540, y=1000, grid="hex", d=.45)],
      cam=[dict(t=0, s=1.0), dict(t=END, s=1.03)],
      els=[
        # HOOK
        dict(k="txt", lines=["Regarde", "l'heure."], c="white", s=210, align="c", y=560, mode="punch", at=-.3, out=W(2) - .02, od=.12),
        dict(k="num", **{"from": 1305}, to=1320, dur=.9, fmt="h", s=280, c="white", align="c", y=320, at=W(2), out=W(13) - .08),
        dict(k="txt", lines=["Et tu es encore", "{blue}sur tes mails ?"], c="white", s=110, align="c", y=760, at=W(6), out=W(13) - .08, om="up"),
        # CONTEXTE
        dict(k="steps", y=360, gap=220, at=W(13), out=W(21) - .05, items=[
             dict(t="Relances", at=W(13) + .05), dict(t="Devis", at=W(14)), dict(t="Factures", at=W(15)), dict(t="Tableaux à jour", at=W(16))]),
        dict(k="txt", lines=["Pas ton métier.", "Mais personne", "{blue}d'autre ne le fait."], s=100, align="c", y=500, at=W(21), out=W(32) - .12, om="up"),
        # RE-HOOK
        dict(k="txt", t="Et le pire ?", c="white", s=150, align="c", y=420, mode="punch", at=W(32), out=W(35) - .05),
        dict(k="txt", lines=["Tout ça peut", "tourner {blue}sans toi."], c="white", s=120, align="c", y=330, at=W(35), out=W(41) - .15, om="up"),
        dict(k="arc", x=390, y=820, w=300, h=300, col="#ffffff", at=W(36), out=W(41) - .15),
        # RÉPONSE
        dict(k="lock", y=560, at=W(41) - .1, sp=1.9, tag="Ton majordome digital", out=W(44) + .05, om="shrink"),
        dict(k="txt", lines=["Tes tâches répétitives", "deviennent", "{blue}un outil simple."], s=88, align="c", y=270, at=W(44), out=W(51) - .05, om="up"),
        dict(k="card", av="OS", t="Ton outil", b="Relances · devis · factures", cc="blue", x=110, y=900, w=860, at=W(47), out=W(51) - .05),
        dict(k="txt", lines=["Tu as mieux", "{blue}à faire."], s=170, align="c", y=560, mode="punch", at=W(51), out=W(56) - .1),
        # CTA
        *diag_end(W, 56, 61, END, "Je passe mes soirées sur les relances, les devis et les factures."),
      ])
ALL["r15"] = r15
