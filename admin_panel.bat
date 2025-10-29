@echo off
title Bot Anonyme Smartphone - Administration

:menu
cls
echo.
echo  ========================================
echo   BOT ANONYME SMARTPHONE - ADMIN PANEL
echo  ========================================
echo.
echo  1. Demarrer le bot principal
echo  2. Obtenir mon ID Telegram
echo  3. Tester la connexion MongoDB
echo  4. Voir le guide d'administration
echo  5. Quitter
echo.
set /p choice="Choisissez une option (1-5): "

if "%choice%"=="1" goto start_bot
if "%choice%"=="2" goto get_id
if "%choice%"=="3" goto test_db
if "%choice%"=="4" goto guide
if "%choice%"=="5" goto exit

echo Option invalide, veuillez recommencer...
pause
goto menu

:start_bot
cls
echo Demarrage du bot Anonyme Smartphone...
echo.
"C:/Users/INGENIEUR/AppData/Local/Programs/Python/Python310/python.exe" main.py
pause
goto menu

:get_id
cls
echo Demarrage du script pour obtenir votre ID Telegram...
echo Envoyez /getid au bot pour obtenir votre ID
echo.
"C:/Users/INGENIEUR/AppData/Local/Programs/Python/Python310/python.exe" get_telegram_id.py
pause
goto menu

:test_db
cls
echo Test de connexion a la base de donnees...
echo.
"C:/Users/INGENIEUR/AppData/Local/Programs/Python/Python310/python.exe" test_bot.py
pause
goto menu

:guide
cls
echo.
echo  ========================================
echo   GUIDE RAPIDE DES COMMANDES ADMIN
echo  ========================================
echo.
echo  /admin          - Panneau d'administration
echo  /stats          - Statistiques du bot
echo  /listusers      - Liste des utilisateurs  
echo  /addproduct     - Ajouter un produit
echo  /broadcast      - Diffuser un message
echo.
echo  Exemple ajout produit:
echo  /addproduct "Coque iPhone" pochettes iphone "15 Pro" 29.99 "Description"
echo.
echo  Voir ADMIN_GUIDE.md pour le guide complet
echo.
pause
goto menu

:exit
echo.
echo Au revoir !
pause
exit
