#!/usr/bin/env python3
"""
Script de validation finale pour le déploiement Render
Vérifie tous les composants critiques du bot
"""

import os
import sys
import importlib.util

def check_file_exists(file_path, description):
    """Vérifie qu'un fichier existe"""
    if os.path.exists(file_path):
        print(f"✅ {description} : {file_path}")
        return True
    else:
        print(f"❌ {description} MANQUANT : {file_path}")
        return False

def check_config():
    """Vérifie la configuration"""
    try:
        from config import BOT_TOKEN, ADMIN_ID
        print(f"✅ Configuration : BOT_TOKEN et ADMIN_ID chargés")
        return True
    except ImportError as e:
        print(f"❌ Erreur configuration : {e}")
        return False

def check_handlers():
    """Vérifie que tous les handlers peuvent être importés"""
    handlers_to_check = [
        'handlers.basic_handlers',
        'handlers.admin_handlers', 
        'handlers.mobile_admin_handlers',
        'handlers.callback_handlers'
    ]
    
    all_ok = True
    for handler in handlers_to_check:
        try:
            importlib.import_module(handler)
            print(f"✅ Handler : {handler}")
        except Exception as e:
            print(f"❌ Erreur handler {handler} : {e}")
            all_ok = False
    
    return all_ok

def check_database():
    """Vérifie la connexion base de données"""
    try:
        from database.db_functions import init_database
        print(f"✅ Base de données : Fonctions importées")
        return True
    except Exception as e:
        print(f"❌ Erreur base de données : {e}")
        return False

def main():
    print("🔍 VALIDATION FINALE - BOT ANONYME SMARTPHONE")
    print("=" * 50)
    
    # Vérifier les fichiers critiques
    files_ok = True
    critical_files = [
        ("main.py", "Fichier principal"),
        ("config.py", "Configuration"),
        ("requirements.txt", "Dépendances Python"),
        ("runtime.txt", "Version Python"),
        ("Procfile", "Commande Render"),
        ("RENDER_DEPLOYMENT_FIXED.md", "Guide déploiement")
    ]
    
    for file_path, description in critical_files:
        if not check_file_exists(file_path, description):
            files_ok = False
    
    print()
    
    # Vérifier les imports
    config_ok = check_config()
    handlers_ok = check_handlers()
    database_ok = check_database()
    
    print()
    print("📋 RÉSUMÉ DE LA VALIDATION")
    print("=" * 30)
    
    if files_ok:
        print("✅ Tous les fichiers critiques sont présents")
    else:
        print("❌ Des fichiers critiques sont manquants")
    
    if config_ok:
        print("✅ Configuration chargée correctement")
    else:
        print("❌ Problème de configuration")
    
    if handlers_ok:
        print("✅ Tous les handlers importés avec succès")
    else:
        print("❌ Problème avec certains handlers")
    
    if database_ok:
        print("✅ Fonctions de base de données accessibles")
    else:
        print("❌ Problème avec la base de données")
    
    print()
    
    if files_ok and config_ok and handlers_ok and database_ok:
        print("🎉 VALIDATION RÉUSSIE !")
        print("🚀 Votre bot est PRÊT pour le déploiement Render")
        print()
        print("📋 ÉTAPES SUIVANTES :")
        print("1. Commitez et pushez sur GitHub")
        print("2. Créez un Web Service sur Render")
        print("3. Configurez les variables d'environnement") 
        print("4. Déployez !")
        return 0
    else:
        print("❌ VALIDATION ÉCHOUÉE")
        print("Corrigez les erreurs ci-dessus avant le déploiement")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
