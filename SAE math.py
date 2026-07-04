# SAE 2-02 - Automates finis


# Un automate est un dictionnaire Python avec :
#   "alphabet"    -> les lettres utilisées,       ex: ['a', 'b']
#   "etats"       -> la liste des états,           ex: [0, 1, 2]
#   "transitions" -> les transitions [de, lettre, vers]
#   "I"           -> les états de départ
#   "F"           -> les états d'arrivée (finaux)



# PARTIE 1.1 - Les mots


def pref(u):
    # On prend le mot u et on retourne tous ses débuts possibles
    # ex: pref("ab") -> ["", "a", "ab"]
    liste = []
    for i in range(len(u) + 1):
        liste.append(u[:i])   # u[:0]="", u[:1]="a", u[:2]="ab", etc.
    return liste


def suf(u):
    # On retourne toutes les fins possibles du mot u
    # ex: suf("ab") -> ["ab", "b", ""]
    liste = []
    for i in range(len(u) + 1):
        liste.append(u[i:])   # u[0:]="ab", u[1:]="b", u[2:]="", etc.
    return liste


def fact(u):
    # On retourne tous les sous-mots de u, sans doublons
    # Pour chaque position de début i et de fin j, on extrait u[i:j]
    liste = []
    for i in range(len(u) + 1):
        for j in range(i, len(u) + 1):
            sous_mot = u[i:j]
            if sous_mot not in liste:   # on évite les doublons
                liste.append(sous_mot)
    return liste


def miroir(u):
    # On retourne le mot à l'envers
    # u[::-1] c'est une façon Python de lire une chaîne de droite à gauche
    return u[::-1]



# PARTIE 1.2 - Les langages


def concatene(L1, L2):
    # On colle chaque mot de L1 avec chaque mot de L2, sans doublons
    # ex: concatene(["a"], ["b","c"]) -> ["ab", "ac"]
    liste = []
    for mot1 in L1:
        for mot2 in L2:
            nouveau = mot1 + mot2
            if nouveau not in liste:
                liste.append(nouveau)
    return liste


def puis(L, n):
    # On retourne L puissance n, c'est-à-dire L concaténé n fois avec lui-même
    # L^0 = mot vide, L^1 = L, L^2 = L concaténé avec L, etc.
    if n == 0:
        return ['']   # L^0 c'est juste le mot vide
    resultat = L[:]   # on copie L pour commencer à L^1
    for i in range(n - 1):
        resultat = concatene(resultat, L)   # on rajoute une concaténation à chaque tour
    return resultat


# Question 1.2.3 :
# On ne peut pas coder l'étoile L* car c'est une union infinie (L^0, L^1, L^2, ...)
# Un programme doit forcément s'arrêter donc c'est impossible.


def tousmots(A, n):
    # On génère tous les mots de longueur strictement inférieure à n sur l'alphabet A
    # On part du mot vide et on rajoute une lettre à la fois
    resultat = ['']      # au départ on a juste le mot vide
    courant = ['']       # "courant" = les mots qu'on vient de créer

    for longueur in range(1, n):
        suivant = []
        for mot in courant:
            for lettre in A:
                suivant.append(mot + lettre)   # on allonge chaque mot d'une lettre
        resultat = resultat + suivant   # on ajoute les nouveaux mots au résultat
        courant = suivant               # les nouveaux mots deviennent le "courant"

    return resultat



# PARTIE 1.3 - Les automates


# L'automate de test du sujet
auto = {"alphabet": ['a', 'b'],
        "etats": [1, 2, 3, 4],
        "transitions": [[1,'a',2], [2,'a',2], [2,'b',3], [3,'a',4]],
        "I": [1],
        "F": [4]}


def defauto():
    # On demande à l'utilisateur de taper les infos de l'automate une par une
    alpha = input("Alphabet (lettres séparées par des espaces) : ").split()
    etats = list(map(int, input("États : ").split()))
    I     = list(map(int, input("États initiaux : ").split()))
    F     = list(map(int, input("États finaux : ").split()))
    T     = []
    print("Transitions au format 'départ lettre arrivée', ligne vide pour arrêter :")
    while True:
        ligne = input()
        if ligne == '':
            break
        p = ligne.split()
        t = [int(p[0]), p[1], int(p[2])]
        if t not in T:
            T.append(t)
    return {"alphabet": alpha, "etats": etats, "transitions": T, "I": I, "F": F}


