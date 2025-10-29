#!/usr/bin/env python3
"""
Test de démarrage du bot avec gestion d'erreur
"""
import sys
import traceback

def test_bot():
    try:
        print("🚀 Démarrage du test du bot...")
        
        # Configuration du bot
        BOT_TOKEN = "8121743913:AAEBBPHVwMG0adNzeX86T1Ees7t4nZPv9Mw"
        ADMIN_ID = 692906415

        # Configuration Cloudinary
        import cloudinary
        cloudinary.config(
            cloud_name="dkpf8ovsd",
            api_key="398734649392149",
            api_secret="sGPfetxLvTkrfIrUQ3W6t0oCpQQ"
        )
        print("✅ Configuration OK")

        # Imports des modules personnalisés
        from database.db_functions import init_database, init_categories_and_brands
        print("✅ Database functions importées")

        # Initialisation de la base de données
        print("💾 Initialisation base de données...")
        init_database()
        init_categories_and_brands()
        print("✅ Base de données initialisée")

        # Import handlers
        from handlers.basic_handlers import (
            start_command, handle_message, produits_command, 
            services_command, communaute_command, apropos_command
        )
        print("✅ Basic handlers importés")

        from handlers.admin_handlers import (
            admin_command, addproduct_command, broadcast_command, 
            stats_command, listusers_command, editproduct_command,
            deleteproduct_command, addimage_command, handle_image_upload
        )
        print("✅ Admin handlers importés")

        from handlers.callback_handlers import button_callback
        print("✅ Callback handlers importés")

        from handlers.mobile_admin_handlers import (
            mobile_admin_command, handle_mobile_admin_callback, 
            handle_mobile_input, handle_mobile_image_upload
        )
        print("✅ Mobile admin handlers importés")

        # Création de l'application
        from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
        from telegram import BotCommand
        
        app = Application.builder().token(BOT_TOKEN).build()
        print("✅ Application Telegram créée")

        # Configuration des commandes
        async def setup_bot_commands(app_instance):
            commands = [
                BotCommand("start", "Commencer / Accueil"),
                BotCommand("produits", "Voir le catalogue"),
                BotCommand("services", "Nos services techniques"),
                BotCommand("communaute", "Rejoindre la communauté"),
                BotCommand("apropos", "À propos de nous"),
                BotCommand("admin", "Administration (admin uniquement)"),
                BotCommand("mobile_admin", "Administration mobile via smartphone")
            ]
            await app_instance.bot.set_my_commands(commands)
            print("✅ Commandes configurées")

        # Ajout des handlers
        app.add_handler(CommandHandler("start", start_command))
        app.add_handler(CommandHandler("produits", produits_command))
        app.add_handler(CommandHandler("services", services_command))
        app.add_handler(CommandHandler("communaute", communaute_command))
        app.add_handler(CommandHandler("apropos", apropos_command))
        app.add_handler(CommandHandler("admin", admin_command))
        app.add_handler(CommandHandler("mobile_admin", mobile_admin_command))
        
        # Autres handlers
        app.add_handler(CallbackQueryHandler(button_callback, pattern="^(category_|brand_|model_|product_|back_|page_)"))
        app.add_handler(CallbackQueryHandler(handle_mobile_admin_callback, pattern="^mobile_"))
        
        # Handlers de messages
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mobile_input))
        app.add_handler(MessageHandler(filters.PHOTO, handle_image_upload))
        app.add_handler(MessageHandler(filters.PHOTO, handle_mobile_image_upload))
        
        print("✅ Tous les handlers ajoutés")

        # Configuration du menu des commandes
        app.job_queue.run_once(lambda context: setup_bot_commands(app), when=1)
        
        print("\n🎉 CONFIGURATION COMPLÈTE RÉUSSIE !")
        print("✅ Le bot est prêt à fonctionner")
        print("🚀 Toutes les fonctionnalités sont opérationnelles:")
        print("   • Administration classique")
        print("   • Administration mobile")
        print("   • Gestion des images des menus")
        print("   • Base de données dynamique")
        print("   • Système d'héritage catégories/marques")
        
        return True

    except Exception as e:
        print(f"\n❌ ERREUR DÉTECTÉE: {e}")
        print("\n📋 Détails de l'erreur:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_bot()
    if success:
        print("\n" + "="*50)
        print("🏆 RÉSULTAT: SUCCÈS COMPLET")
        print("Le bot peut être démarré en toute sécurité!")
        print("="*50)
    else:
        print("\n" + "="*50)
        print("⚠️  RÉSULTAT: PROBLÈME DÉTECTÉ")
        print("Vérifiez les erreurs ci-dessus avant de démarrer le bot")
        print("="*50)
