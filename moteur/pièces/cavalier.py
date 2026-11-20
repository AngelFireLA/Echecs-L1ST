from moteur.pièce import Pièce


class Cavalier(Pièce):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "cavalier", x, y, 300)

    def copy(self):
        nouvelle_pièce = Cavalier(self.couleur, self.x, self.y)
        return nouvelle_pièce

    def get_patterne_possible(self):
        patterne = [(+2, +1), (+2, -1), (-2, +1), (-2, -1), (+1, +2), (+1, -2), (-1, +2), (-1, -2)]
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + \
                    patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        coups = self.get_patterne_possible()
        move_illegaux = []
        for coup in coups:
            if grille[self.y+coup[1]][self.x+coup[0]]:
                if grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur and not peut_capturer_allie:
                    move_illegaux.append(coup)
        for move in move_illegaux:
            coups.remove(move)
        return coups

    def bouge(self, x_ajouté, y_ajouté, grille: list):
        if (x_ajouté, y_ajouté) in self.liste_coups_legaux(grille):
            self.a_bougé = True
            if grille[self.y + y_ajouté][self.x + x_ajouté]:
                if grille[self.y + y_ajouté][self.x + x_ajouté].couleur == self.couleur:
                    raise ValueError(f"Le coup({x_ajouté}, {y_ajouté}) n'est pas valide pour la piéce {self.type_de_pièce} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")

            grille[self.y][self.x] = None
            self.x += x_ajouté
            self.y += y_ajouté
            grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(f"Le coup({x_ajouté}, {y_ajouté}) n'est pas valide pour la pièce {self.type_de_pièce} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")
