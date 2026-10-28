from engine import s_hook as H, s_statement as S, s_step as ST, s_list as L, s_dark as D, s_cta as C

def hook(kicker, title, sub="", pose="telephone"): return (H, dict(kicker=kicker, title=title, sub=sub, pose=pose))
def st(title, sub="", pose="bras-croises"): return (S, dict(title=title, sub=sub, pose=pose))
def step(label, title, card, note="", pose=None, card_blue=True): return (ST, dict(label=label, title=title, card=card, note=note, pose=pose, card_blue=card_blue))
def lst(title, items, pose="telephone", label=None): return (L, dict(title=title, items=items, pose=pose, label=label))
def dark(title, card="", note="", label=None): return (D, dict(label=label, title=title, card=card, note=note))
def cta(q): return (C, dict(question=q))

CAR = {}

CAR["c01-devis"] = [
    hook("Devis", "Les 3 messages qui *font signer* un devis déjà envoyé.", "Mot pour mot. À copier ce soir."),
    st("Un devis sans relance ne meurt pas. *Il s'endort.*", "Le client n'a pas dit non. Il a oublié, il compare, ou il attend un déclic."),
    step("J+3", "Le message court. SMS ou WhatsApp.", "« Bonjour [prénom], je reviens vers vous pour le devis [travaux] envoyé lundi. Vous avez pu le regarder ? Je reste dispo si une ligne n'est pas claire. »", "Court. Sans pression. *C'est celui qu'il lit vraiment.*", pose="telephone"),
    lst("L'appel à J+7. Trois phrases, pas plus.", ["« Je vous appelle pour le devis [travaux], vous en êtes où ? »", "S'il hésite : « Qu'est-ce qui vous fait hésiter, le prix, le délai, ou autre chose ? »", "« Je bloque une date de démarrage, ou on se rappelle la semaine prochaine ? »"], pose="telephone"),
    dark("J+15 : le mail qui clôt. Souvent celui qui fait revenir le client.", "« Bonjour [prénom], sans nouvelles de votre part, je considère que le projet est en pause et je libère le créneau prévu. Si vous souhaitez le relancer, il suffit de répondre à ce mail. »", "Tu ne supplies pas. *Tu fermes la porte poliment.*"),
    st("Après J+15, *tu passes au suivant.*", "Un client qu'on force à dire oui, c'est un chantier qui se passe mal.", pose="classeur"),
    cta("Et toi, tu en signes combien sur 10 ? *Dis-le en commentaire.*"),
]


CAR["c02-ouvriers"] = [
    hook("Patrons du bâtiment", "J'ai lu *100 commentaires d'ouvriers.* Voilà ce qu'ils veulent.", "Sous une vidéo sur les salaires du bâtiment.", "bras-croises"),
    st("Le salaire revient. *Mais pas en premier.*", "La plupart parlent d'autre chose que d'une augmentation de 200 €."),
    lst("Ce qui revient le plus", ["« Parle en net, s'il te plaît. » Le brut sonne comme une façon de cacher la paie.", "L'ambiance et la façon dont le patron leur parle.", "Du matériel qui marche et des horaires tenus."], pose="classeur"),
    dark("« Quand on vient d'en bas, *on peut être un bon patron.* »", "", "Ils ne demandent pas un patron parfait. Ils demandent un patron *qui tient sa parole.*"),
    lst("Ce que tu peux changer lundi", ["Annoncer les salaires en net, primes comprises.", "Un point de 15 minutes par semaine avec chaque équipe.", "Remplacer l'outil qui les fait râler depuis 6 mois."], pose="bras-croises"),
    cta("Et chez toi, *qu'est-ce qui fait partir les bons ?*"),
]

