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

def get_joueur(joueurs,couleur):
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

#analyse=analyse_plateau_bis(plateau3,(3,6),10)
#print(analyse)
#print(" ")
#new_analyse=retirer_analyse(analyse,'e')
#print(new_analyse)
#chemin=fabrique_chemin(plateau3,(3,6),(5,13),10)
#print(chemin)



######################################################################
#  Ajout de Julian 
######################################################################
def choix_distance_pacmans(plateau, tuple_donnee,positon_fantome):
    
    pos= tuple_donnee[2]
    distance = tuple_donnee[0]
    return prochaine_position(plateau,positon_fantome, pos, distance)
    
def trouver_direction(pos_init, pos_arrivee):
    direction_str = ""
    pos_init_x,pos_init_y = pos_init
    pos_arrivee_x,pos_arrivee_y = pos_arrivee 

    diff_x = pos_init_x-pos_arrivee_x
    diff_y = pos_init_y-pos_arrivee_y

    # (0, +1) Nord
    # (0, -1) Sud
    # (+1, 0) Est
    # (-1, 0) Ouest
    match (diff_x, diff_y):
        case (0,1):
            direction_str = "N"
        case (0,-1):
            direction_str = "S"
        case (1,0):
            direction_str = "E"
        case (-1,0):
            direction_str = "O"
    print("init : ",pos_init, ", arrivee: ",pos_arrivee)
    print(diff_x,diff_y)
    return direction_str

print("par de ",(4, 7), "a", (4, 6)," donc vers le nord",trouver_direction((4, 7), (4, 6)))
print("par de ",(4, 6), "a", (4, 7)," donc vers le Sud",trouver_direction((4, 6), (4, 7)))
print("par de ",(5, 6), "a", (4, 6)," donc vers le Est",trouver_direction((5,6), (4, 6)))
print("par de ",(3, 6), "a", (4, 6)," donc vers le Ouest",trouver_direction((3, 6), (4, 6)))

# print(tri_distance_pacman({'objets': [(10, '!', (5, 13))], 'pacmans': [(7, 'A', (1, 2)), (1, 'C', (3, 6))]}))



 
####################################  PARTIE ANALYSE DES PACMANS  ####################################



def pacmans_glouton(analyse,joueurs):
    """A partir d'une analyse, renvoie un ensemble des pacmans qui ont le pouvoir glouton

    Args:
        analyse (dict): dictionnaire d'analyse
        joueurs (dict): dictionnaire des différents joueurs
    """    
    pac_danger=set()
    for _,pac,_ in analyse["pacmans"]:
        info_joueur=get_joueur(joueurs,pac)
        if joueur.get_duree(info_joueur,const.GLOUTON)!=0:
            pac_danger.add(pac)
    return pac_danger
    
def analyse_pacman(analyse,plateau):
    """
    
    """
    status = dict()
    for (_,couleur,position_pac) in analyse["pacmans"]:
        status[couleur]=analyse_plateau_bis(plateau,position_pac,5)
    return status

def glouton_proximité(analyse_pac):
    """à partir de l'analyse pacman, renvoi un ensemble de pacmans qui ont l'objet glouton dans leur analyse

    Returns:
        set: ensemble de pacmans qui ont l'objet glouton dans leur analyse
    """    
    pacman_glouton = set()
    for pacman,dico_stats in analyse_pac.items():
        for objet in dico_stats["objets"]:
            if const.GLOUTON in objet[1]:
                pacman_glouton.add(pacman)
    return pacman_glouton


def pacmans_dangereux(glouton_prox,a_glouton):
    """Renvoie un ensemble des pacmans dangereux, 
    à partir des ensembles de pacmans qui on l'objet glouton et 
    ceux qu'ils l'ont dans un rayon de 5

    Args:
        glouton_prox (set): ensemble des pacmans qui ont l'objet glouton à proximité (fonction glouton_proximité)
        a_glouton (set): ensemble des pacmans qui ont l'objet glouton (fonction pacmans_glouton)

    Returns:
        ensemble: l'union des deux ensembles 
    """    
    return glouton_prox|a_glouton
    

####################################  FIN PARTIE ANALYSE DES PACMANS  ####################################


                
def tri_proche(plateau,pos_fantome,analyse):
    """_summary_

    Args:
        plateau (dict): plateau de jeu
        pos_fantome (tuple): position du fantome sur le plateau

    Return une liste dans l'ordre croissant des pacmans les plus proches du fantomes
    """    
    def critere(nom):
        return dico_dist[nom]
    dico_dist = dict()
    for pac,stats in analyse_pacman(analyse,plateau):
        dist = abs(stats["position_pac"][0] - pos_fantome[0]) + abs(stats["position_pac"][1] - pos_fantome[1])
        dico_dist[pac] = dist
    dist_min = sorted(dico_dist, key=critere)
    return dist_min
        



def choix(dernière_analyse,joueurs):
    """_summary_

    Returns:
        tuple: distance par entre le fantome a la position selon le choix,ident, position selon le choix
    """    
    

    if len(dernière_analyse["pacmans"])!=0:
        def ratio_pac(pacman):
            """_summary_

            Args:
                distance (int): distance par rapport au fantome
                valeur (int): nb_points

            Returns:
                int: ratio entre distance et valeur, afin de faire un choix par la suite
            """    
            return (pacman[0]+joueur.get_nb_points(get_joueur(joueurs,pacman[1]))) // 2 *100
        tri=max(dernière_analyse["pacmans"],key=ratio_pac)
    else:
        def ratio_objet(objet):
            """_summary_

            Args:
                objet (_type_): _description_

            Returns:
                int: ratio entre distance et valeur, afin de faire un choix par la suite
            """            
            return (objet[0]+const.PROP_OBJET[objet[1]][0]) //2 *100
        tri= max(dernière_analyse["objets"],key=ratio_objet)
    return tri


#joueur1 ="A;152;3;5;4;0;12;5;0;9;Greedy"
#joueur2 ="B;-8;0;5;4;6;4;0;0;0;iut'o"
#joueur3="C;14;2;6;4;23;1;3;2;1;Ghost"
#analyse_test={"objets":[(5,const.IMMOBILITE,(1,1))],"pacmans":[(3,"A",(5,4)),(3,"B",(5,4)),(4,"C",(6,4))]}
#joueurs=dict()
#joueur1=joueur.joueur_from_str(joueur1)
#joueur2=joueur.joueur_from_str(joueur2)
#joueur3=joueur.joueur_from_str(joueur3)
#joueurs[joueur.get_couleur(joueur1)]=joueur1
#joueurs[joueur.get_couleur(joueur2)]=joueur2
#joueurs[joueur.get_couleur(joueur3)]=joueur3
#print(choix(analyse_test,joueurs))


def IA_Fantome(joueurs,ident_fantome,plateau,position_fantome,distance=20):
    ### Partie analyse ###
    pacmans_danger=set()
    analyse_fantome=analyse_plateau_bis(plateau,position_fantome,distance)
    analyse_fantome=retirer_analyse(analyse_fantome,ident_fantome,pacmans_danger)
    pacmans_danger=pacmans_dangereux(glouton_proximité(analyse_pacman(analyse_fantome,plateau)),pacmans_glouton(analyse_fantome,joueurs))
    analyse_fantome=retirer_analyse(analyse_fantome,ident_fantome,pacmans_danger,True)
    ### On détermine le choix du fantome
    distance_choix,_,position_choix=choix(analyse_fantome,joueurs)
    prochaine_pos=prochaine_position(plateau,position_fantome,position_choix,distance_choix)
    return trouver_direction(position_fantome,prochaine_pos)

