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
    """il mets dans un ensemble, l'ensemble des coordonnées ou se situe des murs 

    Args:
        plateau (dict): dico du plateau de jeu

    Returns:
        set: ensemble des coordonnées ou se situ un mur
    """
    murs= set()
    lignes=plat.get_nb_lignes(plateau)
    colonnes=plat.get_nb_colonnes(plateau)
    for i in range(lignes):
        for j in range(colonnes):
            if case.est_mur(plat.get_case(plateau,(i,j))):
                murs.add((i,j))
    return murs

def cul_de_sac(plateau):
    """il mets dans un ensemble, l'ensemble des coordonnées ou se situe des culs de sacs

    Args:
        plateau (dict): dico du plateau de jeu

    Returns:
        set: ensemble des coordonnées ou se situ un cul de sac
    """
    pos_cul_de_sac= set()
    lignes=plat.get_nb_lignes(plateau)
    colonnes=plat.get_nb_colonnes(plateau)
    for i in range (lignes):
        for j in range(colonnes):
            if i !=0 and j!=0 and i !=lignes-1 and j!=colonnes-1 and not len(plat.directions_possibles(plateau, (i,j), False)) != 1:
                if (i,j) not in est_un_mur(plateau):
                    print(len(plat.directions_possibles(plateau, (i,j), False))) 
                    pos_cul_de_sac.add((i,j))
            else:
                pass
    return pos_cul_de_sac


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
    """il mets dans un ensemble, l'ensemble des coordonnées ou se situe des intersections de la carte

    Args:
        plateau (dict): dico du plateau de jeu

    Returns:
        set: ensemble des coordonnées ou se situ une intersection
    """
    les_intersections= set()
    lignes=plat.get_nb_lignes(plateau)
    colonnes=plat.get_nb_colonnes(plateau)
    for i in range (lignes):
        for j in range(colonnes):
            if i !=0 and j!=0 and i !=lignes-1 and j!=colonnes-1 and len(plat.directions_possibles(plateau, (i,j), False)) >= 3:
                if (i,j) not in est_un_mur(plateau):
                    les_intersections.add((i,j))

    return les_intersections

def analyse_objets(analyse):
    """return un dict qui prends en clé la position (tuple) de l'objet, et en valeur un tuple (nom de l'objet, distance avec pacman)
    
    Args:
        analyse (dict): ....

    Returns:
        dict:un dictionnaraire
                clé(tuple):position
                valeur(tuple): (nom de l'objet, distance avec pacman)

    """
    status = dict()
    for (distance,nom_objet,position_objet) in analyse["objets"]:
        status[position_objet]= (nom_objet,distance)
    return status

def fantome_present(analyse):
    """nombre de fantome dans le perimetre definie par analyse autour du pacman
        
    Args:
        analyse (dict): ....

    Returns:
        int: nombre de fantome autour 
    """
    status = set()
    for (_,couleur,_) in analyse["fantomes"]:
        status.add(couleur)
    return len(status)

def oppose(direction):
    """inverse le direction
        
    Args:
        direction (str): une chaine de caractere composé de d'une lettre comme NSEO  

    Returns:
        int: nombre de fantome autour 
    """
    if direction == 'N':
        return 'S'
    if direction == 'S':
        return 'N'
    if direction == 'O':
        return 'E'
    if direction == 'E':
        return 'O'

def tp_urgent(plateau, pos, encercle):
    les_murs = est_un_mur(plateau)
    if encercle is True:
        for direction in const.DIRECTIONS:
            pos_arrivee = plat.pos_arrivee(plateau, pos, direction)
            if pos_arrivee in les_murs:
                return (direction, pos_arrivee)
    else:
        return None


player = joueur.joueur_from_str("A;152;3;28;0;0;12;5;0;9;Greedy")    

 ##########################
#  pas FINI
 ##########################

def chemin_non_cul_de_sac(plateau, cul_de_sac):

    final = {}
    for co_cds in cul_de_sac:
        for direction in const.DIRECTIONS:
            # distance = 0
            pos_debut = plat.pos_arrivee(plateau,co_cds,direction)
            pos_actuelle = pos_debut
            back = oppose(direction)
            while len(plat.directions_possibles(plateau,pos_actuelle)) == 3:
                if direction in plat.directions_possibles(plateau,pos_actuelle):
                    pos_actuelle = plat.pos_arrivee(plateau,pos_actuelle,direction)
                    if co_cds not in final.keys():
                        final[co_cds] = []
                        final[co_cds].append(pos_actuelle)                
                else:
                    for dir in plat.directions_possibles(plateau,pos_actuelle):
                        if dir != back:
                            back = oppose(dir)
                            pos_actuelle = plat.pos_arrivee(plateau,pos_actuelle,dir)
                            if co_cds not in final.keys():

                                final[co_cds] = []
                                final[co_cds].append(pos_actuelle)
            # if plat.directions_possibles(plateau,pos_actuelle) == direction:   
            #     distance = -1
                
    return final

def combinaison(analyse):
    """Vient ajouter les tuple de la liste fantome de analyse dans celles des objets, 
    et ils se comporteront comme des objets avec une identifcation '*' (rajouté dans const)  qui a une valeur de 20 points

    Args:
        analyse (dict): analyse
    """    
    const.PROP_OBJET['*']=(20,0) # O(1)
    for fant in analyse["fantomes"]: # O(4) 4 joueurs max 
        new_tuple=(fant[0],'*',fant[2]) # O(1)
        analyse["objets"].append(new_tuple) # O(1)

def choix(analyse,GLOUTON=False):
    def ratio_objet(objet):
        fantomes_presents=fantome_present(analyse)
        if not GLOUTON:
            return const.PROP_OBJET[objet[1]][0] // objet[0] - fantomes_presents * 20, objet[0]
        else:
            combinaison(analyse)
            return const.PROP_OBJET[objet[1]][0] // objet[0] + fantomes_presents * 20, objet[0]
    tri= max(analyse["objets"],key=ratio_objet) # O(N)
    return tri

def IA_Pacman(joueurs,ident_pac,plateau,position_pac,distance=2000):
    Joueur_Pac=IA.get_joueur(joueurs,ident_pac)
    Duree_pass=joueur.get_duree(Joueur_Pac,const.PASSEMURAILLE)
    passemuraille=False
    if Duree_pass>0:
        passemuraille=True
    analyse_pacman=IA.analyse_plateau_bis(plateau,position_pac,distance,ident_pac,False,passemuraille)
    distance_choix,_,position_choix=choix(analyse_pacman)
    #print("pacman",ident_pac, position_pac,IA.prochaine_position(plateau,position_pac,position_choix,distance_choix),"direction:",IA.trouver_direction(position_pac,IA.prochaine_position(plateau,position_pac,position_choix,distance_choix)))
    return IA.trouver_direction(position_pac,IA.prochaine_position(plateau,position_pac,position_choix,distance_choix,passemuraille))

