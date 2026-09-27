from observateurs.observateur import Observateur

class Alertes(Observateur):
    def __init__(self, label_alertes):
        self.label_alertes = label_alertes

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        messages = []
        for ticker, info in donnees["titres"].items():
            if info["prix"] >= info["seuil_haut"]:
                messages.append(f"{ticker} : seuil haut atteint")
        self.label_alertes.config(text="\n".join(messages) if messages else "Aucune alerte")