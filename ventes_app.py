"""
Application de Gestion des Ventes
Auteur: Developer
Version: 1.0

Cette application permet aux commerçants d'enregistrer et de gérer leurs ventes
de manière simple et efficace.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import os


class VentesApp:
    """Application principale de gestion des ventes."""
    
    def __init__(self, root):
        """Initialise l'application."""
        self.root = root
        self.root.title("Gestion des Ventes")
        self.root.geometry("1000x700")
        self.root.minsize(800, 500)
        
        # Données de l'application
        self.ventes = []
        self.fichier_donnees = "ventes.json"
        
        # Initialiser les attributs de l'interface
        self.label_total_general = None
        
        # Charger les données existantes
        self.charger_donnees()
        
        # Créer l'interface
        self.creer_interface()
        
    def creer_interface(self):
        """Crée les éléments de l'interface utilisateur."""
        # Barre de menu
        self.creer_menu()
        
        # Frame principal
        frame_principal = ttk.Frame(self.root, padding="10")
        frame_principal.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurer le redimensionnement
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        frame_principal.columnconfigure(0, weight=1)
        frame_principal.rowconfigure(3, weight=1)
        
        # Section de saisie
        self.creer_section_saisie(frame_principal)
        
        # Séparateur
        ttk.Separator(frame_principal, orient='horizontal').grid(
            row=2, column=0, sticky=(tk.W, tk.E), pady=10
        )
        
        # Section du tableau
        self.creer_section_tableau(frame_principal)
        
        # Section du résumé
        self.creer_section_resume(frame_principal)
        
    def creer_menu(self):
        """Crée le menu de l'application."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        menu_fichier = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=menu_fichier)
        menu_fichier.add_command(label="Exporter les ventes (CSV)", command=self.exporter_csv)
        menu_fichier.add_separator()
        menu_fichier.add_command(label="Quitter", command=self.root.quit)
        
        # Menu À propos
        menu_apropos = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="À propos", menu=menu_apropos)
        menu_apropos.add_command(label="À propos de l'application", command=self.afficher_apropos)
        
    def creer_section_saisie(self, parent):
        """Crée la section de saisie des données."""
        # Frame de la section
        frame_saisie = ttk.LabelFrame(parent, text="Nouvelle Vente", padding="10")
        frame_saisie.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        frame_saisie.columnconfigure(1, weight=1)
        frame_saisie.columnconfigure(3, weight=1)
        
        # Label et champ - Nom du produit
        ttk.Label(frame_saisie, text="Nom du produit:").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entree_produit = ttk.Entry(frame_saisie, width=30)
        self.entree_produit.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Label et champ - Quantité
        ttk.Label(frame_saisie, text="Quantité:").grid(
            row=0, column=2, sticky=tk.W, padx=5, pady=5
        )
        self.entree_quantite = ttk.Entry(frame_saisie, width=15)
        self.entree_quantite.grid(row=0, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Label et champ - Prix unitaire
        ttk.Label(frame_saisie, text="Prix unitaire (€):").grid(
            row=1, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.entree_prix = ttk.Entry(frame_saisie, width=30)
        self.entree_prix.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Label - Prix total (affichage)
        ttk.Label(frame_saisie, text="Prix total (€):").grid(
            row=1, column=2, sticky=tk.W, padx=5, pady=5
        )
        self.label_total = ttk.Label(frame_saisie, text="0.00", foreground="green")
        self.label_total.grid(row=1, column=3, sticky=tk.W, padx=5, pady=5)
        
        # Bouton d'ajout
        ttk.Button(frame_saisie, text="Ajouter une vente", command=self.ajouter_vente).grid(
            row=2, column=0, columnspan=4, pady=10
        )
        
        # Bind des changements pour le calcul automatique
        self.entree_quantite.bind('<KeyRelease>', lambda e: self.calculer_total())
        self.entree_prix.bind('<KeyRelease>', lambda e: self.calculer_total())
        
    def creer_section_tableau(self, parent):
        """Crée la section du tableau des ventes."""
        # Frame du tableau
        frame_tableau = ttk.LabelFrame(parent, text="Historique des Ventes", padding="10")
        frame_tableau.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        frame_tableau.columnconfigure(0, weight=1)
        frame_tableau.rowconfigure(0, weight=1)
        
        # Créer le tableau avec scrollbar
        frame_scroll = ttk.Frame(frame_tableau)
        frame_scroll.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        frame_scroll.columnconfigure(0, weight=1)
        frame_scroll.rowconfigure(0, weight=1)
        
        # Scrollbar verticale
        scrollbar = ttk.Scrollbar(frame_scroll)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Tableau
        self.tableau = ttk.Treeview(
            frame_scroll,
            columns=("Produit", "Quantité", "Prix Unit.", "Total", "Actions"),
            height=12,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tableau.yview)
        
        # Configurer les colonnes
        self.tableau.column("#0", width=0, stretch=False)
        self.tableau.column("Produit", anchor=tk.W, width=300)
        self.tableau.column("Quantité", anchor=tk.CENTER, width=100)
        self.tableau.column("Prix Unit.", anchor=tk.E, width=100)
        self.tableau.column("Total", anchor=tk.E, width=100)
        self.tableau.column("Actions", anchor=tk.CENTER, width=100)
        
        # Configurer les en-têtes
        self.tableau.heading("#0", text="", anchor=tk.W)
        self.tableau.heading("Produit", text="Produit", anchor=tk.W)
        self.tableau.heading("Quantité", text="Quantité", anchor=tk.CENTER)
        self.tableau.heading("Prix Unit.", text="Prix Unit. (€)", anchor=tk.E)
        self.tableau.heading("Total", text="Total (€)", anchor=tk.E)
        self.tableau.heading("Actions", text="Actions", anchor=tk.CENTER)
        
        self.tableau.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Bind du clic droit pour la suppression
        self.tableau.bind("<Button-3>", self.afficher_menu_contexte)
        
        # Remplir le tableau avec les ventes existantes
        self.actualiser_tableau()
        
    def creer_section_resume(self, parent):
        """Crée la section du résumé des ventes."""
        frame_resume = ttk.LabelFrame(parent, text="Résumé", padding="10")
        frame_resume.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=10)
        frame_resume.columnconfigure(1, weight=1)
        
        # Total général
        ttk.Label(frame_resume, text="Total général des ventes (€):").grid(
            row=0, column=0, sticky=tk.W, padx=5, pady=5
        )
        self.label_total_general = ttk.Label(
            frame_resume,
            text="0.00",
            foreground="blue",
            font=("Arial", 12, "bold")
        )
        self.label_total_general.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Bouton Réinitialiser
        ttk.Button(frame_resume, text="Réinitialiser tout", command=self.reinitialiser).grid(
            row=0, column=2, padx=5
        )
        
    def calculer_total(self):
        """Calcule et affiche le prix total de la vente en cours."""
        try:
            quantite = float(self.entree_quantite.get()) if self.entree_quantite.get() else 0
            prix = float(self.entree_prix.get()) if self.entree_prix.get() else 0
            total = quantite * prix
            self.label_total.config(text=f"{total:.2f}")
        except ValueError:
            self.label_total.config(text="Erreur")
            
    def valider_saisie(self):
        """Valide les données saisies dans le formulaire."""
        produit = self.entree_produit.get().strip()
        quantite_str = self.entree_quantite.get().strip()
        prix_str = self.entree_prix.get().strip()
        
        # Vérifier que tous les champs sont remplis
        if not produit:
            messagebox.showerror("Erreur", "Veuillez entrer le nom du produit")
            return False
        
        if not quantite_str:
            messagebox.showerror("Erreur", "Veuillez entrer la quantité")
            return False
        
        if not prix_str:
            messagebox.showerror("Erreur", "Veuillez entrer le prix unitaire")
            return False
        
        # Vérifier que quantité et prix sont des nombres valides
        try:
            quantite = float(quantite_str)
            prix = float(prix_str)
            
            if quantite <= 0:
                messagebox.showerror("Erreur", "La quantité doit être supérieure à 0")
                return False
            
            if prix < 0:
                messagebox.showerror("Erreur", "Le prix ne peut pas être négatif")
                return False
                
            return True
        except ValueError:
            messagebox.showerror("Erreur", "Quantité et prix doivent être des nombres")
            return False
            
    def ajouter_vente(self):
        """Ajoute une nouvelle vente à la liste."""
        if not self.valider_saisie():
            return
        
        produit = self.entree_produit.get().strip()
        quantite = float(self.entree_quantite.get())
        prix = float(self.entree_prix.get())
        total = quantite * prix
        
        # Créer l'enregistrement de vente
        vente = {
            "produit": produit,
            "quantite": quantite,
            "prix": prix,
            "total": total,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        # Ajouter à la liste
        self.ventes.append(vente)
        
        # Sauvegarder
        self.sauvegarder_donnees()
        
        # Actualiser l'affichage
        self.actualiser_tableau()
        self.actualiser_resume()
        
        # Vider le formulaire
        self.vider_formulaire()
        
        messagebox.showinfo("Succès", "Vente enregistrée avec succès!")
        
    def vider_formulaire(self):
        """Vide tous les champs du formulaire."""
        self.entree_produit.delete(0, tk.END)
        self.entree_quantite.delete(0, tk.END)
        self.entree_prix.delete(0, tk.END)
        self.label_total.config(text="0.00")
        self.entree_produit.focus()
        
    def actualiser_tableau(self):
        """Met à jour l'affichage du tableau des ventes."""
        # Effacer tous les éléments
        for item in self.tableau.get_children():
            self.tableau.delete(item)
        
        # Ajouter les ventes
        for idx, vente in enumerate(self.ventes):
            self.tableau.insert(
                "",
                "end",
                iid=idx,
                values=(
                    vente["produit"],
                    f"{vente['quantite']:.2f}",
                    f"{vente['prix']:.2f}",
                    f"{vente['total']:.2f}",
                    "Supprimer"
                )
            )
        
        self.actualiser_resume()
        
    def actualiser_resume(self):
        """Met à jour le total général des ventes."""
        if self.label_total_general is not None:
            total_general = sum(vente["total"] for vente in self.ventes)
            self.label_total_general.config(text=f"{total_general:.2f}")
        
    def afficher_menu_contexte(self, event):
        """Affiche un menu contextuel pour supprimer une vente."""
        # Identifier la ligne cliquée
        selection = self.tableau.identify_row(event.y)
        
        if not selection:
            return
        
        # Créer le menu contextuel
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(
            label="Supprimer cette vente",
            command=lambda: self.supprimer_vente(int(selection))
        )
        menu.post(event.x_root, event.y_root)
        
    def supprimer_vente(self, index):
        """Supprime une vente de la liste."""
        if 0 <= index < len(self.ventes):
            produit = self.ventes[index]["produit"]
            
            # Confirmer la suppression
            if messagebox.askyesno(
                "Confirmation",
                f"Supprimer la vente de '{produit}'?"
            ):
                del self.ventes[index]
                self.sauvegarder_donnees()
                self.actualiser_tableau()
                
    def reinitialiser(self):
        """Réinitialise toutes les ventes."""
        if messagebox.askyesno(
            "Confirmation",
            "Êtes-vous sûr de vouloir supprimer toutes les ventes?"
        ):
            self.ventes = []
            self.sauvegarder_donnees()
            self.actualiser_tableau()
            
    def sauvegarder_donnees(self):
        """Sauvegarde les données dans un fichier JSON."""
        try:
            with open(self.fichier_donnees, 'w', encoding='utf-8') as f:
                json.dump(self.ventes, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la sauvegarde: {e}")
            
    def charger_donnees(self):
        """Charge les données depuis le fichier JSON."""
        if os.path.exists(self.fichier_donnees):
            try:
                with open(self.fichier_donnees, 'r', encoding='utf-8') as f:
                    self.ventes = json.load(f)
            except Exception as e:
                messagebox.showerror("Erreur", f"Erreur lors du chargement: {e}")
                self.ventes = []
                
    def exporter_csv(self):
        """Exporte les ventes en format CSV."""
        if not self.ventes:
            messagebox.showwarning("Attention", "Aucune vente à exporter")
            return
        
        try:
            nom_fichier = f"ventes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(nom_fichier, 'w', encoding='utf-8') as f:
                # En-têtes
                f.write("Produit,Quantité,Prix Unitaire (€),Total (€),Date\n")
                
                # Données
                for vente in self.ventes:
                    f.write(
                        f'"{vente["produit"]}",'
                        f'{vente["quantite"]:.2f},'
                        f'{vente["prix"]:.2f},'
                        f'{vente["total"]:.2f},'
                        f'{vente["date"]}\n'
                    )
            
            messagebox.showinfo("Succès", f"Export réussi: {nom_fichier}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'export: {e}")
            
    def afficher_apropos(self):
        """Affiche la fenêtre À propos."""
        fenetre_apropos = tk.Toplevel(self.root)
        fenetre_apropos.title("À propos")
        fenetre_apropos.geometry("500x300")
        fenetre_apropos.resizable(False, False)
        
        # Contenu
        frame = ttk.Frame(fenetre_apropos, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Titre
        titre = ttk.Label(
            frame,
            text="Application de Gestion des Ventes",
            font=("Arial", 14, "bold")
        )
        titre.pack(pady=10)
        
        # Version
        version = ttk.Label(frame, text="Version 1.0")
        version.pack()
        
        # Description
        description = ttk.Label(
            frame,
            text="Gestionnaire simple et efficace de ventes pour commerçants",
            justify=tk.CENTER
        )
        description.pack(pady=10)
        
        # Auteur
        auteur = ttk.Label(
            frame,
            text="Développé par: Developer\nDate: 2026",
            justify=tk.CENTER,
            foreground="blue"
        )
        auteur.pack(pady=10)
        
        # Fonctionnalités
        fonctionnalites = ttk.Label(
            frame,
            text="✓ Enregistrement automatique des ventes\n"
                 "✓ Calcul automatique du total\n"
                 "✓ Export en CSV\n"
                 "✓ Historique des ventes persistant",
            justify=tk.LEFT
        )
        fonctionnalites.pack(pady=20, anchor=tk.W)
        
        # Bouton Fermer
        ttk.Button(frame, text="Fermer", command=fenetre_apropos.destroy).pack(pady=10)


def main():
    """Fonction principale de l'application."""
    root = tk.Tk()
    app = VentesApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
