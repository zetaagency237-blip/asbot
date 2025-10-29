#!/usr/bin/env python3
"""
Test rapide de la configuration Cloudinary
"""
import os
from dotenv import load_dotenv

def test_cloudinary_config():
    print("🧪 TEST CONFIGURATION CLOUDINARY\n")
    
    # Charger les variables d'environnement
    load_dotenv()
    
    # Vérifier les variables
    api_secret = os.getenv('CLOUDINARY_API_SECRET', '')
    cloudinary_url = os.getenv('CLOUDINARY_URL', '')
    
    print("📋 Variables d'environnement:")
    print(f"   CLOUDINARY_API_SECRET: {'✅ Définie (' + str(len(api_secret)) + ' chars)' if api_secret else '❌ Manquante'}")
    print(f"   CLOUDINARY_URL: {'✅ Définie (' + str(len(cloudinary_url)) + ' chars)' if cloudinary_url else '❌ Manquante'}")
    
    if api_secret:
        expected_secret = "9AJGURM4X2oaDV01r3XIKt7pomI"
        if api_secret == expected_secret:
            print(f"   ✅ API Secret correcte: {api_secret[:10]}...{api_secret[-5:]}")
        else:
            print(f"   ❌ API Secret incorrecte!")
            print(f"      Attendue: {expected_secret}")
            print(f"      Trouvée:  {api_secret}")
            return False
    
    # Test de connexion
    try:
        import cloudinary
        import cloudinary.api
        
        cloudinary.config(
            cloud_name="dkpf8ovsd",
            api_key="398734649392149", 
            api_secret=api_secret,
            secure=True
        )
        
        print("\n🔧 Configuration Cloudinary:")
        print(f"   Cloud Name: dkpf8ovsd")
        print(f"   API Key: 398734649392149")
        print(f"   API Secret: {api_secret[:10]}...{api_secret[-5:]}")
        
        # Test ping
        print(f"\n📡 Test de connexion...")
        result = cloudinary.api.ping()
        print(f"   ✅ Connexion réussie: {result}")
        
        return True
        
    except ImportError as e:
        print(f"\n❌ Module Cloudinary manquant: {e}")
        print("   Installez avec: pip install cloudinary")
        return False
        
    except Exception as e:
        print(f"\n❌ Erreur de connexion Cloudinary: {e}")
        return False

if __name__ == "__main__":
    success = test_cloudinary_config()
    print(f"\n🎯 Résultat: {'✅ Configuration OK' if success else '❌ Problème détecté'}")
