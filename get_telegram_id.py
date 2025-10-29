#!/usr/bin/env python3
"""
Script pour obtenir votre ID Telegram
Utilisez ce script pour configurer ADMIN_ID dans le .env
"""
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()
API_TOKEN = os.getenv('BOT_TOKEN')

async def get_my_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande pour obtenir son ID Telegram"""
    user = update.effective_user
    await update.message.reply_text(
        f"👤 *Vos informations Telegram :*\n\n"
        f"🆔 **Votre ID :** `{user.id}`\n"
        f"👤 **Nom :** {user.first_name}\n"
        f"📛 **Username :** @{user.username if user.username else 'Non défini'}\n\n"
        f"📝 *Pour configurer l'administration :*\n"
        f"Ajoutez cette ligne dans votre fichier `.env` :\n"
        f"`ADMIN_ID={user.id}`",
        parse_mode='Markdown'
    )

def main():
    """Script principal pour obtenir l'ID"""
    print("🆔 Script pour obtenir votre ID Telegram")
    print("📱 Envoyez la commande /getid au bot...")
    
    app = Application.builder().token(API_TOKEN).build()
    app.add_handler(CommandHandler("getid", get_my_id))
    
    print("✅ Bot démarré ! Envoyez /getid pour obtenir votre ID")
    print("⏹️ Appuyez sur Ctrl+C pour arrêter")
    
    app.run_polling()

if __name__ == "__main__":
    main()
