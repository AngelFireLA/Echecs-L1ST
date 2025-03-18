#from app_interface import chess_game
from .. import utils
#import moteur.endgame_and_opening_move_finder as endgame_and_opening_move_finder
#from app_interface import chess_game
from .pièces.roi import Roi
from .pièces.dame import Dame
from .pièces.tour import Tour
from .pièces.fou import Fou
from .pièces.cavalier import Cavalier
from .pièces.pion import Pion
import time
from ..bots import negamax


def pièce_depuis_symbole(symbol: str):
    symbol_piece_dict = {
        'K': (Roi, "blanc"), 'Q': (Dame, "blanc"), 'R': (Tour, "blanc"), 'B': (Fou, "blanc"),
        'N': (Cavalier, "blanc"), 'P': (Pion, "blanc"),
        'k': (Roi, "noir"), 'q': (Dame, "noir"), 'r': (Tour, "noir"), 'b': (Fou, "noir"),
        'n': (Cavalier, "noir"), 'p': (Pion, "noir")
    }
    return symbol_piece_dict[symbol]


class Partie:
    def __init__(self):
        self.terminee = False
        self.tour_joueur = "blanc"
        self.grille = None
        self.compteur_de_tour = 0
        self.répétitions = []
        self.grilles = []
        self.tour_depuis_coup_intéressant = 0
        self.joueur1 = None
        self.joueur2 = None

    def grille_depuis_fen(self, notation_fen: str):
        if notation_fen == "basique":
            notation_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"

        grille = []
        lignes_fen = notation_fen.split('/')

        for i, ligne_fen in enumerate(lignes_fen):
            ligne = []
            index_colonne = 0
            for symbole in ligne_fen:
                if symbole.isdigit():
                    cases_vides = int(symbole)
                    for _ in range(cases_vides):
                        ligne.append(None)
                    index_colonne += cases_vides
                else:
                    pièce, couleur = pièce_depuis_symbole(symbole)
                    piece = pièce(x=index_colonne, y=i, couleur=couleur)
                    ligne.append(piece)
                    index_colonne += 1
            grille.append(ligne)
        self.grille = grille

    def ajouter_joueur(self, joueur):
        if not self.joueur1:
            self.joueur1 = joueur
        elif not self.joueur2:
            self.joueur2 = joueur
        else:
            raise ValueError("La partie est déjà pleine")
