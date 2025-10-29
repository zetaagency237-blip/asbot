#!/usr/bin/env python3
"""
Script de test pour le bot Anonyme Smartphone
"""
from dotenv import load_dotenv
import os
from pymongo import MongoClient
import cloudinary

def test_environment():
    """Teste les variables d'environnement"""
    load_dotenv()
    
    print("🔍 Test des variables d'environnement...")
    
    # Test des variables
    bot_token = os.getenv('BOT_TOKEN')
    mongodb_uri = os.getenv('MONGODB_URI')
    cloudinary_url = os.getenv('CLOUDINARY_URL')
    
    if bot_token:
        print("✅ BOT_TOKEN configuré")
    else:
        print("❌ BOT_TOKEN manquant")
    
    if mongodb_uri:
        print("✅ MONGODB_URI configuré")
    else:
        print("❌ MONGODB_URI manquant")
        
    if cloudinary_url:
        print("✅ CLOUDINARY_URL configuré")
    else:
        print("❌ CLOUDINARY_URL manquant")

def test_mongodb():
    """Teste la connexion MongoDB"""
    print("\n🔍 Test de connexion MongoDB...")
    try:
        load_dotenv()
        client = MongoClient(os.getenv('MONGODB_URI'))
        
        # Test de ping
        client.admin.command('ping')
        print("✅ Connexion MongoDB réussie")
        
        # Test de base de données
        db = client[os.getenv('DATABASE_NAME')]
        print(f"✅ Base de données '{os.getenv('DATABASE_NAME')}' accessible")
        
        client.close()
        
    except Exception as e:
        print(f"❌ Erreur MongoDB : {e}")

def test_cloudinary():
    """Teste la configuration Cloudinary"""
    print("\n🔍 Test de configuration Cloudinary...")
    try:
        load_dotenv()
        cloudinary.config(cloudinary_url=os.getenv('CLOUDINARY_URL'))
        
        # Vérifier la configuration
        config = cloudinary.config()
        if config.cloud_name and config.api_key:
            print("✅ Configuration Cloudinary réussie")
        else:
            print("❌ Configuration Cloudinary incomplète")
            
    except Exception as e:
        print(f"❌ Erreur Cloudinary : {e}")

if __name__ == "__main__":
    print("🚀 Test du bot Anonyme Smartphone\n")
    test_environment()
    test_mongodb() 
    test_cloudinary()
    print("\n✅ Tests terminés !")
