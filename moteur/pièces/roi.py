from moteur.pièce import Pièce


class Roi(Pièce):
    def __init__(self, couleur: str, x: int = 0, y: int = 0):
        super().__init__(couleur, "roi", x, y, 30000)

    def copy(self):
        pièce_copiée = Roi(self.couleur,  self.x, self.y)
        pièce_copiée.a_bougé = self.a_bougé
        return pièce_copiée

    def get_patterne_possible(self):
        patterne = [(2, 0), (-2, 0), (+1, +0), (+1, +1), (+0, +1), (-1, +1), (-1, +0), (-1, -1), (+0, -1), (+1, -1)]
        for i in range(len(patterne) - 1, -1, -1):
            if self.x + patterne[i][0] < 0 or self.x + patterne[i][0] > 7 or self.y + patterne[i][1] < 0 or self.y + patterne[i][1] > 7:
                patterne.pop(i)
        return patterne

    def liste_coups_legaux(self, grille: list, peut_capturer_allie=False):
        patterne = self.get_patterne_possible()
        coup_legaux = []

        for coup in patterne:
            if coup == (2, 0):
                if self.x + 3 <= 7 and not self.a_bougé:
                    if grille[self.y][self.x + 3]:
                        piece = grille[self.y][self.x + 3]
                        if piece.type_de_pièce == "tour" and piece.couleur == self.couleur and not piece.a_bougé:
                            if not grille[self.y][self.x + 2] and not grille[self.y][self.x + 1]:
                                coup_legaux.append(coup)
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            elif coup == (-2, 0):
                if self.x - 4 >= 0 and not self.a_bougé:
                    if grille[self.y][self.x - 4]:
                        piece = grille[self.y][self.x - 4]
                        if piece.type_de_pièce == "tour" and piece.couleur == self.couleur and not piece.a_bougé:
                            if not grille[self.y][self.x - 3] and not grille[self.y][self.x - 2] and not grille[self.y][self.x - 1]:
                                coup_legaux.append(coup)
                            else:
                                continue
                        else:
                            continue
                    else:
                        continue
                else:
                    continue

            if grille[self.y + coup[1]][self.x + coup[0]]:
                if peut_capturer_allie and grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur:
                    coup_legaux.append(coup)
                elif not grille[self.y + coup[1]][self.x + coup[0]].couleur == self.couleur:
                    coup_legaux.append(coup)
            else:
                coup_legaux.append(coup)

        return coup_legaux

    def bouge(self, x_ajouté, y_ajouté, grille: list):
        if (x_ajouté, y_ajouté) in self.liste_coups_legaux(grille):
            self.a_bougé = True
            if (x_ajouté, y_ajouté) == (2, 0):
                tour = grille[self.y + y_ajouté][self.x + x_ajouté+1]
                grille = tour.bouge(-2, 0, grille, True)
                grille[self.y][self.x] = None
                self.x += x_ajouté
                self.y += y_ajouté
                grille[self.y][self.x] = self
                return grille
            if (x_ajouté, y_ajouté) == (-2, 0):
                tour = grille[self.y + y_ajouté][self.x + x_ajouté - 2]
                grille = tour.bouge(3, 0, grille, True)
                grille[self.y][self.x] = None
                self.x += x_ajouté
                self.y += y_ajouté
                grille[self.y][self.x] = self
                return grille
            else:
                grille[self.y][self.x] = None
                self.x += x_ajouté
                self.y += y_ajouté
                grille[self.y][self.x] = self
            return grille
        else:
            raise ValueError(f"Le coup({x_ajouté}, {y_ajouté}) n'est pas valide pour la pièce {self.type_de_pièce} de couleur {self.couleur} au coordonnées {(self.x, self.y)}.")