def lirelettre(T, E, a):
    # On regarde toutes les transitions et on garde celles qui :
    # - partent d'un état dans E
    # - utilisent la lettre a
    # On retourne la liste des états où on peut arriver
    arrivees = []
    for transition in T:
        depart  = transition[0]
        lettre  = transition[1]
        arrivee = transition[2]
        if depart in E and lettre == a and arrivee not in arrivees:
            arrivees.append(arrivee)
    return arrivees


def liremot(T, E, m):
    # On lit le mot lettre par lettre, en mettant à jour les états courants à chaque fois
    etats_courants = list(E)
    for lettre in m:
        etats_courants = lirelettre(T, etats_courants, lettre)
    return etats_courants


def accepte(automate, m):
    # On lit le mot depuis les états initiaux
    # Si on finit dans un état final, le mot est accepté
    etats_arrives = liremot(automate["transitions"], automate["I"], m)
    for etat in etats_arrives:
        if etat in automate["F"]:
            return True
    return False


def langage_accept(automate, n):
    # On génère tous les mots possibles puis on garde ceux que l'automate accepte
    tous_les_mots = tousmots(automate["alphabet"], n)
    acceptes = []
    for mot in tous_les_mots:
        if accepte(automate, mot):
            acceptes.append(mot)
    return acceptes

# Question 1.3.6 :
# On ne peut pas retourner TOUT le langage car il peut être infini (ex: a*)
# On peut seulement regarder les mots jusqu'à une certaine longueur n.



# PARTIE 2 - Déterminisation


auto0 = {"alphabet":['a','b'], "etats":[0,1,2,3],
         "transitions":[[0,'a',1],[1,'a',1],[1,'b',2],[2,'a',3]], "I":[0], "F":[3]}
auto1 = {"alphabet":['a','b'], "etats":[0,1],
         "transitions":[[0,'a',0],[0,'b',1],[1,'b',1],[1,'a',1]], "I":[0], "F":[1]}
auto2 = {"alphabet":['a','b'], "etats":[0,1],
         "transitions":[[0,'a',0],[0,'a',1],[1,'b',1],[1,'a',1]], "I":[0], "F":[1]}


def deterministe(automate):
    # Un automate est déterministe si :
    # 1. il a exactement un seul état initial
    # 2. depuis chaque état, pour chaque lettre, il y a au plus une transition
    if len(automate["I"]) != 1:
        return False
    for t1 in automate["transitions"]:
        for t2 in automate["transitions"]:
            # si deux transitions différentes ont le même départ ET la même lettre -> problème
            if t1 != t2 and t1[0] == t2[0] and t1[1] == t2[1]:
                return False
    return True


def determinise(automate):
    # Algorithme des sous-ensembles :
    # Dans le nouvel automate, chaque "état" est en fait un groupe d'anciens états.
    # On explore ces groupes un par un jusqu'à ne plus en trouver de nouveaux.
    alphabet  = automate["alphabet"]
    T         = automate["transitions"]
    F_anciens = automate["F"]

    etat_init = sorted(automate["I"])   # le premier état = groupe des états initiaux
    etats_det = [etat_init]             # liste de tous les groupes trouvés
    a_traiter = [etat_init]             # groupes qu'on n'a pas encore traités
    transitions_det = []
    finaux_det = []

    while a_traiter:
        groupe = a_traiter.pop(0)   # on prend le prochain groupe à traiter

        # ce groupe est final s'il contient un ancien état final
        for e in groupe:
            if e in F_anciens and groupe not in finaux_det:
                finaux_det.append(groupe)

        # pour chaque lettre, on calcule le groupe suivant
        for lettre in alphabet:
            groupe_suivant = sorted(lirelettre(T, groupe, lettre))
            if groupe_suivant:   # on ignore si le groupe est vide
                transitions_det.append([groupe, lettre, groupe_suivant])
                if groupe_suivant not in etats_det:
                    etats_det.append(groupe_suivant)
                    a_traiter.append(groupe_suivant)

    return {"alphabet": alphabet, "etats": etats_det,
            "transitions": transitions_det, "I": [etat_init], "F": finaux_det}


def renommage(automate):
    # Après déterminisation les états sont des listes comme [0,1].
    # On les renomme en simples entiers : 0, 1, 2, ...
    # Pour ça on fait un dictionnaire : ancien état -> nouvel entier
    correspondance = {}
    for i in range(len(automate["etats"])):
        # str() car les listes ne peuvent pas être des clés de dictionnaire
        correspondance[str(automate["etats"][i])] = i

    nouveaux_etats = list(range(len(automate["etats"])))

    nouvelles_transitions = []
    for t in automate["transitions"]:
        dep = correspondance[str(t[0])]
        arr = correspondance[str(t[2])]
        nouvelles_transitions.append([dep, t[1], arr])

    nouveaux_I = [correspondance[str(e)] for e in automate["I"]]
    nouveaux_F = [correspondance[str(e)] for e in automate["F"]]

    return {"alphabet": automate["alphabet"], "etats": nouveaux_etats,
            "transitions": nouvelles_transitions, "I": nouveaux_I, "F": nouveaux_F}



