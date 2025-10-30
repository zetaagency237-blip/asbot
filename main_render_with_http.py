import os
import threading
import asyncio
from http.server import HTTPServer, BaseHTTPRequestHandler
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

class HealthCheckHandler(BaseHTTPRequestHandler):
    """Serveur HTTP simple pour satisfaire les exigences de port de Render"""
    
    def do_GET(self):
        if self.path == '/health' or self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            response = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Bot Anonyme Smartphone - Status</title>
                <meta charset="utf-8">
            </head>
            <body>
                <h1>🤖 Bot Anonyme Smartphone</h1>
                <p>✅ <strong>Status:</strong> En ligne et opérationnel</p>
                <p>📱 <strong>Type:</strong> Bot Telegram</p>
                <p>🔄 <strong>Mode:</strong> Polling actif</p>
                <p>🖼️ <strong>Fonctionnalités:</strong> Gestion d'images et administration mobile</p>
                <hr>
                <p><em>Ce serveur HTTP existe uniquement pour satisfaire les exigences de port de Render.</em></p>
                <p><em>Le bot fonctionne via l'API Telegram en mode polling.</em></p>
            </body>
            </html>
            """
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Supprimer les logs HTTP pour éviter le spam
        pass

def start_http_server():
    """Démarre le serveur HTTP pour Render"""
    PORT = int(os.environ.get('PORT', 8000))
    
    server = HTTPServer(('0.0.0.0', PORT), HealthCheckHandler)
    print(f"🌐 Serveur HTTP démarré sur le port {PORT}")
    print(f"🔗 Health check disponible sur :{PORT}/health")
    
    try:
        server.serve_forever()
    except Exception as e:
        print(f"❌ Erreur serveur HTTP: {e}")

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
        app = Application.builder().token(BOT_TOKEN).build()
    except Exception as e:
        print(f"Erreur création app: {e}")
        app = Application.builder().token(BOT_TOKEN).updater(None).build()
    
    # Ajouter les handlers de commandes de base
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("produits", produits_command))
    app.add_handler(CommandHandler("services", services_command))
    app.add_handler(CommandHandler("communaute", communaute_command))
    app.add_handler(CommandHandler("apropos", apropos_command))
    
    # Commandes admin
    app.add_handler(CommandHandler("admin", admin_command))
    app.add_handler(CommandHandler("addproduct", addproduct_command))
    app.add_handler(CommandHandler("broadcast", broadcast_command))
    app.add_handler(CommandHandler("stats", stats_command))
    app.add_handler(CommandHandler("listusers", listusers_command))
    app.add_handler(CommandHandler("editproduct", editproduct_command))
    app.add_handler(CommandHandler("deleteproduct", deleteproduct_command))
    app.add_handler(CommandHandler("addimage", addimage_command))
    app.add_handler(CommandHandler("mobileadmin", mobile_admin_command))
    
    # Handlers de callbacks
    app.add_handler(CallbackQueryHandler(
        handle_mobile_admin_callback, 
        pattern="^(mobile_|edit_cat_|toggle_cat_|rename_cat_|delete_cat_|confirm_delete_cat_|edit_brand_|toggle_brand_|manage_brand_|add_category|add_brand|add_model_)"
    ))
    app.add_handler(CallbackQueryHandler(button_callback))
    
    # Handlers de messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mobile_input))
    app.add_handler(MessageHandler(filters.PHOTO, handle_mobile_image_upload))

    # Handler d'erreurs
    app.add_error_handler(error_handler)

    print("🎉 BOT TELEGRAM CONFIGURÉ AVEC SUCCÈS!")
    print("📱 Administration mobile disponible avec /mobileadmin")
    print("🖼️ Gestion d'images des menus intégrée")
    
    # Démarrer le polling
    print("🔄 Démarrage du polling Telegram...")
    try:
        app.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True,
            close_loop=False
        )
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du polling: {e}")

def main():
    """Point d'entrée principal - démarre le serveur HTTP et le bot Telegram"""
    print("🚀 Démarrage du bot Anonyme Smartphone sur Render...")
    
    # Démarrer le serveur HTTP dans un thread séparé
    http_thread = threading.Thread(target=start_http_server, daemon=True)
    http_thread.start()
    
    # Attendre un peu que le serveur HTTP démarre
    import time
    time.sleep(2)
    
    # Démarrer le bot Telegram dans le thread principal
    start_telegram_bot()

if __name__ == "__main__":
    main()
