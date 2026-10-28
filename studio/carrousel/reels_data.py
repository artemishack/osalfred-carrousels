"""15 reels : un tous les 2 jours (23/10 -> 20/11). Cible : dirigeants TPE/PME, indépendants.
Chaque beat = (texte dit, titre à l'écran). *mot* = mot en bleu."""

CTA = {
    "kit": ("Les messages mot pour mot sont dans le kit gratuit. Écris KIT en commentaire, ou va sur osalfred.com/kit.",
            "Le kit *gratuit*"),
    "diag": ("Audit gratuit de trente minutes, feuille de route sous quarante-huit heures. Écris DIAG en commentaire.",
             "Audit *gratuit*"),
}

REELS = [
 dict(date="2026-10-23", slug="r01-devis-silence", cta="kit", theme="nuit", beats=[
  ("Ton devis est parti il y a dix jours. Et depuis… silence.", "Devis envoyé. *Silence.*"),
  ("Tu te dis qu'il réfléchit. En vrai, il a oublié. Ou un concurrent l'a relancé avant toi.", "Il n'a pas *réfléchi.* Il a oublié."),
  ("Le client ne choisit pas toujours le meilleur. Il choisit celui qui revient vers lui.", "Il choisit celui qui *revient.*"),
  ("Une relance à J+3. Une autre à J+7. Courte, polie, utile. Et elle part toute seule.", "J+3, J+7. *Automatique.*"),
 ]),
 dict(date="2026-10-25", slug="r02-excel-patron", cta="diag", theme="snow", beats=[
  ("Ton fichier Excel a quarante onglets. Et une seule personne sait s'en servir. [short pause] Toi.", "40 onglets. *1 seule personne.*"),
  ("Chaque matin, tu recopies. Tu vérifies. Tu répares une formule cassée.", "Recopier. Vérifier. *Réparer.*"),
  ("Un tableur, c'est parfait pour démarrer. Mais quand toute ton activité repose dessus, c'est lui qui te dirige.", "Ton tableur est devenu *ton patron.*"),
  ("La bonne question, ce n'est pas quel logiciel acheter. C'est : qu'est-ce que tu refais à la main, chaque semaine ? On part de là, et on construit un outil simple, autour de ta façon de travailler.", "Un outil *autour de toi.*"),
 ]),
 dict(date="2026-10-27", slug="r03-cinq-taches", cta="kit", theme="bleu", beats=[
  ("Cinq tâches qu'un dirigeant ne devrait plus faire à la main.", "5 tâches à *ne plus faire* à la main"),
  ("Un. Relancer les devis sans réponse. Deux. Relancer les factures impayées.", "1. Relancer les devis\n2. Relancer les *factures*"),
  ("Trois. Recopier les mêmes infos client dans trois outils.", "3. Recopier les *mêmes infos*"),
  ("Quatre. Répondre dix fois par jour aux mêmes questions. Cinq. Chercher un document dans ses mails.", "4. Les mêmes *questions*\n5. Fouiller ses *mails*"),
  ("Chacune prend cinq minutes. Ensemble, elles te mangent tes soirées.", "5 minutes chacune. *Tes soirées* au total."),
 ]),
 dict(date="2026-10-29", slug="r04-facture-retard", cta="kit", theme="brume", beats=[
  ("Ton client te doit de l'argent. Et c'est toi qui es gêné de le relancer.", "Il te doit de l'argent. *Et c'est toi qui es gêné.*"),
  ("On a tous ce réflexe : attendre. Ne pas froisser. Espérer que ça arrive.", "Attendre. *Espérer.*"),
  ("Sauf qu'une facture qu'on ne relance pas, c'est une facture qui passe en dernier.", "Pas relancée = *payée en dernier*"),
  ("La solution : une relance prévue dès l'envoi. Un rappel avant l'échéance, le jour même, puis une semaine après. Le ton reste cordial, et tu n'as plus à y penser.", "Relance prévue *dès l'envoi*"),
 ]),
 dict(date="2026-10-31", slug="r05-50-fonctions", cta="diag", theme="nuit", beats=[
  ("Tu n'as pas besoin d'un logiciel à cinquante fonctionnalités.", "50 fonctionnalités. *Tu en utilises 3.*"),
  ("Tu en utilises trois. Les quarante-sept autres te compliquent la vie, et tu les paies chaque mois.", "47 qui te *compliquent la vie*"),
  ("Ce qu'il te faut, c'est un outil qui fait exactement ce que fait ton entreprise. Pas plus.", "Exactement ce que tu fais. *Pas plus.*"),
  ("Chez O.S. Alfred, on part de tes process, on les fixe dans un cahier des charges validé par écrit, et on construit l'outil autour.", "Cahier des charges *validé par écrit*"),
 ]),
 dict(date="2026-11-02", slug="r06-ia-copier-coller", cta="diag", theme="bleu", beats=[
  ("L'IA ne va pas remplacer ton entreprise. Elle va remplacer tes copier-coller.", "L'IA va remplacer *tes copier-coller.*"),
  ("Le mail que tu réécris chaque jour. Le compte rendu après chaque rendez-vous. Le devis que tu retapes à partir d'une note vocale.", "Mail. Compte rendu. *Devis.*"),
  ("C'est là que l'IA est utile. Pas dans les grandes promesses. Dans les petites tâches qui reviennent tout le temps.", "Les petites tâches *qui reviennent*"),
  ("Branchée sur tes outils, elle prépare. Toi, tu valides.", "Elle prépare. *Tu valides.*"),
 ]),
 dict(date="2026-11-04", slug="r07-site-nuit", cta="diag", theme="snow", beats=[
  ("Ton site devrait travailler pendant que tu dors.", "Ton site devrait *travailler la nuit.*"),
  ("Aujourd'hui, il affiche ton numéro. Et il attend.", "Il affiche ton numéro. *Et il attend.*"),
  ("Un vrai site répond aux questions fréquentes. Il qualifie la demande. Il propose un créneau. Et il t'envoie un résumé propre, le matin.", "Répondre. Qualifier. *Réserver.*"),
  ("Si ton site ne fait rien de tout ça, c'est une plaquette. Pas un outil.", "Une plaquette. *Pas un outil.*"),
 ]),
 dict(date="2026-11-06", slug="r08-appel-manque", cta="diag", theme="brume", beats=[
  ("Ton téléphone sonne. Tu es en rendez-vous. Tu ne réponds pas.", "Appel *manqué.*"),
  ("Le prospect, lui, appelle le suivant sur la liste.", "Il appelle *le suivant.*"),
  ("Ce n'est pas un problème de disponibilité. C'est un problème de système.", "Pas un problème de temps. *De système.*"),
  ("Un SMS automatique répond à l'appel manqué. Un lien lui permet de décrire son besoin. Et tu rappelles avec toutes les infos, au bon moment.", "SMS auto. Besoin décrit. *Tu rappelles prêt.*"),
 ]),
 dict(date="2026-11-08", slug="r09-double-saisie", cta="diag", theme="nuit", beats=[
  ("Combien de fois tu tapes le nom du même client ?", "Combien de fois *le même nom ?*"),
  ("Une fois dans le devis. Une fois dans la facture. Une fois dans l'agenda. Une fois dans ton suivi.", "Devis. Facture. Agenda. *Suivi.*"),
  ("Chaque saisie, c'est du temps. Et chaque saisie, c'est une erreur possible.", "Chaque saisie = *une erreur possible*"),
  ("Une information devrait être saisie une seule fois. Ensuite, elle circule toute seule entre tes outils.", "Saisie *une seule fois*"),
 ]),
 dict(date="2026-11-10", slug="r10-marge-reelle", cta="diag", theme="bleu", beats=[
  ("Ta marge réelle, sur ton dernier projet. Tu la connais ?", "Ta marge réelle. *Tu la connais ?*"),
  ("Pas le prix de vente. Pas le chiffre d'affaires. La marge, une fois le temps passé et les achats comptés.", "Temps passé + achats. *Ce qui reste.*"),
  ("Beaucoup de dirigeants la découvrent… chez le comptable. Des mois plus tard.", "Découverte *des mois plus tard*"),
  ("Un tableau de bord simple, alimenté au fil de l'eau, te la donne pendant le projet. Quand tu peux encore agir.", "Pendant le projet. *Quand tu peux agir.*"),
 ]),
 dict(date="2026-11-12", slug="r11-outils-abandonnes", cta="diag", theme="snow", beats=[
  ("Pourquoi tes nouveaux outils sont abandonnés au bout de trois semaines ?", "Abandonné *en 3 semaines*"),
  ("Parce qu'on t'a vendu un outil. Puis on t'a demandé de changer ta façon de travailler pour lui.", "On t'a demandé de *t'adapter à l'outil*"),
  ("Résultat : l'équipe revient au papier, aux mails, aux vieilles habitudes.", "Retour au *papier.*"),
  ("L'ordre est inverse. D'abord comprendre comment tu travailles. Ensuite construire l'outil qui colle à ça. Et le mettre en place avec toi.", "L'outil s'adapte *à toi.*"),
 ]),
 dict(date="2026-11-14", slug="r12-tout-passe-par-toi", cta="diag", theme="brume", beats=[
  ("Si tu pars une semaine, ton entreprise s'arrête ?", "Tu pars une semaine. *Tout s'arrête ?*"),
  ("Les devis attendent. Les questions s'accumulent. Personne ne sait où est le dernier fichier.", "Où est *le dernier fichier ?*"),
  ("Ce n'est pas un manque d'équipe. C'est que tout est dans ta tête.", "Tout est *dans ta tête.*"),
  ("Quand les process sont écrits et outillés, chacun sait quoi faire. Et toi, tu peux enfin décrocher.", "Écrit. Outillé. *Tu décroches.*"),
 ]),
 dict(date="2026-11-16", slug="r13-avant-automatiser", cta="diag", theme="nuit", beats=[
  ("Avant d'automatiser quoi que ce soit, fais ça.", "Avant d'automatiser, *fais ça.*"),
  ("Prends une feuille. Écris chaque étape, du premier contact jusqu'au paiement.", "Du premier contact *au paiement*"),
  ("Entoure ce que tu fais chaque semaine. Barre ce qui ne sert à rien.", "Entoure. *Barre.*"),
  ("Automatiser un process mal pensé, c'est juste faire des erreurs plus vite. Ce qui reste entouré, c'est ton cahier des charges.", "Mal pensé = *des erreurs plus vite*"),
 ]),
 dict(date="2026-11-18", slug="r14-acompte", cta="kit", theme="bleu", beats=[
  ("Tu commences encore un projet sans acompte ?", "Un projet *sans acompte ?*"),
  ("Le client est sympa. Il a promis. Tu lui fais confiance.", "Il a *promis.*"),
  ("Puis le projet glisse, les demandes s'ajoutent, et le paiement recule.", "Le paiement *recule.*"),
  ("L'acompte, ce n'est pas de la méfiance. C'est un engagement des deux côtés. Prévu dans le devis, demandé à la signature, relancé tout seul s'il n'arrive pas.", "Un engagement *des deux côtés*"),
 ]),
 dict(date="2026-11-20", slug="r15-mieux-a-faire", cta="diag", theme="snow", beats=[
  ("Il est vingt-deux heures. Tu es encore sur tes mails.", "22h. *Encore tes mails.*"),
  ("Pas parce que c'est important. Parce que personne d'autre ne peut le faire.", "Personne d'autre *ne peut le faire.*"),
  ("Les relances. Les devis. Les factures. Les tableaux à mettre à jour. Tout ça peut tourner sans toi, avec des outils simples, construits pour ton entreprise.", "Tout ça peut *tourner sans toi.*"),
  ("Tu as monté ta boîte pour faire ton métier. [short pause] Tu as mieux à faire.", "Tu as *mieux à faire.*"),
 ]),
]

