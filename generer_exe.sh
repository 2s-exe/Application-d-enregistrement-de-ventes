#!/bin/bash

# Script de génération d'un exécutable Linux/Mac pour l'application de gestion des ventes

echo ""
echo "========================================"
echo "Génération de l'exécutable Linux/Mac"
echo "========================================"
echo ""

# Vérifier que PyInstaller est installé
if ! command -v pyinstaller &> /dev/null; then
    echo "PyInstaller n'est pas installé."
    echo "Installation en cours..."
    pip install pyinstaller
fi

# Générer l'exécutable
echo ""
echo "Génération de l'exécutable..."
pyinstaller --onefile --windowed --name "Gestion des Ventes" ventes_app.py

# Vérifier le succès
if [ $? -eq 0 ]; then
    echo ""
    echo "========================================"
    echo "Succès! Exécutable généré!"
    echo "========================================"
    echo ""
    echo "L'exécutable se trouve dans le dossier: dist/"
    echo "Fichier: Gestion des Ventes"
    echo ""
    echo "Vous pouvez maintenant exécuter l'application avec:"
    echo "./dist/Gestion\ des\ Ventes"
    echo ""
else
    echo ""
    echo "Erreur lors de la génération. Vérifiez que tout est bien installé."
    echo ""
fi
