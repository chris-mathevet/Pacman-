# Fichier pour l'IA du fantome

import const
import plateau as plat
import case
import joueur
import API_IA as IA

def retirer_analyse(analyse,pacmans_danger):
    """ Complexité: O(4)
    A partir d'une analyse (via analyse_plateau), retire les infos inutiles au fantome donné,
        c'est à dire, les autres fantomes, le pacman de notre équipe et les vitamines

    Args:
        analyse (dict): un dictionnaire de listes. 
                        Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                        Les valeurs du dictionnaire sont des listes de paires de la forme
                        (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet
        couleur (str): couleur de l'equipe
        pacmans_danger(set): ensemble des pacmans dangerex (ont l'objet glouton ou l'ont près d'eux)
        analyse_bis(bool): booléens signifiant si c'est la deuxième analyse ou non (éviter redondence)
        PAC(bool): Vrai, retire pour pacman, sinon pour fantome
    """    
    for pacman in analyse["pacmans"]: # O(4) 4 joueurs max
        if pacman[1] in pacmans_danger: # O(1)
            analyse["pacmans"].remove(pacman) # O(1)

####################################  PARTIE ANALYSE DES PACMANS  ####################################

def pacmans_glouton(analyse,joueurs):
    """Complexité: O(4)
    A partir d'une analyse, renvoie un ensemble des pacmans qui ont le pouvoir glouton

    Args:
        analyse (dict): un dictionnaire de listes. 
                        Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                        Les valeurs du dictionnaire sont des listes de paires de la forme
                        (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet
        joueurs (dict): dictionnaire des différents joueurs

    Returns:
        set:ensemble des pacmans (couleur) (str) qui ont le pouvoir glouton

    """    
    pac_danger=set() # O(1)
    for _,pac,_ in analyse["pacmans"]: # O(4) 4 joueurs max
        info_joueur=IA.get_joueur(joueurs,pac) # O(1)
        if joueur.get_duree(info_joueur,const.GLOUTON)!=0: # O(1)
            pac_danger.add(pac) # O(1)
    return pac_danger # O(1)
    
def analyse_pacman(analyse,plateau):
    """Complexité: O(N*n*4)
    Analyse le plateau dans un rayon de 5 cases pour un pacman (présent dans l'analyse du fantome)

    Args:
        analyse (dict): un dictionnaire de listes. 
                        Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                        Les valeurs du dictionnaire sont des listes de paires de la forme
                        (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet
        plateau (dict): plateau de jeu

    Returns:
        dict: dictionnaire clef: couleur du pacman, valeur: son analyse (dict)
    """    
    status = dict() # O(1)
    for (_,couleur,position_pac) in analyse["pacmans"]: # O(4)
        status[couleur]=IA.analyse_plateau_bis(plateau,position_pac,5,couleur) # O(N*n)
    return status # O(1)

def glouton_proximité(analyse_pac):
    """Complexité: # O(4N)
    A partir de l'analyse pacman, renvoi un ensemble de pacmans qui ont l'objet glouton dans un rayon de 5 cases 

    Args:
        analyse_pac (dict):un dictionnaire de listes. 
                            Les clés du dictionnaire sont 'objets', 'pacmans', 'fantomes
                            Les valeurs du dictionnaire sont des listes de paires de la forme
                            (dist,ident,pos) où dist est la distance de l'objet, du pacman ou du fantome
                                        et ident est l'identifiant de l'objet, du pacman ou du fantome
                                        pos est un tuple des coordonnés de l'objet

    Returns:
        set: ensemble de pacmans qui ont l'objet glouton dans leur un rayon de 5 cases
    """  
    pacman_glouton = set() # O(1) 
    for pacman,dico_stats in analyse_pac.items(): # O(4) 4 joueurs max
        for objet in dico_stats["objets"]: # O(N)
            if const.GLOUTON in objet[1]: # O(1)
                pacman_glouton.add(pacman) # O(1)
    return pacman_glouton # O(1)

