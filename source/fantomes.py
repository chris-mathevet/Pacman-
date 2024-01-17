# Fichier pour l'IA du fantome

import const
import plateau as plat
import case
import joueur
import API_IA as IA

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


####################################  PARTIE ANALYSE DES PACMANS  ####################################

def pacmans_glouton(analyse,joueurs):
    """A partir d'une analyse, renvoie un ensemble des pacmans qui ont le pouvoir glouton

    Args:
        analyse (dict): dictionnaire d'analyse
        joueurs (dict): dictionnaire des différents joueurs
    """    
    pac_danger=set()
    for _,pac,_ in analyse["pacmans"]:
        info_joueur=IA.get_joueur(joueurs,pac)
        if joueur.get_duree(info_joueur,const.GLOUTON)!=0:
            pac_danger.add(pac)
    return pac_danger
    
def analyse_pacman(analyse,plateau):
    """
    
    """
    status = dict()
    for (_,couleur,position_pac) in analyse["pacmans"]:
        status[couleur]=IA.analyse_plateau_bis(plateau,position_pac,5)
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

def est_vide(analyse):
    return len(analyse["pacmans"])==0 and len(analyse["objets"])==0

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
            return (joueur.get_nb_points(IA.get_joueur(joueurs,pacman[1]))) // pacman[0],pacman[0]
        tri=max(dernière_analyse["pacmans"],key=ratio_pac)
    else:
        def ratio_objet(objet):
            """_summary_

            Args:
                objet (_type_): _description_

            Returns:
                int: ratio entre distance et valeur, afin de faire un choix par la suite
            """            
            return (const.PROP_OBJET[objet[1]][0]) // objet[0],objet[0]
        tri= max(dernière_analyse["objets"],key=ratio_objet)
    return tri

def IA_Fantome(joueurs,ident_fantome,plateau,position_fantome,distance=2000):
    ### Partie analyse ###
    pacmans_danger=set()
    analyse_fantome=IA.analyse_plateau_bis(plateau,position_fantome,distance)
    analyse_fantome=retirer_analyse(analyse_fantome,ident_fantome,pacmans_danger)
    pacmans_danger=pacmans_dangereux(glouton_proximité(analyse_pacman(analyse_fantome,plateau)),pacmans_glouton(analyse_fantome,joueurs))
    analyse_fantome=retirer_analyse(analyse_fantome,ident_fantome,pacmans_danger,True)
    ### On détermine le choix du fantome
    print(ident_fantome,position_fantome,analyse_fantome)
    if not est_vide(analyse_fantome):
        distance_choix,_,position_choix=choix(analyse_fantome,joueurs)
        prochaine_pos=IA.prochaine_position(plateau,position_fantome,position_choix,distance_choix)
        return IA.trouver_direction(position_fantome,prochaine_pos)
    else:
        return IA.random_possible(plateau,position_fantome)