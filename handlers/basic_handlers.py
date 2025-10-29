"""
Handlers pour les commandes de base du bot
"""
from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_functions import get_user, add_user, update_user_activity, get_catalog_image, get_services_image
from menus.menu_functions import create_main_menu, create_products_menu, create_services_menu
from notifications.admin_notifications import notify_admin_new_user, notify_admin_contact_request

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /start"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if user is None:
        # Nouvel utilisateur
        await update.message.reply_text(
            "*Bienvenue chez Anonyme Smartphone*\n\n"
            "Votre spécialiste des téléphones\n\n"
            "Veuillez saisir votre prénom et l'envoyer :",
            parse_mode='Markdown'
        )
        context.user_data['awaiting_name'] = True
    else:
        # Utilisateur existant
        prenom = user['prenom']
        update_user_activity(user_id)
        
        # Créer le menu admin si c'est l'admin
        admin_menu = create_main_menu(user_id)
        
        # Récupérer le logo d'accueil
        from database.db_functions import get_welcome_logo
        welcome_logo = get_welcome_logo()
        
        message_text = (
            f"Bonjour *{prenom.title()}* !\n\n"
            f"Ravi de vous retrouver chez Anonyme Smartphone\n\n"
            f"Votre spécialiste de confiance pour tous vos besoins mobiles\n\n"
            f"Pour découvrir nos produits et services, appuyez simplement sur le petit bouton menu à côté de votre clavier"
        )
        
        # Si on a un logo, essayer de l'envoyer avec le texte
        if welcome_logo and welcome_logo.strip():
            try:
                print(f"🏠 Tentative affichage logo d'accueil: {welcome_logo}")
                await update.message.reply_photo(
                    photo=welcome_logo,
                    caption=message_text,
                    parse_mode='Markdown',
                    reply_markup=admin_menu
                )
                print("✅ Logo d'accueil affiché avec succès")
            except Exception as e:
                print(f"❌ Erreur affichage logo d'accueil: {e}")
                # En cas d'erreur, envoyer juste le texte
                await update.message.reply_text(
                    message_text,
                    parse_mode='Markdown',
                    reply_markup=admin_menu
                )
        else:
            # Pas de logo, envoyer juste le texte
            await update.message.reply_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=admin_menu
            )

async def produits_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /produits"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if user is None:
        await update.message.reply_text(
            "*Bienvenue chez Anonyme Smartphone*\n\n"
            "Veuillez d'abord vous enregistrer avec /start",
            parse_mode='Markdown'
        )
        return
    
    update_user_activity(user_id)
    
    # Récupérer l'image du catalogue
    catalog_image_url = get_catalog_image()
    
    message_text = "*Catalogue Produits*\n\nSélectionnez une catégorie :"
    
    if catalog_image_url:
        try:
            await update.message.reply_photo(
                photo=catalog_image_url,
                caption=message_text,
                parse_mode='Markdown',
                reply_markup=create_products_menu()
            )
        except Exception as e:
            print(f"❌ Erreur affichage image catalogue: {e}")
            # Fallback vers message texte si l'image ne fonctionne pas
            await update.message.reply_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=create_products_menu()
            )
    else:
        # Pas d'image catalogue, affichage texte normal
        await update.message.reply_text(
            message_text,
            parse_mode='Markdown',
            reply_markup=create_products_menu()
        )

async def services_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /services"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if user is None:
        await update.message.reply_text(
            "*Bienvenue chez Anonyme Smartphone*\n\n"
            "Veuillez d'abord vous enregistrer avec /start",
            parse_mode='Markdown'
        )
        return
    
    update_user_activity(user_id)
    
    # Récupérer l'image des services
    services_image_url = get_services_image()
    
    message_text = "*Nos Services*\n\nChoisissez le service dont vous avez besoin :"
    
    if services_image_url:
        try:
            await update.message.reply_photo(
                photo=services_image_url,
                caption=message_text,
                parse_mode='Markdown',
                reply_markup=create_services_menu()
            )
        except Exception as e:
            print(f"❌ Erreur affichage image services: {e}")
            # Fallback vers message texte si l'image ne fonctionne pas
            await update.message.reply_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=create_services_menu()
            )
    else:
        # Pas d'image services, affichage texte normal
        await update.message.reply_text(
            message_text,
            parse_mode='Markdown',
            reply_markup=create_services_menu()
        )

