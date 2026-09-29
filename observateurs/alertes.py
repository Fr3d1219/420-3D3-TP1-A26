from observateurs.observateur import Observateur

class Alertes(Observateur):
    def __init__(self, label_alertes):
        self.label_alertes = label_alertes

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        messages = []
        for ticker, info in donnees["titres"].items():
            if info["prix"] >= info["seuil_haut"]:
                messages.append(
                    f"⚠️ {ticker} dépasse le seuil haut ({info['prix']:.2f} $ ≥ {info['seuil_haut']:.2f} $)"
                )
            elif info["prix"] <= info["seuil_bas"]:
                messages.append(
                    f"⚠️ {ticker} sous le seuil bas ({info['prix']:.2f} $ ≤ {info['seuil_bas']:.2f} $)"
                )
        self.label_alertes.config(
            text="\n".join(messages) if messages else "Aucune alerte",
            fg="red" if messages else "gray",
        )