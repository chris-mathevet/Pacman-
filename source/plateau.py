"""
            SAE1.02 PACMAN IUT'O
         BUT1 Informatique 2023-2024

        Module plateau.py
        Ce module contient l'implémentation de la structure de données
        qui gère le plateau jeu aussi qu'un certain nombre de fonctions
        permettant d'observer le plateau et d'aider l'IA à prendre des décisions
"""
import const
import case
import random



def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """
    return plateau["proportion"][0]


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """
    return plateau["proportion"][1]

def pos_ouest(plateau, pos):
    """retourne la position de la case à l'ouest de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    colonne = get_nb_colonnes(plateau)
    return (pos[0],(pos[1]-1)%colonne)


def pos_est(plateau, pos):
    """retourne la position de la case à l'est de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    colonne = get_nb_colonnes(plateau)
    return (pos[0],(pos[1]+1)%colonne)

def pos_nord(plateau, pos):
    """retourne la position de la case au nord de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    ligne = get_nb_lignes(plateau)
    return ((pos[0]-1)%ligne,pos[1])

def pos_sud(plateau, pos):
    """retourne la position de la case au sud de pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position
    Returns:
        int: un tuple d'entiers
    """
    ligne = get_nb_lignes(plateau)
    return ((pos[0]+1)%ligne,pos[1])


def pos_arrivee(plateau,pos,direction):
    """ calcule la position d'arrivée si on part de pos et qu'on va dans
    la direction indiquée en tenant compte que le plateau est un tore
    si la direction n'existe pas la fonction retourne None
    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire d'entiers qui donne la position de départ
        direction (str): un des caractère NSEO donnant la direction du déplacement

    Returns:
        None|tuple: None ou une paire d'entiers indiquant la position d'arrivée
    """
    pos_fin = None
    match direction:
        case"N":
            pos_fin = pos_nord(plateau,pos)
        case "S":
            pos_fin = pos_sud(plateau,pos)
        case "O":
            pos_fin = pos_ouest(plateau,pos)
        case "E":
            pos_fin = pos_est(plateau,pos)
    return pos_fin

def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """
    return plateau["matrice"][pos[0]][pos[1]]

def get_objet(plateau, pos):
    """retourne l'objet qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        str: le caractère symbolisant l'objet
    """
    get_case(plateau,pos)["objet"]

def poser_pacman(plateau, pacman, pos):
    """pose un pacman en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le pacman
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_pacman(get_case(plateau,pos),pacman)

def poser_fantome(plateau, fantome, pos):
    """pose un fantome en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_fantome(get_case(plateau,pos),fantome)

def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    case.poser_objet(get_case(plateau,pos),objet)

random_chaine="20;30\n##############################\n.......##..........##.........\n######.##.#####.##.##.##.#####\n######.##.#####.##.##.##.#####\n#.........#####.##.##.##.#####\n..#######.......##.##.##......\n#.#######.#####.##....##.#####\n#.##......#####.########.#####\n#.##.####.##....########....##\n#.##.####.##.##..........##.##\n#......##.##.#####.##.#####.##\n######.##.##.#####.##.#####.##\n..####.##..........##.........\n#......##.#####.##.##.##.#####\n#.####.##.#####.##.##.##.#####\n#.####....##....##.##.##....##\n#...##.##.##.##.##.##.##.##.##\n..#.##.##....##..........##...\n###....#####....###..###....##\n##############################\n5\nA;1;2\nB;1;22\nC;3;6\nD;10;21\nE;16;1\n5\na;7;5\nb;10;1\nc;10;12\nd;7;5\ne;3;6\n"