CAR["c03-situations"] = [
    hook("Trésorerie", "Chantier de 40 k€ : pourquoi tu dois *facturer 3 fois,* pas 1.", "Tu avances le matériel et les salaires. Ton client, lui, attend la fin."),
    st("Facturer à la fin, c'est *porter le chantier à la place du client.*", "Pendant des semaines, c'est ta trésorerie qui finance ses travaux.", pose="classeur"),
    lst("L'échéancier sur 40 k€", ["*30 % à la signature* : 12 000 €. Le matériel est couvert.", "*40 % à mi-chantier* : 16 000 €, sur situation de travaux.", "*30 % à la réception* : 12 000 €. Le solde, pas tout."], pose=None),
    step("LA RÈGLE", "Facture le jour de la fin. Pas le 31.", "Chantier fini le 2, facture envoyée le 31 : tu viens d'offrir 29 jours de crédit gratuit à ton client.", "Sur une année, *ça se compte en dizaines de milliers d'euros.*"),
    dark("Écris l'échéancier *dans le devis.*", "« Acompte de 30 % à la signature, 40 % sur situation à mi-chantier, solde de 30 % à la réception des travaux. »", "Signé par le client = *pas de discussion le jour J.*"),
    cta("Tu factures en *combien de fois* aujourd'hui ?"),
]

CAR["c04-delais"] = [
    hook("Trésorerie", "Facture en attente depuis décembre ? *Voilà ce qu'elle te coûte.*", "Un calcul simple, sur une boîte du 2nd œuvre à 600 k€."),
    st("*600 k€* de CA. Clients payés à *90 jours.*", "En permanence, environ 148 000 € dorment chez tes clients.", pose="classeur"),
    st("Même boîte, payée à *30 jours.*", "Environ 49 000 € dehors. Pas un euro de CA en plus."),
    dark("La différence : *environ 100 000 €.*", "", "C'est souvent exactement *le montant de ton découvert.* Tu ne manques pas d'argent : il est chez tes clients."),
    step("LA PHRASE", "À mettre dans tes devis et tes CGV", "« Paiement à réception de facture. Tout retard entraîne des pénalités et, pour les professionnels, une indemnité forfaitaire de 40 € pour frais de recouvrement. »", card_blue=False),
    cta("Ta plus vieille facture impayée, *elle date de quand ?*"),
]

CAR["c05-camion"] = [
    hook("Équipe", "Ton camion est *le premier devis* que voit le client.", "Avant ton prix, avant ton travail, il voit ça.", "classeur"),
    st("Un camion en vrac, c'est *du matériel perdu* et une image qui coûte cher.", "Et le lundi, la phrase connue : « on n'a pas le bon matériel ».", pose="telephone"),
    lst("La prime camion propre", ["Une règle claire : rangé, propre, matériel complet.", "Un montant symbolique, mais tous les mois.", "Une photo du camion le vendredi soir. C'est le contrôle."], pose="bras-croises"),
    dark("Ce que tu récupères *n'est pas la prime.*", "", "C'est le matériel retrouvé, les allers-retours au dépôt évités et *un client qui te fait confiance avant de lire ton devis.*"),
    cta("Ta prime, *tu la mets en place ce mois-ci ?*"),
]

CAR["c06-bouche"] = [
    hook("Trouver des chantiers", "« Ça sera toujours le bouche-à-oreille. » *Jusqu'au mois creux.*", "", "bras-croises"),
    st("Le bouche-à-oreille *ne se pilote pas.*", "Tu ne peux ni l'accélérer, ni le prévoir, ni l'allumer quand le planning se vide.", pose="telephone"),
    st("Il te ramène *des clients qui te ressemblent.*", "Si on te recommande parce que tu n'es pas cher, on t'enverra des clients qui cherchent le pas cher.", pose="classeur"),
    dark("Quand le carnet se vide, *il est déjà trop tard.*", "", "Les chantiers de mars se décident en décembre."),
    lst("Les 2 canaux à ajouter", ["Ta fiche Google, avec de vraies photos de chantier.", "Des contenus qui montrent comment tu travailles, avant que le client t'appelle."], pose="telephone"),
    cta("Tes 3 derniers chantiers, *ils venaient d'où ?*"),
]

