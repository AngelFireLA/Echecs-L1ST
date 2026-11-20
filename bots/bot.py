from moteur.joueur import Joueur
from utils import liste_coups_légaux


class Bot(Joueur):
    def __init__(self, nom, couleur):
        super().__init__(nom, couleur)

    def trouver_coup(self, partie) -> int:
        grille = partie.grille
        coups = liste_coups_légaux(self.couleur, grille)
        return coups[0]