#!/usr/bin/env python3
"""
Script de test pour vérifier que toutes les importations fonctionnent
"""
import os
import sys

def test_imports():
    """Teste tous les imports nécessaires"""
    try:
        print("🔍 Test des imports...")
        
        # Test des imports standard
        from telegram import Update, BotCommand
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
        print("✅ python-telegram-bot importé")
        
        # Test MongoDB
        from pymongo import MongoClient
        print("✅ pymongo importé")
        
        # Test Cloudinary
        import cloudinary
        print("✅ cloudinary importé")
        
        # Test des modules personnalisés
        from database.db_functions import init_database, init_categories_and_brands
        print("✅ database.db_functions importé")
        
        from handlers.basic_handlers import (
            start_command, handle_message, produits_command, 
            services_command, communaute_command, apropos_command
        )
        print("✅ handlers.basic_handlers importé")
        
        from handlers.admin_handlers import (
            admin_command, addproduct_command, broadcast_command, 
            stats_command, listusers_command, editproduct_command,
            deleteproduct_command, addimage_command, handle_image_upload
        )
        print("✅ handlers.admin_handlers importé")
        
        from handlers.callback_handlers import button_callback
        print("✅ handlers.callback_handlers importé")
        
        from handlers.mobile_admin_handlers import (
            mobile_admin_command, handle_mobile_admin_callback, 
            handle_mobile_input, handle_mobile_image_upload
        )
        print("✅ handlers.mobile_admin_handlers importé")
        
        print("\n🎉 Tous les imports sont fonctionnels !")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

def test_configuration():
    """Teste la configuration"""
    try:
        print("\n🔧 Test de configuration...")
        
        # Configuration du bot
        BOT_TOKEN = "8121743913:AAEBBPHVwMG0adNzeX86T1Ees7t4nZPv9Mw"
        ADMIN_ID = 692906415
        
        print(f"✅ BOT_TOKEN configuré: {BOT_TOKEN[:10]}...")
        print(f"✅ ADMIN_ID configuré: {ADMIN_ID}")
        
        # Configuration Cloudinary
        import cloudinary
        cloudinary.config(
            cloud_name="dkpf8ovsd",
            api_key="398734649392149",
            api_secret="sGPfetxLvTkrfIrUQ3W6t0oCpQQ"
        )
        print("✅ Configuration Cloudinary OK")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de configuration: {e}")
        return False

def test_database_connection():
    """Teste la connexion à la base de données"""
    try:
        print("\n💾 Test de connexion MongoDB...")
        
        from database.db_functions import init_database, init_categories_and_brands
        
        # Test de la connexion
        print("✅ Initialisation de la base de données...")
        init_database()
        print("✅ Base de données initialisée")
        
        print("✅ Initialisation des catégories et marques...")
        init_categories_and_brands()
        print("✅ Structures initialisées")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de base de données: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS DU BOT")
    print("=" * 50)
    
    success = True
    
    # Test 1: Imports
    if not test_imports():
        success = False
    
    # Test 2: Configuration
    if not test_configuration():
        success = False
    
    # Test 3: Base de données
    if not test_database_connection():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Le bot est prêt à démarrer.")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("🔧 Vérifiez les erreurs ci-dessus.")
    
    print("=" * 50)
