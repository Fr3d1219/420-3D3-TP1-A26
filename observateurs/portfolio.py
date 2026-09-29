from observateurs.observateur import Observateur

class Portfolio(Observateur):
    def __init__(self, label_valeur, label_variation):
        self.label_valeur = label_valeur
        self.label_variation = label_variation

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        titres = donnees["titres"]
        valeur = 0
        for ticker, info in titres.items():
            valeur += info["prix"] * info["quantite"]
        self.label_valeur.config(text=f"Valeur totale : {valeur:.2f} $")

    