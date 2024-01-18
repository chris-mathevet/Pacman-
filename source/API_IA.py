
import argparse
import random
import client
import const
import plateau as plat
import case
import joueur

##########################  PLATEAU POUR TESTS  ##########################
test1="20;30\n##############################\n.......##..........##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n..#######.......##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########....##\n#.##.####.##.##..........##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n..####.##..........##.........\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n..#.##.##....##..........##...\n###....#####....###..###....##\n##############################\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"
test2="10;10\n##########\n..##..... \n# ####!###\n#.      ##\n#.#### ###\n .##..@.. \n#.##.# ###\n#.##.# ###\n#&....~ ##\n##########\n4\nA;1;1\nB;1;8\nC;8;6\nD;6;6\n4\na;8;2\nb;3;5\nc;1;9\nd;6;4\n"
test3="20;30\n##############################\n.......##.....@....##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n#.#######....!..##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########.$..##\n#.##.####.##.##..~.......##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n######.##..........##..&......\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n###.##.##....##..........##...\n###.##.#####.##.###..###.##.##\n###.##.#####.##.###..###.##.##\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"

plateau1=plat.Plateau(test1)
plateau2=plat.Plateau(test2)
plateau3=plat.Plateau(test3)
##########################  PLATEAU POUR TESTS  ##########################

def get_joueur(joueurs,couleur):
    """ Complexité : O(1)
        renvoie les informations du joueur gràce à sa couleur 

    Args:
        joueurs (dict): dictionnaire des joueurs 
        couleur (str): couleur du joueur 

    Returns:
        dict: infos du joueurs 
    """    
    return joueurs[couleur] # O(1)

def random_possible(plateau,pos):
    """Complexité: O(1)
        renvoie une direction possible aléatoirement 

    Args:
        plateau (dict): plateau
        pos (tuple): tuple de positions 

    Returns:
        str: direction N S E O
    """    
    return random.choice(plat.directions_possibles(plateau,pos)) # O(1)

def est_un_mur(plateau):
    """Il stock tout les murs dans un ensemble 

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
    """Complexité: # O(N ?)
        Creer un calque sur le principe de l'innondation, 
       à partir de pos en se limitant à la distance max.

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche

    Returns:
        list: matrice du calque ou None si le calque n'est pas réalisable
    """    
    lignes=plat.get_nb_lignes(plateau) # O(1)
    colonnes=plat.get_nb_colonnes(plateau) # O(1)
    calque=[[0 for __ in range(colonnes)]for _ in range(lignes)] # O(ij)
    calque[pos[0]][pos[1]]=0 # O(1)
    if pos!=None and (not case.est_mur(plat.get_case(plateau,pos))): # O(1)
        positions={pos} # O(1)
        innondation=1 # O(1)
        while len(positions)!=0 and innondation<=distance_max: # O(N)  N*(n+J)   N<=distance_max
            pos_cases_voisines=set() # O(1)
            for position in positions: # O(n)
                directions_vois=(plat.directions_possibles(plateau,position)) # O(1)
                for directions_ in directions_vois: # O(4)
                    new_pos=plat.pos_arrivee(plateau,position,directions_) # O(1)
                    if calque[new_pos[0]][new_pos[1]]==0 and new_pos!=pos: # O(1)
                        pos_cases_voisines.add(new_pos) # O(1)
            positions=set() # O(1)
            for voisins in pos_cases_voisines: # O(J)  J>=n  à la fin: J<n
                calque[voisins[0]][voisins[1]]=innondation # O(1)
                positions.add(voisins) # O(1)
            innondation+=1 # O(1)
        
        return calque # O(1)
    else:
        return None # O(1)

def analyse_plateau_bis(plateau, pos, distance_max,couleur,FANTOME=False):
    """ Complexité: O(N*n) 
    DIFFERENCE : Analyse_plateau, mais en rajoutant la position des objets, 
                    pacmans et fantomes dans le dictionnaire
        calcul les distances entre la position pos et les différents objets et
        joueurs du plateau si on commence par partir dans la direction indiquée
        en se limitant à la distance max. Si il n'est pas possible d'aller dans la
        direction indiquée à partir de pos, la fonction doit retourner None

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers indiquant la postion de calcul des distances
        distance_max (int): un entier indiquant la distance limite de la recherche
        couleur(str): couleur de l'equipe
        FANTOME(bool):Si l'analyse est pour un fantome, True, sinon False

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
    lignes=plat.get_nb_lignes(plateau) # O(1)
    colonnes=plat.get_nb_colonnes(plateau) # O(1)
    calque=creation_calque(plateau,pos,distance_max) # O(N)
    if calque!=None: # O(1)
        dico_distance=dict() # O(1)
        dico_distance["objets"]=[] # O(1)
        dico_distance["pacmans"]=[] # O(1)
        dico_distance["fantomes"]=[] # O(1)
        for i in range (lignes): # O(N)
            for j in range(colonnes): # O(n)
                valeur=calque[i][j] # O(1)
                pos=(i,j) # O(1)
                if valeur!=0: # O(1)
                    case_actuel=plat.get_case(plateau,pos) # O(1)
                    pacmans=case.get_pacmans(case_actuel) # O(1)
                    fantomes=case.get_fantomes(case_actuel) # O(1)
                    objet=case.get_objet(case_actuel) # O(1)
                    if objet!=const.AUCUN: # O(1)
                        if FANTOME and objet!=const.VITAMINE and objet!=const.GLOUTON: # O(1)
                            dico_distance["objets"].append((valeur,objet,pos)) # O(1)
                        elif not FANTOME:
                            dico_distance["objets"].append((valeur,objet,pos)) # O(1)
                    if FANTOME: # O(1)
                        for pac in pacmans: # O(1)
                            if pac!=couleur.upper(): # O(1)
                                dico_distance["pacmans"].append((valeur,pac,pos)) # O(1)
                    if not FANTOME: # O(1) 
                        for fan in fantomes: # O(1)
                            if fan!=couleur.lower(): # O(1)
                                dico_distance["fantomes"].append((valeur,fan,pos)) # O(1)
        return dico_distance # O(1)
    else: # O(1)
        return None # O(1)

