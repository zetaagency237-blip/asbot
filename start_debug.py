"""
Test du nouveau token Telegram
"""
from telegram.ext import Application, CommandHandler
from telegram import Update

# Configuration avec le nouveau token
BOT_TOKEN = "8424154788:AAEuobN21v6QHuvEsl5EaZQ2aptz0jncRfc"
ADMIN_ID = 1888960312

async def start_command(update: Update, context):
    """Test de la commande /start"""
    await update.message.reply_text(
        "🎉 *SUCCÈS !*\n\n"
        "✅ Le nouveau token fonctionne parfaitement !\n"
        "🤖 Bot Anonyme Smartphone opérationnel\n\n" 
        f"👤 Votre ID: {update.effective_user.id}\n"
        f"👑 Admin ID: {ADMIN_ID}\n\n"
        "🚀 Prêt pour les fonctionnalités complètes !",
        parse_mode='Markdown'
    )

def test_connection():
    """Test de base du token"""
    try:
        print("🔍 Test de connexion...")
        print(f"📱 Token: {BOT_TOKEN[:20]}...")
        
        app = Application.builder().token(BOT_TOKEN).build()
        print("✅ Application créée avec succès")
        
        return app
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

if __name__ == "__main__":
    try:
        print("🚀 DÉMARRAGE TEST BOT...")
        
        # Test de connexion
        app = test_connection()
        if not app:
            exit(1)
        
        # Ajouter le handler de test
        app.add_handler(CommandHandler("start", start_command))
        
        print("✅ Handler ajouté")
        print("🔄 Démarrage du polling...")
        print("📱 Ouvrez Telegram et tapez /start pour tester!")
        print(f"🆔 Votre ID admin: {ADMIN_ID}")
        
        # Démarrer le bot
        app.run_polling()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
