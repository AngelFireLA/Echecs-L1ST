import random
import time

from .. import utils
from .bot import Bot
from ..utils import liste_coups_légaux, copier_grille, vérifie_si_nul, vérifie_si_victoire, montrer_grille

zobrist = []
pièce_type_mapping = {"roi": 0, "dame": 1, "tour": 2, "fou": 3, "cavalier": 4, "pion": 5}
pièce_color_mapping = {"blanc": 0, "noir": 1}

table_cavalier_blanc = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

table_fou_blanc = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

table_tour_blanc = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [5, 10, 10, 10, 10, 10, 10, 5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [-5, 0, 0, 0, 0, 0, 0, -5],
    [0, 0, 0, 5, 5, 0, 0, 0]
]

table_dame_blanc = [
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 5, 5, 5, 0, -10],
    [-5, 0, 5, 5, 5, 5, 0, -5],
    [0, 0, 5, 5, 5, 5, 0, -5],
    [-10, 5, 5, 5, 5, 5, 0, -10],
    [-10, 0, 5, 0, 0, 0, 0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
]

table_pion_blanc = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0]
]

table_roi_blanc = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]


#Inverse les tables pour les noirs
table_cavalier_noir = [row[::-1] for row in table_cavalier_blanc[::-1]]
table_fou_noir = [row[::-1] for row in table_fou_blanc[::-1]]
table_tour_noir = [row[::-1] for row in table_tour_blanc[::-1]]
table_dame_noir = [row[::-1] for row in table_dame_blanc[::-1]]
table_roi_noir = [row[::-1] for row in table_roi_blanc[::-1]]
table_pion_noir = [row[::-1] for row in table_pion_blanc[::-1]]

tables_positions_optimales_pièces = {
    "blanc": {
        "cavalier": table_cavalier_blanc,
        "fou": table_fou_blanc,
        "tour": table_tour_blanc,
        "dame": table_dame_blanc,
        "roi": table_roi_blanc,
        "pion": table_pion_blanc
    },
    "noir": {
        "cavalier": table_cavalier_noir,
        "fou": table_fou_noir,
        "tour": table_tour_noir,
        "dame": table_dame_noir,
        "roi": table_roi_noir,
        "pion": table_pion_noir
    }
}


def init_transposition():
    global zobrist
    for _ in range(64):
        case = []
        for _ in range(12):
            pièce = []
            for _ in range(2):
                pièce.append(random.getrandbits(64))
            case.append(pièce)
        zobrist.append(case)



def zobrist_hash(board):
    valeur_hash = 0
    for ligne in range(8):
        for colonne in range(8):
            pièce = board[ligne][colonne]
            if pièce:
                square_index = ligne * 8 + colonne
                valeur_hash ^= zobrist[square_index][pièce_type_mapping[pièce.type_de_pièce]][pièce_color_mapping[pièce.couleur]]

    return valeur_hash



