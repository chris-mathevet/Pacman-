# Fichier pour l'IA du pacmand

import random
import const
import plateau as plat
import case
import joueur
import API_IA as IA

plateau1=plat.Plateau(IA.test1)
plateau2=plat.Plateau(IA.test2)
plateau3=plat.Plateau(IA.test3)
plateauC=plat.Plateau(IA.carte)
plateau_perso=plat.Plateau(IA.perso_map)






def est_un_mur(plateau):
    """Complexité: O(N²)
    il mets dans un ensemble, l'ensemble des coordonnées ou se situe des murs 

    Args:
        plateau (dict): dico du plateau de jeu

    Returns:
        set: ensemble des coordonnées ou se situ un mur
    """
    murs= set() # O(1)
    lignes=plat.get_nb_lignes(plateau)# O(1)
    colonnes=plat.get_nb_colonnes(plateau)# O(1)
    for i in range(lignes): # O(N)
        for j in range(colonnes): # O(N)
            if case.est_mur(plat.get_case(plateau,(i,j))): # O(1)
                murs.add((i,j)) # O(1)
    return murs # O(1)

def cul_de_sac(plateau):
    """Complexité: O(N²)
    il mets dans un ensemble, l'ensemble des coordonnées ou se situe des culs de sacs

    Args:
        plateau (dict): dico du plateau de jeu

    Returns:
        set: ensemble des coordonnées ou se situ un cul de sac
    """
    pos_cul_de_sac= set()# O(1)
    lignes=plat.get_nb_lignes(plateau)# O(1)
    colonnes=plat.get_nb_colonnes(plateau)# O(1)
    for i in range (lignes): # O(N)
        for j in range(colonnes): # O(N)
            if i !=0 and j!=0 and i !=lignes-1 and j!=colonnes-1 and not len(plat.directions_possibles(plateau, (i,j), False)) != 1: # O(1)
                if (i,j) not in est_un_mur(plateau): # O(1)
                    print(len(plat.directions_possibles(plateau, (i,j), False)))  # O(1)
                    pos_cul_de_sac.add((i,j)) # O(1)
    return pos_cul_de_sac# O(1)


def test():
    print(cul_de_sac(plateau1))
    print(cul_de_sac(plateau2))
    print(cul_de_sac(plateau3))
    print(cul_de_sac(plateauC))
    print(est_un_mur(plateau2))
    print(plat.Plateau(plateau2))
    print(intersection(plateau2))
    print(len(intersection(plateau2)))
    print("tp urgent, mur vers:",tp_urgent(plateau_perso, (1,6), True))  #   ('N', (0, 6))
    print("tp urgent, mur vers:",tp_urgent(plateau_perso, (3,3), True))  #   ('N', (2, 3))
    print("tp urgent, mur vers:",tp_urgent(plateau_perso, (8, 7), True)) #   ('N', (7, 7))
    print("tp urgent, mur vers:",tp_urgent(plateau_perso, (8,1), True))  #   ('S', (9, 1))
    print("tp urgent, mur vers:",tp_urgent(plateau_perso, (4,1), True))  #   ('E', (4, 2))
    print("chemin",chemin_non_cul_de_sac(plateau_perso, cul_de_sac(plateau_perso)))

    # set= {(4, 3), (4, 9), (3, 7), (9, 2), (9, 5), (1, 3), (2, 8), (6, 2), (6, 8), (4, 8), (5, 3), (9, 1), (9, 7), (9, 4), (8, 8), (1, 2), (5, 2), (3, 8), (9, 3), (8, 7), (9, 6), (1, 4), (2, 3), (2, 9), (6, 3), (6, 9)}
    set = cul_de_sac(plateau2)
    for co in set:
        print("pour", co," on peut faire:",plat.directions_possibles(plateau2, co, False))
            
# test()

def intersection(plateau):
    """Complexité: O(N²)
    il mets dans un ensemble, l'ensemble des coordonnées ou se situe des intersections de la carte

    Args:
        plateau (dict): dico du plateau de jeu

    Returns:
        set: ensemble des coordonnées ou se situ une intersection
    """
    les_intersections= set() # O(1)
    lignes=plat.get_nb_lignes(plateau)# O(N)
    colonnes=plat.get_nb_colonnes(plateau)# O(N)
    for i in range (lignes): # O(1)
        for j in range(colonnes): # O(1)
            if i !=0 and j!=0 and i !=lignes-1 and j!=colonnes-1 and len(plat.directions_possibles(plateau, (i,j), False)) >= 3:# O(1)
                if (i,j) not in est_un_mur(plateau):# O(1)
                    les_intersections.add((i,j))# O(1)
    return les_intersections# O(1)