def plateau_from_str(la_chaine, complet=True):
    """Construit un plateau à partir d'une chaine de caractère contenant les informations
        sur le contenu du plateau (voir sujet)

    Args:
        la_chaine (str): la chaine de caractères décrivant le plateau

    Returns:
        dict: le plateau correspondant à la chaine. None si l'opération a échoué
    """
    plateau=dict()
    chaine=la_chaine.split("\n")
    proportions=chaine[0].split(';')
    proportions=[int(i)for i in proportions]
    plateau['proportion']=(proportions[0],proportions[1])
    matrice=[]
    for mat in range(1,proportions[0]+1):
        la_ligne=chaine[mat]
        ligne=[]
        for cara in la_ligne:
            match cara:
                case "#":
                    nouvelle_case = case.Case(True)
                case ".":
                    nouvelle_case = case.Case(objet=const.VITAMINE)
                case "$":
                    nouvelle_case = case.Case(objet=const.GLOUTON)
                case "@":
                    nouvelle_case = case.Case(objet=const.IMMOBILITE)
                case "~":
                    nouvelle_case = case.Case(objet=const.PASSEMURAILLE)
                case "!":
                    nouvelle_case = case.Case(objet=const.TELEPORTATION)
                case "&":
                    nouvelle_case = case.Case(objet=const.VALEUR)
                case " ":
                    nouvelle_case = case.Case()
            ligne.append(nouvelle_case)
        matrice.append(ligne)

    plateau["matrice"]=matrice
    plateau["pacmans"]=dict()
    plateau["fantomes"]=dict()
    nb_pacs=int(chaine[1+proportions[0]])
    nb_fant=int(chaine[2+proportions[0]+nb_pacs])
    for _ in range(nb_pacs):
        pacman=chaine[2+proportions[0]+_].split(";")
        plateau["pacmans"][pacman[0]]=(int(pacman[1]),int(pacman[2]))
        case.poser_pacman(plateau["matrice"][int(pacman[1])][int(pacman[2])],pacman[0])
    for _ in range(nb_fant):
        fantome=chaine[3+proportions[0]+nb_pacs+_].split(";")
        plateau["fantomes"][fantome[0]]=(int(fantome[1]),int(fantome[2]))
        case.poser_fantome(plateau["matrice"][int(fantome[1])][int(fantome[2])],fantome[0])
    return plateau

plateau_from_str(random_chaine)

def Plateau(plan):
    """Créer un plateau en respectant le plan donné en paramètre.
        Le plan est une chaine de caractères contenant
            '#' (mur)
            ' ' (couloir non peint)
            une lettre majuscule (un couloir peint par le joueur représenté par la lettre)

    Args:
        plan (str): le plan sous la forme d'une chaine de caractères

    Returns:
        dict: Le plateau correspondant au plan
    """
    return plateau_from_str(plan)

