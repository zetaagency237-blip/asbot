import os
import threading
from flask import Flask
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import Update, BotCommand
from telegram.ext import ContextTypes

# Importer la configuration
from config import BOT_TOKEN, ADMIN_ID

# Importer les fonctions de la base de données
from database.db_functions import init_database

# Importer les handlers
from handlers.basic_handlers import (
    start_command, produits_command, services_command, 
    communaute_command, apropos_command, handle_message
)

from handlers.admin_handlers import (
    admin_command, addproduct_command, broadcast_command,
    stats_command, listusers_command, editproduct_command,
    deleteproduct_command, addimage_command
)

from handlers.mobile_admin_handlers import (
    mobile_admin_command, handle_mobile_admin_callback, 
    handle_mobile_input, handle_mobile_image_upload
)

from handlers.callback_handlers import button_callback

# Créer l'application Flask pour le keep-alive
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 Bot Anonyme Smartphone</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
            .container { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #2c3e50; }
            .status { color: #27ae60; font-weight: bold; }
            .info { background: #ecf0f1; padding: 15px; border-radius: 5px; margin: 10px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Bot Anonyme Smartphone</h1>
            <p class="status">✅ Status: En ligne et opérationnel</p>
            
            <div class="info">
                <p><strong>📱 Type:</strong> Bot Telegram</p>
                <p><strong>🔄 Mode:</strong> Polling actif</p>
                <p><strong>🖼️ Fonctionnalités:</strong> Gestion d'images et administration mobile</p>
                <p><strong>⚡ Keep-alive:</strong> Système Flask actif</p>
            </div>
            
            <p><em>Ce serveur web maintient le bot actif 24/7 et évite la mise en veille.</em></p>
            <p><em>Le bot fonctionne via l'API Telegram en mode polling.</em></p>
        </div>
    </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "online", "bot": "Anonyme Smartphone", "mode": "polling"}

def keep_alive():
    """Démarre le serveur Flask pour maintenir le bot actif"""
    PORT = int(os.environ.get('PORT', 8080))
    
    # Supprimer les logs Flask pour éviter le spam
    import logging
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    print(f"🌐 Serveur Flask démarré sur le port {PORT}")
    print(f"🔗 Keep-alive disponible sur :{PORT}/")
    print(f"📊 Health check sur :{PORT}/health")
    
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler d'erreur global"""
    print(f'❌ Erreur: {context.error}')

def start_telegram_bot():
    """Démarre le bot Telegram"""
    print("🤖 Initialisation du bot Telegram...")
    
    # Initialiser la base de données
    init_database()
    
    # Créer l'application
    try:
        telegram_app = Application.builder().token(BOT_TOKEN).build()
        print("✅ Application Telegram créée avec succès")
    except Exception as e:
        print(f"Erreur création app: {e}")
        try:
            telegram_app = Application.builder().token(BOT_TOKEN).updater(None).build()
            print("✅ Application Telegram créée avec fallback")
        except Exception as e2:
            print(f"❌ Impossible de créer l'application: {e2}")
            return
    
    # Ajouter les handlers de commandes de base
    telegram_app.add_handler(CommandHandler("start", start_command))
    telegram_app.add_handler(CommandHandler("produits", produits_command))
    telegram_app.add_handler(CommandHandler("services", services_command))
    telegram_app.add_handler(CommandHandler("communaute", communaute_command))
    telegram_app.add_handler(CommandHandler("apropos", apropos_command))
    
    # Commandes admin
    telegram_app.add_handler(CommandHandler("admin", admin_command))
    telegram_app.add_handler(CommandHandler("addproduct", addproduct_command))
    telegram_app.add_handler(CommandHandler("broadcast", broadcast_command))
    telegram_app.add_handler(CommandHandler("stats", stats_command))
    telegram_app.add_handler(CommandHandler("listusers", listusers_command))
    telegram_app.add_handler(CommandHandler("editproduct", editproduct_command))
    telegram_app.add_handler(CommandHandler("deleteproduct", deleteproduct_command))
    telegram_app.add_handler(CommandHandler("addimage", addimage_command))
    telegram_app.add_handler(CommandHandler("mobileadmin", mobile_admin_command))
    
    # Handlers de callbacks
    telegram_app.add_handler(CallbackQueryHandler(
        handle_mobile_admin_callback, 
        pattern="^(mobile_|edit_cat_|toggle_cat_|rename_cat_|delete_cat_|confirm_delete_cat_|edit_brand_|toggle_brand_|manage_brand_|add_category|add_brand|add_model_)"
    ))
    telegram_app.add_handler(CallbackQueryHandler(button_callback))
    
    # Handlers de messages
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mobile_input))
    telegram_app.add_handler(MessageHandler(filters.PHOTO, handle_mobile_image_upload))

    # Handler d'erreurs
    telegram_app.add_error_handler(error_handler)

    print("🎉 BOT TELEGRAM CONFIGURÉ AVEC SUCCÈS!")
    print("📱 Administration mobile disponible avec /mobileadmin")
    print("🖼️ Gestion d'images des menus intégrée")
    
    # Démarrer le polling
    print("🔄 Démarrage du polling Telegram...")
    try:
        telegram_app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du polling: {e}")

def main():
    """Point d'entrée principal - démarre Flask et le bot Telegram"""
    print("🚀 Démarrage du bot Anonyme Smartphone avec keep-alive Flask...")
    
    # Démarrer le serveur Flask dans un thread séparé (keep-alive)
    flask_thread = threading.Thread(target=keep_alive, daemon=True)
    flask_thread.start()
    
    # Attendre que Flask démarre
    import time
    time.sleep(3)
    
    # Démarrer le bot Telegram dans le thread principal
    start_telegram_bot()

if __name__ == "__main__":
    main()