# PARTIE 3 - Complémentation


auto3 = {"alphabet":['a','b'], "etats":[0,1,2],
         "transitions":[[0,'a',1],[0,'a',0],[1,'b',2],[1,'b',1]], "I":[0], "F":[2]}


def complet(automate):
    # L'automate est complet si depuis chaque état, pour chaque lettre,
    # il existe au moins une transition
    for etat in automate["etats"]:
        for lettre in automate["alphabet"]:
            trouve = False
            for t in automate["transitions"]:
                if t[0] == etat and t[1] == lettre:
                    trouve = True
            if not trouve:
                return False   # il manque une transition -> pas complet
    return True


def complete(automate):
    # On ajoute un état "puits" : toutes les transitions manquantes vont vers lui
    # L'état puits n'est pas final, donc tout mot qui y arrive est refusé
    if complet(automate):
        return automate   # rien à faire si déjà complet

    puits = max(automate["etats"]) + 1   # un nouvel entier pas encore utilisé
    nouveaux_etats = automate["etats"] + [puits]
    nouvelles_transitions = automate["transitions"][:]   # copie des transitions existantes

    # Pour chaque état (y compris le puits), on ajoute les transitions manquantes
    for etat in nouveaux_etats:
        for lettre in automate["alphabet"]:
            existe = False
            for t in nouvelles_transitions:
                if t[0] == etat and t[1] == lettre:
                    existe = True
            if not existe:
                nouvelles_transitions.append([etat, lettre, puits])

    return {"alphabet": automate["alphabet"], "etats": nouveaux_etats,
            "transitions": nouvelles_transitions, "I": automate["I"], "F": automate["F"]}


def complement(automate):
    # Pour complémenter :
    # 1. on déterminise si besoin
    # 2. on complète (ajouter l'état puits)
    # 3. on inverse les états finaux (les finaux deviennent non-finaux et inversement)
    if not deterministe(automate):
        a = renommage(determinise(automate))
    else:
        a = automate

    a = complete(a)

    # les nouveaux finaux = tous les états qui n'étaient PAS finaux avant
    nouveaux_F = []
    for etat in a["etats"]:
        if etat not in a["F"]:
            nouveaux_F.append(etat)

    return {"alphabet": a["alphabet"], "etats": a["etats"],
            "transitions": a["transitions"], "I": a["I"], "F": nouveaux_F}



# PARTIE 4 - Automate produit


auto4 = {"alphabet":['a','b'], "etats":[0,1,2],
         "transitions":[[0,'a',1],[1,'b',2],[2,'b',2],[2,'a',2]], "I":[0], "F":[2]}
auto5 = {"alphabet":['a','b'], "etats":[0,1,2],
         "transitions":[[0,'a',0],[0,'b',1],[1,'a',1],[1,'b',2],[2,'a',2],[2,'b',0]],
         "I":[0], "F":[0,1]}


def inter(a1, a2):
    # L'automate produit simule les deux automates en même temps.
    # Chaque état est une paire (état dans a1, état dans a2).
    # Un état (p,q) est final si p est final dans a1 ET q est final dans a2.
    init = (a1["I"][0], a2["I"][0])
    etats_prod    = [init]
    a_traiter     = [init]
    transitions_prod = []
    finaux_prod   = []

    while a_traiter:
        p, q = a_traiter.pop(0)

        # cet état est final si les deux composantes sont finales
        if p in a1["F"] and q in a2["F"] and (p, q) not in finaux_prod:
            finaux_prod.append((p, q))

        for lettre in a1["alphabet"]:
            for p2 in lirelettre(a1["transitions"], [p], lettre):
                for q2 in lirelettre(a2["transitions"], [q], lettre):
                    nouvel_etat = (p2, q2)
                    transitions_prod.append([(p, q), lettre, nouvel_etat])
                    if nouvel_etat not in etats_prod:
                        etats_prod.append(nouvel_etat)
                        a_traiter.append(nouvel_etat)

    return {"alphabet": a1["alphabet"], "etats": etats_prod,
            "transitions": transitions_prod, "I": [init], "F": finaux_prod}


