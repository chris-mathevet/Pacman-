# Fichier pour l'IA du pacmand

import argparse
import random
import client
import const
import plateau as plat
import case
import joueur
import fantomes

test1="20;30\n##############################\n.......##..........##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n..#######.......##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########....##\n#.##.####.##.##..........##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n..####.##..........##.........\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n..#.##.##....##..........##...\n###....#####....###..###....##\n##############################\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"
test2="10;10\n##########\n..##..... \n# ####!###\n#.      ##\n#.#### ###\n .##..@.. \n#.##.# ###\n#.##.# ###\n#&....~ ##\n##########\n4\nA;1;1\nB;1;8\nC;8;6\nD;6;6\n4\na;8;2\nb;3;5\nc;1;9\nd;6;4\n"
test3="20;30\n##############################\n.......##.....@....##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n#.#######....!..##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########.$..##\n#.##.####.##.##..~.......##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n######.##..........##..&......\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n###.##.##....##..........##...\n###.##.#####.##.###..###.##.##\n###.##.#####.##.###..###.##.##\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"

carte = "12;12\n.#.#..#.###.\n.#.#.@#..#..\n.#.#..#..#..\n.#.####!.#..\n............\n.####..####.\n.#..#..#..#.\n....#...&.#.\n.~..#...###.\n.####.....#.\n.#.....#..#.\n.####..####.\n5\nA;0;2\nB;1;0\nC;3;11\nD;10;5\nE;4;2\n5\na;0;2\nb;10;2\nc;10;11\nd;0;2\ne;1;0\nf;1;0\n"
perso_map="10;10\n##########\n..##..... \n# ####!###\n#.      ##\n#.#### ###\n .##..@.. \n#.##.# ###\n#.##.#####\n#&....~ ##\n##########\n4\nA;1;1\nB;1;8\nC;8;6\nD;6;6\n4\na;8;2\nb;3;5\nc;1;9\nd;6;4\n"


plateau1=plat.Plateau(test1)
plateau2=plat.Plateau(test2)
plateau3=plat.Plateau(test3)
plateauC=plat.Plateau(carte)
plateau_perso=plat.Plateau(perso_map)


def get_joueur(joueurs,couleur):
    """_summary_

    Args:
        joueurs (_type_): _description_
        couleur (_type_): _description_

    Returns:
        _type_: _description_
    """    
    return joueurs[couleur]

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
    
    if diff_x!=0:
        diff_x=diff_x//abs(diff_x)
    if diff_y!=0:
        diff_y=diff_y//abs(diff_y)

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

    res = []
    final = dict()
    back = None
    new_dir = ""
    for co_cds in cul_de_sac:
        print('les cos_cds:',co_cds)
        
        for dir in const.DIRECTIONS:
            print('la dir:',dir)
            new_co = plat.pos_arrivee(plateau, co_cds, dir)
            if len(plat.directions_possibles(plateau, new_co, False)) >=2 and new_dir != back or back is None:
                back = oppose(dir)
                new_dir = dir
                print(("newdir:",new_dir, "back:", back))
                
                if co_cds not in final.keys():
                    final[co_cds] = []
                    final[co_cds].append(new_co)
                    
                print("final:",final)
                res.append(new_dir)
                
            # plat.prochaine_intersection(plateau,co_cds,dir)
            # for co_inter in intersection(plateau):
            #     res = fantomes.fabrique_chemin(plateau, co_cds,co_inter,20)
    return final
