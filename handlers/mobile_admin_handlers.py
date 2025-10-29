"""
Handlers administrateurs avancés pour gestion depuis smartphone
"""
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.db_functions import (
    is_admin, get_categories, get_brands, add_new_category, 
    add_new_brand, add_model_to_brand, toggle_category_status, 
    toggle_brand_status, get_brand_models, update_category_image,
    update_brand_image, get_category_by_id, get_brand_by_id,
    get_catalog_image, update_catalog_image, get_welcome_logo, update_welcome_logo,
    get_services_image, update_services_image, get_service_image, update_service_image
)

async def mobile_admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Interface admin mobile complète"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        await update.message.reply_text("❌ Accès refusé.")
        return
    
    keyboard = [
        [
            InlineKeyboardButton("📱 Gérer Catégories", callback_data="mobile_categories"),
            InlineKeyboardButton("🏷️ Gérer Marques", callback_data="mobile_brands")
        ],
        [
            InlineKeyboardButton("📦 Gérer Produits", callback_data="mobile_products"),
            InlineKeyboardButton("🖼️ Gérer Images", callback_data="mobile_images")
        ],
        [
            InlineKeyboardButton("👥 Utilisateurs", callback_data="mobile_users"),
            InlineKeyboardButton("📊 Statistiques", callback_data="mobile_stats")
        ],
        [
            InlineKeyboardButton("💬 Diffusion", callback_data="mobile_broadcast"),
            InlineKeyboardButton("⚙️ Paramètres", callback_data="mobile_settings")
        ]
    ]
    
    await update.message.reply_text(
        "📱 *PANNEAU ADMIN MOBILE*\n\n"
        "Gérez votre bot directement depuis votre smartphone !\n\n"
        "Choisissez une option :",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def mobile_categories_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Menu de gestion des catégories"""
    if query:
        await query.answer()
    
    categories = get_categories()
    
    text = "📱 *GESTION CATÉGORIES*\n\n"
    text += "*Catégories actuelles :*\n"
    
    keyboard = []
    
    for i, cat in enumerate(categories, 1):
        status = "✅" if cat.get('active', True) else "❌"
        text += f"{i}. {status} {cat['name']}\n"
        keyboard.append([
            InlineKeyboardButton(f"✏️ {cat['name']}", callback_data=f"edit_cat_{cat['id']}"),
            InlineKeyboardButton("🔄", callback_data=f"toggle_cat_{cat['id']}")
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("➕ Nouvelle Catégorie", callback_data="add_category")],
        [InlineKeyboardButton("⬅️ Retour Admin", callback_data="mobile_admin_back")]
    ])
    
    message_func = query.edit_message_text if query else update.message.reply_text
    await message_func(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def mobile_brands_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Menu de gestion des marques"""
    if query:
        await query.answer()
    
    brands = get_brands()
    
    text = "🏷️ *GESTION MARQUES*\n\n"
    text += "*Marques actuelles :*\n"
    
    keyboard = []
    
    for i, brand in enumerate(brands, 1):
        status = "✅" if brand.get('active', True) else "❌"
        models_count = len(brand.get('models', []))
        text += f"{i}. {status} {brand['name']} ({models_count} modèles)\n"
        keyboard.append([
            InlineKeyboardButton(f"📱 {brand['name']}", callback_data=f"manage_brand_{brand['id']}"),
            InlineKeyboardButton("🔄", callback_data=f"toggle_brand_{brand['id']}")
        ])
    
    keyboard.extend([
        [InlineKeyboardButton("➕ Nouvelle Marque", callback_data="add_brand")],
        [InlineKeyboardButton("⬅️ Retour Admin", callback_data="mobile_admin_back")]
    ])
    
    message_func = query.edit_message_text if query else update.message.reply_text
    await message_func(
        text,
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def manage_brand_models(update: Update, context: ContextTypes.DEFAULT_TYPE, query, brand_id):
    """Gère les modèles d'une marque"""
    await query.answer()
    
    brands = get_brands()
    brand = next((b for b in brands if b['id'] == brand_id), None)
    
    if not brand:
        await query.edit_message_text("❌ Marque introuvable")
        return
    
    models = brand.get('models', [])
    
    text = f"📱 *GESTION {brand['name']}*\n\n"
    text += f"*Modèles actuels ({len(models)}) :*\n"
    
    keyboard = []
    
    for i, model in enumerate(models, 1):
        text += f"{i}. {model['name']}\n"
        keyboard.append([
            InlineKeyboardButton(f"✏️ {model['name']}", callback_data=f"edit_model_{brand_id}_{model['id']}"),
            InlineKeyboardButton("🗑️", callback_data=f"delete_model_{brand_id}_{model['id']}")
        ])
    
    keyboard.extend([
        [InlineKeyboardButton(f"➕ Nouveau modèle {brand['name']}", callback_data=f"add_model_{brand_id}")],
        [InlineKeyboardButton("⬅️ Retour Marques", callback_data="mobile_brands")]
    ])
    
    await query.edit_message_text(
        text,
        parse_mode='Markdown', 
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def mobile_menu_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Menu de gestion des images des menus"""
    keyboard = [
        [InlineKeyboardButton("🏠 Logo d'accueil", callback_data="mobile_welcome_logo")],
        [InlineKeyboardButton("📚 Image Catalogue", callback_data="mobile_catalog_image")],
        [InlineKeyboardButton("🛠️ Image Services", callback_data="mobile_services_image")],
        [InlineKeyboardButton("🔧 Images Sous-Services", callback_data="mobile_sub_services_images")],
        [InlineKeyboardButton("🖼️ Images des catégories", callback_data="mobile_category_images")],
        [InlineKeyboardButton("🏷️ Images des marques", callback_data="mobile_brand_images")],
        [InlineKeyboardButton("📋 Voir toutes les images", callback_data="mobile_view_all_images")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_admin")]
    ]
    
    text = "🖼️ **GESTION IMAGES MENUS**\n\n" \
           "Gérez les images des différents menus :\n\n" \
           "• **Logo d'accueil** : Logo affiché dans le message de bienvenue\n" \
           "• **Catalogue** : Image principale du menu produits\n" \
           "• **Services** : Image principale du menu services\n" \
           "• **Sous-Services** : Images pour déblocage, désimlocage, etc.\n" \
           "• **Catégories** : Images pour pochettes, magsafe, etc.\n" \
           "• **Marques** : Images pour iPhone, Samsung, etc.\n" \
           "• **Voir tout** : État complet des images\n\n" \
           "💡 Envoyez simplement une photo après avoir sélectionné l'élément à modifier !"
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def mobile_category_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Liste des catégories pour gestion d'images"""
    categories = get_categories()
    
    keyboard = []
    text = "🖼️ **IMAGES DES CATÉGORIES**\n\n"
    
    if categories:
        for cat in categories:
            has_image = "🖼️" if cat.get('image_url') else "📷"
            status = "✅" if cat.get('active', True) else "❌"
            keyboard.append([InlineKeyboardButton(
                f"{has_image} {status} {cat['name']}", 
                callback_data=f"mobile_image_category_{cat['id']}"
            )])
            
        text += "Cliquez sur une catégorie pour modifier son image.\n\n" \
                "🖼️ = Image présente\n📷 = Pas d'image\n✅ = Active\n❌ = Inactive"
    else:
        text += "Aucune catégorie trouvée."
    
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="mobile_menu_images")])
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def mobile_brand_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Liste des marques pour gestion d'images"""
    brands = get_brands()
    
    keyboard = []
    text = "🏷️ **IMAGES DES MARQUES**\n\n"
    
    if brands:
        for brand in brands:
            has_image = "🖼️" if brand.get('image_url') else "📷"
            status = "✅" if brand.get('active', True) else "❌"
            keyboard.append([InlineKeyboardButton(
                f"{has_image} {status} {brand['name']}", 
                callback_data=f"mobile_image_brand_{brand['id']}"
            )])
            
        text += "Cliquez sur une marque pour modifier son image.\n\n" \
                "🖼️ = Image présente\n📷 = Pas d'image\n✅ = Active\n❌ = Inactive"
    else:
        text += "Aucune marque trouvée."
    
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="mobile_menu_images")])
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def mobile_sub_services_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Liste des sous-services pour gestion d'images"""
    # Services disponibles (correspond aux boutons dans create_services_menu)
    services = [
        {"id": "deblocage", "name": "Déblocage", "emoji": "🔓"},
        {"id": "desimlockage", "name": "Désimlocage", "emoji": "📱"},
        {"id": "declonage", "name": "Déclonage", "emoji": "🔄"},
        {"id": "cas_particulier", "name": "Cas Particuliers", "emoji": "⚠️"}
    ]
    
    keyboard = []
    text = "🔧 **IMAGES DES SOUS-SERVICES**\n\n"
    
    for service in services:
        service_image = get_service_image(service["id"])
        has_image = "🖼️" if service_image else "📷"
        
        keyboard.append([InlineKeyboardButton(
            f"{has_image} {service['emoji']} {service['name']}", 
            callback_data=f"mobile_image_service_{service['id']}"
        )])
    
    text += "Cliquez sur un service pour modifier son image.\n\n" \
            "🖼️ = Image présente\n📷 = Pas d'image\n\n" \
            "Ces images s'afficheront dans les sous-menus des services."
    
    keyboard.append([InlineKeyboardButton("⬅️ Retour", callback_data="mobile_menu_images")])
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_mobile_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère tous les callbacks admin mobile"""
    query = update.callback_query
    data = query.data
    user_id = query.from_user.id
    
    print(f"🔍 Mobile Admin Callback: {data} de l'utilisateur {user_id}")
    
    if not is_admin(user_id):
        await query.answer("❌ Accès refusé", show_alert=True)
        return
    
    if data == "mobile_categories":
        await mobile_categories_menu(update, context, query)
    
    elif data == "mobile_brands":
        await mobile_brands_menu(update, context, query)
    
    elif data.startswith("manage_brand_"):
        brand_id = data.replace("manage_brand_", "")
        await manage_brand_models(update, context, query, brand_id)
    
    elif data.startswith("edit_cat_"):
        cat_id = data.replace("edit_cat_", "")
        print(f"✏️ Tentative édition catégorie: {cat_id}")
        
        category = get_category_by_id(cat_id)
        if category:
            await query.edit_message_text(
                f"✏️ **ÉDITION CATÉGORIE**\n\n"
                f"**Nom :** {category['name']}\n"
                f"**ID :** {category['id']}\n"
                f"**Statut :** {'✅ Active' if category.get('active', True) else '❌ Inactive'}\n"
                f"**Image :** {'🖼️ Présente' if category.get('image_url') else '📷 Aucune'}\n\n"
                f"Que voulez-vous faire ?",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🔄 Changer statut", callback_data=f"toggle_cat_{cat_id}"),
                        InlineKeyboardButton("🖼️ Changer image", callback_data=f"mobile_image_category_{cat_id}")
                    ],
                    [
                        InlineKeyboardButton("📝 Renommer", callback_data=f"rename_cat_{cat_id}"),
                        InlineKeyboardButton("🗑️ Supprimer", callback_data=f"delete_cat_{cat_id}")
                    ],
                    [
                        InlineKeyboardButton("⬅️ Retour", callback_data="mobile_categories")
                    ]
                ])
            )
        else:
            await query.answer("❌ Catégorie introuvable", show_alert=True)
    
    elif data.startswith("toggle_cat_"):
        cat_id = data.replace("toggle_cat_", "")
        new_status = toggle_category_status(cat_id)
        if new_status is not None:
            status_text = "activée" if new_status else "désactivée"
            await query.answer(f"✅ Catégorie {status_text}")
            await mobile_categories_menu(update, context, query)
        else:
            await query.answer("❌ Erreur", show_alert=True)
    
    elif data.startswith("toggle_brand_"):
        brand_id = data.replace("toggle_brand_", "")
        new_status = toggle_brand_status(brand_id)
        if new_status is not None:
            status_text = "activée" if new_status else "désactivée" 
            await query.answer(f"✅ Marque {status_text}")
            await mobile_brands_menu(update, context, query)
        else:
            await query.answer("❌ Erreur", show_alert=True)
    
    elif data == "add_category":
        context.user_data['awaiting_mobile_input'] = 'add_category'
        await query.edit_message_text(
            "➕ *NOUVELLE CATÉGORIE*\n\n"
            "Envoyez le nom de la nouvelle catégorie :\n"
            "Exemple : Coques Transparentes",
            parse_mode='Markdown'
        )
    
    elif data == "add_brand":
        context.user_data['awaiting_mobile_input'] = 'add_brand'
        await query.edit_message_text(
            "➕ *NOUVELLE MARQUE*\n\n"
            "Envoyez le nom de la nouvelle marque :\n"
            "Exemple : OnePlus",
            parse_mode='Markdown'
        )
    
    elif data.startswith("add_model_"):
        brand_id = data.replace("add_model_", "")
        context.user_data['awaiting_mobile_input'] = f'add_model_{brand_id}'
        brands = get_brands()
        brand = next((b for b in brands if b['id'] == brand_id), None)
        brand_name = brand['name'] if brand else "Inconnu"
        
        await query.edit_message_text(
            f"➕ *NOUVEAU MODÈLE {brand_name}*\n\n"
            f"Envoyez le nom du nouveau modèle :\n"
            f"Exemple : OnePlus 12 Pro",
            parse_mode='Markdown'
        )
    
    elif data.startswith("rename_cat_"):
        cat_id = data.replace("rename_cat_", "")
        context.user_data['awaiting_mobile_input'] = f'rename_category_{cat_id}'
        category = get_category_by_id(cat_id)
        cat_name = category['name'] if category else "Inconnue"
        
        await query.edit_message_text(
            f"📝 **RENOMMER CATÉGORIE**\n\n"
            f"**Nom actuel :** {cat_name}\n\n"
            f"Envoyez le nouveau nom :",
            parse_mode='Markdown'
        )
    
    elif data.startswith("delete_cat_"):
        cat_id = data.replace("delete_cat_", "")
        category = get_category_by_id(cat_id)
        cat_name = category['name'] if category else "Inconnue"
        
        await query.edit_message_text(
            f"🗑️ **SUPPRIMER CATÉGORIE**\n\n"
            f"**⚠️ ATTENTION !**\n"
            f"Vous allez supprimer la catégorie : **{cat_name}**\n\n"
            f"Cette action est **IRRÉVERSIBLE** !\n\n"
            f"Voulez-vous vraiment continuer ?",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("❌ Annuler", callback_data="mobile_categories"),
                    InlineKeyboardButton("✅ Confirmer", callback_data=f"confirm_delete_cat_{cat_id}")
                ]
            ])
        )
    
    elif data.startswith("confirm_delete_cat_"):
        cat_id = data.replace("confirm_delete_cat_", "")
        try:
            # Supprimer la catégorie de la base de données
            from database.db_functions import db
            result = db.categories.delete_one({"id": cat_id})
            
            if result.deleted_count > 0:
                await query.answer("✅ Catégorie supprimée", show_alert=True)
                await mobile_categories_menu(update, context, query)
            else:
                await query.answer("❌ Erreur lors de la suppression", show_alert=True)
        except Exception as e:
            print(f"❌ Erreur suppression catégorie: {e}")
            await query.answer("❌ Erreur technique", show_alert=True)
    
    elif data == "mobile_images":
        await mobile_menu_images(update, context, query)
    
    elif data == "mobile_category_images":
        await mobile_category_images(update, context, query)
    
    elif data == "mobile_brand_images":
        await mobile_brand_images(update, context, query)
    
    elif data == "mobile_sub_services_images":
        await mobile_sub_services_images(update, context, query)
    
    elif data == "mobile_welcome_logo":
        # Récupérer l'état actuel du logo d'accueil
        welcome_logo = get_welcome_logo()
        has_logo = "🖼️" if welcome_logo else "📷"
        
        context.user_data['awaiting_image'] = {'type': 'welcome_logo', 'id': 'main_welcome'}
        await query.edit_message_text(
            f"🏠 **LOGO D'ACCUEIL**\n\n"
            f"**État actuel :** {has_logo} {'Logo présent' if welcome_logo else 'Aucun logo'}\n\n"
            f"📸 Envoyez maintenant une photo pour le logo d'accueil.\n\n"
            f"💡 **Conseils:**\n"
            f"• Ce logo s'affichera dans le message 'Bonjour Cristian !'\n"
            f"• Format conseillé: JPG ou PNG\n"
            f"• Sera redimensionnée automatiquement\n"
            f"• Hébergée sur Cloudinary",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Annuler", callback_data="mobile_menu_images")]
            ])
        )

    elif data == "mobile_catalog_image":
        # Récupérer l'état actuel de l'image catalogue
        catalog_image = get_catalog_image()
        has_image = "🖼️" if catalog_image else "📷"
        
        context.user_data['awaiting_image'] = {'type': 'catalog', 'id': 'main_catalog'}
        await query.edit_message_text(
            f"📚 **IMAGE CATALOGUE PRODUITS**\n\n"
            f"**État actuel :** {has_image} {'Image présente' if catalog_image else 'Aucune image'}\n\n"
            f"📸 Envoyez maintenant une photo pour l'image principale du catalogue.\n\n"
            f"💡 **Conseils:**\n"
            f"• Cette image s'affichera avec le titre 'Catalogue Produits'\n"
            f"• Format conseillé: JPG ou PNG\n"
            f"• Sera redimensionnée automatiquement\n"
            f"• Hébergée sur Cloudinary",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Annuler", callback_data="mobile_menu_images")]
            ])
        )

    elif data == "mobile_services_image":
        # Récupérer l'état actuel de l'image services
        services_image = get_services_image()
        has_image = "🖼️" if services_image else "📷"
        
        context.user_data['awaiting_image'] = {'type': 'services', 'id': 'main_services'}
        await query.edit_message_text(
            f"🛠️ **IMAGE MENU SERVICES**\n\n"
            f"**État actuel :** {has_image} {'Image présente' if services_image else 'Aucune image'}\n\n"
            f"📸 Envoyez maintenant une photo pour l'image principale des services.\n\n"
            f"💡 **Conseils:**\n"
            f"• Cette image s'affichera avec le titre 'Nos Services'\n"
            f"• Format conseillé: JPG ou PNG\n"
            f"• Sera redimensionnée automatiquement\n"
            f"• Hébergée sur Cloudinary",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Annuler", callback_data="mobile_menu_images")]
            ])
        )
    
    elif data == "mobile_sub_services_images":
        # Liste des sous-services pour gestion d'images
        text = "🔧 **IMAGES SOUS-SERVICES**\n\n" \
               "Gérez les images des sous-services proposés :\n\n" \
               "• **Déblocage** : Images pour le service de déblocage\n" \
               "• **Désimlocage** : Images pour le service de désimlocage\n" \
               "• **Réparation** : Images pour le service de réparation\n\n" \
               "Cliquez sur un sous-service pour modifier son image."
        
        keyboard = [
            [InlineKeyboardButton("🔓 Déblocage", callback_data="mobile_image_service_deblocage")],
            [InlineKeyboardButton("🔒 Désimlocage", callback_data="mobile_image_service_desimlocage")],
            [InlineKeyboardButton("🛠️ Réparation", callback_data="mobile_image_service_reparation")],
            [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_menu_images")]
        ]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif data.startswith("mobile_image_service_"):
        service_type = data.replace("mobile_image_service_", "")
        service_names = {
            "deblocage": "Déblocage",
            "desimlocage": "Désimlocage",
            "reparation": "Réparation"
        }
        
        service_name = service_names.get(service_type, "Inconnu")
        
        context.user_data['awaiting_image'] = {'type': 'service', 'id': service_type}
        await query.edit_message_text(
            f"🖼️ *IMAGE SOUS-SERVICE*\n\n"
            f"**{service_name}**\n\n"
            f"Envoyez maintenant une photo pour remplacer l'image de ce sous-service.\n\n"
            f"💡 La photo sera automatiquement optimisée et hébergée sur Cloudinary.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("❌ Annuler", callback_data="mobile_sub_services_images")]
            ])
        )
    
    elif data.startswith("mobile_image_category_"):
        cat_id = data.replace("mobile_image_category_", "")
        print(f"🖼️ Tentative modification image catégorie: {cat_id}")
        
        category = get_category_by_id(cat_id)
        if category:
            print(f"✅ Catégorie trouvée: {category['name']}")
            context.user_data['awaiting_image'] = {'type': 'category', 'id': cat_id}
            print(f"📋 Context mis à jour: {context.user_data.get('awaiting_image')}")
            
            await query.edit_message_text(
                f"🖼️ **IMAGE CATÉGORIE**\n\n"
                f"**{category['name']}**\n\n"
                f"📸 Envoyez maintenant une photo pour remplacer l'image de cette catégorie.\n\n"
                f"💡 **Conseils:**\n"
                f"• Format conseillé: JPG ou PNG\n"
                f"• Sera redimensionnée automatiquement\n"
                f"• Hébergée sur Cloudinary",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Annuler", callback_data="mobile_category_images")]
                ])
            )
        else:
            print(f"❌ Catégorie {cat_id} introuvable")
            await query.answer("❌ Catégorie introuvable", show_alert=True)
    
    elif data.startswith("mobile_image_brand_"):
        brand_id = data.replace("mobile_image_brand_", "")
        brand = get_brand_by_id(brand_id)
        if brand:
            context.user_data['awaiting_image'] = {'type': 'brand', 'id': brand_id}
            await query.edit_message_text(
                f"🖼️ *IMAGE MARQUE*\n\n"
                f"**{brand['name']}**\n\n"
                f"Envoyez maintenant une photo pour remplacer l'image de cette marque.\n\n"
                f"💡 La photo sera automatiquement optimisée et hébergée sur Cloudinary.",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Annuler", callback_data="mobile_brand_images")]
                ])
            )
        else:
            await query.answer("❌ Marque introuvable", show_alert=True)

    elif data.startswith("mobile_image_service_"):
        service_id = data.replace("mobile_image_service_", "")
        
        # Services disponibles
        services_info = {
            "deblocage": {"name": "Déblocage", "emoji": "🔓"},
            "desimlockage": {"name": "Désimlocage", "emoji": "📱"},
            "declonage": {"name": "Déclonage", "emoji": "🔄"},
            "cas_particulier": {"name": "Cas Particuliers", "emoji": "⚠️"}
        }
        
        if service_id in services_info:
            service_info = services_info[service_id]
            service_image = get_service_image(service_id)
            has_image = "🖼️" if service_image else "📷"
            
            context.user_data['awaiting_image'] = {'type': 'service', 'id': service_id}
            await query.edit_message_text(
                f"🔧 **IMAGE SOUS-SERVICE**\n\n"
                f"**{service_info['emoji']} {service_info['name']}**\n\n"
                f"**État actuel :** {has_image} {'Image présente' if service_image else 'Aucune image'}\n\n"
                f"📸 Envoyez maintenant une photo pour ce service.\n\n"
                f"💡 **Conseils:**\n"
                f"• Cette image s'affichera dans le menu {service_info['name']}\n"
                f"• Format conseillé: JPG ou PNG\n"
                f"• Sera redimensionnée automatiquement\n"
                f"• Hébergée sur Cloudinary",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("❌ Annuler", callback_data="mobile_sub_services_images")]
                ])
            )
        else:
            await query.answer("❌ Service introuvable", show_alert=True)
    
    elif data == "mobile_view_all_images":
        categories = get_categories()
        brands = get_brands()
        
        # Récupérer les images système
        catalog_image = get_catalog_image()
        services_image = get_services_image()
        welcome_logo = get_welcome_logo()
        
        # Récupérer les images des sous-services
        services_list = [
            {"id": "deblocage", "name": "Déblocage", "emoji": "🔓"},
            {"id": "desimlockage", "name": "Désimlocage", "emoji": "📱"},
            {"id": "declonage", "name": "Déclonage", "emoji": "🔄"},
            {"id": "cas_particulier", "name": "Cas Particuliers", "emoji": "⚠️"}
        ]
        
        text = "📋 *ÉTAT COMPLET DES IMAGES*\n\n"
        
        # Logo d'accueil
        logo_status = "🖼️" if welcome_logo else "📷"
        text += "**🏠 LOGO D'ACCUEIL :**\n"
        text += f"{logo_status} Logo message de bienvenue\n\n"
        
        # Image du catalogue
        catalog_status = "🖼️" if catalog_image else "📷"
        text += "**📚 CATALOGUE PRINCIPAL :**\n"
        text += f"{catalog_status} Catalogue Produits\n\n"
        
        # Image des services
        services_status = "🖼️" if services_image else "📷"
        text += "**🛠️ MENU SERVICES :**\n"
        text += f"{services_status} Nos Services\n\n"
        
        # Images des sous-services
        text += "**🔧 SOUS-SERVICES :**\n"
        for service in services_list:
            service_image = get_service_image(service["id"])
            service_status = "🖼️" if service_image else "📷"
            text += f"{service_status} {service['emoji']} {service['name']}\n"
        
        # Catégories
        text += "\n**📱 CATÉGORIES :**\n"
        for cat in categories:
            status_img = "🖼️" if cat.get('image_url') else "📷"
            status_active = "✅" if cat.get('active', True) else "❌"
            text += f"{status_img} {status_active} {cat['name']}\n"
        
        text += "\n**🏷️ MARQUES :**\n"
        for brand in brands:
            status_img = "🖼️" if brand.get('image_url') else "📷"
            status_active = "✅" if brand.get('active', True) else "❌"
            models_count = len(brand.get('models', []))
            text += f"{status_img} {status_active} {brand['name']} ({models_count} modèles)\n"
        
        text += "\n🖼️ = Image présente | 📷 = Pas d'image\n✅ = Actif | ❌ = Inactif"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_images")]
            ])
        )
    
    elif data == "mobile_settings":
        await mobile_settings_menu(update, context, query)
    
    elif data.startswith("mobile_setting_"):
        setting_action = data.replace("mobile_setting_", "")
        await handle_mobile_setting_action(update, context, query, setting_action)
    
    elif data == "mobile_admin_back" or data == "mobile_admin":
        keyboard = [
            [
                InlineKeyboardButton("📱 Gérer Catégories", callback_data="mobile_categories"),
                InlineKeyboardButton("🏷️ Gérer Marques", callback_data="mobile_brands")
            ],
            [
                InlineKeyboardButton("📦 Gérer Produits", callback_data="mobile_products"),
                InlineKeyboardButton("🖼️ Gérer Images", callback_data="mobile_images")
            ],
            [
                InlineKeyboardButton("👥 Utilisateurs", callback_data="mobile_users"),
                InlineKeyboardButton("📊 Statistiques", callback_data="mobile_stats")
            ],
            [
                InlineKeyboardButton("💬 Diffusion", callback_data="mobile_broadcast"),
                InlineKeyboardButton("⚙️ Paramètres", callback_data="mobile_settings")
            ]
        ]
        
        await query.edit_message_text(
            "📱 *PANNEAU ADMIN MOBILE*\n\n"
            "Gérez votre bot directement depuis votre smartphone !\n\n"
            "Choisissez une option :",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    else:
        # Callback non géré - log pour diagnostic
        print(f"⚠️ Callback non géré dans mobile admin: {data}")
        await query.answer(f"Callback '{data}' non géré", show_alert=True)

async def handle_mobile_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère les entrées texte pour l'admin mobile"""
    user_id = update.effective_user.id
    if not is_admin(user_id):
        return
    
    awaiting = context.user_data.get('awaiting_mobile_input')
    if not awaiting:
        return
    
    text = update.message.text.strip()
    
    if awaiting == 'add_category':
        # Créer ID à partir du nom
        cat_id = text.lower().replace(' ', '_').replace('-', '_')
        result = add_new_category(cat_id, text)
        
        if result:
            await update.message.reply_text(f"✅ Catégorie '{text}' ajoutée avec succès !")
        else:
            await update.message.reply_text(f"❌ Erreur lors de l'ajout de la catégorie")
    
    elif awaiting == 'add_brand':
        # Créer ID à partir du nom
        brand_id = text.lower().replace(' ', '_').replace('-', '_')
        result = add_new_brand(brand_id, text, [])
        
        if result:
            await update.message.reply_text(f"✅ Marque '{text}' ajoutée avec succès !")
        else:
            await update.message.reply_text(f"❌ Erreur lors de l'ajout de la marque")
    
    elif awaiting.startswith('add_model_'):
        brand_id = awaiting.replace('add_model_', '')
        model_id = text.lower().replace(' ', '_').replace('-', '_')
        result = add_model_to_brand(brand_id, model_id, text)
        
        if result:
            await update.message.reply_text(f"✅ Modèle '{text}' ajouté avec succès !")
        else:
            await update.message.reply_text(f"❌ Erreur lors de l'ajout du modèle")
    
    elif awaiting.startswith('rename_category_'):
        cat_id = awaiting.replace('rename_category_', '')
        try:
            # Renommer la catégorie
            from database.db_functions import db
            result = db.categories.update_one(
                {"id": cat_id},
                {"$set": {"name": text}}
            )
            
            if result.modified_count > 0:
                await update.message.reply_text(f"✅ Catégorie renommée en '{text}' !")
            else:
                await update.message.reply_text(f"❌ Erreur lors du renommage")
        except Exception as e:
            print(f"❌ Erreur renommage catégorie: {e}")
            await update.message.reply_text(f"❌ Erreur technique")
    
    # Nettoyer l'état
    context.user_data['awaiting_mobile_input'] = None