def difference(a1, a2):
    # Même principe que inter, mais un état (p,q) est final si :
    # p est final dans a1 ET q n'est PAS final dans a2
    # On doit d'abord compléter les deux automates pour ne rater aucun mot
    a1c = complete(a1)
    a2c = complete(a2)

    init = (a1c["I"][0], a2c["I"][0])
    etats_prod    = [init]
    a_traiter     = [init]
    transitions_prod = []
    finaux_prod   = []

    while a_traiter:
        p, q = a_traiter.pop(0)

        if p in a1c["F"] and q not in a2c["F"] and (p, q) not in finaux_prod:
            finaux_prod.append((p, q))

        for lettre in a1c["alphabet"]:
            for p2 in lirelettre(a1c["transitions"], [p], lettre):
                for q2 in lirelettre(a2c["transitions"], [q], lettre):
                    nouvel_etat = (p2, q2)
                    transitions_prod.append([(p, q), lettre, nouvel_etat])
                    if nouvel_etat not in etats_prod:
                        etats_prod.append(nouvel_etat)
                        a_traiter.append(nouvel_etat)

    return {"alphabet": a1c["alphabet"], "etats": etats_prod,
            "transitions": transitions_prod, "I": [init], "F": finaux_prod}


# PARTIE 5 - Fermeture


def prefixe(automate):
    # Pour accepter les préfixes : tout état depuis lequel on peut encore
    # atteindre un état final devient lui-même final.
    # On fait une recherche (DFS) depuis chaque état pour voir s'il mène à un final.
    T = automate["transitions"]
    F = automate["F"]

    def peut_atteindre_final(etat):
        deja_vus = []
        a_visiter = [etat]
        while a_visiter:
            e = a_visiter.pop()
            if e in F:
                return True       # on a trouvé un état final !
            deja_vus.append(e)
            for t in T:
                if t[0] == e and t[2] not in deja_vus:
                    a_visiter.append(t[2])
        return False

    nouveaux_F = []
    for etat in automate["etats"]:
        if peut_atteindre_final(etat):
            nouveaux_F.append(etat)

    return {"alphabet": automate["alphabet"], "etats": automate["etats"],
            "transitions": T, "I": automate["I"], "F": nouveaux_F}


def suffixe(automate):
    # Pour accepter les suffixes : tout état accessible depuis un état initial
    # devient lui-même un état initial.
    # On fait une recherche (DFS) depuis les états initiaux.
    T = automate["transitions"]
    I = automate["I"]

    def est_accessible(etat):
        deja_vus = []
        a_visiter = list(I)
        while a_visiter:
            e = a_visiter.pop()
            if e == etat:
                return True       # on a atteint l'état cherché !
            deja_vus.append(e)
            for t in T:
                if t[0] == e and t[2] not in deja_vus:
                    a_visiter.append(t[2])
        return False

    nouveaux_I = []
    for etat in automate["etats"]:
        if est_accessible(etat):
            nouveaux_I.append(etat)

    return {"alphabet": automate["alphabet"], "etats": automate["etats"],
            "transitions": T, "I": nouveaux_I, "F": automate["F"]}


def facteur(automate):
    # Les facteurs = on applique prefixe puis suffixe
    a = prefixe(automate)
    a = suffixe(a)
    return a


def miroir_auto(automate):
    # On inverse toutes les transitions (départ <-> arrivée)
    # et on échange les états initiaux et finaux
    transitions_inversees = []
    for t in automate["transitions"]:
        transitions_inversees.append([t[2], t[1], t[0]])   # on retourne la flèche

    return {"alphabet": automate["alphabet"],
            "etats": automate["etats"],
            "transitions": transitions_inversees,
            "I": automate["F"],   # les anciens finaux deviennent les initiaux
            "F": automate["I"]}   # les anciens initiaux deviennent les finaux



# PARTIE 6 - Minimisation (algorithme de Moore)


# L'idée de Moore : on regroupe les états qui se comportent pareil.
# On part de 2 groupes (finaux / non-finaux) et on les sépare petit à petit.

auto6 = {"alphabet":['a','b'], "etats":[0,1,2,3,4,5],
         "transitions":[[0,'a',4],[0,'b',3],[1,'a',5],[1,'b',5],[2,'a',5],[2,'b',2],
                        [3,'a',1],[3,'b',0],[4,'a',1],[4,'b',2],[5,'a',2],[5,'b',5]],
         "I":[0], "F":[0,1,2,5]}


