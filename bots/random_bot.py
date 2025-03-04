import random

from bots.bot import Bot
from utils import liste_coups_légaux


class RandomBot(Bot):
    def __init__(self, nom, couleur):
        super().__init__(nom, couleur)

    def trouver_coup(self, partie) -> int:
        grille = partie.grille
        coups = liste_coups_légaux(self.couleur, grille)
        return random.choice(coups)