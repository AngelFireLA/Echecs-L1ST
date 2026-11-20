from moteur.pièce import Pièce
from moteur.pièces.dame import Dame


class Pion(Pièce):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "pion", x, y, 100)

    def copy(self):
        pièce_copiée = Pion(self.couleur, self.x, self.y)
        return pièce_copiée

    def get_patterne_possible(self, grille: list):
        if self.couleur == "blanc":
            patterne = []
            if not grille[self.y - 1][self.x]:
                patterne.append((0, -1))
            if self.y == 6 and not grille[4][self.x] and not grille[5][self.x]:
                patterne.append((0, -2))
            return patterne
        else:
            patterne = []
            if not grille[self.y + 1][self.x]:
                patterne.append((0, +1))
            if self.y == 1 and not grille[3][self.x] and not grille[2][self.x]:
                patterne.append((0, +2))
            return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible(grille)
        if self.couleur == "blanc":
            if self.y - 1 >= 0 and self.x - 1 >= 0:
                if grille[self.y - 1][self.x - 1]:
                    if not grille[self.y - 1][self.x - 1].couleur == self.couleur:
                        patterne.append((-1, -1))
                    elif peut_capturer_allie:
                        patterne.append((-1, -1))
            if self.y - 1 >= 0 and self.x + 1 <= 7:
                if grille[self.y - 1][self.x + 1]:
                    if not grille[self.y - 1][self.x + 1].couleur == self.couleur:
                        patterne.append((1, -1))
                    elif peut_capturer_allie:
                        patterne.append((1, -1))
        else:
            if self.x - 1 >= 0 and self.y + 1 <= 7:
                if grille[self.y + 1][self.x - 1]:
                    if not grille[self.y + 1][self.x - 1].couleur == self.couleur:
                        patterne.append((-1, +1))
                    elif peut_capturer_allie:
                        patterne.append((-1, +1))
            if self.y + 1 <= 7 and self.x + 1 <= 7:
                if grille[self.y + 1][self.x + 1]:
                    if not grille[self.y + 1][self.x + 1].couleur == self.couleur:
                        patterne.append((1, +1))
                    elif peut_capturer_allie:
                        patterne.append((1, +1))
        return patterne

    def bouge(self, x_ajouté, y_ajouté, grille: list):
        if (x_ajouté, y_ajouté) in self.liste_coups_legaux(grille):
            self.a_bougé = True
            grille[self.y][self.x] = None
            self.x += x_ajouté
            self.y += y_ajouté
            grille[self.y][self.x] = self
            if (self.couleur == "blanc" and self.y == 0) or (self.couleur == "noir" and self.y == 7):
                nouvelle_pièce = Dame(self.couleur)
                return self.promotion(grille, nouvelle_pièce)
            else:
                return grille
        else:
            raise ValueError(
                f"Le coup({x_ajouté}, {y_ajouté}) n'est pas valide pour la pièce {self.type_de_pièce} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")

    def promotion(self, grille, nouvelle_pièce):
        grille[self.y][self.x] = nouvelle_pièce
        nouvelle_pièce.x = self.x
        nouvelle_pièce.y = self.y
        nouvelle_pièce.a_bougé = True
        return grille