CAR["c07-devis-soir"] = [
    hook("Devis", "Sortir les devis de tes soirées *en 3 réglages.*", "23h30, le repas est loin, le devis n'est pas fini."),
    step("1", "Une bibliothèque d'ouvrages chiffrés", "Tes 30 postes les plus courants, déjà chiffrés : main-d'œuvre, fourniture, temps. Le devis devient un assemblage.", pose="classeur"),
    step("2", "Un créneau fixe dans la semaine", "Mardi et jeudi, 7h-8h30. Les devis ne se font plus à 23h, ils ont leur place dans l'agenda.", card_blue=False),
    step("3", "Une visite technique structurée", "Toujours les mêmes questions, les mêmes photos, les mêmes cotes. Une visite bien faite, c'est un devis à moitié fait.", pose="telephone"),
    dark("Et ce qui peut *ne plus passer par toi* :", "La mise en forme, l'envoi, et la relance du devis.", "Toi, tu gardes le chiffrage. *Le reste peut tourner sans toi.*"),
    cta("Tu es plutôt *devis du soir ou du dimanche ?*"),
]

CAR["c08-relance-facture"] = [
    hook("Se faire payer", "Ta facture a 45 jours. *Voici le message à envoyer ce soir.*", "Mot pour mot."),
    st("Celui qui appelle *est payé avant* celui qui envoie un mail.", "Un client qui doit de l'argent à cinq entreprises paie dans l'ordre où on le relance.", pose="telephone"),
    step("LE MESSAGE", "Poli, factuel, avec une date", "« Bonjour [prénom], je reviens vers vous pour la facture [n°] du [date], d'un montant de [montant]. Je ne vois pas encore le règlement. Pouvez-vous me dire quand il est prévu ? »", "Tu ne te justifies pas. *Tu demandes une date.*"),
    lst("En B2B, sur chaque facture", ["La date d'échéance.", "Le taux des pénalités de retard.", "L'indemnité forfaitaire de 40 € pour frais de recouvrement."], pose=None),
    dark("Sans réponse après 2 relances : *la mise en demeure.*", "", "Par écrit, avec un délai précis. *Souvent, elle suffit.*"),
    cta("Combien de factures en retard *dans ta boîte en ce moment ?*"),
]

CAR["c09-prix-bas"] = [
    hook("Prix", "Si personne ne discute ton prix, *il est trop bas.*", "", "bras-croises"),
    st("« Ce sont les *prix de 2015.* »", "Commentaire d'un artisan sous un devis peinture partagé en ligne.", pose="telephone"),
    st("Le bouche-à-oreille du pas cher *te ramène du pas cher.*", "Et les chantiers dont personne ne veut.", pose="classeur"),
    lst("Augmenter un client existant", ["Annonce-le à l'avance, avec une date.", "Explique ce qui a changé : matériaux, charges, garanties.", "Applique-le à tous. Pas d'exception discrète."], pose="bras-croises"),
    dark("Un artisan l'a fait.", "« Depuis 2 mois je facture 2 fois plus cher. Je travaille deux fois moins, je gagne le même argent. »", "On ne le recommande plus pour son prix. *On le recommande pour son travail.*"),
    cta("Ta dernière hausse de prix, *c'était quand ?*"),
]

CAR["c10-journee"] = [
    hook("Rentabilité", "« Comment calculer la journée d'un salarié ? » *En 4 lignes.*", "Une question qui revient sans arrêt sous les vidéos de gestion.", "classeur"),
    step("1", "Son coût chargé à l'année", "Exemple : 40 000 € par an, salaire et charges patronales compris.", card_blue=False),
    step("2", "Ses heures vraiment productives", "Pas 1 607 h. Retire congés, intempéries, trajets, SAV, dépôt. Exemple : 1 400 h facturables.", "40 000 € ÷ 1 400 h = *28,60 € de coût par heure.*", pose="telephone"),
    step("3", "La part des frais de structure", "Camions, assurances, bureau, logiciels, ton salaire de gestion. Exemple : + 15 € par heure.", "Coût complet : *43,60 € par heure.*", card_blue=False),
    dark("4. Ajoute ta marge.", "Avec 15 % de marge : 43,60 € ÷ 0,85 ≈ 51 € HT de l'heure, soit environ 360 € HT la journée de 7 h.", "Tes chiffres ne sont pas ceux-là. *La méthode, si.*"),
    cta("Tu vends la journée d'un gars *à combien aujourd'hui ?*"),
]

