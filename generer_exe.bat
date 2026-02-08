@echo off
REM Script de génération d'un exécutable Windows pour l'application de gestion des ventes

echo.
echo ========================================
echo Génération de l'exécutable Windows
echo ========================================
echo.

REM Vérifier que PyInstaller est installé
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller n'est pas installé.
    echo Installation en cours...
    pip install pyinstaller
)

REM Générer l'exécutable
echo.
echo Génération de l'exécutable...
pyinstaller --onefile --windowed --name "Gestion des Ventes" ventes_app.py

REM Vérifier le succès
if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo Succès! Exécutable généré!
    echo ========================================
    echo.
    echo L'exécutable se trouve dans le dossier: dist\
    echo Fichier: Gestion des Ventes.exe
    echo.
    echo Vous pouvez maintenant doubler-cliquer sur cet exécutable pour lancer l'application.
    echo.
    pause
) else (
    echo.
    echo Erreur lors de la génération. Vérifiez que tout est bien installé.
    echo.
    pause
)
