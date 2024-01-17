
import argparse
import random
import client
import const
import plateau as plat
import case
import joueur


def get_joueur(joueurs,couleur):
    """renvoie les informations du joueur gràce à sa couleur 

    Args:
        joueurs (dict): dictionnaire des joueurs 
        couleur (str): couleur du joueur 

    Returns:
        dict: infos du joueurs 
    """    
    return joueurs[couleur]


def random_possible(plateau,pos):
    """renvoie une direction possible aléatoirement 

    Args:
        plateau (dict): plateau
        pos (tuple): tuple de positions 

    Returns:
        str: direction N S E O
    """    
    return random.choice(plat.directions_possibles(plateau,pos))


def est_un_mur(plateau):
    """il stock tout les murs dans un ensemble 

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


def creation_calque(plateau,pos,distance_max):
    """Creer un calque sur le principe de l'innondation, 
       à partir de pos en se limitant à la distance max.

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche

    Returns:
        list: matrice du calque ou None si le calque n'est pas réalisable
    """    
    lignes=plat.get_nb_lignes(plateau)
    colonnes=plat.get_nb_colonnes(plateau)
    calque=[[0 for __ in range(colonnes)]for _ in range(lignes)]
    calque[pos[0]][pos[1]]=0
    if pos!=None and (not case.est_mur(plat.get_case(plateau,pos))):
        positions={pos}
        innondation=1
        while len(positions)!=0 and innondation<=distance_max:
            pos_cases_voisines=set()
            for position in positions:
                directions_vois=(plat.directions_possibles(plateau,position))
                for directions_ in directions_vois:
                    new_pos=plat.pos_arrivee(plateau,position,directions_)
                    if calque[new_pos[0]][new_pos[1]]==0 and new_pos!=pos:
                        pos_cases_voisines.add(new_pos)
            positions=set()
            for voisins in pos_cases_voisines:
                calque[voisins[0]][voisins[1]]=innondation
                positions.add(voisins)
            innondation+=1
        
        return calque
    else:
        return None

def analyse_plateau_bis(plateau, pos, distance_max):
    """ DIFFERENCE : Analyse_plateau, mais en rajoutant la position des objets, 
                    pacmans et fantomes dans le dictionnaire
        calcul les distances entre la position pos et les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
    Returns:
        dict: un dictionnaire de listes. 
                Les clés du dictionnaire sont 'objets', 'pacmans' et 'fantomes'
                Les valeurs du dictionnaire sont des listes de paires de la forme
                    (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
                                    pos est un tuple des coordonnés de l'objet
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 
    lignes=plat.get_nb_lignes(plateau)
    colonnes=plat.get_nb_colonnes(plateau)
    calque=creation_calque(plateau,pos,distance_max)
    if calque!=None:
        dico_distance=dict()
        dico_distance["objets"]=[]
        dico_distance["pacmans"]=[]
        dico_distance["fantomes"]=[]
        for i in range (lignes):
            for j in range(colonnes):
                valeur=calque[i][j]
                pos=(i,j)
                if valeur!=0:
                    case_actuel=plat.get_case(plateau,pos)
                    pacmans=case.get_pacmans(case_actuel)
                    fantomes=case.get_fantomes(case_actuel)
                    objet=case.get_objet(case_actuel)
                    if objet!=const.AUCUN:
                        dico_distance["objets"].append((valeur,objet,pos))
                    for pac in pacmans:
                        dico_distance["pacmans"].append((valeur,pac,pos))
                    for fan in fantomes:
                        dico_distance["fantomes"].append((valeur,fan,pos))
        return dico_distance
    else:
        return None

def retirer_analyse(analyse,fantome,pacmans_danger,analyse_bis=False):
    """A partir d'une analyse (via analyse_plateau), retire les infos inutiles au fantome donné,
        c'est à dire, les autres fantomes, le pacman de notre équipe et les vitamines

    Args:
        analyse (dict): un dictionnaire de listes. 
                        Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                        Les valeurs du dictionnaire sont des listes de paires de la forme
                        (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet
        fantome (str): couleur du fantome
        pacmans_danger(set): ensemble des pacmans dangerex (ont l'objet glouton ou l'ont près d'eux)
        analyse_bis(bool): booléens signifiant si c'est la deuxième analyse ou non (éviter redondence)

    Returns:
        dict: nouveau dictionnaire de listes, avec les informations non nécéssaire en moins
    """    
    nouvelle_analyse={"objets":[],"pacmans":[]}
    if not analyse_bis:
        for objets in analyse["objets"]:
            if objets[1]!=const.VITAMINE:
                nouvelle_analyse["objets"].append(objets)
    else:
        nouvelle_analyse["objets"]=analyse["objets"]
    for pacmans in analyse["pacmans"]:
        if pacmans[1]!=fantome.upper() and pacmans[1] not in pacmans_danger:
            nouvelle_analyse["pacmans"].append(pacmans)
    return nouvelle_analyse

def fabrique_chemin(plateau, position_depart, position_arrivee,distance_arrivee):
    """Renvoie le plus court chemin entre position_depart position_arrivee dans le rayon de distance arrivee

    Args:
        plateau (plateau): un plateau de jeu
        position_depart (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        position_arrivee (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        distance_arrivee (int) :  distance entre position_depart et position_arrivee (gràce à analyse) 
    
    Returns:
        list: Une liste de positions entre position_arrivee et position_depart
        qui représente un plus court chemin entre les deux positions
    """
    calque=creation_calque(plateau,position_depart,distance_arrivee)
    chemin=[position_arrivee]
    position_actuel=position_arrivee
    distance_min=distance_arrivee
    for _ in range (distance_arrivee-1):
        dir_voisins=plat.directions_possibles(plateau,position_actuel)
        for direction in dir_voisins:
            pos_voisin=plat.pos_arrivee(plateau,position_actuel,direction)
            valeur_voisin=calque[pos_voisin[0]][pos_voisin[1]]
            if valeur_voisin!=0 and valeur_voisin<distance_min:
                distance_min=valeur_voisin
                position_actuel=pos_voisin
        if position_actuel!=position_depart:
            chemin.append(position_actuel)
    print(chemin)
    return chemin

def prochaine_position(plateau, position_depart, position_arrivee,distance_arrivee):
    """renvoie la prochaine position du fantome gràce à chemin

    Args:
        plateau (plateau): un plateau de jeu
        position_depart (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        position_arrivee (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        distance_arrivee (int) :  distance entre position_depart et position_arrivee (gràce à analyse) 

    Returns:
        tuple: nouvelle_pos
    """    
    return fabrique_chemin(plateau, position_depart, position_arrivee,distance_arrivee)[-1]

def trouver_direction(pos_init, pos_arrivee):
    """A partir d'une position de départ et d'arriver, renvoi la direction correspondante au mouvement

    Args:
        pos_init (tuple): tuple de position de départ 
        pos_arrivee (tuple): tuple de position d'arriver

    Returns:
        str: direction N S E O
    """

    direction_str = ""
    pos_init_x,pos_init_y = pos_init
    pos_arrivee_x,pos_arrivee_y = pos_arrivee 

    diff_x = (pos_init_x-pos_arrivee_x)
    diff_y = (pos_init_y-pos_arrivee_y)
    
    if diff_x>1 or diff_x<-1:
        diff_x=diff_x//abs(diff_x)*-1
    if diff_y>1 or diff_y<-1:
        diff_y=diff_y//abs(diff_y)*-1

    match (diff_x, diff_y):
        case (1,0):
            direction_str = "N"
        case (-1,0):
            direction_str = "S"
        case (0,-1):
            direction_str = "E"
        case (0,1):
            direction_str = "O"
    print("init : ",pos_init, ", arrivee: ",pos_arrivee)
    print(diff_x,diff_y)
    return direction_str