CAR["c11-coordination"] = [
    hook("Chantier", "Le message de la veille *qui évite la reprise* du lendemain.", "« Le plaquiste discute pas avec l'électricien. Après, l'électricien fait des trous partout dans le placo. »"),
    st("Une reprise ne coûte *jamais seulement une heure.*", "Trajet, matériel, planning décalé, client à rassurer.", pose="classeur"),
    step("LA VEILLE", "Un message aux autres corps d'état", "« Demain on ferme les cloisons de la pièce 2. Gaines et boîtiers à passer avant 10h. Photo des réservations jointe. »", "Une photo, une contrainte, *une heure limite.*"),
    lst("La réunion de chantier courte", ["Qui passe avant qui cette semaine.", "Ce qui bloque, et qui le débloque.", "La prochaine étape qui ferme quelque chose."], pose="telephone"),
    cta("Une reprise à cause d'un autre corps d'état *ce mois-ci ?*"),
]

CAR["c12-acompte"] = [
    hook("Trésorerie", "Le client qui refuse 30 % d'acompte *vient de te dire quelque chose.*", "", "bras-croises"),
    st("L'acompte n'est pas *de la méfiance.*", "C'est une condition normale, pratiquée par les entreprises bien gérées.", pose="telephone"),
    st("Fourchette courante : *20 à 30 %* à la signature.", "De quoi couvrir le matériel, sans que tu avances l'argent.", pose="classeur"),
    step("LA PHRASE", "Pour l'annoncer sans gêne", "« Pour réserver votre créneau et commander les matériaux, je demande un acompte de 30 % à la signature. Le reste suit l'avancement du chantier. »", card_blue=False),
    dark("Un refus *est une information.*", "", "Un client qui ne peut pas avancer 30 % aujourd'hui *aura du mal à payer 100 % demain.*"),
    cta("Tu demandes *combien d'acompte ?*"),
]

CAR["c13-marge"] = [
    hook("Rentabilité", "Ta marge ne disparaît pas. *Elle fuit par 4 trous.*", "", "classeur"),
    dark("« On est 12. Marge nette 2024 : *1,6 %.* »", "", "Un autre, à 3 salariés : *4,5 %.* Deux chiffres réels, donnés en commentaire par des patrons."),
    lst("Les 4 fuites", ["Les heures passées mais jamais facturées.", "Les reprises : on revient, on ne facture pas.", "Les déplacements sous-estimés.", "Les « petits trucs en plus » offerts."], pose="telephone"),
    st("Un point de marge sur *800 k€ de CA,* c'est *8 000 €.*", "Par an. Sans un chantier de plus.", pose="bras-croises"),
    cta("Ta marge nette, *tu la connais au point près ?*"),
]

CAR["c14-google"] = [
    hook("Trouver des chantiers", "4 réglages Google qui ramènent *des demandes sérieuses.*", "Le client t'a trouvé sur Google. Puis il est parti."),
    lst("Les 4 réglages", ["De vraies photos de chantier, avant et après. Pas d'images de banque.", "Ta zone d'intervention, ville par ville.", "L'avis demandé le jour de la réception, pas un mois après.", "Une réponse à chaque avis, même court."], pose=None),
    st("Une fiche sans photo, *c'est un client qui passe au suivant.*", "Il veut voir ce que tu fais avant de t'appeler.", pose="telephone"),
    cta("Ta fiche Google, *elle a combien d'avis ?*"),
]

CAR["c15-oubli"] = [
    hook("Devis", "Le client n'a pas dit non. *Il a oublié.*", "", "telephone"),
    dark("« Je cours pas derrière les clients. *On est les médecins, eux les patients.* »", "", "Un avis fréquent. Mais un devis n'est pas une ordonnance."),
    st("Un devis perdu, c'est *du temps de chiffrage jeté.*", "Visite, calcul, mise en forme. Souvent 2 à 3 heures.", pose="classeur"),
    st("Relancer *n'est pas supplier.*", "C'est finir le travail commencé avec le devis.", pose="bras-croises"),
    step("LA RELANCE", "Celle qui ne force pas", "« Vous avez pu regarder le devis ? Je reste dispo si une ligne n'est pas claire. »", "Une question ouverte. *Pas une pression.*"),
    cta("Tu relances tes devis, *toi ?*"),
]

