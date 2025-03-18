from ..pièce import Pièce


class Dame(Pièce):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "dame", x, y, 900)

    def copy(self):
        nouvelle_pièce = Dame(self.couleur,  self.x, self.y)
        return nouvelle_pièce
    def get_patterne_possible(self):
        patterne_diagonale = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        patterne_tour = [(+1, +0), (-1, +0), (+0, +1), (+0, -1)]
        for i in range(len(patterne_diagonale) - 1, -1, -1):
            if self.x + patterne_diagonale[i][0] < 0 or self.x + patterne_diagonale[i][0] > 7 or self.y + \
                    patterne_diagonale[i][1] < 0 or self.y + patterne_diagonale[i][1] > 7:
                patterne_diagonale.pop(i)
        for i in range(len(patterne_tour) - 1, -1, -1):
            if self.x + patterne_tour[i][0] < 0 or self.x + patterne_tour[i][0] > 7 or self.y + patterne_tour[i][1] < 0 or self.y + patterne_tour[i][1] > 7:
                patterne_tour.pop(i)
        return patterne_diagonale, patterne_tour

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible()
        nouveau_patterne = []
        for coup in patterne[0]:
            x = coup[0]
            y = coup[1]
            while True:
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
                if not grille[self.y+y][self.x+x]:
                    nouveau_patterne.append((x, y))
                else:
                    if grille[self.y+y][self.x+x].couleur != self.couleur:
                        nouveau_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
                        nouveau_patterne.append((x, y))
                        break
                    else:
                        break
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
        for coup in patterne[1]:
            x = coup[0]
            y = coup[1]
            if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                break

            while True:
                if not grille[self.y+y][self.x+x]:
                    nouveau_patterne.append((x, y))
                else:
                    if grille[self.y+y][self.x+x].couleur != self.couleur:
                        nouveau_patterne.append((x, y))
                        break
                    elif peut_capturer_allie:
                        nouveau_patterne.append((x, y))
                        break
                    else:
                        break
                if x > 0:
                    x += 1
                if x < 0:
                    x -= 1
                if y > 0:
                    y += 1
                if y < 0:
                    y -= 1
                if x + self.x > 7 or x + self.x < 0 or y + self.y > 7 or y + self.y < 0:
                    break
        return list(set(nouveau_patterne))

    def bouge(self, x_ajouté, y_ajouté, grille: list):
        if (x_ajouté, y_ajouté) in self.liste_coups_legaux(grille):
            self.a_bougé = True
            grille[self.y][self.x] = None
            self.x += x_ajouté
            self.y += y_ajouté
            grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(f"Le coup({x_ajouté}, {y_ajouté}) n'est pas valide pour la pièce {self.type_de_pièce} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")
