from observateurs.observateur import Observateur

class Portfolio(Observateur):
    def __init__(self, label_valeur, label_variation):
        self.label_valeur = label_valeur
        self.label_variation = label_variation

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        titres = donnees["titres"]
        valeur = 0
        valeur_ouverture = 0
        for ticker, info in titres.items():
            valeur += info["prix"] * info["quantite"]
            valeur_ouverture += info["ouverture"] * info["quantite"]
        self.label_valeur.config(text=f"Valeur totale : {valeur:.2f} $")
        variation = valeur - valeur_ouverture
        symbole = "▲" if variation >= 0 else "▼"
        self.label_variation.config(
            text=f"{symbole} {abs(variation):.2f} $ depuis l'ouverture",
            fg="green" if variation >= 0 else "red",
        )

    