async def communaute_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /communaute"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if user is None:
        await update.message.reply_text(
            "*Bienvenue chez Anonyme Smartphone*\n\n"
            "Veuillez d'abord vous enregistrer avec /start",
            parse_mode='Markdown'
        )
        return
    
    update_user_activity(user_id)
    await update.message.reply_text(
        "*Communauté Anonyme Smartphone*\n\n"
        "Rejoignez notre communauté pour :\n"
        "• Échanger avec d'autres utilisateurs\n"
        "• Recevoir des conseils d'experts\n"
        "• Être informé des nouveautés\n"
        "• Bénéficier d'offres exclusives\n\n"
        "Lien du groupe : [Rejoindre la communauté](https://t.me/votre_groupe)",
        parse_mode='Markdown'
    )

async def apropos_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /apropos"""
    user_id = update.effective_user.id
    user = get_user(user_id)
    
    if user is None:
        await update.message.reply_text(
            "*Bienvenue chez Anonyme Smartphone*\n\n"
            "Veuillez d'abord vous enregistrer avec /start",
            parse_mode='Markdown'
        )
        return
    
    update_user_activity(user_id)
    await update.message.reply_text(
        "*À propos d'Anonyme Smartphone*\n\n"
        "Nous sommes votre spécialiste en :\n"
        "• Accessoires pour smartphones\n"
        "• Services techniques spécialisés\n"
        "• Solutions professionnelles\n\n"
        "Notre mission : vous offrir les meilleurs produits et services "
        "pour vos appareils mobiles.\n\n"
        "**Localisation :** [Votre adresse]\n"
        "**Horaires :** Lun-Sam 9h-18h\n\n"
        "*Contact :*\n"
        "**Telegram :** @anonyme_smartphone\n"
        "**Email :** contact@anonymesmartphone.com",
        parse_mode='Markdown'
    )
    
    # Notifier l'admin de la demande d'informations de contact
    await notify_admin_contact_request(context, update.effective_user, user['name'])

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les messages texte"""
    user_id = update.effective_user.id
    text = update.message.text.strip()
    
    # Vérifier si on attend le prénom
    if context.user_data.get('awaiting_name'):
        if len(text) > 0 and text.isalpha():
            # Enregistrer l'utilisateur
            add_user(user_id, text)
            context.user_data['awaiting_name'] = False
            
            # Notifier l'admin du nouvel utilisateur
            await notify_admin_new_user(context, update.effective_user, text)
            
            await update.message.reply_text(
                f"Parfait *{text.title()}* !\n\n"
                f"Félicitations, vous faites maintenant partie de la famille Anonyme Smartphone\n\n"
                f"Découvrez tout ce que nous avons à vous offrir en appuyant sur le bouton menu juste à côté de votre clavier",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text(
                "Veuillez saisir un prénom valide (lettres uniquement) :"
            )
        return
    
    # Vérifier si l'utilisateur est authentifié
    user = get_user(user_id)
    if user is None:
        await update.message.reply_text(
            "*Bienvenue chez Anonyme Smartphone*\n\n"
            "Votre spécialiste des téléphones\n\n"
            "Veuillez saisir votre prénom et l'envoyer :",
            parse_mode='Markdown'
        )
        context.user_data['awaiting_name'] = True
    else:
        # Utilisateur authentifié mais message non reconnu
        prenom = user['prenom']
        update_user_activity(user_id)
        await update.message.reply_text(
            f"Bonjour *{prenom.title()}* !\n\n"
            f"Comment puis-je vous aider aujourd'hui ?\n\n"
            f"Tout ce dont vous avez besoin se trouve dans le petit menu à côté de votre clavier",
            parse_mode='Markdown'
        )