def script(r):
    return " ".join(t for t, _ in r["beats"]) + " " + CTA[r["cta"]][0]

CAPTION = {
 "r01-devis-silence": "Un devis sans réponse, ce n'est pas un non. C'est souvent un oubli.\n\nUne relance à J+3, une autre à J+7. Courte, polie, et elle part toute seule.",
 "r02-excel-patron": "Ton tableur a pris le pouvoir ?\n\nAvant de chercher un logiciel, liste ce que tu refais à la main chaque semaine. C'est ça, le vrai cahier des charges.",
 "r03-cinq-taches": "5 tâches qu'un dirigeant ne devrait plus faire à la main.\n\nEnregistre la vidéo et compte combien tu en fais encore.",
 "r04-facture-retard": "Relancer une facture, ce n'est pas être lourd. C'est être pro.\n\nLa relance se prévoit dès l'envoi : avant l'échéance, le jour J, puis J+7.",
 "r05-50-fonctions": "Tu paies 50 fonctionnalités. Tu en utilises 3.\n\nUn outil utile fait ce que fait ton entreprise. Pas plus.",
 "r06-ia-copier-coller": "L'IA ne va pas remplacer ton entreprise. Elle va remplacer tes copier-coller.\n\nMails, comptes rendus, devis : elle prépare, tu valides.",
 "r07-site-nuit": "Ton site affiche ton numéro. Et il attend.\n\nUn vrai site répond, qualifie, propose un créneau et te résume tout le matin.",
 "r08-appel-manque": "Un appel manqué, c'est souvent un client qui appelle le suivant.\n\nSMS automatique, besoin décrit, et tu rappelles avec toutes les infos.",
 "r09-double-saisie": "Le même nom de client, tapé 4 fois.\n\nUne information se saisit une seule fois. Ensuite, elle circule toute seule.",
 "r10-marge-reelle": "Ta marge réelle sur ton dernier projet, tu la connais ?\n\nLa connaître pendant le projet, c'est pouvoir encore agir.",
 "r11-outils-abandonnes": "Pourquoi tes outils sont abandonnés au bout de 3 semaines ?\n\nParce que c'est l'outil qui doit s'adapter à toi. Pas l'inverse.",
 "r12-tout-passe-par-toi": "Tu pars une semaine. Tout s'arrête ?\n\nCe n'est pas un manque d'équipe. C'est que tout est dans ta tête.",
 "r13-avant-automatiser": "Avant d'automatiser quoi que ce soit, prends une feuille.\n\nAutomatiser un process mal pensé, c'est faire des erreurs plus vite.",
 "r14-acompte": "Un projet sans acompte, c'est un paiement qui recule.\n\nL'acompte n'est pas de la méfiance. C'est un engagement des deux côtés.",
 "r15-mieux-a-faire": "22h. Encore tes mails.\n\nRelances, devis, factures, tableaux : tout ça peut tourner sans toi. Tu as mieux à faire.",
}
TAGS = "#tpe #pme #entrepreneur #dirigeant #automatisation #digitalisation #gestiondentreprise"

def caption(r, net):
    c = CAPTION[r["slug"]]
    if r["cta"] == "kit":
        end = ("Les messages mot pour mot sont dans le kit gratuit. Écris KIT en commentaire, ou lien en bio."
               if net == "ig" else "Les messages mot pour mot sont dans le kit gratuit : https://osalfred.com/kit/")
    else:
        end = ("Audit gratuit de 30 min, feuille de route sous 48h. Écris DIAG en commentaire."
               if net == "ig" else "Audit gratuit de 30 min, feuille de route sous 48h : https://osalfred.com/rendez-vous/")
    return f"{c}\n\n{end}\n\n{TAGS}"
