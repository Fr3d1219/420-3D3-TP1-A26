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
            variation = (prix - ouverture) / ouverture * 100
            texte = f"{ticker}: {prix:.2f} $ ({variation:.2f}%)"
            self.labels[ticker].config(text=texte)


