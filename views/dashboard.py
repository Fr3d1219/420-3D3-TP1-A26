import tkinter as tk
from datetime import datetime

from modeles.prix import Prix
from observateurs.affichageprix import AffichagePrix
from observateurs.alertes import Alertes
from observateurs.portfolio import Portfolio
from observateurs.journalcsv import JournalCSV
from views.gestion_titres import GestionTitres

class Dashboard(tk.Tk):
    INTERVALLE_MS = 30000
    POLICE = ("Segoe UI", 10)
    POLICE_TITRE = ("Segoe UI", 16, "bold")
    POLICE_VALEUR = ("Segoe UI", 13, "bold")

    def __init__(self, prix: Prix):
        super().__init__()
        self.title("Portfolio Tracker")
        self.resizable(False, False)
        self.option_add("*Font", self.POLICE)
        self._prix = prix
        self.labels_prix = {}
        self.frames_prix = {}

        tk.Label(self, text="Portfolio Tracker", font=self.POLICE_TITRE).pack(pady=10)
        self.frame_prix = tk.LabelFrame(self, text="Prix en temps réel", padx=10, pady=10)
        self.frame_prix.pack(fill=tk.X, padx=10, pady=5)
        for ticker in self._titres():
            self._creer_ligne_prix(ticker)

        self.gestion_titres = GestionTitres(
            self, self._prix, self._titre_ajoute, self._titre_retire
        )
        self.gestion_titres.pack(fill=tk.X, padx=10, pady=5)

        frame_portfolio = tk.LabelFrame(self, text="Mon portfolio", padx=10, pady=10)
        frame_portfolio.pack(fill=tk.X, padx=10, pady=5)
        self.label_valeur = tk.Label(
            frame_portfolio, text="Valeur totale : calcul en cours...", font=self.POLICE_VALEUR
        )
        self.label_valeur.pack()
        self.label_variation = tk.Label(frame_portfolio, text="")
        self.label_variation.pack()

        frame_alertes = tk.LabelFrame(self, text="Alertes", padx=10, pady=10)
        frame_alertes.pack(fill=tk.X, padx=10, pady=5)
        self.label_alertes = tk.Label(
            frame_alertes, text="Aucune alerte", fg="gray", justify=tk.LEFT, wraplength=380
        )
        self.label_alertes.pack(anchor="w")

        self.label_maj = tk.Label(self, text="", font=("Segoe UI", 9), fg="gray")
        self.label_maj.pack(pady=5)

        self._creer_observateurs()
        self._abonner_observateurs()
        self.after(0, self.rafraichir)

    def _titres(self):
        return self._prix.get_donnees()["titres"]

    def _creer_observateurs(self) -> None:
        self._affichage_prix = AffichagePrix(self)
        self._affichage_prix.labels = self.labels_prix
        self._alertes = Alertes(self.label_alertes)
        self._portfolio = Portfolio(self.label_valeur, self.label_variation)
        self._journalcsv = JournalCSV()

    def _abonner_observateurs(self) -> None:
        self._prix.abonner(self._affichage_prix)
        self._prix.abonner(self._alertes)
        self._prix.abonner(self._portfolio)
        self._prix.abonner(self._journalcsv)

    def _creer_ligne_prix(self, ticker):
        frame = tk.Frame(self.frame_prix)
        frame.pack(fill=tk.X, pady=2)
        tk.Label(frame, text=f"{ticker}:", width=8, font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT)
        label = tk.Label(frame, text="Chargement...")
        label.pack(side=tk.LEFT)
        self.labels_prix[ticker] = label
        self.frames_prix[ticker] = frame

    def _titre_ajoute(self, ticker):
        self._creer_ligne_prix(ticker)
        self._affichage_prix.actualiser(self._prix)

    def _titre_retire(self, ticker):
        self.labels_prix.pop(ticker, None)
        self.frames_prix.pop(ticker).destroy()

    def rafraichir(self):
        try:
            self._prix.rafraichir()
            horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.label_maj.config(text=f"Dernière mise à jour : {horodatage}", fg="gray")
        except Exception as erreur:
            self.label_maj.config(text=f"Erreur : {erreur}", fg="red")
        self.after(self.INTERVALLE_MS, self.rafraichir)
    
