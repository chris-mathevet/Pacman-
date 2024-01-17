# Fichier pour l'IA du pacman
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
print(est_un_mur(plateau2))
# print(plat.Plateau(plateau2))

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

# print(cul_de_sac(plateau1))
print(cul_de_sac(plateau2))
print(cul_de_sac(plateau3))
print(cul_de_sac(plateauC))
def test():
    # set= {(4, 3), (4, 9), (3, 7), (9, 2), (9, 5), (1, 3), (2, 8), (6, 2), (6, 8), (4, 8), (5, 3), (9, 1), (9, 7), (9, 4), (8, 8), (1, 2), (5, 2), (3, 8), (9, 3), (8, 7), (9, 6), (1, 4), (2, 3), (2, 9), (6, 3), (6, 9)}
    set = cul_de_sac(plateau2)
    for co in set:
        print("pour", co," on peut faire:",plat.directions_possibles(plateau2, co, False))
            
test()

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
print(intersection(plateau2))
print(len(intersection(plateau2)))

def chemin_non_cul_de_sac(plateau, cul_de_sac):
    res = None
    for co_cds in cul_de_sac:
        for dir in const.DIRECTIONS:
            plat.prochaine_intersection(plateau,co_cds,dir)
            for co_inter in intersection(plateau):
                res = fantomes.fabrique_chemin(plateau, co_cds,co_inter,20)
    return res

print("chemin",chemin_non_cul_de_sac(plateau_perso, cul_de_sac(plateau_perso)))


# fabrique_chemin(plateau, position_depart, position_arrivee,distance_arrivee)