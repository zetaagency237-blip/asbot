"""
Handlers pour les callbacks des boutons (menus interactifs)
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes
import re
from notifications.admin_notifications import notify_admin_product_interest, notify_admin_service_request, notify_admin_contact_request
from database.db_functions import get_service_image

def escape_markdown(text):
    """Échapper les caractères spéciaux pour Markdown"""
    if not text:
        return ""
    # Remplacer les caractères qui peuvent poser problème
    return re.sub(r'[*_\[\]()~`>#+=|{}.!-]', '', str(text))
from database.db_functions import (
    get_products_by_category_and_brand, is_admin, get_user_stats, 
    get_all_users, get_all_products, products_collection
)
from menus.menu_functions import (
    create_main_menu, create_products_menu, create_services_menu, 
    create_brands_menu, create_models_menu, create_admin_menu, create_product_admin_menu,
    create_image_admin_menu
)
from datetime import datetime

async def smart_edit_message(query, text, reply_markup=None, parse_mode='Markdown'):
    """Édite intelligemment un message selon son type (photo ou texte)"""
    try:
        if query.message.photo:
            # Si le message actuel a une photo, envoyer un nouveau message texte
            new_message = await query.message.reply_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
            # Supprimer l'ancien message photo
            await query.message.delete()
            return new_message
        else:
            # Vérifier si le contenu est différent avant de modifier
            current_text = query.message.text or query.message.caption or ""
            if current_text.strip() == text.strip():
                print("📝 DEBUG: Contenu identique, modification du clavier seulement")
                return await query.edit_message_reply_markup(reply_markup=reply_markup)
            
            # Si c'est un message texte, le modifier normalement
            return await query.edit_message_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
    except Exception as e:
        error_msg = str(e).lower()
        print(f"❌ Erreur smart_edit_message: {e}")
        
        # Gestion spéciale pour "message is not modified"
        if "message is not modified" in error_msg:
            print("📝 Message identique détecté, pas de modification nécessaire")
            return query.message
        
        # Fallback: envoyer un nouveau message
        try:
            await query.message.delete()
            return await query.message.reply_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )
        except:
            # Si la suppression échoue, juste répondre
            return await query.message.reply_text(
                text=text,
                parse_mode=parse_mode,
                reply_markup=reply_markup
            )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les callbacks des boutons"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "main_menu":
        user_id = query.from_user.id
        await query.edit_message_text(
            text="*Menu Principal*\n\nUtilisez les commandes :\n/produits\n/services\n/communaute\n/apropos",
            parse_mode='Markdown',
            reply_markup=create_main_menu(user_id)
        )
    
    elif data == "produits":
        # Récupérer l'image du catalogue depuis la base de données ou utiliser une image par défaut
        from database.db_functions import get_catalog_image
        
        text = "*Catalogue Produits*\n\nSélectionnez une catégorie :"
        catalog_image_url = get_catalog_image()
        
        # Si on a une image pour le catalogue, l'afficher
        if catalog_image_url:
            try:
                if query.message.photo:
                    # Modifier un message photo existant
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=catalog_image_url,
                            caption=text,
                            parse_mode='Markdown'
                        ),
                        reply_markup=create_products_menu()
                    )
                else:
                    # Modifier un message texte en message photo
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=catalog_image_url,
                            caption=text,
                            parse_mode='Markdown'
                        ),
                        reply_markup=create_products_menu()
                    )
                print(f"✅ DEBUG: Image catalogue affichée avec succès")
            except Exception as e:
                print(f"❌ Erreur affichage image catalogue: {e}")
                await smart_edit_message(query, text, create_products_menu())
        else:
            # Pas d'image, message texte normal
            await smart_edit_message(query, text, create_products_menu())
    
    elif data == "services":
        await query.edit_message_text(
            text="*Nos Services*\n\nChoisissez le service dont vous avez besoin :",
            parse_mode='Markdown',
            reply_markup=create_services_menu()
        )
    
    elif data == "communaute":
        await query.edit_message_text(
            text="*Communauté Anonyme Smartphone*\n\n"
                 "Rejoignez notre communauté pour :\n"
                 "• Échanger avec d'autres utilisateurs\n"
                 "• Recevoir des conseils d'experts\n"
                 "• Être informé des nouveautés\n"
                 "• Bénéficier d'offres exclusives\n\n"
                 "Lien du groupe : [Rejoindre la communauté](https://t.me/votre_groupe)",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retour", callback_data="main_menu")]])
        )
    
    elif data.startswith("category_"):
        # Nouveau système avec catégories dynamiques et images
        from database.db_functions import get_category_by_id
        
        category_id = data.replace("category_", "")
        category = get_category_by_id(category_id)
        
        if category:
            # Stocker la catégorie sélectionnée pour la suite (utiliser l'ID)
            context.user_data['selected_category'] = category_id
            
            # Préparer le message avec l'image si disponible
            text = f"*{category['name']}*\n\nSélectionnez une marque :"
            
            # Si la catégorie a une image, modifier le message avec la photo
            if category.get('image_url'):
                try:
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=category['image_url'],
                            caption=text,
                            parse_mode='Markdown'
                        ),
                        reply_markup=create_brands_menu()
                    )
                except Exception as e:
                    print(f"❌ Erreur modification image catégorie: {e}")
                    # Fallback sur message texte si l'image échoue
                    await query.edit_message_text(
                        text=text,
                        parse_mode='Markdown',
                        reply_markup=create_brands_menu()
                    )
            else:
                # Pas d'image, message texte normal
                await query.edit_message_text(
                    text=text,
                    parse_mode='Markdown',
                    reply_markup=create_brands_menu()
                )
        else:
            await query.edit_message_text(
                text="❌ Catégorie introuvable",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retour", callback_data="produits")]])
            )
    
    elif data in ["pochettes", "magsafe", "gadgets", "packs"]:
        # Anciens callbacks pour compatibilité - rediriger vers les nouveaux
        category_mapping = {
            "pochettes": "pochettes",
            "magsafe": "chargeurs_magsafe", 
            "gadgets": "autres_gadgets",
            "packs": "packs"
        }
        
        mapped_id = category_mapping.get(data, "pochettes")
        # Rediriger vers le nouveau système
        query.data = f"category_{mapped_id}"
        return await button_callback(update, context)
    
    elif data in ["deblocage", "desimlockage", "declonage", "cas_particulier"]:
        service_names = {
            "deblocage": "Déblocage",
            "desimlockage": "Désimlocage",
            "declonage": "Déclonage", 
            "cas_particulier": "Cas Particuliers"
        }
        
        service_emojis = {
            "deblocage": "🔓",
            "desimlockage": "📱",
            "declonage": "🔄",
            "cas_particulier": "⚠️"
        }
        
        service_name = service_names.get(data, "Service")
        service_emoji = service_emojis.get(data, "🔧")
        
        # Récupérer l'image du service
        service_image_url = get_service_image(data)
        
        message_text = f"{service_emoji} *{service_name}*\n\n" \
                      f"Vous êtes intéressé par notre service {service_name}.\n\n" \
                      f"Un de nos experts vous contactera rapidement pour vous proposer une solution adaptée.\n\n" \
                      f"💡 *Notre équipe est là pour vous aider !*"
        
        keyboard = [
            [InlineKeyboardButton("📞 Être contacté", callback_data="contact")],
            [InlineKeyboardButton("⬅️ Retour Services", callback_data="services")]
        ]
        
        # Afficher avec image si disponible
        if service_image_url:
            try:
                await query.edit_message_media(
                    media=InputMediaPhoto(
                        media=service_image_url,
                        caption=message_text,
                        parse_mode='Markdown'
                    ),
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
            except Exception as e:
                print(f"❌ Erreur affichage image service {data}: {e}")
                # Fallback vers message texte
                await query.edit_message_text(
                    message_text,
                    parse_mode='Markdown',
                    reply_markup=InlineKeyboardMarkup(keyboard)
                )
        else:
            # Pas d'image, affichage texte normal
            await query.edit_message_text(
                message_text,
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        # 🔔 NOTIFICATION ADMIN - Demande de service
        user_info = {
            'id': query.from_user.id,
            'first_name': query.from_user.first_name,
            'username': query.from_user.username or 'Pas de username'
        }
        
        # Envoyer notification à l'admin
        await notify_admin_service_request(
            context=context,
            user_info=user_info,
            service_type=data
        )
        
        await smart_edit_message(
            query,
            f"*{service_names[data]}*\n\n"
            f"Pour obtenir ce service, veuillez nous contacter directement :\n"
            f"Téléphone : \\+XXX XXX XXX XXX\n"
            f"Telegram : `@anonyme_smartphone`\n"
            f"Email : contact@anonymesmartphone\\.com",
            InlineKeyboardMarkup([[InlineKeyboardButton("Retour", callback_data="services")]])
        )
    
    elif data in ["iphone", "samsung", "xiaomi", "huawei", "pixel"]:
        # Récupérer les vraies informations de la marque depuis la base
        from database.db_functions import get_brand_by_id, get_category_by_id
        
        print(f"🔍 DEBUG: Callback marque '{data}' reçu")
        
        # Stocker la marque sélectionnée
        context.user_data['selected_brand'] = data
        category_id = context.user_data.get('selected_category', 'pochettes')
        
        print(f"🔍 DEBUG: Category ID = {category_id}")
        
        # Récupérer les objets complets depuis la base
        brand = get_brand_by_id(data)
        category = get_category_by_id(category_id)
        
        print(f"🔍 DEBUG: Brand trouvée = {brand is not None}")
        if brand:
            print(f"🔍 DEBUG: Brand name = {brand['name']}")
            image_url = brand.get('image_url', 'AUCUNE')
            print(f"🔍 DEBUG: Brand image_url = {image_url}")
            if image_url and image_url != 'AUCUNE':
                print(f"🔍 DEBUG: URL complète = {image_url}")
                print(f"🔍 DEBUG: URL valide = {'http' in image_url.lower()}")
        else:
            print(f"❌ DEBUG: BRAND iPhone NON TROUVÉE!")
        
        print(f"🔍 DEBUG: Category trouvée = {category is not None}")
        if category:
            print(f"🔍 DEBUG: Category name = {category['name']}")
        
        # Préparer le texte avec les vrais noms
        brand_name = brand['name'] if brand else data.title()
        category_name = category['name'] if category else category_id.title()
        
        text = f"*{brand_name}* - {category_name}\n\nSélectionnez le modèle :"
        print(f"🔍 DEBUG: Texte généré = {text}")
        
        # Vérification détaillée de l'image
        has_image = brand and brand.get('image_url') and brand.get('image_url') not in ['', 'AUCUNE', None]
        print(f"🔍 DEBUG: has_image = {has_image}")
        
        # Si la marque a une image, l'afficher
        if has_image:
            image_url = brand['image_url']
            print(f"✅ DEBUG: Tentative affichage image marque: {image_url}")
            print(f"✅ DEBUG: Type message actuel: {'photo' if query.message.photo else 'text'}")
            
            try:
                if query.message.photo:
                    # Modifier un message photo existant
                    print("🔄 DEBUG: Modification d'un message photo existant")
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=image_url,
                            caption=text,
                            parse_mode='Markdown'
                        ),
                        reply_markup=create_models_menu(data)
                    )
                else:
                    # Modifier un message texte en message photo
                    print("🔄 DEBUG: Modification d'un message texte en photo")
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=image_url,
                            caption=text,
                            parse_mode='Markdown'
                        ),
                        reply_markup=create_models_menu(data)
                    )
                print(f"✅ DEBUG: Image marque affichée avec succès")
            except Exception as e:
                print(f"❌ Erreur affichage image marque: {e}")
                print(f"❌ Type d'erreur: {type(e)}")
                await smart_edit_message(query, text, create_models_menu(data))
        else:
            print(f"📷 DEBUG: Pas d'image pour cette marque")
            if brand:
                print(f"📷 DEBUG: Image URL vide ou invalide: '{brand.get('image_url', 'NONE')}'")
            await smart_edit_message(query, text, create_models_menu(data))

    
    elif data.startswith("model_"):
        # Gestion de la sélection d'un modèle
        model = data.replace("model_", "")
        category = context.user_data.get('selected_category', 'pochettes')
        brand = context.user_data.get('selected_brand', 'iphone')
        
        # Récupérer les produits pour ce modèle spécifique
        from database.db_functions import get_products_by_category_brand_model
        products = get_products_by_category_brand_model(category, brand, model)
        
        brand_names = {
            "iphone": "iPhone",
            "samsung": "Samsung", 
            "xiaomi": "Xiaomi",
            "huawei": "Huawei",
            "pixel": "Google Pixel"
        }
        
        # 🔔 NOTIFICATION ADMIN - Demande de produit
        user_info = {
            'id': query.from_user.id,
            'first_name': query.from_user.first_name,
            'username': query.from_user.username or 'Pas de username'
        }
        
        # Préparer le nom du modèle pour la notification
        brand_name = brand_names.get(brand, brand)
        model_display = model.replace('_', ' ').title()
        model_name = f"{brand_name} {model_display}"
        
        # Récupérer le prix du premier produit s'il existe
        model_price = None
        if products and len(products) > 0:
            model_price = products[0].get('price')
        
        # Envoyer notification à l'admin
        await notify_admin_product_interest(
            context=context,
            user_info=user_info,
            model_name=model_name,
            model_price=model_price
        )
        
        if products:
            product_text = f"*{brand_names[brand]}* - {model.replace('_', ' ').title()}\n\n"
            
            for i, product in enumerate(products[:3], 1):
                product_text += f"{i}\\. {escape_markdown(product['name'])}\n"
                product_text += f"Prix : {product['price']}€\n\n"
            
            product_text += "*Contact :*\n"
            product_text += "Telegram : `@anonyme_smartphone`"
        else:
            product_text = f"*{brand_names[brand]}* - {model.replace('_', ' ').title()}\n\n"
            product_text += "Aucun produit disponible pour ce modèle\\.\n\n"
            product_text += "*Contact :*\n"
            product_text += "Telegram : `@anonyme_smartphone`"
        
        try:
            await smart_edit_message(
                query,
                product_text,
                InlineKeyboardMarkup([
                    [InlineKeyboardButton("Autres modèles", callback_data=brand)],
                    [InlineKeyboardButton("Retour au catalogue", callback_data="produits")]
                ])
            )
        except Exception as e:
            print(f"Erreur affichage produits: {e}")
            # Fallback si edit échoue
            try:
                await query.message.delete()
                await context.bot.send_message(
                    chat_id=query.message.chat_id,
                    text=product_text,
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("Autres modèles", callback_data=brand)],
                        [InlineKeyboardButton("Retour au catalogue", callback_data="produits")]
                    ])
                )
            except:
                await query.answer("Erreur lors de l'affichage des produits", show_alert=True)
    
    elif data == "back_to_brands":
        # Retour vers le menu des marques avec support des images
        from database.db_functions import get_category_by_id
        
        category_id = context.user_data.get('selected_category', 'pochettes')
        category = get_category_by_id(category_id)
        
        if category:
            text = f"*{category['name']}*\n\nSélectionnez une marque :"
            
            # Si la catégorie a une image, l'afficher
            if category.get('image_url'):
                try:
                    await query.edit_message_media(
                        media=InputMediaPhoto(
                            media=category['image_url'],
                            caption=text,
                            parse_mode='Markdown'
                        ),
                        reply_markup=create_brands_menu()
                    )
                except Exception as e:
                    print(f"❌ Erreur retour avec image: {e}")
                    await smart_edit_message(query, text, create_brands_menu())
            else:
                await smart_edit_message(query, text, create_brands_menu())
        else:
            # Fallback si catégorie introuvable
            await smart_edit_message(query, "*Pochettes*\n\nSélectionnez une marque :", create_brands_menu())

    elif data.startswith("back_to_"):
        # Gestion des boutons de retour vers une catégorie
        category = data.replace("back_to_", "")
        category_names = {
            "pochettes": "Pochettes",
            "magsafe": "Chargeurs MagSafe", 
            "gadgets": "Autres Gadgets",
            "packs": "Packs"
        }
        context.user_data['selected_category'] = category
        
        await query.edit_message_text(
            text=f"*{category_names[category]}*\n\nSélectionnez une marque :",
            parse_mode='Markdown',
            reply_markup=create_brands_menu()
        )
    
    elif data == "apropos":
        await query.edit_message_text(
            text="*À propos d'Anonyme Smartphone*\n\n"
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
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Retour", callback_data="main_menu")]])
        )
    
    # === ADMINISTRATION ===
    elif data == "admin_menu":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé. Vous n'êtes pas administrateur.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="⚙️ *PANNEAU D'ADMINISTRATION*\n\nChoisissez une option :",
            parse_mode='Markdown',
            reply_markup=create_admin_menu()
        )
    
    elif data == "admin_stats":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        stats = get_user_stats()
        products_count = products_collection.count_documents({})
        
        await query.edit_message_text(
            text=f"📊 *STATISTIQUES*\n\n"
                 f"👥 *Utilisateurs :*\n"
                 f"• Total : {stats['total']} utilisateurs\n"
                 f"• Aujourd'hui : {stats['today']} nouveaux\n\n"
                 f"📱 *Produits :*\n"
                 f"• Total : {products_count} produits\n\n"
                 f"🕒 Dernière mise à jour : {datetime.now().strftime('%H:%M')}",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Actualiser", callback_data="admin_stats")],
                [InlineKeyboardButton("⬅️ Retour Admin", callback_data="admin_menu")]
            ])
        )
    
    elif data == "admin_users":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        users = get_all_users()
        user_text = "👥 *GESTION UTILISATEURS*\n\n"
        
        if users:
            for i, user in enumerate(users[:10], 1):  # Limiter à 10 utilisateurs
                user_text += f"{i}. *{user['prenom']}* (ID: {user['user_id']})\n"
                user_text += f"   📅 Inscrit : {user['created_at'].strftime('%d/%m/%Y')}\n\n"
        else:
            user_text += "Aucun utilisateur trouvé."
            
        await query.edit_message_text(
            text=user_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour Admin", callback_data="admin_menu")]])
        )
    
    elif data == "admin_products":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="📱 *GESTION DES PRODUITS*\n\nChoisissez une action :",
            parse_mode='Markdown',
            reply_markup=create_product_admin_menu()
        )
    
    elif data == "list_products":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        products = get_all_products()
        product_text = "📋 *LISTE DES PRODUITS*\n\n"
        
        if products:
            for i, product in enumerate(products[:8], 1):  # Limiter à 8 produits
                product_text += f"{i}. *{product['name']}*\n"
                product_text += f"   💰 {product['price']}€ | 🏷️ {product['category']} | 📱 {product['brand']}\n\n"
        else:
            product_text += "Aucun produit trouvé."
            
        await query.edit_message_text(
            text=product_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_products")]])
        )
    
    elif data == "admin_broadcast":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="💬 *DIFFUSION DE MESSAGE*\n\n"
                 "Pour envoyer un message à tous les utilisateurs, utilisez la commande :\n\n"
                 "`/broadcast Votre message ici`\n\n"
                 "⚠️ Utilisez cette fonction avec précaution !",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour Admin", callback_data="admin_menu")]])
        )
    
    elif data == "admin_images":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="🖼️ *GESTION DES IMAGES*\n\n"
                 "Gérez les images de vos produits avec Cloudinary :\n\n"
                 "• **Ajouter** : Associer une image à un produit\n"
                 "• **Modifier** : Changer l'image d'un produit\n"
                 "• **Lister** : Voir tous les produits avec/sans images\n"
                 "• **Supprimer** : Retirer l'image d'un produit\n\n"
                 "💡 *Conseil* : Utilisez `/addimage [ID]` pour un ajout rapide !",
            parse_mode='Markdown',
            reply_markup=create_image_admin_menu()
        )
    
    elif data == "add_image":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        products = get_all_products()
        if not products:
            await query.edit_message_text(
                text="❌ *Aucun produit trouvé*\n\nAjoutez d'abord des produits avant de gérer les images.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_images")]])
            )
            return
        
        product_text = "🖼️ *AJOUTER UNE IMAGE*\n\n"
        product_text += "Utilisez : `/addimage [ID_produit]`\n\n"
        product_text += "📋 *Produits disponibles :*\n\n"
        
        for i, product in enumerate(products[:8], 1):
            has_image = "🖼️" if product.get('image_url') else "📷"
            product_text += f"{i}. {has_image} *{product['name']}*\n"
            product_text += f"   🆔 ID: `{str(product['_id'])}`\n"
            product_text += f"   💰 Prix: {product['price']}€\n\n"
        
        await query.edit_message_text(
            text=product_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_images")]])
        )
    
    elif data == "modify_image":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        products_with_images = [p for p in get_all_products() if p.get('image_url')]
        
        if not products_with_images:
            await query.edit_message_text(
                text="📷 *Aucune image à modifier*\n\nAucun produit n'a d'image associée pour le moment.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_images")]])
            )
            return
        
        product_text = "🔄 *MODIFIER UNE IMAGE*\n\n"
        product_text += "Utilisez : `/addimage [ID_produit]` pour remplacer\n\n"
        
        for i, product in enumerate(products_with_images[:6], 1):
            product_text += f"{i}. 🖼️ *{product['name']}*\n"
            product_text += f"   🆔 ID: `{str(product['_id'])}`\n"
            product_text += f"   🔗 Image: Oui\n\n"
        
        await query.edit_message_text(
            text=product_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_images")]])
        )
    
    elif data == "list_images":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        products = get_all_products()
        products_with_images = [p for p in products if p.get('image_url')]
        products_without_images = [p for p in products if not p.get('image_url')]
        
        product_text = "📋 *ÉTAT DES IMAGES*\n\n"
        product_text += f"🖼️ **Avec images** : {len(products_with_images)}\n"
        product_text += f"📷 **Sans images** : {len(products_without_images)}\n\n"
        
        if products_with_images:
            product_text += "*Produits avec images :*\n"
            for i, product in enumerate(products_with_images[:5], 1):
                product_text += f"{i}. ✅ {product['name']}\n"
        
        if products_without_images:
            product_text += f"\n*Produits sans images :*\n"
            for i, product in enumerate(products_without_images[:5], 1):
                product_text += f"{i}. ❌ {product['name']}\n"
        
        await query.edit_message_text(
            text=product_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_images")]])
        )
    
    elif data == "delete_image":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="🗑️ *SUPPRIMER UNE IMAGE*\n\n"
                 "Pour supprimer l'image d'un produit, utilisez :\n\n"
                 "`/editproduct [ID] image_url \"\"`\n\n"
                 "Cela supprimera le lien vers l'image du produit.\n\n"
                 "💡 *Note* : L'image restera sur Cloudinary mais ne sera plus associée au produit.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_images")]])
        )
    
    elif data == "add_product":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="➕ *AJOUTER UN PRODUIT*\n\n"
                 "Utilisez la commande :\n\n"
                 "`/addproduct nom catégorie marque modèle prix description`\n\n"
                 "**Exemple :**\n"
                 "`/addproduct \"Coque iPhone\" pochettes iphone \"15 Pro\" 25.99 \"Coque premium\"`\n\n"
                 "**Catégories :** pochettes, magsafe, gadgets, packs\n"
                 "**Marques :** iphone, samsung, xiaomi, huawei",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_products")]])
        )
    
    elif data == "edit_product":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="✏️ *MODIFIER UN PRODUIT*\n\n"
                 "Utilisez la commande :\n\n"
                 "`/editproduct [ID] [champ] [nouvelle_valeur]`\n\n"
                 "**Exemples :**\n"
                 "`/editproduct 6543210abc name \"Nouveau nom\"`\n"
                 "`/editproduct 6543210abc price 35.99`\n\n"
                 "**Champs :** name, price, description, category, brand, model\n\n"
                 "💡 Pour voir la liste des produits : `/editproduct`",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_products")]])
        )
    
    elif data == "delete_product_menu":
        user_id = query.from_user.id
        if not is_admin(user_id):
            await query.answer("❌ Accès refusé.", show_alert=True)
            return
            
        await query.edit_message_text(
            text="🗑️ *SUPPRIMER UN PRODUIT*\n\n"
                 "Utilisez la commande :\n\n"
                 "`/deleteproduct [ID]`\n\n"
                 "**Exemple :**\n"
                 "`/deleteproduct 6543210abcdef`\n\n"
                 "⚠️ **Attention !** Cette action est irréversible.\n\n"
                 "💡 Pour voir la liste des produits : `/deleteproduct`",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ Retour", callback_data="admin_products")]])
        )
    
def get_category_name_from_id(category_id):
    """Convertit un ID de catégorie en nom pour la compatibilité"""
    from database.db_functions import get_category_by_id
    
    category = get_category_by_id(category_id)
    if category:
        return category['name']
    
    # Fallback pour les anciens IDs
    category_mapping = {
        "pochettes": "Pochettes",
        "chargeurs_magsafe": "Chargeurs MagSafe",
        "magsafe": "Chargeurs MagSafe", 
        "autres_gadgets": "Autres Gadgets",
        "gadgets": "Autres Gadgets",
        "packs": "Packs"
    }
    return category_mapping.get(category_id, "Pochettes")
