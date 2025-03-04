import random
import socket
import uuid

import pygame
import utils
from bots import negamax, bot
from interface import boutton
from interface import menu_pause
from moteur.joueur import Joueur
from moteur.partie import Partie
from moteur.pièces.roi import Roi
from utils import couleurs_cases


def afficher_grille(fenêtre, couleur_joueur):
    nom_colonnes = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for colonne in range(8):
        for ligne in range(8):
            pygame.draw.rect(fenêtre, couleurs_cases[(colonne + ligne) % 2], (colonne * taille_case + decalage, ligne * taille_case + decalage, taille_case, taille_case))

            #les numéros des lignes
            if colonne == 0:
                couleur_texte = couleurs_cases[(colonne + ligne + 1) % 2]
                if couleur_joueur == "blanc":
                    utils.afficher_texte(fenêtre, decalage + int(taille_case/9), ligne * taille_case + decalage + taille_case // 2 - taille_case // 3.5, str(8 - ligne), 30, couleur=couleur_texte)
                else:
                    utils.afficher_texte(fenêtre, decalage+taille_case//9, ligne * taille_case + decalage + taille_case // 2 - taille_case//3.5, str(ligne + 1), 30, couleur=couleur_texte)

            #les lettres des colonnes
            x = colonne * taille_case + decalage + taille_case // 1.2
            y = 8 * taille_case + decalage - taille_case // 5
            couleur_texte = couleurs_cases[(colonne + 0) % 2]
            utils.afficher_texte(fenêtre, x, y, nom_colonnes[colonne], 30, couleur=couleur_texte)


def afficher_pièces(fenêtre, grille, couleur_joueur):
    for ligne in grille:
        for case in ligne:
            if case:
                pièce_rect = images_pièces[case.couleur][case.type_de_pièce].get_rect()
                if couleur_joueur == "blanc":
                    pièce_rect.center = (case.x * taille_case + decalage + taille_case//2, case.y * taille_case + decalage + taille_case//2)
                else:
                    pièce_rect.center = (case.x * taille_case + decalage + taille_case//2, (7 - case.y) * taille_case + decalage + taille_case//2)
                fenêtre.blit(images_pièces[case.couleur][case.type_de_pièce], pièce_rect)


taille_case = 90
decalage = 60
largeur_fenêtre = taille_case * 8 + decalage * 2
hauteur_fenêtre = taille_case * 8 + decalage * 2
arriere_plan = pygame.image.load("assets/images/menu_arrière_plan.jpg")
arriere_plan = pygame.transform.scale(arriere_plan, (largeur_fenêtre, hauteur_fenêtre))
image_case_séléctionnée = pygame.image.load("assets/images/case_séléctionnée.png")
image_case_séléctionnée = pygame.transform.scale(image_case_séléctionnée, (taille_case, taille_case))
taille_pièce = int(90/100 * taille_case), int(90/100 * taille_case)
images_pièces = {
    "blanc": {
        "pion": pygame.image.load("assets/images/pion blanc.png"),
        "tour": pygame.image.load("assets/images/tour blanc.png"),
        "cavalier": pygame.image.load("assets/images/cavalier blanc.png"),
        "fou": pygame.image.load("assets/images/fou blanc.png"),
        "dame": pygame.image.load("assets/images/dame blanc.png"),
        "roi": pygame.image.load("assets/images/roi blanc.png")
    },
    "noir": {
        "pion": pygame.image.load("assets/images/pion noir.png"),
        "tour": pygame.image.load("assets/images/tour noir.png"),
        "cavalier": pygame.image.load("assets/images/cavalier noir.png"),
        "fou": pygame.image.load("assets/images/fou noir.png"),
        "dame": pygame.image.load("assets/images/dame noir.png"),
        "roi": pygame.image.load("assets/images/roi noir.png")
    }
}

for couleur in images_pièces:
    for pièce in images_pièces[couleur]:
        images_pièces[couleur][pièce] = pygame.transform.scale(images_pièces[couleur][pièce], taille_pièce)


def case_de_la_souris(couleur_du_joueur):
    if couleur_du_joueur == "blanc":
        x, y = pygame.mouse.get_pos()
        colonne = (x - decalage) // taille_case
        ligne = (y - decalage) // taille_case
        if 0 <= colonne < 8 and 0 <= ligne < 8:
            return colonne, ligne
        return None
    else:
        x, y = pygame.mouse.get_pos()
        colonne = (x - decalage) // taille_case
        ligne = 7 - (y - decalage) // taille_case
        if 0 <= colonne < 8 and 0 <= ligne < 8:
            return colonne, ligne
        return None


def vérifie_fin_de_partie(partie: Partie, zobrist_grille, fenêtre, couleur_joueur, multi=False):
    est_victoire = utils.vérifie_si_victoire(partie.grille)
    est_nul = utils.vérifie_si_nul(partie.grille, zobrist_grille, partie)
    joueur_actuel = partie.joueur1 if partie.tour_joueur == partie.joueur1.couleur else partie.joueur2
    if est_victoire:
        fenêtre.blit(arriere_plan, (0, 0))
        afficher_grille(fenêtre, couleur_joueur)
        afficher_pièces(fenêtre, partie.grille, couleur_joueur)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.mixer.music.load("assets/audio/game-end.mp3")
        pygame.mixer.music.play()
        texte_afficher = f"Victoire de {joueur_actuel.nom} !"
        if multi:
            if joueur_actuel.couleur == couleur_joueur:
                texte_afficher = "Victoire !"
            else:
                texte_afficher = "Défaite..."
        utils.afficher_texte(fenêtre, largeur_fenêtre // 2, hauteur_fenêtre // 2, texte_afficher, 60, utils.dict_couleurs["bleu marin"])
        pygame.display.flip()
        pygame.time.wait(3000)

        return False
    elif est_nul:
        fenêtre.blit(arriere_plan, (0, 0))
        afficher_grille(fenêtre, couleur_joueur)
        afficher_pièces(fenêtre, partie.grille, couleur_joueur)
        pygame.display.flip()
        pygame.time.wait(1000)
        pygame.mixer.music.load("assets/audio/game-end.mp3")
        pygame.mixer.music.play()
        utils.afficher_texte(fenêtre, largeur_fenêtre // 2, hauteur_fenêtre // 2, f"Match nul !", 60, utils.dict_couleurs["bleu marin"])
        pygame.display.flip()
        pygame.time.wait(3000)
        return False
    return True

def est_tour_bot(partie: Partie, couleur_joueur):
    return not partie.tour_joueur == couleur_joueur

def case_en_pixels(case):
    return case * taille_case + decalage


def main(profondeur=4):

    clock = pygame.time.Clock()
    fenêtre = pygame.display.set_mode((largeur_fenêtre, hauteur_fenêtre))
    pygame.display.set_caption("Partie d'Échecs")
    en_cours = True
    couleur_joueur = "blanc"
    partie = Partie()
    partie.grille_depuis_fen("basique")
    joueur1 = Joueur("Joueur 1", "blanc")
    if profondeur > 0:
        temp_de_pensée_max = 0.5 if profondeur >= 4 else 0
        joueur2 = negamax.Negamax("Robot", "noir", profondeur=profondeur, temps_max=temp_de_pensée_max)
        #joueur2 = bot.Bot("Robot", "noir")
    else:
        joueur2 = Joueur("Joueur 2", "noir")
    # joueur2 = Joueur("Joueur 2", "noir")
    partie.ajouter_joueur(joueur1)
    partie.ajouter_joueur(joueur2)
    negamax.init_transposition()
    pièce_sélectionnée: Roi = None
    cases_sélectionnées = []
    viens_de_jouer = False

    while en_cours:
        fenêtre.blit(arriere_plan, (0, 0))
        afficher_grille(fenêtre, couleur_joueur)
        afficher_pièces(fenêtre, partie.grille, couleur_joueur)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_pause.main():
                        return
                    else:
                        fenêtre = pygame.display.set_mode((largeur_fenêtre, hauteur_fenêtre))
            if event.type == pygame.MOUSEBUTTONDOWN:
                cases_sélectionnées.clear()
                case_actuelle = case_de_la_souris(couleur_joueur)
                if not case_actuelle:
                    continue
                pièce_actuelle = partie.grille[case_actuelle[1]][case_actuelle[0]]
                if pièce_sélectionnée:
                    if pièce_sélectionnée.couleur != partie.tour_joueur or (profondeur > 0 and pièce_sélectionnée.couleur != couleur_joueur):
                        print("Ce n'est pas votre pièce/tour, joueur", couleur_joueur)
                        continue

                    coup = (case_actuelle[0] - pièce_sélectionnée.x, case_actuelle[1] - pièce_sélectionnée.y)
                    coup_légaux_séléctionnés = pièce_sélectionnée.liste_coups_legaux(partie.grille)
                    if coup in coup_légaux_séléctionnés:
                        if partie.grille[case_actuelle[1]][case_actuelle[0]] or pièce_sélectionnée.type_de_pièce == "pion":
                            partie.tour_depuis_coup_intéressant = 0
                        pièce_sélectionnée.bouge(coup[0], coup[1], partie.grille)
                        viens_de_jouer = True
                        partie.compteur_de_tour += 1
                        partie.grilles.append(utils.copier_grille(partie.grille))
                        if len(partie.grilles) > 1 and utils.nombre_pièces_restantes(partie.grilles[-1]) < utils.nombre_pièces_restantes(partie.grilles[-2]):
                            pygame.mixer.music.load("assets/audio/capture.mp3")
                            pygame.mixer.music.play()
                        else:
                            pygame.mixer.music.load("assets/audio/move-self.mp3")
                            pygame.mixer.music.play()
                        grille_zobrist = negamax.zobrist_hash(partie.grille)
                        partie.répétitions.append(negamax.zobrist_hash(partie.grille))
                        en_cours = vérifie_fin_de_partie(partie, grille_zobrist, fenêtre, couleur_joueur)
                        if not en_cours:
                            return
                        partie.tour_joueur = utils.couleur_opposée(partie.tour_joueur)
                        pièce_sélectionnée = None
                        cases_sélectionnées = []


                    elif pièce_actuelle and pièce_actuelle.couleur == partie.tour_joueur:
                        cases_sélectionnées.clear()
                        pièce_sélectionnée = pièce_actuelle
                        coups_légaux_actuels = pièce_sélectionnée.liste_coups_legaux(partie.grille)
                        for coup_légal in coups_légaux_actuels:
                            cases_sélectionnées.append(
                                (pièce_sélectionnée.x + coup_légal[0], pièce_sélectionnée.y + coup_légal[1]))

                else:
                    if not (pièce_actuelle and pièce_actuelle.couleur == partie.tour_joueur):
                        continue
                    if profondeur > 0 and pièce_actuelle.couleur != couleur_joueur:
                        print("Ce n'est pas votre pièce/tour, joueur", couleur_joueur)
                        continue
                    pièce_sélectionnée = pièce_actuelle
                    coups_légaux_actuels = pièce_sélectionnée.liste_coups_legaux(partie.grille)
                    for coup_légal in coups_légaux_actuels:
                        cases_sélectionnées.append((pièce_sélectionnée.x + coup_légal[0], pièce_sélectionnée.y + coup_légal[1]))


        # draw a white circle is it's blanc's turn in top left corner, otherwise black circle
        pygame.draw.circle(fenêtre, utils.dict_couleurs[partie.tour_joueur], (largeur_fenêtre - decalage // 2, decalage // 2), 25)
        if pièce_sélectionnée and cases_sélectionnées:
            for case in cases_sélectionnées:
                fenêtre.blit(image_case_séléctionnée, (case[0] * taille_case + decalage, case[1] * taille_case + decalage))


        if en_cours: pygame.display.update()
        clock.tick(60)
        if est_tour_bot(partie, couleur_joueur) and profondeur > 0 and not viens_de_jouer:
            pygame.time.wait(500)
            utils.afficher_texte(fenêtre, largeur_fenêtre // 2, decalage // 2, f"{joueur2.nom} réfléchit...", 45, utils.dict_couleurs["bleu marin"])
            pygame.display.flip()
            pièce_choisie, coup_choisi = joueur2.trouver_coup(partie)
            pièce_choisie.bouge(coup_choisi[0], coup_choisi[1], partie.grille)
            partie.compteur_de_tour += 1
            partie.grilles.append(utils.copier_grille(partie.grille))
            if len(partie.grilles) > 1 and utils.nombre_pièces_restantes(
                    partie.grilles[-1]) < utils.nombre_pièces_restantes(partie.grilles[-2]):
                pygame.mixer.music.load("assets/audio/capture.mp3")
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.load("assets/audio/move-self.mp3")
                pygame.mixer.music.play()
            grille_zobrist = negamax.zobrist_hash(partie.grille)
            partie.répétitions.append(negamax.zobrist_hash(partie.grille))
            en_cours = vérifie_fin_de_partie(partie, grille_zobrist, fenêtre, couleur_joueur)
            if not en_cours:
                return
            partie.tour_joueur = utils.couleur_opposée(partie.tour_joueur)

        viens_de_jouer = False

def main_multi(profondeur=4):

    clock = pygame.time.Clock()
    fenêtre = pygame.display.set_mode((largeur_fenêtre, hauteur_fenêtre))
    pygame.display.set_caption("Partie d'Échecs")
    negamax.init_transposition()
    en_cours = True
    partie = Partie()
    partie.grille_depuis_fen("basique")
    port = utils.récupérer_port()
    local = utils.est_local()
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_serveur = utils.récupérer_ip_cible() if not local else "127.0.0.1"
    socket_client.connect((ip_serveur, port))

    socket_client.setblocking(False)
    nom_utilisateur = str(uuid.uuid4())
    socket_client.sendall(f"@connexion:{nom_utilisateur}".encode('utf-8'))
    print("Connexion établie")
    fenêtre.blit(arriere_plan, (0, 0))
    utils.afficher_texte(fenêtre, largeur_fenêtre // 2, hauteur_fenêtre // 2, "En attente d'un adversaire...", 60, utils.dict_couleurs["bleu marin"])
    pygame.display.flip()
    réponse = ""
    while not réponse.startswith("@commencer:"):
        try:
            réponse = socket_client.recv(2048).decode('utf-8')
        except BlockingIOError:
            pass
        clock.tick(60)
    print("Partie va commencer")
    couleur_joueur, nom_adversaire = réponse.split(":")[1].split("|")
    joueur1 = Joueur("Joueur 1", couleur_joueur)
    joueur2 = Joueur(nom_adversaire, utils.couleur_opposée(couleur_joueur))
    partie.ajouter_joueur(joueur1)
    partie.ajouter_joueur(joueur2)

    pièce_sélectionnée: Roi = None
    cases_sélectionnées = []

    while en_cours:
        fenêtre.blit(arriere_plan, (0, 0))
        afficher_grille(fenêtre, couleur_joueur)
        afficher_pièces(fenêtre, partie.grille, couleur_joueur)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if menu_pause.main():
                        return
                    else:
                        fenêtre = pygame.display.set_mode((largeur_fenêtre, hauteur_fenêtre))
            if event.type == pygame.MOUSEBUTTONDOWN:
                cases_sélectionnées.clear()
                case_actuelle = case_de_la_souris(couleur_joueur)
                if not case_actuelle:
                    continue
                pièce_actuelle = partie.grille[case_actuelle[1]][case_actuelle[0]]
                if pièce_sélectionnée:
                    if pièce_sélectionnée.couleur != partie.tour_joueur or (profondeur > 0 and pièce_sélectionnée.couleur != couleur_joueur):
                        print("Ce n'est pas votre pièce/tour, joueur", couleur_joueur)
                        continue

                    coup = (case_actuelle[0] - pièce_sélectionnée.x, case_actuelle[1] - pièce_sélectionnée.y)
                    coup_légaux_séléctionnés = pièce_sélectionnée.liste_coups_legaux(partie.grille)
                    if coup in coup_légaux_séléctionnés:
                        if partie.grille[case_actuelle[1]][case_actuelle[0]] or pièce_sélectionnée.type_de_pièce == "pion":
                            partie.tour_depuis_coup_intéressant = 0
                        socket_client.sendall(f"@jouer:{pièce_sélectionnée.x}|{pièce_sélectionnée.y}|{coup[0]}|{coup[1]}".encode('utf-8'))
                        pièce_sélectionnée.bouge(coup[0], coup[1], partie.grille)
                        partie.compteur_de_tour += 1
                        partie.grilles.append(utils.copier_grille(partie.grille))
                        if len(partie.grilles) > 1 and utils.nombre_pièces_restantes(partie.grilles[-1]) < utils.nombre_pièces_restantes(partie.grilles[-2]):
                            pygame.mixer.music.load("assets/audio/capture.mp3")
                            pygame.mixer.music.play()
                        else:
                            pygame.mixer.music.load("assets/audio/move-self.mp3")
                            pygame.mixer.music.play()
                        grille_zobrist = negamax.zobrist_hash(partie.grille)
                        partie.répétitions.append(negamax.zobrist_hash(partie.grille))
                        en_cours = vérifie_fin_de_partie(partie, grille_zobrist, fenêtre, couleur_joueur)
                        if not en_cours:
                            return
                        partie.tour_joueur = utils.couleur_opposée(partie.tour_joueur)
                        pièce_sélectionnée = None
                        cases_sélectionnées = []


                    elif pièce_actuelle and pièce_actuelle.couleur == partie.tour_joueur:
                        cases_sélectionnées.clear()
                        pièce_sélectionnée = pièce_actuelle
                        coups_légaux_actuels = pièce_sélectionnée.liste_coups_legaux(partie.grille)
                        for coup_légal in coups_légaux_actuels:
                            cases_sélectionnées.append(
                                (pièce_sélectionnée.x + coup_légal[0], pièce_sélectionnée.y + coup_légal[1]))

                else:
                    if not (pièce_actuelle and pièce_actuelle.couleur == partie.tour_joueur):
                        continue
                    if profondeur > 0 and pièce_actuelle.couleur != couleur_joueur:
                        print("Ce n'est pas votre pièce/tour, joueur", couleur_joueur)
                        continue
                    pièce_sélectionnée = pièce_actuelle
                    coups_légaux_actuels = pièce_sélectionnée.liste_coups_legaux(partie.grille)
                    for coup_légal in coups_légaux_actuels:
                        cases_sélectionnées.append((pièce_sélectionnée.x + coup_légal[0], pièce_sélectionnée.y + coup_légal[1]))


        # draw a white circle is it's blanc's turn in top left corner, otherwise black circle
        pygame.draw.circle(fenêtre, utils.dict_couleurs[partie.tour_joueur], (largeur_fenêtre - decalage // 2, decalage // 2), 25)
        if pièce_sélectionnée and cases_sélectionnées:
            for case in cases_sélectionnées:
                if couleur_joueur == "blanc":
                    fenêtre.blit(image_case_séléctionnée, (case[0] * taille_case + decalage, case[1] * taille_case + decalage))
                else:
                    fenêtre.blit(image_case_séléctionnée, (case[0] * taille_case + decalage, (7 - case[1]) * taille_case + decalage))


        if partie.tour_joueur == utils.couleur_opposée(couleur_joueur):
            try:
                réponse = socket_client.recv(2048).decode('utf-8')
                if réponse.startswith("@jouer:"):
                    pièce_x, pièce_y, coup_x, coup_y = réponse.split(":")[1].split("|")
                    pièce_choisie = partie.grille[int(pièce_y)][int(pièce_x)]
                    pièce_choisie.bouge(int(coup_x), int(coup_y), partie.grille)

                    partie.compteur_de_tour += 1
                    partie.grilles.append(utils.copier_grille(partie.grille))
                    if len(partie.grilles) > 1 and utils.nombre_pièces_restantes(
                            partie.grilles[-1]) < utils.nombre_pièces_restantes(partie.grilles[-2]):
                        pygame.mixer.music.load("assets/audio/capture.mp3")
                        pygame.mixer.music.play()
                    else:
                        pygame.mixer.music.load("assets/audio/move-self.mp3")
                        pygame.mixer.music.play()
                    grille_zobrist = negamax.zobrist_hash(partie.grille)
                    partie.répétitions.append(negamax.zobrist_hash(partie.grille))
                    en_cours = vérifie_fin_de_partie(partie, grille_zobrist, fenêtre, couleur_joueur)
                    if not en_cours:
                        return
                    partie.tour_joueur = utils.couleur_opposée(partie.tour_joueur)
            except BlockingIOError:
                pass

        if en_cours: pygame.display.update()
        clock.tick(60)
