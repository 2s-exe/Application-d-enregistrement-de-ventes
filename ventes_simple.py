import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json, os

class VentesApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion des Ventes")
        self.root.geometry("900x600")
        self.fichier = "ventes.json"
        self.ventes = []
        self.charger()
        self.creer_ui()

    def creer_ui(self):
        # Menu
        menu = tk.Menu(self.root)
        self.root.config(menu=menu)
        m = tk.Menu(menu, tearoff=0)
        menu.add_cascade(label="Fichier", menu=m)
        m.add_command(label="Quitter", command=self.root.quit)

        f = ttk.Frame(self.root, padding=10)
        f.pack(fill=tk.BOTH, expand=True)

        # Formulaire
        saisie = ttk.LabelFrame(f, text="Nouvelle Vente", padding=10)
        saisie.pack(fill=tk.X, pady=5)

        for col, label in enumerate(["Produit", "Quantité", "Prix (€)"]):
            ttk.Label(saisie, text=label).grid(row=0, column=col*2, padx=5)

        self.e_produit = ttk.Entry(saisie, width=25)
        self.e_produit.grid(row=0, column=1, padx=5)
        self.e_qte = ttk.Entry(saisie, width=10)
        self.e_qte.grid(row=0, column=3, padx=5)
        self.e_prix = ttk.Entry(saisie, width=10)
        self.e_prix.grid(row=0, column=5, padx=5)

        ttk.Label(saisie, text="Total:").grid(row=0, column=6, padx=5)
        self.lbl_total = ttk.Label(saisie, text="0.00", foreground="green")
        self.lbl_total.grid(row=0, column=7, padx=5)

        ttk.Button(saisie, text="➕ Ajouter", command=self.ajouter).grid(row=0, column=8, padx=10)

        for e in (self.e_qte, self.e_prix):
            e.bind('<KeyRelease>', lambda _: self.calc_total())

        # Tableau
        tableau_f = ttk.LabelFrame(f, text="Historique", padding=10)
        tableau_f.pack(fill=tk.BOTH, expand=True, pady=5)

        self.tableau = ttk.Treeview(tableau_f,
            columns=("Produit", "Qté", "Prix", "Total"), show="headings", height=12)
        for col, w in [("Produit", 300), ("Qté", 80), ("Prix", 100), ("Total", 100)]:
            self.tableau.heading(col, text=col)
            self.tableau.column(col, width=w)
        self.tableau.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        sb = ttk.Scrollbar(tableau_f, command=self.tableau.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.tableau.config(yscrollcommand=sb.set)
        self.tableau.bind("<Button-3>", self.menu_contextuel)

        # Résumé
        resume = ttk.Frame(f)
        resume.pack(fill=tk.X, pady=5)
        ttk.Label(resume, text="Total général (€):").pack(side=tk.LEFT, padx=5)
        self.lbl_general = ttk.Label(resume, text="0.00", foreground="blue",
                                      font=("Arial", 12, "bold"))
        self.lbl_general.pack(side=tk.LEFT)
        ttk.Button(resume, text="🗑 Réinitialiser", command=self.reinitialiser).pack(side=tk.RIGHT, padx=5)

        self.actualiser()

    def calc_total(self):
        try:
            total = float(self.e_qte.get() or 0) * float(self.e_prix.get() or 0)
            self.lbl_total.config(text=f"{total:.2f}")
        except ValueError:
            self.lbl_total.config(text="Erreur")

    def ajouter(self):
        produit = self.e_produit.get().strip()
        try:
            qte = float(self.e_qte.get())
            prix = float(self.e_prix.get())
            assert produit and qte > 0 and prix >= 0
        except:
            messagebox.showerror("Erreur", "Champs invalides. Vérifiez les valeurs.")
            return

        self.ventes.append({"produit": produit, "quantite": qte, "prix": prix,
                             "total": qte * prix,
                             "date": datetime.now().strftime("%d/%m/%Y %H:%M")})
        self.sauvegarder()
        self.actualiser()
        for e in (self.e_produit, self.e_qte, self.e_prix):
            e.delete(0, tk.END)
        self.lbl_total.config(text="0.00")
        messagebox.showinfo("Succès", "Vente ajoutée!")

    def actualiser(self):
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        for i, v in enumerate(self.ventes):
            self.tableau.insert("", "end", iid=i,
                values=(v["produit"], f"{v['quantite']:.2f}",
                        f"{v['prix']:.2f}", f"{v['total']:.2f}"))
        self.lbl_general.config(text=f"{sum(v['total'] for v in self.ventes):.2f}")

    def menu_contextuel(self, event):
        sel = self.tableau.identify_row(event.y)
        if not sel:
            return
        m = tk.Menu(self.root, tearoff=0)
        m.add_command(label="Supprimer", command=lambda: self.supprimer(int(sel)))
        m.post(event.x_root, event.y_root)

    def supprimer(self, idx):
        if messagebox.askyesno("Confirmation", f"Supprimer '{self.ventes[idx]['produit']}'?"):
            del self.ventes[idx]
            self.sauvegarder()
            self.actualiser()

    def reinitialiser(self):
        if messagebox.askyesno("Confirmation", "Supprimer toutes les ventes?"):
            self.ventes = []
            self.sauvegarder()
            self.actualiser()

    def sauvegarder(self):
        with open(self.fichier, 'w', encoding='utf-8') as f:
            json.dump(self.ventes, f, ensure_ascii=False, indent=2)

    def charger(self):
        if os.path.exists(self.fichier):
            with open(self.fichier, 'r', encoding='utf-8') as f:
                self.ventes = json.load(f)


if __name__ == "__main__":
    root = tk.Tk()
    VentesApp(root)
    root.mainloop()
