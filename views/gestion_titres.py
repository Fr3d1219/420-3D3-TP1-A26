import tkinter as tk

from modeles.prix import Prix


class GestionTitres(tk.LabelFrame):
    def __init__(self, parent, prix: Prix, titre_ajoute, titre_retire):
        super().__init__(parent, text="Gérer les titres", padx=10, pady=10)
        self._prix = prix
        self._titre_ajoute = titre_ajoute
        self._titre_retire = titre_retire

        ligne_ajout = tk.Frame(self)
        ligne_ajout.pack(fill=tk.X)
        self.entry_ticker = self._champ(ligne_ajout, "Ticker", width=8)
        self.entry_quantite = self._champ(ligne_ajout, "Qté", width=5, valeur_defaut="1")
        self.entry_seuil_bas_ajout = self._champ(ligne_ajout, "Alerte basse", width=7)
        self.entry_seuil_haut_ajout = self._champ(ligne_ajout, "Alerte haute", width=7)
        tk.Button(ligne_ajout, text="Ajouter", command=self.ajouter_titre).pack(side=tk.LEFT)
        tk.Label(
            self,
            text="(Alertes optionnelles : si vides, calculées à ±20% du prix actuel)",
            font=("Segoe UI", 8), fg="gray"
        ).pack(anchor="w", pady=(2, 5))

        ligne_liste = tk.Frame(self)
        ligne_liste.pack(fill=tk.X)
        self.listbox_titres = tk.Listbox(ligne_liste, height=4, exportselection=False)
        self.listbox_titres.pack(side=tk.LEFT, fill=tk.X, expand=True)
        for ticker in self._titres():
            self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        tk.Button(ligne_liste, text="Retirer", command=self.retirer_titre).pack(
            side=tk.LEFT, padx=(5, 0), anchor="n"
        )

        ligne_modif = tk.Frame(self)
        ligne_modif.pack(fill=tk.X, pady=(8, 0))
        tk.Label(ligne_modif, text="Sélection →").pack(side=tk.LEFT)
        self.entry_nouvelle_quantite = self._champ(ligne_modif, "Qté", width=5)
        self.entry_nouveau_seuil_bas = self._champ(ligne_modif, "Alerte basse", width=7)
        self.entry_nouveau_seuil_haut = self._champ(ligne_modif, "Alerte haute", width=7)
        tk.Button(ligne_modif, text="Modifier sélection", command=self.modifier_selection).pack(side=tk.LEFT)

        self.label_statut = tk.Label(self, text="", font=("Segoe UI", 9), fg="gray")
        self.label_statut.pack(anchor="w", pady=(5, 0))

    def _titres(self):
        return self._prix.get_donnees()["titres"]

    def _champ(self, parent, texte, width, valeur_defaut=""):
        tk.Label(parent, text=f"{texte}:").pack(side=tk.LEFT)
        entry = tk.Entry(parent, width=width)
        if valeur_defaut:
            entry.insert(0, valeur_defaut)
        entry.pack(side=tk.LEFT, padx=(2, 8))
        return entry

    def _texte_listbox(self, ticker):
        infos = self._titres()[ticker]
        return (
            f"{ticker} — {infos['quantite']} action(s) "
            f"(alerte : {infos['seuil_bas']:.2f} $ / {infos['seuil_haut']:.2f} $)"
        )

    def _rafraichir_ligne_listbox(self, index, ticker):
        self.listbox_titres.delete(index)
        self.listbox_titres.insert(index, self._texte_listbox(ticker))
        self.listbox_titres.selection_set(index)

    def _ticker_selectionne(self):
        selection = self.listbox_titres.curselection()
        if not selection:
            return None
        index = selection[0]
        return index, self.listbox_titres.get(index).split(" — ")[0]

    def _statut(self, texte, couleur):
        self.label_statut.config(text=texte, fg=couleur)

    @staticmethod
    def _entier_positif(texte):
        valeur = int(texte)
        if valeur <= 0:
            raise ValueError
        return valeur

    @staticmethod
    def _flottant_positif(texte):
        valeur = float(texte)
        if valeur <= 0:
            raise ValueError
        return valeur

    def ajouter_titre(self):
        ticker = self.entry_ticker.get().strip().upper()
        if not ticker:
            return
        if ticker in self._titres():
            self._statut(f"{ticker} est déjà dans le portfolio.", "orange")
            return
        try:
            quantite = self._entier_positif(self.entry_quantite.get().strip())
        except ValueError:
            self._statut("La quantité doit être un nombre entier positif.", "red")
            return

        texte_bas = self.entry_seuil_bas_ajout.get().strip()
        texte_haut = self.entry_seuil_haut_ajout.get().strip()
        try:
            seuil_bas = self._flottant_positif(texte_bas) if texte_bas else None
            seuil_haut = self._flottant_positif(texte_haut) if texte_haut else None
        except ValueError:
            self._statut("Les alertes doivent être des nombres positifs.", "red")
            return
        if seuil_bas is not None and seuil_haut is not None and seuil_bas >= seuil_haut:
            self._statut("L'alerte basse doit être inférieure à l'alerte haute.", "red")
            return

        try:
            self._prix.ajouter_titre(ticker, quantite, seuil_bas, seuil_haut)
        except Exception:
            self._statut(f"Impossible de récupérer les données du titre '{ticker}'.", "red")
            return

        self.listbox_titres.insert(tk.END, self._texte_listbox(ticker))
        for entry, valeur in (
            (self.entry_ticker, ""), (self.entry_quantite, "1"),
            (self.entry_seuil_bas_ajout, ""), (self.entry_seuil_haut_ajout, ""),
        ):
            entry.delete(0, tk.END)
            entry.insert(0, valeur)
        self._titre_ajoute(ticker)
        self._statut(f"{ticker} ajouté au portfolio ({quantite} action(s)).", "green")

    def retirer_titre(self):
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à retirer.", "orange")
            return
        index, ticker = selectionne
        self._prix.retirer_titre(ticker)
        self.listbox_titres.delete(index)
        self._titre_retire(ticker)
        self._statut(f"{ticker} retiré du portfolio.", "gray")

    def modifier_selection(self):
        selectionne = self._ticker_selectionne()
        if selectionne is None:
            self._statut("Sélectionnez un titre à modifier.", "orange")
            return
        index, ticker = selectionne
        texte_qte = self.entry_nouvelle_quantite.get().strip()
        texte_bas = self.entry_nouveau_seuil_bas.get().strip()
        texte_haut = self.entry_nouveau_seuil_haut.get().strip()
        if not texte_qte and not texte_bas and not texte_haut:
            self._statut("Entrez une nouvelle quantité et/ou de nouvelles alertes.", "orange")
            return
        if bool(texte_bas) != bool(texte_haut):
            self._statut("Les deux alertes doivent être fournies ensemble.", "red")
            return
        try:
            quantite = self._entier_positif(texte_qte) if texte_qte else None
            seuil_bas = self._flottant_positif(texte_bas) if texte_bas else None
            seuil_haut = self._flottant_positif(texte_haut) if texte_haut else None
        except ValueError:
            self._statut("La quantité et les alertes doivent être des nombres positifs.", "red")
            return
        if seuil_bas is not None and seuil_bas >= seuil_haut:
            self._statut("L'alerte basse doit être inférieure à l'alerte haute.", "red")
            return

        self._prix.modifier_titre(ticker, quantite, seuil_bas, seuil_haut)
        changements = []
        if quantite is not None:
            changements.append(f"{quantite} action(s)")
        if seuil_bas is not None:
            changements.append(f"alertes {seuil_bas:.2f} $ / {seuil_haut:.2f} $")
        self._rafraichir_ligne_listbox(index, ticker)
        for entry in (self.entry_nouvelle_quantite, self.entry_nouveau_seuil_bas, self.entry_nouveau_seuil_haut):
            entry.delete(0, tk.END)
        self._statut(f"{ticker} mis à jour : {', '.join(changements)}.", "green")