CAR["c16-avenant"] = [
    hook("Chantier", "Travaux en plus : *l'accord écrit en 2 minutes,* même par SMS.", "« Vous pourriez me faire ça en plus ? » Traduction : gratuit."),
    lst("Avant de commencer", ["Fais préciser la demande : quoi, où, comment.", "Chiffre le temps, le matériel et le déplacement.", "Dis l'effet sur le planning."], pose="classeur"),
    step("LE SMS", "L'accord écrit, même court", "« Comme convenu : ajout de [travaux], [prix] € HT, +[x] jour(s) sur le planning. Merci de me confirmer par retour. »", "Sa réponse « OK » *vaut trace écrite.*"),
    cta("Le pire « petit truc en plus » *qu'on t'ait demandé ?*"),
]

CAR["c17-annonce"] = [
    hook("Recrutement", "L'annonce de recrutement *réécrite pour que les bons répondent.*", "« Quand ça parle en brut, c'est pas bon signe. »", "classeur"),
    dark("Avant", "« Recherche peintre motivé. Salaire selon profil. »", "Résultat : *des candidats qui demandent tous « c'est combien ? ».*"),
    lst("Ce qu'il faut afficher", ["Le salaire en net, primes comprises.", "Paniers, déplacements, véhicule.", "Les horaires réels, pas « flexibles ».", "Le secteur des chantiers."], pose="telephone"),
    step("APRÈS", "Une annonce qui trie pour toi", "« Peintre N3, [ville] et 30 km. [x] € net/mois + paniers + véhicule. 7h30-16h30, vendredi 15h. Chantiers de rénovation chez particuliers. »", card_blue=False),
    cta("Tu recrutes *en ce moment ?*"),
]

CAR["c18-geste"] = [
    hook("Rentabilité", "Arrête les gestes commerciaux. *Fais ça à la place.*", "", "bras-croises"),
    st("Chantier de *10 000 €.* Marge nette à *4 %.*", "Ton bénéfice sur ce chantier : 400 €.", pose="classeur"),
    dark("Un geste de *500 €,*", "", "et ce chantier *est à perte.* Tu as travaillé pour payer le client."),
    lst("À offrir à la place", ["Un créneau de démarrage prioritaire.", "Une visite de contrôle à 6 mois.", "Un conseil d'entretien écrit, à garder."], pose="telephone"),
    cta("Tu fais encore *des gestes commerciaux ?*"),
]

CAR["c19-peinture"] = [
    hook("Chiffrage", "Le devis peinture *qui fait rire les pros* en commentaire.", "Maison de 110 m². « Tu le chiffres à combien ? »", "telephone"),
    st("110 m² au sol, *ce n'est pas 110 m² à peindre.*", "Murs et plafonds : comptez largement plus de 300 m².", pose="classeur"),
    lst("Ce qu'il faut compter", ["La protection et la préparation : rebouchage, ponçage.", "La sous-couche.", "Les deux couches de finition.", "La fourniture, au bon prix."], pose=None),
    dark("Ton prix plancher *se défend.*", "", "Si un client compare au m² de sol, *il ne compare pas le même travail.*"),
    cta("Toi, *tu le chiffres à combien ?*"),
]

CAR["c20-reseau"] = [
    hook("Réseau", "5 corps d'état de confiance = *des chantiers que tu ne cherches pas.*", "", "classeur"),
    st("Le menuisier *envoie les photos au plombier.*", "Le client ne cherche personne d'autre : il reste dans le réseau.", pose="telephone"),
    dark("« Tu mets en jeu *ta crédibilité* face au client si celui que tu recommandes fait mal son travail. »", "", "C'est vrai. Alors on choisit."),
    lst("Choisir qui recommander", ["Tu as vu son travail, pas seulement sa carte.", "Il répond au téléphone et tient ses dates.", "Après le chantier, tu demandes au client comment ça s'est passé."], pose="bras-croises"),
    cta("Tu recommandes *qui, toi ?*"),
]