def trouver_direction(pos_init, pos_arrivee):
    """Complexité: O(1)
    A partir d'une position de départ et d'arrivee, renvoi la direction correspondante au mouvement

    Args:
        pos_init (tuple): tuple de position de départ 
        pos_arrivee (tuple): tuple de position d'arriver

    Returns:
        str: direction N S E O
    """

    direction_str = "" # O(1)
    pos_init_x,pos_init_y = pos_init # O(1)
    pos_arrivee_x,pos_arrivee_y = pos_arrivee  # O(1)

    diff_x = (pos_init_x-pos_arrivee_x) # O(1)
    diff_y = (pos_init_y-pos_arrivee_y) # O(1)
    
    if diff_x>1 or diff_x<-1: # O(1)
        diff_x=diff_x//abs(diff_x)*-1 # O(1)
    if diff_y>1 or diff_y<-1: # O(1)
        diff_y=diff_y//abs(diff_y)*-1 # O(1)

    match (diff_x, diff_y): # O(1)
        case (1,0): # O(1)
            direction_str = "N" # O(1)
        case (-1,0): # O(1)
            direction_str = "S" # O(1)
        case (0,-1): # O(1)
            direction_str = "E" # O(1)
        case (0,1): # O(1)
            direction_str = "O" # O(1)
    print("init : ",pos_init, ", arrivee: ",pos_arrivee) 
    print(diff_x,diff_y)
    return direction_str# O(1)

def fabrique_chemin(plateau, position_depart, position_arrivee,distance_arrivee):
    """Complexité: O(N)
    Renvoie le plus court chemin entre position_depart position_arrivee dans le rayon de distance arrivee

    Args:
        plateau (plateau): un plateau de jeu
        position_depart (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        position_arrivee (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        distance_arrivee (int) :  distance entre position_depart et position_arrivee (gràce à analyse) 
    
    Returns:
        list: Une liste de positions entre position_arrivee et position_depart
        qui représente un plus court chemin entre les deux positions
    """
    calque=creation_calque(plateau,position_depart,distance_arrivee) # O(N)
    chemin=[position_arrivee] # O(1)
    position_actuel=position_arrivee # O(1)
    distance_min=distance_arrivee # O(1)
    for _ in range (distance_arrivee-1): # O(N)
        dir_voisins=plat.directions_possibles(plateau,position_actuel) # O(1)
        for direction in dir_voisins: # O(4)
            pos_voisin=plat.pos_arrivee(plateau,position_actuel,direction) # O(1)
            valeur_voisin=calque[pos_voisin[0]][pos_voisin[1]] # O(1)
            if valeur_voisin!=0 and valeur_voisin<distance_min: # O(1)
                distance_min=valeur_voisin # O(1)
                position_actuel=pos_voisin # O(1)
        if position_actuel!=position_depart: # O(1)
            chemin.append(position_actuel) # O(1)
    return chemin # O(1)

def prochaine_position(plateau, position_depart, position_arrivee,distance_arrivee):
    """ Complexité: O(N)
    renvoie la prochaine position du fantome gràce à chemin

    Args:
        plateau (plateau): un plateau de jeu
        position_depart (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        position_arrivee (tuple): un tuple de deux entiers de la forme (no_ligne, no_colonne) 
        distance_arrivee (int) :  distance entre position_depart et position_arrivee (gràce à analyse) 

    Returns:
        tuple: nouvelle_pos
    """    
    return fabrique_chemin(plateau, position_depart, position_arrivee,distance_arrivee)[-1] # O(N)
