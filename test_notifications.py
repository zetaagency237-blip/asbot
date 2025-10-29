#!/usr/bin/env python3
"""
Test des notifications admin
"""

import asyncio
import os
from dotenv import load_dotenv
from telegram import Bot

# Charger les variables d'environnement
load_dotenv()

async def test_notifications():
    """Test des notifications"""
    try:
        # Configuration
        BOT_TOKEN = os.getenv('BOT_TOKEN')
        ADMIN_ID = int(os.getenv('ADMIN_ID', 1888960312))
        
        if not BOT_TOKEN:
            print("❌ Token du bot non trouvé dans .env")
            return False
            
        bot = Bot(token=BOT_TOKEN)
        
        # Initialiser le bot
        await bot.initialize()
        
        # Test de notification simple
        print("🧪 Test des notifications admin...")
        
        test_text = (
            "🧪 **TEST NOTIFICATIONS**\n\n"
            "✅ Le système de notifications fonctionne !\n\n"
            "Vous recevrez désormais des alertes pour :\n"
            "• 📱 Demandes de produits\n"
            "• 🔧 Demandes de services\n"
            "• 👋 Nouveaux utilisateurs\n"
            "• 📞 Demandes de contact\n\n"
            f"🆔 **Admin ID :** {ADMIN_ID}"
        )
        
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=test_text,
            parse_mode='Markdown'
        )
        
        print("✅ Notification de test envoyée!")
        
        # Fermer la connexion
        await bot.shutdown()
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test des notifications: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_notifications())