CAR["c21-brief"] = [
    hook("Équipe", "3 questions à poser *avant que tes gars démarrent.*", "7h15, le camion part. 10h, ton téléphone sonne.", "telephone"),
    step("1", "On fait quoi, dans quel ordre ?", "La tâche du jour et ce qui doit être fini ce soir.", card_blue=False),
    step("2", "Avec quel matériel ?", "Ce qui est dans le camion, et ce qu'il faut récupérer avant de partir.", pose="classeur"),
    step("3", "Ce qu'ils peuvent décider sans toi", "Les points particuliers du chantier, et jusqu'où ils peuvent trancher seuls.", card_blue=False),
    dark("Une page suffit.", "", "Si le chantier est encore dans ta tête à 7h15, *il sera dans ton téléphone à 10h.*"),
    cta("Combien d'appels *avant 10h, chez toi ?*"),
]

CAR["c22-devis-lisible"] = [
    hook("Devis", "Ton devis de 3 lignes *perd contre un devis de 30 lignes.*", "Même s'il est moins cher.", "classeur"),
    st("Un devis illisible *est comparé au prix.*", "Le client compare ce qu'il comprend. Le reste ne compte pas.", pose="telephone"),
    dark("Avant", "« Rénovation salle de bain : 8 500 € HT »", "Le client n'a rien à défendre face au devis concurrent."),
    lst("Après", ["Le détail par poste : dépose, plomberie, carrelage, finitions.", "Ce qui est compris, et ce qui ne l'est pas.", "Garanties, assurances et délai écrits noir sur blanc."], pose=None),
    cta("Tes devis font *combien de lignes ?*"),
]

CAR["c23-masse"] = [
    hook("Rentabilité", "Ton ratio masse salariale / CA, *calculé en 3 lignes.*", "", "classeur"),
    step("1", "Ce qu'on met dedans", "Salaires bruts + charges patronales + ta propre rémunération.", card_blue=False),
    step("2", "Ce qu'on ajoute dans le 2nd œuvre", "La sous-traitance de main-d'œuvre. Sinon le ratio ment.", pose="telephone"),
    step("3", "On divise par le chiffre d'affaires", "Exemple : 210 000 € de masse salariale sur 600 000 € de CA = 35 %.", card_blue=False),
    dark("Le chiffre seul *ne dit rien.*", "", "Lis-le avec *le taux d'occupation de tes équipes.* Un ratio qui monte sans que le CA suive, ce sont des gars qui attendent."),
    cta("Tu es à *combien de %, toi ?*"),
]

CAR["c24-materiel"] = [
    hook("Équipe", "8 000 € de matériel *volé dans un camion ouvert.*", "Un patron raconte, en commentaire.", "bras-croises"),
    dark("« Primes ou pas, *ils s'en tapent.* »", "", "Le problème n'est pas la prime. *C'est l'absence de cadre.*"),
    lst("Le cadre", ["Qui est responsable du camion, nommément.", "Un inventaire simple, vérifié le vendredi.", "Une conséquence connue d'avance, appliquée à tous."], pose="classeur"),
    st("Une prime *ne remplace pas* une règle.", "Elle récompense une règle qui existe déjà.", pose="telephone"),
    cta("Tu as déjà perdu *du matériel sur un chantier ?*"),
]

CAR["c25-qualif"] = [
    hook("Devis", "3 questions avant de faire *40 km pour un devis.*", "« 2 000 € max. » Ce client, tu pouvais l'éviter."),
    lst("Les 3 questions", ["Le budget : « Vous avez une enveloppe en tête ? »", "Le délai : « Vous souhaitez démarrer quand ? »", "Le décideur : « Qui valide le devis avec vous ? »"], pose="classeur"),
    step("LE MESSAGE", "À envoyer avant la visite", "« Pour bien préparer ma visite : quel budget avez-vous en tête, pour quand, et qui décidera avec vous ? »", "Les sérieux répondent. *Les autres se trient seuls.*"),
    cta("Combien de devis pour rien *le mois dernier ?*"),
]