def fantome_present(plateau,pos_objet,couleur):
    """Complexité: O(N²)
    Nombre de fantome dans le perimetre definie par analyse autour de l'objet
        
    Args:
        plateau (dict): plateau de jeu
        pos_objet (tuple): tuple de position de l'objet
        couleur (str): couleur du pacman
        
    Returns:
        int: nombre de fantome autour 
    """
    analyse = IA.analyse_plateau_bis(plateau,pos_objet,5,couleur) # O(N²)
    return len(analyse["fantomes"])# O(1)

def oppose(direction):
    """Complexité: O(1)
    inverse la direction
        
    Args:
        direction (str): une chaine de caractere composé de d'une lettre comme NSEO  

    Returns:
        int: nombre de fantome autour 
    """
    if direction == 'N':# O(1)
        return 'S'# O(1)
    if direction == 'S':# O(1)
        return 'N'# O(1)
    if direction == 'O':# O(1)
        return 'E'# O(1)
    if direction == 'E':# O(1)
        return 'O'# O(1)

def tp_urgent(plateau, pos, encercle):
    """Complexité: O(N²)
    _summary_

    Args:
        plateau (_type_): _description_
        pos (_type_): _description_
        encercle (_type_): _description_

    Returns:
        _type_: _description_
    """    
    les_murs = est_un_mur(plateau)# O(N²)
    if encercle is True:# O(1)
        for direction in const.DIRECTIONS:# O(4) 4 directions
            pos_arrivee = plat.pos_arrivee(plateau, pos, direction)# O(1)
            if pos_arrivee in les_murs:# O(1)
                return (direction, pos_arrivee)# O(1)
    else:# O(1)
        return None# O(1)
        
def encercle_fantome(plateau,pos, distance_max, couleur):
    les_murs = est_un_mur(plateau)
    # print(les_murs)
    var = IA.analyse_plateau_bis(plateau, pos, distance_max,couleur,False,False)
    res = set()
    # print(var)
    for i in range(len(var)):

        # print(var["fantomes"][i][2])
        res.add(var["fantomes"][i][2]) 
        # print(var["fantomes"][2][2])
        print(res)
    return les_murs | res

# player = joueur.joueur_from_str("A;152;3;28;0;0;12;5;0;9;Greedy")    

 ##########################
#  pas FINI
 ##########################

def prochaine_intersection_bis(plateau,pos,direction):
    """Complexité: O(N²)
    calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        tuple: un entier indiquant la distance à la prochaine intersection
               un tuple de coordonné (x,y)
    """
    les_murs = est_un_mur(plateau)# O(N²)
    distance = 1# O(1)
    pos_debut = plat.pos_arrivee(plateau,pos,direction)# O(1)
    res = [pos,pos_debut]# O(1)
    pos_actuelle = pos_debut# O(1)
    while len(plat.directions_possibles(plateau,pos_actuelle)) == 2 and pos_actuelle not in les_murs :# O(n)
        if direction in plat.directions_possibles(plateau,pos_actuelle): # O(1)
            if pos_actuelle not in les_murs: # O(1)
                pos_actuelle = plat.pos_arrivee(plateau,pos_actuelle,direction) # O(1)    
                res.append(pos_actuelle) # O(1)
                distance += 1 # O(1)

    return distance,res

def chemin_non_cul_de_sac(plateau, cul_de_sac):
    """Complexité: O(N)
    renvoie le chemin d'un cul de sac a une intersection (qui permettera pas la suite de prendre la 1er valeur d'entré du chemin vers le cul de sac et donc de ne pas y aller)

    Args:
        plateau (dict): le plateau considéré
        cul_de_sac (set): ensemble de coordonné qui sont des culs de sac 
    Return:
        dico (dict): un dictionnaire avec en clé les coordonnées du cul de sac
                        en valeur les chemins entre la position du cul de sac et sont intersection la plus proche 
    """
    dico = {}  # O(1)
    for dir in const.DIRECTIONS:  # O(4) 4 Directions
        for co in cul_de_sac:  # O(N)
            if co not in dico.keys(): # O(1)
                dico[co]= [] # O(1)
                dico[co].append(prochaine_intersection_bis(plateau, co,dir)) # O(1)

            elif len(prochaine_intersection_bis(plateau, co,dir)) > len(dico[co]): # O(1)
                dico[co]=[]
                dico[co].append(prochaine_intersection_bis(plateau, co,dir)) # O(1)
    return dico # O(1)

def est_vide(analyse):
    """Complexité: O(1)
    Vérifie si les listes d'objets et de fantomes sont tous deux vides

    Args:
        analyse (dict): un dictionnaire de listes. 
                        Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                        Les valeurs du dictionnaire sont des listes de paires de la forme
                        (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet

    Returns:
        bool: Vrai si oui, sinon Faux
    """    
    return len(analyse["fantomes"])==0 and len(analyse["objets"])==0 # O(1)

