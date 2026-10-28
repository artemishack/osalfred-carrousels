"""Légendes v7 (IG / FB) — on vend le résultat. Zéro chiffre inventé."""
TAGS = "#tpe #pme #entrepreneur #dirigeant #automatisation #digitalisation #gestiondentreprise"
KIT = "kit"
B = {
 "r01": ("Un devis sans réponse, c'est rarement un non. C'est souvent un oubli.\n\nAvec OS Alfred, chaque devis est relancé tout seul, à J+3 puis à J+7. Toi, tu n'y penses plus.", KIT),
 "r02": ("Les devis d'un côté, les factures de l'autre, et un tableau à remettre à jour chaque semaine.\n\nTu peux garder tes habitudes et ne plus rien recopier : tu saisis une fois, tout se met à jour.", None),
 "r03": ("Relancer les devis. Relancer les factures. Caler les rendez-vous. Répondre aux mêmes questions. Faire le point de la semaine.\n\nAucune de ces tâches ne demande ton expertise. Elles peuvent tourner toutes seules, et tu récupères tes soirées.", KIT),
 "r04": ("Une facture qu'on ne relance pas passe toujours en dernier.\n\nLa relance prévue dès l'envoi : un rappel avant l'échéance, puis un message ferme et poli. Tu es payé sans courir après.", KIT),
 "r05": ("Un abonnement chaque mois, des fonctions jamais ouvertes, des contournements pour le reste.\n\nCe que tu cherches est souvent simple. On part de ta façon de travailler, et on construit l'outil qui fait exactement ça. Rien de plus.", None),
 "r06": ("Comptes rendus, devis à partir de tes notes, réponses aux clients : des heures de frappe chaque semaine.\n\nL'IA prépare tes messages et tes documents. Toi, tu relis et tu valides.", None),
 "r07": ("Ton site affiche ton numéro, et il attend. Les questions arrivent en plein chantier.\n\nIl pourrait répondre aux questions, proposer un créneau, et t'envoyer un résumé propre chaque matin.", None),
 "r08": ("En rendez-vous, le téléphone sonne. Tu rappelles deux heures plus tard : il a appelé le suivant.\n\nChaque appel manqué peut recevoir un SMS dans la minute, avec un lien pour décrire son besoin. Tu rappelles avec toutes les infos.", None),
 "r09": ("Le même client tapé dans le devis, la facture, l'agenda et le suivi. Quatre fois la même info, quatre chances de te tromper.\n\nTu saisis une fois, et l'info circule toute seule entre tes outils.", None),
 "r10": ("Pas le prix de vente : ce qui reste une fois les achats et ton temps payés.\n\nTa marge peut s'afficher pendant le projet, quand tu peux encore agir. Pas au bilan.", None),
 "r11": ("Semaine 1, on essaie. Semaine 2, on contourne. Semaine 3, retour au papier.\n\nLe problème n'était pas ton équipe, c'était l'outil. On part de tes habitudes, et l'outil s'y adapte.", None),
 "r12": ("Si tu pars une semaine, qu'est-ce qui s'arrête ?\n\nCe n'est pas un problème d'équipe : tout est dans ta tête. Des process écrits et outillés, et chacun sait quoi faire.", None),
 "r13": ("Automatiser un process mal pensé, c'est faire des erreurs plus vite.\n\nD'abord on cartographie tes tâches en 30 minutes. Puis tu reçois une feuille de route, dans l'ordre.", None),
 "r14": ("Le client est sympa, il a promis. Puis le projet glisse, et le paiement recule.\n\nUn acompte rassure aussi ton client. Prévu dans le devis, demandé à la signature, relancé tout seul.", KIT),
 "r15": ("22 h, et tu es encore sur tes mails. Relances, devis, factures, tableaux.\n\nCe n'est pas ton métier. Tes tâches répétitives peuvent devenir un outil simple. Tu as mieux à faire.", None),
}
def caption(r, net):
    body, kind = B[r]
    if kind == KIT:
        cta = "Les messages mot pour mot sont dans le kit gratuit. Écris KIT en commentaire, ou lien en bio." if net == "ig" else "Les messages mot pour mot sont dans le kit gratuit : https://osalfred.com/kit/"
    else:
        cta = "Décris ton problème sur osalfred.com (lien en bio) et reçois ta feuille de route sous 48 h." if net == "ig" else "Décris ton problème sur https://osalfred.com/diagnostic/ et reçois ta feuille de route sous 48 h."
    return f"{body}\n\n{cta}\n\n{TAGS}"
