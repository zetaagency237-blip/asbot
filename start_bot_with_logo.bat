@echo off
echo 🚀 LANCEMENT DU BOT AVEC NOUVELLES FONCTIONNALITÉS
echo ==================================================
echo.
echo 📋 FONCTIONNALITÉS AJOUTÉES:
echo    🏠 Logo d'accueil dans le message de bienvenue
echo    📚 Image catalogue dans /produits
echo    🖼️ Interface admin mobile pour gérer les images
echo.
echo 💡 COMMENT UTILISER:
echo    1. Envoyez /mobileadmin pour accéder à l'admin
echo    2. Cliquez sur "Gérer Images"
echo    3. Ajoutez vos images (logo et catalogue)
echo.
echo ⏳ Lancement du bot en cours...
echo.

cd /d "%~dp0"
py main.py

pause