def combinaison(analyse):
    """Complexite: O(1)
    Vient ajouter les tuple de la liste fantome de analyse dans celles des objets, 
    et ils se comporteront comme des objets avec une identifcation '*' (rajouté dans const)  qui a une valeur de 20 points

    Args:
        analyse (dict): analyse
    """    
    for fant in analyse["fantomes"]: # O(4) 4 joueurs max 
        const.PROP_OBJET[fant[1]]=(20,0)  # O(1)
        analyse["objets"].append(fant) # O(1)

def choix(analyse,plateau,couleur,GLOUTON=False):
    """Complexité: # O(N)
    Renvoi la liste des objets (et fantome s'il peut les manger) triée en fonction du ratio valeur/distance

    Args:
        derniere_analyse (dict): un dictionnaire de listes. 
                        Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                        Les valeurs du dictionnaire sont des listes de paires de la forme
                        (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet
        joueurs (dict): Dictionnaire des joueurs de la partie

    Returns:
        tuple(int,str,tuple(int,int)):tuple avec distance,couleur,position
    """    
    def ratio_objet(objet): 
        fantomes_presents=fantome_present(plateau,objet[2],couleur) 
        if not GLOUTON: # O(1)
            return const.PROP_OBJET[objet[1]][0] // objet[0] - fantomes_presents * 20, objet[0]  # O(1)
        else:  # O(1)
            combinaison(analyse)  # O(1)
            return const.PROP_OBJET[objet[1]][0] // objet[0] + fantomes_presents * 20, objet[0]  # O(1)
    return sorted(analyse["objets"],key=ratio_objet,reverse=True) # O(nlogN)

def choix_bis(liste_choix,joueurs):
    """Complexité:  O(N)
    A partir de la liste obtenu de la fonction choix, si nous avons des fantomes dans les premiers indices, 
    on vient renvoyer le max de cette nouvelle liste en fonction d'un ratio nombre de points/distance

    Args:
        liste_choix (list): _description_
        joueurs (dict): dictionnaires des joueurs 

    Returns:
        tuple: tuple de meilleur objet/fantome à aller (distance,identification,position)
    """    
    choix_b=liste_choix[0]  # O(1)
    if choix_b[1].isalpha():  # O(1) 
        new_liste=[choix_b]  # O(1)
        i=1  # O(1)
        while liste_choix[i][1].isalpha():  # O(4) 4 joueurs max
            new_liste.append(liste_choix[i])  # O(1)
            i+=1  # O(1)
        def critere(fant):
            return (joueur.get_nb_points(IA.get_joueur(joueurs,fant[1].upper()))) // fant[0],fant[0] # O(1) 
        return max(new_liste,key=critere)  # O(N)
    else:
        return choix_b  # O(1)

def IA_Pacman(joueurs,ident_pac,plateau,position_pac,distance=2000):
    """Complexité O(N²)
    L'IA du pacman

    Args:
        joueurs (dict): Liste de dictionnaire représentant les joueurs
        ident_pac (str): couleur du pacman
        plateau (dict): plateau du jeu
        position_pac (tuple): position du pacman
        distance (int, optional): distance pour le calque . Defaults to 2000.

    Returns:
        str: Direction du prochain mouvement du pacman N S O E
    """    
    Joueur_Pac=IA.get_joueur(joueurs,ident_pac)  # O(1)
    Duree_pass=joueur.get_duree(Joueur_Pac,const.PASSEMURAILLE)  # O(1)
    Duree_glout=joueur.get_duree(Joueur_Pac,const.GLOUTON)  # O(1)
    passemuraille=True  # O(1)
    glouton=True  # O(1)
    if Duree_glout<=5:  # O(1)
        glouton=False  # O(1)
    ###### Gère de ne pas être dans un mur à la fin de passemuraille
    if Duree_pass==0 or (Duree_pass<3 and not case.est_mur(plat.get_case(plateau,position_pac))): # O(1)
        passemuraille=False # O(1)
    if Duree_pass<4 and case.est_mur(plat.get_case(plateau,position_pac)): # O(1)
        dir_possible=plat.directions_possibles(plateau,position_pac) # O(1)
        if len(dir_possible)!=0: # O(1)
            return random.choice(dir_possible) # O(1)
    ################################################################
    analyse_pacman=IA.analyse_plateau_bis(plateau,position_pac,distance,ident_pac,False,passemuraille) # O(N²)
    if est_vide(analyse_pacman) or len(analyse_pacman["objets"])==0: # O(1)
        return IA.random_possible(plateau,position_pac) # O(1)

    else: # O(1)
        distance_choix,_,position_choix=choix_bis(choix(analyse_pacman,plateau,ident_pac,glouton),joueurs) # O(N)
        #if position_choix in chemin_non_cul_de_sac(plateau,cul_de_sac(plateau))[-2]: # O(n²)
         #   return IA.random_possible(plateau,position_pac) # O(1)
        return IA.trouver_direction(position_pac,IA.prochaine_position(plateau,position_pac,position_choix,distance_choix,passemuraille))  # O(N)