class Negamax(Bot):
    def __init__(self, nom, couleur, profondeur=4, temps_max=0):
        super().__init__(nom, couleur)
        self.profondeur = profondeur
        self.coups = 0
        self.temps_de_pensée_max = temps_max
        self.table_de_transposition = {}




    def trouver_coup(self, partie) -> int:

        start_time = time.time()
        # self.table_de_transposition = {}
        meilleur_score = -float('inf')
        profondeur_originale = self.profondeur
        if self.temps_de_pensée_max == 0:
            self.coups = 0
            meilleur_score = -float('inf')
            meilleur_coups = []
            coups_légaux = liste_coups_légaux(self.couleur, partie.grille)
            for combo in coups_légaux:
                pièce, coup = combo
                copie_pièce = pièce.copy()
                copie_grille = copie_pièce.bouge(coup[0], coup[1], copier_grille(partie.grille))
                score = -self.negamax(copie_grille, self.profondeur - 1, utils.couleur_opposée(partie.tour_joueur), -float('inf'), float('inf'), partie)
                #print("Score:", score, "Combo:", combo)
                if score > meilleur_score:
                    meilleur_score = score
                    meilleur_coups = [combo]
                elif score == meilleur_score:
                    meilleur_coups.append(combo)
                if meilleur_score > 20000:
                    break
        else:
            self.profondeur -= 1
            while time.time() - start_time <= self.temps_de_pensée_max and meilleur_score < 20000:
                self.profondeur += 1
                print("atteint profondeur", self.profondeur)
                # self.table_de_transposition = {}
                self.coups = 0
                meilleur_score = -float('inf')
                meilleur_coups = []
                coups_légaux = liste_coups_légaux(self.couleur, partie.grille)
                for combo in coups_légaux:
                    pièce, coup = combo
                    copie_pièce = pièce.copy()
                    copie_grille = copie_pièce.bouge(coup[0], coup[1], copier_grille(partie.grille))
                    score = -self.negamax(copie_grille, self.profondeur-1, utils.couleur_opposée(partie.tour_joueur), -float('inf'), float('inf'), partie)
                    if score > meilleur_score:
                        meilleur_score = score
                        meilleur_coups = [combo]
                    elif score == meilleur_score:
                        meilleur_coups.append(combo)
                if meilleur_score > 20000:
                    break
        print("Coups:", self.coups, "Meilleur score:", meilleur_score)
        self.profondeur = profondeur_originale
        return random.choice(meilleur_coups)

    def évaluer_plateau(self, grille, couleur):
        score_blanc, score_noir = utils.points_avec_roi(grille)

        for pièce in utils.liste_pièces_restantes(grille):
            if pièce.couleur == "blanc":
                score_blanc += (tables_positions_optimales_pièces["blanc"][pièce.type_de_pièce][pièce.y][pièce.x])
            else:
                score_noir += (tables_positions_optimales_pièces["noir"][pièce.type_de_pièce][pièce.y][pièce.x])
        if couleur == "blanc":
            score = score_blanc - score_noir
        else:
            score = score_noir - score_blanc

        return score

    def negamax(self, grille, profondeur, couleur, alpha, beta, partie):
        self.coups += 1
        clé_hash = zobrist_hash(grille)
        entrée_transposition = self.récupérer_entrée(clé_hash, partie.compteur_de_tour + profondeur, couleur)
        if entrée_transposition is not None:
            return entrée_transposition

        if vérifie_si_nul(grille, clé_hash):
            return 0

        if profondeur == 0 or vérifie_si_victoire(grille):
            return self.évaluer_plateau(grille, couleur)

        meilleur_score = -float('inf')
        coups_triés = self.trier_coups(grille, couleur)
        for pièce, coup in coups_triés:
            copie_pièce = pièce.copy()
            copie_grille = copie_pièce.bouge(coup[0], coup[1], copier_grille(grille))
            # if profondeur == 2:
            #     montrer_grille(copie_grille)
            score = -self.negamax(copie_grille, profondeur - 1, utils.couleur_opposée(couleur), -beta, -alpha, partie)
            meilleur_score = max(meilleur_score, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break
        self.stocker_entrée(clé_hash, meilleur_score, partie.compteur_de_tour + profondeur, couleur)
        return meilleur_score


    def trier_coups(self, grille, couleur):
        coups_légaux = utils.liste_coups_légaux(couleur, grille)
        coups_captures = utils.captures_possibles(coups_légaux, grille)
        coups_légaux = [coup for coup in coups_légaux if coup not in coups_captures]
        coups_triés = []
        #order moves based on which capture move has the biggest difference in points positive for us
        for (pièce, coup) in coups_captures:
            nouvelle_case = grille[pièce.y + coup[1]][pièce.x + coup[0]]
            différence_points = nouvelle_case.valeur - pièce.valeur
            coups_triés.append((pièce, coup, différence_points))
        coups_triés.sort(key=lambda x: x[2], reverse=True)
        coups_triés = [(pièce, coup) for pièce, coup, _ in coups_triés] + coups_légaux
        return coups_triés



    def récupérer_entrée(self, valeur_hash, profondeur, couleur):
        if valeur_hash in self.table_de_transposition:
            entry = self.table_de_transposition[valeur_hash]
            if entry and entry.get('profondeur', 0) >= profondeur and entry.get('couleur') == couleur:
                return entry.get('score')
        return None

    def stocker_entrée(self, valeur_hash, score, profondeur, couleur):
        self.table_de_transposition[valeur_hash] = {'score': score, 'profondeur': profondeur, 'couleur': couleur}