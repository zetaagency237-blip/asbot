import os
import asyncio
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

async def setup_bot_commands(app):
    """Configure les commandes du bot dans l'interface Telegram"""
    commands = [
        BotCommand("start", "🏠 Commencer"),
        BotCommand("produits", "📱 Voir le catalogue"),
        BotCommand("services", "🛠️ Nos services"),
        BotCommand("communaute", "👥 Rejoindre la communauté"),
        BotCommand("apropos", "ℹ️ À propos de nous"),
        BotCommand("mobileadmin", "📱 Admin mobile (admin uniquement)")
    ]
    
    try:
        await app.bot.set_my_commands(commands)
        print("✅ Commandes du bot configurées")
    except Exception as e:
        print(f"⚠️ Erreur configuration commandes: {e}")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler d'erreur global"""
    print(f'❌ Erreur: {context.error}')

def main():
    """Point d'entrée principal du bot"""
    print("🚀 Démarrage du bot Anonyme Smartphone...")
    
    # Initialiser la base de données
    init_database()
    
    # Créer l'application
    app = Application.builder().token(BOT_TOKEN).build()
    
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
    app.add_error_handler(error)

    # Configuration du menu des commandes (appelé après 1 seconde)
    app.job_queue.run_once(lambda context: setup_bot_commands(app), when=1)

    print("🎉 BOT ANONYME SMARTPHONE DÉMARRÉ AVEC SUCCÈS!")
    print("📱 Administration mobile disponible avec /mobileadmin")
    print("🖼️ Gestion d'images des menus intégrée")
    
    # Démarrer en mode polling (compatible avec tous les environnements)
    print("🔄 Mode POLLING...")
    try:
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print("\n🛑 Bot arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

if __name__ == "__main__":
    main()
