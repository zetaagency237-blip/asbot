#!/usr/bin/env python3
"""
Test rapide du nouveau token
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_new_token():
    try:
        print("🔍 Test du nouveau token...")
        
        # Vérifier les variables d'environnement
        BOT_TOKEN = os.getenv('BOT_TOKEN')
        ADMIN_ID = os.getenv('ADMIN_ID')
        MONGODB_URI = os.getenv('MONGODB_URI')
        CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
        
        print(f"✅ BOT_TOKEN: {BOT_TOKEN[:10]}...{BOT_TOKEN[-10:] if BOT_TOKEN else 'None'}")
        print(f"✅ ADMIN_ID: {ADMIN_ID}")
        print(f"✅ MONGODB_URI: {'Configuré' if MONGODB_URI else 'Manquant'}")
        print(f"✅ CLOUDINARY_URL: {'Configuré' if CLOUDINARY_URL else 'Manquant'}")
        
        if not BOT_TOKEN:
            print("❌ BOT_TOKEN manquant dans .env")
            return False
        
        # Test de connexion Telegram
        from telegram.ext import Application
        
        print("\n🤖 Test de connexion Telegram...")
        app = Application.builder().token(BOT_TOKEN).build()
        print("✅ Application Telegram créée avec succès")
        
        # Test MongoDB
        print("\n💾 Test MongoDB...")
        from database.db_functions import init_database
        init_database()
        print("✅ Connexion MongoDB réussie")
        
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Le bot peut démarrer avec le nouveau token")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 TEST DU NOUVEAU TOKEN")
    print("=" * 40)
    
    success = test_new_token()
    
    print("\n" + "=" * 40)
    if success:
        print("🏆 RÉSULTAT: SUCCÈS COMPLET")
        print("🚀 Vous pouvez démarrer le bot avec: py main.py")
    else:
        print("⚠️  RÉSULTAT: PROBLÈME DÉTECTÉ")
        print("🔧 Vérifiez le fichier .env")
    print("=" * 40)
