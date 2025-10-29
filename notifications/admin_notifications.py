"""
Système de notifications administrateur
Envoie des notifications automatiques à l'admin lors d'actions clients
"""
from telegram import Update
from telegram.ext import ContextTypes
from datetime import datetime
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration Admin
ADMIN_ID = int(os.getenv('ADMIN_ID', 1888960312))

async def notify_admin_product_interest(context, user_info, model_name, model_price=None):
    """Notifie l'admin quand un client s'intéresse à un produit"""
    try:
        # Informations utilisateur
        user_id = user_info.get('id', 'Inconnu')
        user_name = user_info.get('first_name', 'Inconnu')
        user_username = user_info.get('username', 'Pas de @')
        username_display = f"@{user_username}" if user_username != 'Pas de @' else user_username
        
        # Message de notification
        notification_text = (
            "📱 **NOUVEAU INTÉRÊT PRODUIT**\n\n"
            
            "👤 **CLIENT :**\n"
            f"• Nom : {user_name}\n"
            f"• ID : `{user_id}`\n"
            f"• Username : {username_display}\n\n"
            
            "🛒 **PRODUIT D'INTÉRÊT :**\n"
            f"• Modèle : **{model_name}**\n"
        )
        
        if model_price:
            notification_text += f"• Prix : **{model_price}€**\n"
        
        notification_text += f"\n⏰ **Horodatage :** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n\n"
        notification_text += "💬 *Le client a exprimé son intérêt pour ce produit*"
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notification_text,
            parse_mode='Markdown'
        )
        
        print(f"✅ Notification produit envoyée: {model_name} -> Admin {ADMIN_ID}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur notification produit: {e}")
        return False

async def notify_admin_service_request(context, user_info, service_type, user_name=None):
    """Notifie l'admin quand un client demande un service"""
    try:
        # Informations utilisateur
        user_id = user_info.get('id', 'Inconnu')
        user_first_name = user_info.get('first_name', 'Inconnu')
        user_username = user_info.get('username', 'Pas de @')
        username_display = f"@{user_username}" if user_username != 'Pas de @' else user_username
        
        # Utiliser le nom enregistré ou le prénom Telegram
        display_name = user_name if user_name else user_first_name
        
        # Descriptions des services
        service_descriptions = {
            "deblocage": "🔓 Déblocage de smartphone",
            "desimlockage": "📱 Désimlocage opérateur", 
            "declonage": "🔄 Déclonage d'appareil",
            "cas_particulier": "🛠️ Cas particulier / Service spécialisé"
        }
        
        service_name = service_descriptions.get(service_type, f"Service: {service_type}")
        
        # Message de notification
        notification_text = (
            "🔧 **NOUVELLE DEMANDE SERVICE**\n\n"
            
            "👤 **CLIENT :**\n"
            f"• Nom : {display_name}\n"
            f"• ID : `{user_id}`\n"
            f"• Username : {username_display}\n\n"
            
            "🛠️ **SERVICE DEMANDÉ :**\n"
            f"• Type : **{service_name}**\n\n"
            
            f"⏰ **Horodatage :** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n\n"
            "📞 *Le client souhaite être contacté pour ce service*"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notification_text,
            parse_mode='Markdown'
        )
        
        print(f"✅ Notification service envoyée: {service_type} -> Admin {ADMIN_ID}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur notification service: {e}")
        return False

async def notify_admin_new_user(context, user_info, user_name):
    """Notifie l'admin quand un nouvel utilisateur s'enregistre"""
    try:
        # Informations utilisateur
        user_id = user_info.get('id', 'Inconnu')
        user_first_name = user_info.get('first_name', 'Inconnu')
        user_username = user_info.get('username', 'Pas de @')
        username_display = f"@{user_username}" if user_username != 'Pas de @' else user_username
        
        # Message de notification
        notification_text = (
            "👋 **NOUVEL UTILISATEUR**\n\n"
            
            "👤 **INFORMATIONS :**\n"
            f"• Nom enregistré : **{user_name.title()}**\n"
            f"• Prénom Telegram : {user_first_name}\n"
            f"• ID : `{user_id}`\n"
            f"• Username : {username_display}\n\n"
            
            f"⏰ **Inscription :** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n\n"
            "🎉 *Nouvel ajout à la famille Anonyme Smartphone !*"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notification_text,
            parse_mode='Markdown'
        )
        
        print(f"✅ Notification nouvel utilisateur envoyée: {user_name} -> Admin {ADMIN_ID}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur notification nouvel utilisateur: {e}")
        return False

async def notify_admin_contact_request(context, user_info, user_name=None):
    """Notifie l'admin quand un client demande des infos de contact"""
    try:
        # Informations utilisateur
        user_id = user_info.get('id', 'Inconnu')
        user_first_name = user_info.get('first_name', 'Inconnu')
        user_username = user_info.get('username', 'Pas de @')
        username_display = f"@{user_username}" if user_username != 'Pas de @' else user_username
        
        # Utiliser le nom enregistré ou le prénom Telegram
        display_name = user_name if user_name else user_first_name
        
        # Message de notification
        notification_text = (
            "📞 **DEMANDE INFORMATIONS CONTACT**\n\n"
            
            "👤 **CLIENT :**\n"
            f"• Nom : {display_name}\n"
            f"• ID : `{user_id}`\n"
            f"• Username : {username_display}\n\n"
            
            "📋 **ACTION :**\n"
            "• A consulté les informations 'À propos'\n"
            "• A accédé aux coordonnées de contact\n\n"
            
            f"⏰ **Horodatage :** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n\n"
            "💼 *Client potentiellement intéressé par un contact direct*"
        )
        
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=notification_text,
            parse_mode='Markdown'
        )
        
        print(f"✅ Notification demande contact envoyée: {display_name} -> Admin {ADMIN_ID}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur notification demande contact: {e}")
        return False

async def send_test_notification(bot_or_context):
    """Envoie une notification de test à l'admin"""
    try:
        test_text = (
            "🧪 **TEST NOTIFICATIONS**\n\n"
            "✅ Le système de notifications fonctionne !\n\n"
            "Vous recevrez désormais des alertes pour :\n"
            "• 📱 Demandes de produits\n"
            "• 🔧 Demandes de services\n"
            "• 👋 Nouveaux utilisateurs\n"
            "• 📞 Demandes de contact\n\n"
            f"🆔 **Admin ID :** {ADMIN_ID}\n"
            f"⏰ **Test envoyé le :** {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}"
        )
        
        # Gérer les deux cas : Bot direct ou Context
        if hasattr(bot_or_context, 'bot'):
            # C'est un context
            bot = bot_or_context.bot
        else:
            # C'est directement un bot
            bot = bot_or_context
        
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=test_text,
            parse_mode='Markdown'
        )
        
        print(f"✅ Notification test envoyée à l'admin {ADMIN_ID}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur test notification: {e}")
        return False
