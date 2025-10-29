# Configuration du bot Anonyme Smartphone
import os
import cloudinary
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Token du bot (remplacez par votre vrai token)
BOT_TOKEN = os.getenv('BOT_TOKEN', "8424154788:AAEuobN21v6QHuvEsl5EaZQ2aptz0jncRfc")
API_TOKEN = BOT_TOKEN  # Alias pour compatibilité
BOT_USERNAME = "@anonyme_smartphone_bot"

# ID de l'administrateur
ADMIN_ID = int(os.getenv('ADMIN_ID', '1234567890'))  # Remplacez par votre ID Telegram

# Configuration Cloudinary
CLOUDINARY_URL = os.getenv('CLOUDINARY_URL')
if CLOUDINARY_URL:
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET')
    )

# Base de données
DB_FILE = "anonyme_smartphone.db"

# Messages
WELCOME_MESSAGE = """🎉 *Bienvenue chez Anonyme Smartphone* 📱

Votre spécialiste des téléphones !

Veuillez saisir votre prénom et l'envoyer :"""

AUTHENTICATED_MESSAGE = """Salut *{prenom}* ! 👋

Nous vous invitons à appuyer sur le bouton menu et choisir ce qui vous amène :"""

# Contacts
CONTACT_INFO = """📞 Pour commander ou obtenir plus d'informations :
💬 Telegram : @anonyme_smartphone
📧 Email : contact@anonymesmartphone.com
📞 Téléphone : +XXX XXX XXX XXX"""

# Informations sur l'entreprise
COMPANY_INFO = """ℹ️ *À PROPOS D'ANONYME SMARTPHONE*

Nous sommes votre spécialiste en :
📱 Accessoires pour smartphones
🔧 Services techniques spécialisés
💼 Solutions professionnelles

Notre mission : vous offrir les meilleurs produits et services pour vos appareils mobiles.

📍 Localisation : [Votre adresse]
🕒 Horaires : Lun-Sam 9h-18h"""
