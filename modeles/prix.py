import yfinance as yf
from modeles.sujet import Sujet

class Prix(Sujet):
    def __init__(self):
        super().__init__()
        self._prix_actuels = {
            "AAPL": {"quantite": 10, "seuil_bas": 150.0, "seuil_haut": 200.0, "prix": 0.0, "ouverture": 0.0},
            "GOOGL": {"quantite": 5, "seuil_bas": 120.0, "seuil_haut": 160.0, "prix": 0.0, "ouverture": 0.0},
            "MSFT": {"quantite": 8, "seuil_bas": 380.0, "seuil_haut": 430.0, "prix": 0.0, "ouverture": 0.0},
        }

    def recuperer_prix(self, ticker):
        info = yf.Ticker(ticker).fast_info
        prix = info["last_price"]
        ouverture = info["open"]
        return prix, ouverture

    def rafraichir(self):
        for ticker in self._prix_actuels:
            prix, ouverture = self.recuperer_prix(ticker)
            self._prix_actuels[ticker]["prix"] = prix
            self._prix_actuels[ticker]["ouverture"] = ouverture

        self.notifier()

    def ajouter_titre(self, ticker, quantite, seuil_bas=None, seuil_haut=None):
        if ticker in self._prix_actuels:
            return

        prix, ouverture = self.recuperer_prix(ticker)

        if seuil_bas is None:
            seuil_bas = prix * 0.8
        if seuil_haut is None:
            seuil_haut = prix * 1.2

        self._prix_actuels[ticker] = {
            "quantite": quantite,
            "seuil_bas": seuil_bas,
            "seuil_haut": seuil_haut,
            "prix": prix,
            "ouverture": ouverture
        }

        self.notifier()

    def modifier_titre(self, ticker, quantite=None, seuil_bas=None, seuil_haut=None):
        if ticker not in self._prix_actuels:
            return

        if quantite is not None:
            self._prix_actuels[ticker]["quantite"] = quantite
        if seuil_bas is not None:
            self._prix_actuels[ticker]["seuil_bas"] = seuil_bas
        if seuil_haut is not None:
            self._prix_actuels[ticker]["seuil_haut"] = seuil_haut

        self.notifier()

    def retirer_titre(self, ticker):
        if ticker in self._prix_actuels:
            del self._prix_actuels[ticker]
            self.notifier()

    def get_donnees(self) -> dict:
        return {"titres": self._prix_actuels}