import ipaddress
import os

import pygame
import json


def souris_est_dans_zone(souris, zone):
    x, y, largeur, hauteur = zone
    return x < souris[0] < x + largeur and y < souris[1] < y + hauteur


def afficher_texte(fenetre, x, y, texte, taille, couleur=(0, 0, 0), font="freesansbold.ttf"):
    font = pygame.font.Font(font, taille)
    texte = font.render(texte, True, couleur)
    text_rect = texte.get_rect(center=(x, y))
    fenetre.blit(texte, text_rect)


def charger_config():
    with open(chemin_absolu_dossier+"config.json", "r") as fichier:
        return json.load(fichier)


def récupérer_port():
    return charger_config()["port"]


def récupérer_ip_cible():
    return charger_config()["ip"]


def mettre_à_jour_ip(nouvelle_ip):
    config = charger_config()
    config["ip"] = nouvelle_ip
    with open(chemin_absolu_dossier+"config.json", "w") as fichier:
        json.dump(config, fichier)


def est_local():
    return charger_config()["local"]


def mettre_à_jour_port(nouveau_port):
    config = charger_config()
    config["port"] = nouveau_port
    with open(chemin_absolu_dossier+"config.json", "w") as fichier:
        json.dump(config, fichier)


def ip_est_valide(ip):
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ValueError:
        return False


# liste de couleurs nom:rgb
dict_couleurs = {
    "rouge": (255, 0, 0),
    "vert": (0, 255, 0),
    "bleu": (0, 0, 255),
    "jaune": (255, 255, 0),
    "noir": (0, 0, 0),
    "blanc": (255, 255, 255),
    "gris": (128, 128, 128),
    "marron": (139, 69, 19),
    "rose": (255, 105, 180),
    "violet": (128, 0, 128),
    "cyan": (0, 255, 255),
    "orange": (255, 165, 0),
    "bleu marin": (20, 40, 70),
    "boutton": (255, 150, 113),
    "marron clair": (190, 118, 48),
}

largeur_fenetre, hauteur_fenetre = 800, 600
couleurs_cases = (dict_couleurs["blanc"], dict_couleurs["marron clair"])
serveur_tourne = False
chemin_absolu_dossier = os.path.dirname(os.path.abspath(__file__)) + "/"

def status_serveur(status=None):
    global serveur_tourne
    if status is None:
        return serveur_tourne
    serveur_tourne = status


def copier_grille(grille):
    return [[pièce.copy() if pièce else None for pièce in ligne] for ligne in grille]


def liste_pièces_restantes(grille) -> list:
    return [pièce for ligne in grille for pièce in ligne if pièce]


def nombre_pièces_restantes(grille) -> int:
    return len(liste_pièces_restantes(grille))

def couleur_opposée(couleur):
    if type(couleur) == str:
        return "blanc" if couleur == "noir" else "noir"
    else:
        return 1 if couleur == -1 else -1


def vérifie_si_victoire(grille):
    couleurs_avec_un_roi = set()
    for ligne in grille:
        for pièce in ligne:
            if pièce and pièce.type_de_pièce == "roi":
                couleurs_avec_un_roi.add(pièce.couleur)

    if "blanc" not in couleurs_avec_un_roi:
        return "noir"
    elif "noir" not in couleurs_avec_un_roi:
        return "blanc"

    return False

def vérifie_si_nul(grille, zobrsit_grille, partie=None):
    if partie:
        if partie.tour_depuis_coup_intéressant > 50:
            return True
        if partie.répétitions.count(zobrsit_grille) >= 3:
            return "répétition"
        elif pas_assez_de_matériel(grille):
            return "insuffisance de matériel"
    return False

def a_matériel_pour_mat(pièces_couleur):
    nombre_pièces = sum(pièces_couleur.values())
    if nombre_pièces <= 2:
        return False
    if nombre_pièces == 3 and pièces_couleur["cavalier"] == 2:
        return False
    return True


def pas_assez_de_matériel(grille):
    if nombre_pièces_restantes(grille) <= 2:
        return True
    type_de_pièces_restantes = {
        "blanc": {
            "fou": 0,
            "cavalier": 0,
            "roi": 0,
            "dame": 0,
            "pion": 0,
            "tour": 0
        },
        "noir": {
            "fou": 0,
            "cavalier": 0,
            "roi": 0,
            "dame": 0,
            "pion": 0,
            "tour": 0
        }
    }
    for i in grille:
        for j in i:
            if j:
                type_de_pièces_restantes[j.couleur][j.type_de_pièce] += 1
    pièces_blanc = type_de_pièces_restantes["blanc"]
    pièces_noir = type_de_pièces_restantes["noir"]

    for color in [pièces_blanc, pièces_noir]:
        if color["pion"] + color["dame"] + color["tour"] > 0:
            return False

    if not a_matériel_pour_mat(pièces_blanc) and not a_matériel_pour_mat(pièces_noir):
        return True
    return False


def liste_pièces_bougeables(grille, couleur: str) -> list:
    return [pièce for ligne in grille for pièce in ligne if pièce and pièce.couleur == couleur]

def liste_coups_légaux(couleur, grille):
    pièces = liste_pièces_bougeables(grille, couleur)
    return [(pièce, coup) for pièce in pièces for coup in pièce.liste_coups_legaux(grille)]

def points_avec_roi(grille):
    points = {'blanc': 0, 'noir': 0}

    for ligne in grille:
        for case in ligne:
            if case:
                points[case.couleur] += case.valeur

    return points['blanc'], points['noir']

def montrer_grille(grille):
    grid = [[],[],[],[],[],[],[],[]]
    for i in grille:
        ligne = []
        for j in i:
            if j:
                ligne.append(f"{j.couleur[0]}_{j.type_de_pièce}")
                grid[grille.index(i)].append(f"{j.couleur[0]}_{j.type_de_pièce}")
            else:
                ligne.append(None)
                grid[grille.index(i)].append(None)
        print(ligne)
    print()

def captures_possibles(coups_légaux, grille):
    captures = []
    for (pièce, coup) in coups_légaux:
        nouvelle_case = grille[pièce.y + coup[1]][pièce.x + coup[0]]
        if nouvelle_case and nouvelle_case.couleur != pièce.couleur:
            captures.append((pièce, coup))
    return captures
