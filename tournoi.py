import time
import concurrent.futures

import utils
from moteur.partie import Partie
from bots import bot, random_bot, negamax, negamax2


def une_partie(i):
    bot1 = negamax.Negamax("Joueur 1", "blanc", profondeur=4, temps_max=0.01)
    bot2 = negamax2.Negamax("Joueur 2", "noir", profondeur=4, temps_max=0.01)
    partie = Partie()
    partie.grille_depuis_fen("basique")
    partie.ajouter_joueur(bot1)
    partie.ajouter_joueur(bot2)
    couleurs = ["blanc", "noir"]
    partie.tour_joueur = couleurs[i % 2]

    while True:
        if partie.tour_joueur == "blanc":
            pièce, coup = bot1.trouver_coup(partie)
        else:
            pièce, coup = bot2.trouver_coup(partie)
        pièce.bouge(coup[0], coup[1], partie.grille)
        grille_zobrist = negamax.zobrist_hash(partie.grille)
        est_victoire = utils.vérifie_si_victoire(partie.grille)
        est_nul = utils.vérifie_si_nul(partie.grille, grille_zobrist, partie)
        if est_victoire:
            return "bot1" if partie.tour_joueur == bot1.couleur else "bot2"
        if est_nul:
            return "nul"
        partie.tour_joueur = "noir" if partie.tour_joueur == "blanc" else "blanc"
        partie.compteur_de_tour += 1
        print(partie.compteur_de_tour)


def tournoi(parties: int, max_workers=None):
    resultats = {"bot1": 0, "bot2": 0, "nul": 0}
    for i in range(parties):
        resultats[une_partie(i)] += 1
        if i % 50 == 0:
            print(f"Completed game {i}/{parties}")

    return resultats


if __name__ == '__main__':
    negamax.init_transposition()
    negamax2.init_transposition()
    start_time = time.time()
    resultats = tournoi(1)
    print(resultats, "in", time.time() - start_time, "seconds")