def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """
    plateau["matrice"][pos[0]][pos[1]]=une_case




def enlever_pacman(plateau, pacman, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        pacman (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    return case.prendre_pacman(get_case(plateau,pos),pacman)


def enlever_fantome(plateau, fantome, pos):
    """enlève un fantome qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        fantome (str): la lettre représentant le fantome
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    return case.prendre_fantome(get_case(plateau,pos),fantome)


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    return case.prendre_objet(get_case(plateau,pos))

        
def deplacer_pacman(plateau, pacman, pos, direction, passemuraille=False):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau si c'est possible

    Args:
        plateau (dict): Le plateau considéré
        pacman (str): La lettre identifiant le pacman à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement
        passemuraille (bool): un booléen indiquant si le pacman est passemuraille ou non

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du pacman 
                   (None si le pacman n'a pas pu se déplacer)
    """
    new_pos=pos_arrivee(plateau,pos,direction)
    if new_pos!=None:
        new_case=get_case(plateau,new_pos)
        if (not case.est_mur(new_case)) or passemuraille:
            enlever_pacman(plateau,pacman,pos)
            case.poser_pacman(new_case,pacman)
        else:
            new_pos=None
    return new_pos


def deplacer_fantome(plateau, fantome, pos, direction):
    """Déplace dans la direction indiquée un fantome se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        fantome (str): La lettre identifiant le fantome à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        (int,int): une paire (lig,col) indiquant la position d'arrivée du fantome
                   None si le joueur n'a pas pu se déplacer
    """
    new_pos=pos_arrivee(plateau,pos,direction)
    if new_pos!=None:
        new_case=get_case(plateau,new_pos)
        if not case.est_mur(new_case):
            enlever_fantome(plateau,fantome,pos)
            case.poser_fantome(new_case,fantome)
        else:
            new_pos=None
    return new_pos

def case_vide(plateau):
    """choisi aléatoirement sur la plateau une case qui n'est pas un mur et qui
       ne contient ni pacman ni fantome ni objet

    Args:
        plateau (dict): le plateau

    Returns:
        (int,int): la position choisie
    """
    lignes=get_nb_lignes(plateau)
    colonnes=get_nb_colonnes(plateau)
    new_x=random.randint(0,lignes)
    new_y=random.randint(0,colonnes)
    while case.est_mur(get_case(plateau,(new_x,new_y))):
        new_x=random.randint(0,lignes)
        new_y=random.randint(0,colonnes)
    return (new_x,new_y)


def directions_possibles(plateau,pos,passemuraille=False):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
        passemuraille (bool): indique si on s'autorise à passer au travers des murs
    
    Returns:
        str: une chaine de caractères indiquant les directions possibles
              à partir de pos
    """
    directions_pos=""
    for direction in "NESO":
        new_pos=pos_arrivee(plateau,pos,direction)
        if not case.est_mur(get_case(plateau,new_pos)) or passemuraille:
            directions_pos+=direction
    return directions_pos

#---------------------------------------------------------#

def creation_calque(plateau,pos,direction,distance_max=-1):
    lignes=get_nb_lignes(plateau)
    colonnes=get_nb_colonnes(plateau)
    calque=[[0 for j in range(colonnes)]for i in range(lignes)]
    depart=pos_arrivee(plateau,pos,direction)
    if distance_max==-1:
        distance_max=lignes*colonnes
    if depart!=None:
        positions={depart}
        innondation=1
        while len(positions)!=0 or innondation<=distance_max:
            pos_cases_voisines={}
            for position in positions:
                directions_vois=(directions_possibles(plateau,position))
                for directions_ in directions_vois:
                    new_pos=pos_arrivee(plateau,position,directions_)
                    if calque[new_pos[0]][new_pos[1]]!=0:
                        pos_cases_voisines.add(new_pos)
            positions={}
            for voisins in pos_cases_voisines:
                calque[voisins[0]][voisins[1]]=innondation
                positions.add(voisins)
            
            innondation+=1
            calque[depart[0]][depart[1]]=0
            return calque
    else:
        return None
   
    

def analyse_plateau(plateau, pos, direction, distance_max):
    """calcul les distances entre la position pos et les différents objets et
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
                    (dist,ident) où dist est la distance de l'objet, du pacman ou du fantome
                                    et ident est l'identifiant de l'objet, du pacman ou du fantome
            S'il n'est pas possible d'aller dans la direction indiquée à partir de pos
            la fonction retourne None
    """ 
    lignes=get_nb_lignes(plateau)
    colonnes=get_nb_colonnes(plateau)
    calque=creation_calque(plateau,pos,direction,distance_max)
    if calque!=None:
        dico_distance=dict()
        for i in range (lignes):
            for j in range(colonnes):
                valeur=calque[i][j]
                pos=(i,j)
                if valeur!=0:
                    case_actuel=get_case(plateau,pos)
                    pacmans=case.get_pacmans(case_actuel)
                    fantomes=case.get_fantomes(case_actuel)
                    objet=case.get_objet(case_actuel)
                    if objet!=const.AUCUN:
                        dico_distance["objets"]=dico_distance.get("objets",[]).append((valeur,objet))
                    for pac in pacmans:
                        dico_distance["pacmans"]=dico_distance.get("pacmans",[]).append((valeur,pac))
                    for fan in fantomes:
                        dico_distance["fantomes"]=dico_distance.get("fantomes",[]).append((valeur,fan))
        return dico_distance
    else:
        return None
                    
    
        

def prochaine_intersection(plateau,pos,direction):
    """calcule la distance de la prochaine intersection
        si on s'engage dans la direction indiquée

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire d'entiers donnant la position de départ
        direction (str): la direction choisie

    Returns:
        int: un entier indiquant la distance à la prochaine intersection
             -1 si la direction mène à un cul de sac.
    """
    distance = 0
    pos_debut = pos_arrivee(plateau,pos,direction)
    pos_actuelle = pos_debut
    while len(directions_possibles(plateau,pos_actuelle)) == 2:
        distance += 1
        pos_actuelle = pos_arrivee(plateau,pos_actuelle,direction)
        
    if directions_possibles(plateau,pos_actuelle) == direction:   
        distance = -1
    
    return distance
    

# A NE PAS DEMANDER
def plateau_2_str(plateau):
        res = str(get_nb_lignes(plateau))+";"+str(get_nb_colonnes(plateau))+"\n"
        pacmans = []
        fantomes = []
        for lig in range(get_nb_lignes(plateau)):
            ligne = ""
            for col in range(get_nb_colonnes(plateau)):
                la_case = get_case(plateau,(lig, col))
                if case.est_mur(la_case):
                    ligne += "#"
                    les_pacmans = case.get_pacmans(la_case)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                else:
                    obj = case.get_objet(la_case)
                    les_pacmans = case.get_pacmans(la_case)
                    les_fantomes= case.get_fantomes(la_case)
                    ligne += str(obj)
                    for pac in les_pacmans:
                        pacmans.append((pac, lig, col))
                    for fantome in les_fantomes:
                        fantomes.append((fantome,lig,col))
            res += ligne+"\n"
        res += str(len(pacmans))+'\n'
        for pac, lig, col in pacmans:
            res += str(pac)+";"+str(lig)+";"+str(col)+"\n"
        res += str(len(fantomes))+"\n"
        for fantome, lig, col in fantomes:
            res += str(fantome)+";"+str(lig)+";"+str(col)+"\n"
        return res

