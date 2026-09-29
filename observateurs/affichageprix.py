from observateurs.observateur import Observateur
import tkinter as tk

class AffichagePrix(Observateur):
    def __init__(self, parent):
        self.parent = parent
        self.labels = {}

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        for ticker, info in donnees["titres"].items():
            prix = info["prix"]
            ouverture = info["ouverture"]
            label = self.labels.get(ticker)
            if label is None:
                continue
            variation = (prix - ouverture) / ouverture * 100 if ouverture else 0
            symbole = "▲" if variation >= 0 else "▼"
            couleur = "green" if variation >= 0 else "red"
            label.config(text=f"{prix:.2f} $  {symbole} {abs(variation):.2f}%", fg=couleur)