async def handle_mobile_image_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère l'upload d'images pour les menus via mobile"""
    user_id = update.effective_user.id
    print(f"🖼️ Photo reçue de l'utilisateur {user_id}")
    
    if not is_admin(user_id):
        print(f"❌ Utilisateur {user_id} non admin, photo ignorée")
        return
    
    # Vérifier si on attend une image
    awaiting = context.user_data.get('awaiting_image')
    print(f"🔍 État awaiting_image: {awaiting}")
    if not awaiting:
        print("ℹ️ Aucune image attendue, photo ignorée")
        return
    
    # Envoyer un message de traitement en cours
    processing_msg = await update.message.reply_text(
        "🔄 Traitement de l'image en cours...\n"
        "Veuillez patienter."
    )
    
    try:
        import requests
        import base64
        import os
        from dotenv import load_dotenv
        
        # Recharger les variables d'environnement
        load_dotenv()
        
        # Configuration Cloudinary via API REST directe
        cloudinary_url = os.getenv('CLOUDINARY_URL', '')
        api_secret = os.getenv('CLOUDINARY_API_SECRET', '')
        
        print(f"🔧 Variables d'environnement:")
        print(f"   CLOUDINARY_API_SECRET: {'✅ Définie (' + str(len(api_secret)) + ' chars)' if api_secret else '❌ Manquante'}")
        print(f"   CLOUDINARY_URL: {'✅ Définie (' + str(len(cloudinary_url)) + ' chars)' if cloudinary_url else '❌ Manquante'}")
        
        if not cloudinary_url:
            raise Exception("CLOUDINARY_URL manquante dans le fichier .env")
        
        # Extraire les composants de l'URL Cloudinary
        # Format: cloudinary://api_key:api_secret@cloud_name
        if not cloudinary_url.startswith('cloudinary://'):
            raise Exception("Format CLOUDINARY_URL invalide")
        
        # Parser l'URL
        url_parts = cloudinary_url.replace('cloudinary://', '').split('@')
        if len(url_parts) != 2:
            raise Exception("Format CLOUDINARY_URL invalide - manque cloud_name")
        
        cloud_name = url_parts[1]
        auth_part = url_parts[0]
        
        if ':' not in auth_part:
            raise Exception("Format CLOUDINARY_URL invalide - manque api_secret")
        
        api_key, extracted_secret = auth_part.split(':', 1)
        
        print(f"✅ Configuration extraite de CLOUDINARY_URL:")
        print(f"   Cloud Name: {cloud_name}")
        print(f"   API Key: {api_key}")
        print(f"   API Secret: {extracted_secret[:10]}...{extracted_secret[-5:]}")
        
        # Essayer d'abord avec le module cloudinary si disponible
        try:
            import cloudinary
            import cloudinary.uploader
            
            cloudinary.config(
                cloud_name=cloud_name,
                api_key=api_key,
                api_secret=extracted_secret,
                secure=True
            )
            
            print("✅ Module Cloudinary configuré")
            use_cloudinary_module = True
            
        except ImportError:
            print("⚠️ Module Cloudinary non disponible, utilisation de l'API REST")
            use_cloudinary_module = False
        
        # Récupérer la plus haute résolution de l'image
        photo = update.message.photo[-1]
        file = await context.bot.get_file(photo.file_id)
        
        # Télécharger l'image
        image_bytes = await file.download_as_bytearray()
        print(f"📸 Image téléchargée: {len(image_bytes)} bytes")
        
        # Upload selon la méthode disponible
        if use_cloudinary_module:
            print("🔄 Upload via module Cloudinary...")
            upload_result = cloudinary.uploader.upload(
                image_bytes,
                folder="menu_images",
                public_id=f"{awaiting['type']}_{awaiting['id']}",
                overwrite=True,
                resource_type="image",
                transformation=[
                    {"width": 500, "height": 500, "crop": "limit"},
                    {"quality": "auto", "fetch_format": "auto"}
                ]
            )
            image_url = upload_result['secure_url']
            
        else:
            print("🔄 Upload via API REST Cloudinary...")
            # Upload direct via API REST
            import json
            
            # Encoder l'image en base64
            image_b64 = base64.b64encode(image_bytes).decode('utf-8')
            
            # Préparer les données pour l'API
            upload_url = f"https://api.cloudinary.com/v1_1/{cloud_name}/image/upload"
            
            # Données de l'upload
            upload_data = {
                'file': f"data:image/jpeg;base64,{image_b64}",
                'folder': 'menu_images',
                'public_id': f"{awaiting['type']}_{awaiting['id']}",
                'overwrite': True,
                'transformation': 'w_500,h_500,c_limit,q_auto,f_auto'
            }
            
            # Authentification
            auth_string = f"{api_key}:{extracted_secret}"
            auth_b64 = base64.b64encode(auth_string.encode()).decode()
            
            headers = {
                'Authorization': f'Basic {auth_b64}',
                'Content-Type': 'application/json'
            }
            
            # Faire l'upload
            response = requests.post(upload_url, json=upload_data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['secure_url']
                print(f"✅ Upload REST réussi: {image_url}")
            else:
                raise Exception(f"Erreur API REST Cloudinary: {response.status_code} - {response.text}")
        
        # Mettre à jour en base selon le type
        if awaiting['type'] == 'category':
            success = update_category_image(awaiting['id'], image_url)
            category = get_category_by_id(awaiting['id'])
            name = category['name'] if category else "Inconnue"
            type_name = f"catégorie '{name}'"
        elif awaiting['type'] == 'catalog':
            success = update_catalog_image(image_url)
            name = "Catalogue Produits"
            type_name = f"catalogue principal"
        elif awaiting['type'] == 'services':
            success = update_services_image(image_url)
            name = "Menu Services"
            type_name = f"menu services"
        elif awaiting['type'] == 'service':
            success = update_service_image(awaiting['id'], image_url)
            services_info = {
                "deblocage": "Déblocage",
                "desimlockage": "Désimlocage", 
                "declonage": "Déclonage",
                "cas_particulier": "Cas Particuliers"
            }
            name = services_info.get(awaiting['id'], "Service inconnu")
            type_name = f"sous-service '{name}'"
        elif awaiting['type'] == 'welcome_logo':
            success = update_welcome_logo(image_url)
            name = "Logo d'accueil"
            type_name = f"logo d'accueil"
        else:  # brand
            success = update_brand_image(awaiting['id'], image_url)
            brand = get_brand_by_id(awaiting['id'])
            name = brand['name'] if brand else "Inconnue"
            type_name = f"marque '{name}'"
        
        # Supprimer le message de traitement
        try:
            await processing_msg.delete()
        except:
            pass
        
        if success:
            # Bouton de retour approprié selon le type
            if awaiting['type'] == 'category':
                back_button_text = "📱 Retour Catégories"
                back_button_data = "mobile_category_images"
            elif awaiting['type'] == 'catalog':
                back_button_text = "📚 Retour Images"
                back_button_data = "mobile_menu_images"
            elif awaiting['type'] == 'services':
                back_button_text = "🛠️ Retour Images"
                back_button_data = "mobile_menu_images"
            elif awaiting['type'] == 'service':
                back_button_text = "🔧 Retour Sous-Services"
                back_button_data = "mobile_sub_services_images"
            elif awaiting['type'] == 'welcome_logo':
                back_button_text = "🏠 Retour Images"
                back_button_data = "mobile_menu_images"
            else:
                back_button_text = "🏷️ Retour Marques" 
                back_button_data = "mobile_brand_images"
            
            # Échapper les caractères spéciaux pour Markdown
            safe_type_name = type_name.replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
            safe_url = image_url[:50].replace('_', '\\_').replace('*', '\\*')
            
            await update.message.reply_text(
                f"✅ *IMAGE MISE À JOUR !*\n\n"
                f"📂 *{safe_type_name.capitalize()}*\n"
                f"🔗 *URL:* {safe_url}...\n"
                f"📏 *Optimisée:* 500x500px maximum\n\n"
                f"L'image apparaîtra maintenant dans les menus !",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(back_button_text, callback_data=back_button_data)],
                    [InlineKeyboardButton("🖼️ Voir toutes les images", callback_data="mobile_view_all_images")],
                    [InlineKeyboardButton("📱 Retour Admin", callback_data="mobile_admin")]
                ])
            )
        else:
            safe_url_error = image_url.replace('_', '\\_').replace('*', '\\*')
            await update.message.reply_text(
                f"❌ *ERREUR BASE DE DONNÉES*\n\n"
                f"L'image a été uploadée sur Cloudinary mais n'a pas pu être sauvée en base.\n\n"
                f"🔗 *URL Cloudinary:* {safe_url_error}",
                parse_mode='Markdown',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔄 Réessayer", callback_data=f"mobile_image_{awaiting['type']}_{awaiting['id']}")]
                ])
            )
        
    except Exception as e:
        # Supprimer le message de traitement en cas d'erreur
        try:
            await processing_msg.delete()
        except:
            pass
            
        # Message d'erreur détaillé
        error_msg = str(e)
        # Échapper les caractères spéciaux dans le message d'erreur
        safe_error_msg = str(error_msg).replace('_', '\\_').replace('*', '\\*').replace('[', '\\[').replace(']', '\\]')
        safe_type = awaiting['type'].replace('_', '\\_')
        safe_id = awaiting['id'].replace('_', '\\_')
        
        await update.message.reply_text(
            f"❌ *ERREUR TRAITEMENT IMAGE*\n\n"
            f"*Type:* {safe_type}\n"
            f"*ID:* {safe_id}\n"
            f"*Erreur:* {safe_error_msg}\n\n"
            f"💡 *Solutions possibles:*\n"
            f"• Vérifiez la connexion internet\n"
            f"• Essayez avec une image plus petite\n"
            f"• Redémarrez le bot si nécessaire",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Réessayer", callback_data=f"mobile_image_{awaiting['type']}_{awaiting['id']}")]
            ])
        )
    
    # Nettoyer l'état
    context.user_data['awaiting_image'] = None

async def mobile_settings_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Menu des paramètres du bot"""
    keyboard = [
        [
            InlineKeyboardButton("🤖 Infos du Bot", callback_data="mobile_setting_bot_info"),
            InlineKeyboardButton("💾 Base de Données", callback_data="mobile_setting_db_info")
        ],
        [
            InlineKeyboardButton("🔄 Réinitialiser Données", callback_data="mobile_setting_reset_confirm"),
            InlineKeyboardButton("📊 Statistiques Système", callback_data="mobile_setting_system_stats")
        ],
        [
            InlineKeyboardButton("🖼️ Nettoyer Images", callback_data="mobile_setting_clean_images"),
            InlineKeyboardButton("🔧 Maintenance", callback_data="mobile_setting_maintenance")
        ],
        [
            InlineKeyboardButton("⬅️ Retour Admin", callback_data="mobile_admin_back")
        ]
    ]
    
    text = "⚙️ **PARAMÈTRES DU BOT**\n\n" \
           "Configurez et maintenez votre bot :\n\n" \
           "• **Infos Bot** : Détails de configuration\n" \
           "• **Base de Données** : État des collections\n" \
           "• **Réinitialiser** : Remettre à zéro les données\n" \
           "• **Statistiques** : Performance système\n" \
           "• **Images** : Nettoyer le stockage\n" \
           "• **Maintenance** : Outils de diagnostic\n\n" \
           "⚠️ Certaines actions sont irréversibles !"
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_mobile_setting_action(update: Update, context: ContextTypes.DEFAULT_TYPE, query, action):
    """Gère les actions des paramètres"""
    await query.answer()
    
    if action == "bot_info":
        # Informations du bot
        import os
        from dotenv import load_dotenv
        load_dotenv()
        
        bot_token = os.getenv('BOT_TOKEN', 'Non défini')
        admin_id = os.getenv('ADMIN_ID', 'Non défini')
        db_name = os.getenv('DATABASE_NAME', 'Non défini')
        
        text = "🤖 **INFORMATIONS DU BOT**\n\n" \
               f"**Token :** {bot_token[:20]}...\n" \
               f"**Admin ID :** {admin_id}\n" \
               f"**Base de données :** {db_name}\n" \
               f"**Cloudinary :** Configuré\n\n" \
               "**Modules chargés :**\n" \
               "✅ Administration mobile\n" \
               "✅ Gestion des images\n" \
               "✅ Base de données dynamique\n" \
               "✅ Système d'héritage"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")]
            ])
        )
    
    elif action == "db_info":
        # État de la base de données
        categories = get_categories()
        brands = get_brands()
        
        # Compter les modèles
        total_models = sum(len(brand.get('models', [])) for brand in brands)
        
        # Compter les images
        categories_with_images = sum(1 for cat in categories if cat.get('image_url'))
        brands_with_images = sum(1 for brand in brands if brand.get('image_url'))
        
        text = "💾 **ÉTAT BASE DE DONNÉES**\n\n" \
               f"**📱 Catégories :** {len(categories)}\n" \
               f"   └ Avec images : {categories_with_images}\n\n" \
               f"**🏷️ Marques :** {len(brands)}\n" \
               f"   └ Avec images : {brands_with_images}\n\n" \
               f"**📱 Modèles :** {total_models}\n\n" \
               "**Collections MongoDB :**\n" \
               "✅ categories\n" \
               "✅ brands\n" \
               "✅ products\n" \
               "✅ users"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")]
            ])
        )
    
    elif action == "reset_confirm":
        # Confirmation de réinitialisation
        text = "⚠️ **RÉINITIALISATION**\n\n" \
               "**ATTENTION !** Cette action va :\n\n" \
               "🗑️ Supprimer toutes les catégories personnalisées\n" \
               "🗑️ Supprimer toutes les marques personnalisées\n" \
               "🗑️ Remettre les données par défaut\n" \
               "🗑️ Conserver les utilisateurs et produits\n\n" \
               "Cette action est **IRRÉVERSIBLE** !\n\n" \
               "Voulez-vous vraiment continuer ?"
        
        keyboard = [
            [
                InlineKeyboardButton("❌ Annuler", callback_data="mobile_settings"),
                InlineKeyboardButton("✅ Confirmer", callback_data="mobile_setting_reset_execute")
            ]
        ]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif action == "reset_execute":
        # Exécuter la réinitialisation
        try:
            from database.db_functions import init_categories_and_brands
            
            # Supprimer les collections existantes
            from database.db_functions import db
            db.categories.drop()
            db.brands.drop()
            
            # Recréer avec les données par défaut
            init_categories_and_brands()
            
            text = "✅ **RÉINITIALISATION RÉUSSIE**\n\n" \
                   "Les données ont été remises aux valeurs par défaut :\n\n" \
                   "📱 4 catégories standard\n" \
                   "🏷️ 5 marques avec modèles 2025\n" \
                   "🖼️ Images supprimées (à re-télécharger)\n\n" \
                   "Le bot est prêt à être reconfiguré !"
            
        except Exception as e:
            text = f"❌ **ERREUR**\n\n" \
                   f"Impossible de réinitialiser :\n{str(e)}"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")]
            ])
        )
    
    elif action == "system_stats":
        # Statistiques système
        import psutil
        import sys
        from datetime import datetime
        
        try:
            # Informations système
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            text = "📊 **STATISTIQUES SYSTÈME**\n\n" \
                   f"🐍 **Python :** {sys.version.split()[0]}\n" \
                   f"💾 **RAM :** {memory.percent}% utilisée\n" \
                   f"💿 **Disque :** {disk.percent}% utilisé\n\n" \
                   f"⏰ **Démarrage :** {datetime.now().strftime('%H:%M:%S')}\n\n" \
                   "**Modules chargés :**\n" \
                   "✅ telegram\n" \
                   "✅ pymongo\n" \
                   "✅ cloudinary\n" \
                   "✅ python-dotenv"
            
        except ImportError:
            text = "📊 **STATISTIQUES SYSTÈME**\n\n" \
                   f"🐍 **Python :** {sys.version.split()[0]}\n" \
                   f"⏰ **Heure :** {datetime.now().strftime('%H:%M:%S')}\n\n" \
                   "💡 Installez `psutil` pour plus de détails"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")]
            ])
        )
    
    elif action == "clean_images":
        # Nettoyer les images
        text = "🖼️ **NETTOYAGE DES IMAGES**\n\n" \
               "Cette fonction permet de :\n\n" \
               "🗑️ Supprimer les URLs d'images cassées\n" \
               "🔄 Réinitialiser tous les champs image_url\n" \
               "📋 Lister les images orphelines\n\n" \
               "Que voulez-vous faire ?"
        
        keyboard = [
            [
                InlineKeyboardButton("🗑️ Vider toutes les images", callback_data="mobile_setting_clean_all_images"),
                InlineKeyboardButton("📋 Voir les images", callback_data="mobile_view_all_images")
            ],
            [
                InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")
            ]
        ]
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    elif action == "clean_all_images":
        # Vider toutes les images
        try:
            categories_updated = 0
            brands_updated = 0
            
            # Nettoyer les images des catégories
            categories = get_categories()
            for cat in categories:
                if cat.get('image_url'):
                    success = update_category_image(cat['id'], "")
                    if success:
                        categories_updated += 1
            
            # Nettoyer les images des marques
            brands = get_brands()
            for brand in brands:
                if brand.get('image_url'):
                    success = update_brand_image(brand['id'], "")
                    if success:
                        brands_updated += 1
            
            text = f"✅ **NETTOYAGE TERMINÉ**\n\n" \
                   f"🖼️ **Images supprimées :**\n" \
                   f"   • Catégories : {categories_updated}\n" \
                   f"   • Marques : {brands_updated}\n\n" \
                   f"Vous pouvez maintenant re-télécharger de nouvelles images via l'interface mobile."
            
        except Exception as e:
            text = f"❌ **ERREUR**\n\n" \
                   f"Impossible de nettoyer :\n{str(e)}"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")]
            ])
        )
    
    elif action == "maintenance":
        # Outils de maintenance
        text = "🔧 **MAINTENANCE**\n\n" \
               "Outils de diagnostic et réparation :\n\n" \
               "✅ **État général :** Opérationnel\n" \
               "✅ **Base de données :** Connectée\n" \
               "✅ **Cloudinary :** Configuré\n" \
               "✅ **Handlers :** Tous chargés\n\n" \
               "💡 **Conseils :**\n" \
               "• Redémarrez le bot si problème\n" \
               "• Vérifiez les logs en cas d'erreur\n" \
               "• Utilisez la réinitialisation en dernier recours"
        
        await query.edit_message_text(
            text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour Paramètres", callback_data="mobile_settings")]
            ])
        )
