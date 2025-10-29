import os
from dotenv import load_dotenv

print("🔍 DIAGNOSTIC CLOUDINARY SIMPLE")
print("=" * 40)

# Charger .env
load_dotenv()

# Vérifier les variables
api_secret = os.getenv('CLOUDINARY_API_SECRET')
cloudinary_url = os.getenv('CLOUDINARY_URL')

print(f"CLOUDINARY_API_SECRET: {api_secret}")
print(f"CLOUDINARY_URL: {cloudinary_url}")

# Tester l'import
try:
    import cloudinary
    print("✅ Module cloudinary importé")
    print(f"Version: {cloudinary.VERSION}")
    
    import cloudinary.api
    print("✅ Module cloudinary.api importé")
    
    # Configuration
    cloudinary.config(
        cloud_name="dkpf8ovsd",
        api_key="398734649392149", 
        api_secret="9AJGURM4X2oaDV01r3XIKt7pomI",
        secure=True
    )
    print("✅ Configuration Cloudinary OK")
    
    # Test de ping
    result = cloudinary.api.ping()
    print(f"✅ Test ping réussi: {result}")
    
except ImportError as e:
    print(f"❌ Erreur d'import: {e}")
except Exception as e:
    print(f"❌ Erreur Cloudinary: {e}")
    print(f"Type d'erreur: {type(e)}")
