# Fichier pour l'IA du fantome



import argparse
import random
import client
import const
import plateau as plat
import case
import joueur


test1="20;30\n##############################\n.......##..........##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n..#######.......##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########....##\n#.##.####.##.##..........##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n..####.##..........##.........\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n..#.##.##....##..........##...\n###....#####....###..###....##\n##############################\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"
test3="20;30\n##############################\n.......##.....@....##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n#.#######....!..##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########.$..##\n#.##.####.##.##..~.......##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n######.##..........##..&......\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n###.##.##....##..........##...\n###.##.#####.##.###..###.##.##\n###.##.#####.##.###..###.##.##\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"




plateau1=plat.Plateau(test1)
plateau3=plat.Plateau(test3)

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
    calque[pos[0]][pos[1]]=1
    if pos!=None and (not case.est_mur(plat.get_case(plateau,pos))):
        positions={pos}
        innondation=2
        while len(positions)!=0 and innondation<=distance_max:
            pos_cases_voisines=set()
            for position in positions:
                directions_vois=(plat.directions_possibles(plateau,position))
                for directions_ in directions_vois:
                    new_pos=plat.pos_arrivee(plateau,position,directions_)
                    if calque[new_pos[0]][new_pos[1]]==0:
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
                        dico_distance["objets"]=dico_distance.get("objets",[])
                        dico_distance["objets"].append((valeur,objet,pos))
                    for pac in pacmans:
                        dico_distance["pacmans"]=dico_distance.get("pacmans",[])
                        dico_distance["pacmans"].append((valeur,pac,pos))
                    for fan in fantomes:
                        dico_distance["fantomes"]=dico_distance.get("fantomes",[])
                        dico_distance["fantomes"].append((valeur,fan,pos))
        return dico_distance
    else:
        return None

def retirer_analyse(analyse,fantome):
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

    Returns:
        dict: nouveau dictionnaire de listes, avec les informations non nécéssaire en moins
    """    
    nouvelle_analyse={"objets":[],"pacmans":[]}
    for objets in analyse["objets"]:
        if objets[1]!=const.VITAMINE:
            nouvelle_analyse["objets"].append(objets)
    for pacmans in analyse["pacmans"]:
        if pacmans[1]!=fantome.upper():
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
    return chemin

def prochaine_position(plateau, position_depart, position_arrivee,distance_arrivee):
    return fabrique_chemin(plateau, position_depart, position_arrivee,distance_arrivee)[-1]

analyse=analyse_plateau_bis(plateau3,(3,6),10)
print(analyse)
print(" ")
new_analyse=retirer_analyse(analyse,'e')
print(new_analyse)
chemin=fabrique_chemin(plateau3,(3,6),(5,13),10)
print(chemin)



def tri_distance_pacman(analyse):
    """_summary_

    Args:
        analyse (_type_): _description_

    Returns:
        _type_: _description_
    """    
    pacmans_analyse=analyse["pacmans"]
    def critere(pac):
        return pac[0]
    plus_proche = min(pacmans_analyse, key=critere)
    return plus_proche

# print(tri_distance_pacman({'objets': [(10, '!', (5, 13))], 'pacmans': [(7, 'A', (1, 2)), (1, 'C', (3, 6))]}))


def choix_distance_pacmans(plateau, tuple_donnee,positon_fantome):
    
    pos= tuple_donnee[2]
    distance = tuple_donnee[0]
    return prochaine_position(plateau,positon_fantome, pos, distance)
    
def trouver_direction(plateau, pos_init, pos_arrivee):
    direction_str = ""
    pos_init_x,pos_init_y = pos_init
    pos_arrivee_x,pos_arrivee_y = pos_arrivee 
    return direction_str
    
def status_all_pacman(plateau):
    """
    Renvoie un dictionnaire contenant en clé: l'identifiant du pacman, et en valeur : un dictionnaire avec tuple = position du pacman
    , nb de point, et objet du pacman
    """
    status = dict()
    for x in range(plat.get_nb_lignes):
        for y in range(plat.get_nb_colonnes):
            pos = (x,y)
            dico_case = plat.get_case(plateau,pos)
            if case.get_pacmans(dico_case) != {}:
                for pac in case.get_pacmans(dico_case):
                    status[pac] = {"position_pac" : pos,"nb_points" :joueur.get_nb_points(pac),"objets" : joueur.get_objets(pac)}
    return status
                
def tri_proche(plateau,pos_fantome):
    """_summary_

    Args:
        plateau (dict): plateau de jeu
        pos_fantome (tuple): position du fantome sur le platea
    """    
    def critere(nom):
        return dico_dist[nom]
    dico_dist = dict()
    for pac,stats in status_all_pacman(plateau):
        dist = abs(stats["position_pac"][0] - pos_fantome[0]) + abs(stats["position_pac"][1] - pos_fantome[1])
        dico_dist[pac] = dist
    dist_min = min(dico_dist, key=critere)
    plus_proche = 0 # val random
    return dist_min
        