def successeur(etat, lettre, T):
    # Renvoie l'état où on va depuis "etat" en lisant "lettre" (automate déterministe)
    for t in T:
        if t[0] == etat and t[1] == lettre:
            return t[2]
    return None


def trouver_classe(etat, partition):
    # Renvoie le numéro du groupe qui contient "etat" dans la partition
    for i in range(len(partition)):
        if etat in partition[i]:
            return i
    return -1


def raffiner(partition, automate):
    # On sépare les états qui vont vers des groupes différents.
    # Chaque état a une "signature" = les numéros de groupes de ses successeurs.
    # Si deux états ont des signatures différentes, on les met dans des groupes différents.
    T      = automate["transitions"]
    alpha  = automate["alphabet"]
    nouvelle_partition = []

    for groupe in partition:
        sous_groupes = {}
        for etat in groupe:
            # la signature = (groupe_succ_lettre1, groupe_succ_lettre2, ...)
            signature = []
            for lettre in alpha:
                succ = successeur(etat, lettre, T)
                signature.append(trouver_classe(succ, partition))
            signature = tuple(signature)

            if signature not in sous_groupes:
                sous_groupes[signature] = []
            sous_groupes[signature].append(etat)

        # chaque sous-groupe distinct devient un nouveau groupe
        for sg in sous_groupes.values():
            nouvelle_partition.append(sorted(sg))

    return nouvelle_partition


def minimise(automate):
    # Étape 1 : partition de départ = {états finaux} et {états non finaux}
    F     = automate["F"]
    etats = automate["etats"]

    finaux     = sorted([e for e in etats if e in F])
    non_finaux = sorted([e for e in etats if e not in F])
    partition  = []
    if finaux:     partition.append(finaux)
    if non_finaux: partition.append(non_finaux)

    # Étape 2 : on raffine jusqu'à ce que la partition ne change plus
    while True:
        nouvelle = raffiner(partition, automate)
        if sorted([sorted(g) for g in nouvelle]) == sorted([sorted(g) for g in partition]):
            break   # la partition est stable, on s'arrête
        partition = nouvelle

    # Étape 3 : on construit le nouvel automate
    # chaque groupe de la partition = un état du nouvel automate
    T     = automate["transitions"]
    alpha = automate["alphabet"]
    etats_min = [sorted(g) for g in partition]

    transitions_min = []
    for groupe in etats_min:
        rep = groupe[0]   # on prend le premier état du groupe comme représentant
        for lettre in alpha:
            succ = successeur(rep, lettre, T)
            if succ is not None:
                groupe_succ = sorted(partition[trouver_classe(succ, partition)])
                transitions_min.append([groupe, lettre, groupe_succ])

    I_min = [sorted(partition[trouver_classe(e, partition)]) for e in automate["I"]]
    F_min = []
    for groupe in etats_min:
        if any(e in F for e in groupe):
            F_min.append(groupe)

    return {"alphabet": alpha, "etats": etats_min, "transitions": transitions_min,
            "I": I_min, "F": F_min}


# ==============================================
# TESTS
# ==============================================

if __name__ == "__main__":
    print("=== PARTIE 1 : Mots ===")
    print(pref('coucou'))
    print(suf('coucou'))
    print(fact('coucou'))
    print(miroir('coucou'))

    print("\n=== PARTIE 1 : Langages ===")
    print(concatene(['aa','ab','ba','bb'], ['a','b','']))
    print(puis(['aa','ab','ba','bb'], 2))
    print(tousmots(['a','b'], 3))

    print("\n=== PARTIE 1 : Automates ===")
    print(lirelettre(auto["transitions"], auto["etats"], 'a'))
    print(liremot(auto["transitions"], auto["etats"], 'aba'))
    print(accepte(auto, 'aaba'))
    print(langage_accept(auto, 5))

    print("\n=== PARTIE 2 : Déterminisation ===")
    print(deterministe(auto0))
    print(deterministe(auto2))
    print(determinise(auto2))
    print(renommage(determinise(auto2)))

    print("\n=== PARTIE 3 : Complémentation ===")
    print(complet(auto0))
    print(complet(auto1))
    print(complete(auto0))
    print(complement(auto3))

    print("\n=== PARTIE 4 : Automate produit ===")
    print(inter(auto4, auto5))
    print(renommage(inter(auto4, auto5)))
    print(difference(auto4, auto5))
    print(renommage(difference(auto4, auto5)))

    print("\n=== PARTIE 6 : Minimisation ===")
    print(minimise(auto6))
    print(renommage(minimise(auto6)))