CAR["c26-retenue"] = [
    hook("Trésorerie", "Retenue de garantie : *le papier qui te rend tes 5 %* tout de suite.", "« Et les 5 % pendant un an, on en parle ? »", "classeur"),
    st("La retenue est *plafonnée à 5 %.*", "Elle est libérée un an après la réception, sauf réserves motivées.", pose="telephone"),
    dark("Elle peut être remplacée *par une caution bancaire.*", "", "Ta banque se porte garante. *Tu touches 100 % de ta facture.*"),
    step("LE RÉFLEXE", "À la signature du marché", "Demande la substitution de la retenue par une caution, et fais-la prévoir dans le contrat.", "Le coût de la caution est souvent *bien plus faible que 5 % bloqués un an.*", card_blue=False),
    cta("Combien de retenues *dorment chez tes clients ?*"),
]

CAR["c27-ca-salarie"] = [
    hook("Rentabilité", "Le seul chiffre à regarder chaque mois *quand tu as des salariés.*", "", "bras-croises"),
    st("Le CA produit *par salarié de chantier.*", "Pas le CA total. Celui que chaque gars fait rentrer.", pose="classeur"),
    st("Repère souvent cité : *500 € HT par jour.*", "Sur environ 200 jours travaillés : 100 000 € par an et par gars.", pose="telephone"),
    lst("Pourquoi beaucoup n'y sont pas", ["Des journées sans chantier ouvert.", "Des allers-retours au dépôt.", "Des heures passées mais pas facturées."], pose=None),
    cta("Tu es *au-dessus ou en dessous ?*"),
]

CAR["c28-semaine"] = [
    hook("Dirigeant", "Note ta semaine pendant 5 jours. *Tu vas avoir peur.*", "« Ouvrier : 35 h, 5 semaines de congés. Patron : 55 à 60 h, 2 semaines. »", "telephone"),
    lst("3 colonnes, 5 jours", ["*Production* : chantier, chiffrage.", "*Gestion* : factures, planning, commandes.", "*Pompier* : appels, urgences, oublis."], pose="classeur"),
    dark("La colonne qui fait peur *est souvent la troisième.*", "", "Et c'est celle *qui peut le plus baisser.*"),
    cta("Tu fais *combien d'heures par semaine ?*"),
]

CAR["c29-gestion"] = [
    hook("Dirigeant", "Mêmes charges, même métier. *Lui s'en sort. Pourquoi ?*", "« Ça vaut pas la peine de créer une entreprise, il y a trop de charges. »", "bras-croises"),
    st("Les charges *ne sont pas ton problème.*", "Tes concurrents qui s'en sortent paient les mêmes.", pose="classeur"),
    lst("Les 3 leviers", ["Un prix calculé, pas copié sur le voisin.", "Des factures qui partent à temps, et qui sont relancées.", "Des heures produites, pas seulement payées."], pose="telephone"),
    dark("La différence n'est pas dans le métier.", "", "*Elle est dans la gestion.*"),
    cta("Tu te reconnais *dans lequel des deux ?*"),
]

CAR["c30-taches"] = [
    hook("Dirigeant", "3 tâches à sortir de ta tête *avant ce soir.*", "21h, le repas est fini. Tu attaques les factures."),
    step("1", "Les relances de factures", "Elles partent seules à J+1, J+8, J+15. Tu n'interviens que pour appeler.", card_blue=False),
    step("2", "Le planning de la semaine", "Fait une fois, le vendredi, partagé à l'équipe. Plus de planning refait le soir.", pose="classeur"),
    step("3", "Les commandes de matériaux", "Préparées par chantier, à J-2. Plus d'allers-retours au négoce.", card_blue=False),
    dark("Ce qui se délègue, *ce qui s'automatise.*", "", "Toi, tu gardes les décisions. *Le reste peut tourner sans toi.*"),
    cta("Tu y passes *combien de soirées par semaine ?*"),
]
