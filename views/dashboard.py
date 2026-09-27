import tkinter as tk
from modeles.prix import Prix
from observateurs.affichageprix import AffichagePrix
from observateurs.alertes import Alertes
from observateurs.portfolio import Portfolio
from observateurs.journalcsv import JournalCSV

class Dashboard(tk.Tk):

    INTERVALLE_MS = 3000

    def __init__(self, prix: Prix):
        super().__init__()
        self.title("Portfolio Tracker")
        self._prix = prix

    def _creer_observateurs(self) -> None:
        self._affichage_prix = AffichagePrix(self)
        self._alertes = Alertes(self)
        self._portfolio = Portfolio(self)
        self._journalcsv = JournalCSV(self)

    def _abonner_observateurs(self) -> None:
        self._prix.abonner(self._affichage_prix)
        self._prix.abonner(self._alertes)
        self._prix.abonner(self._portfolio)
        self._prix.abonner(self._journalcsv)


    def _creer_boutons(self) -> None:
        #Il faut faire les boutons de l'interface dans cette section (voir app.py)
        pass

    