def pacmans_dangereux(glouton_prox,a_glouton):
    """Complexité: O(4)
    Renvoie un ensemble des pacmans dangereux, 
    à partir des ensembles de pacmans qui on l'objet glouton et 
    ceux qu'ils l'ont dans un rayon de 5

    Args:
        glouton_prox (set): ensemble des pacmans qui ont l'objet glouton à proximité (fonction glouton_proximité)
        a_glouton (set): ensemble des pacmans qui ont l'objet glouton (fonction pacmans_glouton)

    Returns:
        ensemble: l'union des deux ensembles 
    """    
    return glouton_prox|a_glouton # O(4)
    
####################################  FIN PARTIE ANALYSE DES PACMANS  ####################################

def est_vide(analyse):
    """Complexité: O(1)
    Vérifie si les listes d'objets et de pacmans sont tous deux vides

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
    return len(analyse["pacmans"])==0 and len(analyse["objets"])==0 # O(1)

def choix(derniere_analyse,joueurs):
    """Complexité: # O(N)
    Renvoie la position où le fantome ira au prochain tour grace au meilleur choix qui s'offre à lui
        Si il n'y a pas de pacmans à attaquer (dangereux), va aller sur le meilleur objet 

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
    if len(derniere_analyse["pacmans"])!=0: # O(1)
        def ratio_pac(pacman): # O(1)
            """Fonction clé pour tri
                tri en fonction du meilleur ratio nombre_de_points/distance

            Args:
                pacman (tuple): distance entre fantome et pacman, couleur,position

            Returns:
                tuple: le tuple représentant le pacman qui est le meilleur a attaquer
            """            
            return (joueur.get_nb_points(IA.get_joueur(joueurs,pacman[1]))) // pacman[0],pacman[0] # O(1)
        tri=max(derniere_analyse["pacmans"],key=ratio_pac) # O(N)
    else: # O(1)
        def ratio_objet(objet): # O(1)
            """Fonction clé pour tri
                tri en fonction du meilleur ratio valeur/distance

            Args:
                objet (tuple): distance entre fantome et objet, identification,position

            Returns:
                tuple: le tuple représentant l'objet qui est le meilleur à aller dessus 
            """            
            return (const.PROP_OBJET[objet[1]][0]) // objet[0],objet[0] # O(1)
        tri= max(derniere_analyse["objets"],key=ratio_objet) # O(N)
    return tri # O(1)

def IA_Fantome(joueurs,ident_fantome,plateau,position_fantome,distance=2000):
    """Complexité: O(N*n)
    L'IA du Fantome

    Args:
        joueurs (dict): Liste de dictionnaire représentant les joueurs
        ident_fantome (str): couleur du fantome
        plateau (dict): plateau du jeu
        position_fantome (tuple): position du fantome
        distance (int, optional): distance pour le calque . Defaults to 2000.

    Returns:
        str: Direction du prochain mouvement du fantome N S O E
    """    
    ### Partie analyse ###
    analyse_fantome=IA.analyse_plateau_bis(plateau,position_fantome,distance,ident_fantome,True) # O(N*n)
    pacmans_danger=pacmans_dangereux(glouton_proximité(analyse_pacman(analyse_fantome,plateau)),pacmans_glouton(analyse_fantome,joueurs)) # O(N*n*4)
    retirer_analyse(analyse_fantome,pacmans_danger,True) # O(4)
    ### On détermine le choix du fantome
    print(ident_fantome,position_fantome,analyse_fantome)
    if not est_vide(analyse_fantome): # O(1) 
        distance_choix,_,position_choix=choix(analyse_fantome,joueurs) # O(N)
        prochaine_pos=IA.prochaine_position(plateau,position_fantome,position_choix,distance_choix) # O(N)
        return IA.trouver_direction(position_fantome,prochaine_pos) # O(1)
    else:
        return IA.random_possible(plateau,position_fantome) # O(1)
    