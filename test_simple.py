#!/usr/bin/env python3
"""
Test simple du bot
"""
try:
    print("Testing imports...")
    
    # Test import de base
    from telegram import Update, BotCommand
    print("✅ telegram base OK")
    
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    print("✅ telegram.ext OK")
    
    # Test database
    from database.db_functions import init_database
    print("✅ database OK")
    
    # Test configuration
    BOT_TOKEN = "8121743913:AAEBBPHVwMG0adNzeX86T1Ees7t4nZPv9Mw"
    ADMIN_ID = 692906415

    # Configuration Cloudinary
    import cloudinary
    cloudinary.config(
        cloud_name="dkpf8ovsd",
        api_key="398734649392149",
        api_secret="sGPfetxLvTkrfIrUQ3W6t0oCpQQ"
    )
    print("✅ Cloudinary config OK")

    print("\n🎉 Imports de base réussis !")
    
    # Test de création de l'application
    app = Application.builder().token(BOT_TOKEN).build()
    print("✅ Application Telegram créée")
    
    print("\n✅ Le bot peut démarrer !")

except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
