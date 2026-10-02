import csv
from datetime import datetime

from observateurs.observateur import Observateur


class JournalCSV(Observateur):
    def __init__(self, chemin="portfolio.csv"):
        self.chemin = chemin

    def actualiser(self, sujet):
        donnees = sujet.get_donnees()
        titres = donnees["titres"]

        # Crée le fichier s'il n'existe pas
        fichier_existe = False
        try:
            with open(self.chemin, "r", encoding="utf-8"):
                fichier_existe = True
        except FileNotFoundError:
            fichier_existe = False

        with open(self.chemin, "a", newline="", encoding="utf-8") as fichier:
            writer = csv.writer(fichier)

            if not fichier_existe:
                writer.writerow([
                    "datetime",
                    "ticker",
                    "prix",
                    "ouverture",
                    "quantite",
                    "seuil_bas",
                    "seuil_haut"
                ])

            horodatage = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            for ticker, info in titres.items():
                writer.writerow([
                    horodatage,
                    ticker,
                    info["prix"],
                    info["ouverture"],
                    info["quantite"],
                    info["seuil_bas"],
                    info["seuil_haut"]
                ])

