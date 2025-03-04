class Pièce:
    types_de_pièces = ["roi", "dame", "tour", "fou", "cavalier", "pion"]
    def __init__(self, couleur, type_de_pièce, x, y, valeur: int):
        self.couleur = couleur
        self.x, self.y = x, y
        self.type_de_pièce = type_de_pièce
        self.a_bougé = False
        self.valeur = valeur

    def __repr__(self):
        return f"{self.type_de_pièce} {self.couleur} en ({self.x}, {self.y})"
