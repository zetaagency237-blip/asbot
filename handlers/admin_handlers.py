"""
Handlers pour l'administration du bot
"""
from telegram import Update
from telegram.ext import ContextTypes
from database.db_functions import (
    is_admin, get_user_stats, get_all_users, get_all_products, 
    add_product, products_collection
)
from menus.menu_functions import create_admin_menu
from datetime import datetime

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /admin pour accéder au panneau d'administration"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    await update.message.reply_text(
        "*PANNEAU D'ADMINISTRATION*\n\nCHOISISSEZ UNE OPTION :",
        parse_mode='Markdown',
        reply_markup=create_admin_menu()
    )

async def addproduct_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /addproduct pour ajouter un produit"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    if len(context.args) < 6:
        await update.message.reply_text(
            "*AJOUT DE PRODUIT*\n\n"
            "USAGE: `/addproduct nom catégorie marque modèle prix description`\n\n"
            "*EXEMPLE:*\n"
            "`/addproduct \"COQUE IPHONE\" POCHETTES IPHONE \"15 PRO\" 25.99 \"COQUE EN SILICONE PREMIUM\"`\n\n"
            "*CATÉGORIES:* POCHETTES, MAGSAFE, GADGETS, PACKS\n"
            "*MARQUES:* IPHONE, SAMSUNG, XIAOMI, HUAWEI",
            parse_mode='Markdown'
        )
        return
    
    try:
        name = context.args[0]
        category = context.args[1].lower()
        brand = context.args[2].lower()
        model = context.args[3]
        price = float(context.args[4])
        description = " ".join(context.args[5:])
        
        # Vérifier les catégories et marques valides
        valid_categories = ['pochettes', 'magsafe', 'gadgets', 'packs']
        valid_brands = ['iphone', 'samsung', 'xiaomi', 'huawei']
        
        if category not in valid_categories:
            await update.message.reply_text(f"CATÉGORIE INVALIDE. UTILISEZ : {', '.join(valid_categories).upper()}")
            return
            
        if brand not in valid_brands:
            await update.message.reply_text(f"MARQUE INVALIDE. UTILISEZ : {', '.join(valid_brands).upper()}")
            return
        
        # Ajouter le produit
        product_id = add_product(name, category, brand, model, price, "", description)
        
        if product_id:
            await update.message.reply_text(
                f"*PRODUIT AJOUTÉ AVEC SUCCÈS*\n\n"
                f"*{name.upper()}*\n"
                f"CATÉGORIE : {category.upper()}\n"
                f"MARQUE : {brand.upper()}\n"
                f"MODÈLE : {model.upper()}\n"
                f"PRIX : {price}€\n"
                f"DESCRIPTION : {description}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("ERREUR LORS DE L'AJOUT DU PRODUIT.")
            
    except ValueError:
        await update.message.reply_text("PRIX INVALIDE. UTILISEZ UN NOMBRE DÉCIMAL (EX: 25.99)")
    except Exception as e:
        await update.message.reply_text(f"ERREUR : {str(e)}")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /broadcast pour diffuser un message à tous les utilisateurs"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    if not context.args:
        await update.message.reply_text(
            "*DIFFUSION DE MESSAGE*\n\n"
            "USAGE: `/broadcast VOTRE MESSAGE ICI`\n\n"
            "*EXEMPLE:*\n"
            "`/broadcast NOUVELLE PROMOTION SUR TOUS LES PRODUITS IPHONE`",
            parse_mode='Markdown'
        )
        return
    
    message = " ".join(context.args)
    users = get_all_users()
    
    if not users:
        await update.message.reply_text("AUCUN UTILISATEUR TROUVÉ POUR LA DIFFUSION.")
        return
    
    success_count = 0
    error_count = 0
    
    await update.message.reply_text(f"DIFFUSION EN COURS VERS {len(users)} UTILISATEURS...")
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user['user_id'],
                text=f"*MESSAGE ANONYME SMARTPHONE*\n\n{message.upper()}",
                parse_mode='Markdown'
            )
            success_count += 1
        except Exception as e:
            error_count += 1
            print(f"Erreur envoi à {user['user_id']}: {e}")
    
    await update.message.reply_text(
        f"*DIFFUSION TERMINÉE*\n\n"
        f"ENVOYÉS : {success_count}\n"
        f"ERREURS : {error_count}",
        parse_mode='Markdown'
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /stats pour afficher les statistiques"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    stats = get_user_stats()
    products_count = products_collection.count_documents({})
    active_products = products_collection.count_documents({"active": True})
    
    await update.message.reply_text(
        f"*STATISTIQUES ANONYME SMARTPHONE*\n\n"
        f"*UTILISATEURS :*\n"
        f"TOTAL : {stats['total']} UTILISATEURS\n"
        f"NOUVEAUX AUJOURD'HUI : {stats['today']}\n\n"
        f"*PRODUITS :*\n"
        f"TOTAL : {products_count} PRODUITS\n"
        f"ACTIFS : {active_products}\n\n"
        f"GÉNÉRÉ LE : {datetime.now().strftime('%d/%m/%Y À %H:%M')}",
        parse_mode='Markdown'
    )

async def listusers_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /listusers pour lister les utilisateurs"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    users = get_all_users()
    
    if not users:
        await update.message.reply_text("AUCUN UTILISATEUR TROUVÉ.")
        return
    
    user_text = f"*LISTE DES UTILISATEURS* ({len(users)} TOTAL)\n\n"
    
    for i, user in enumerate(users[:20], 1):  # Limiter à 20 utilisateurs
        user_text += f"{i}. *{user['prenom'].upper()}*\n"
        user_text += f"   ID: `{user['user_id']}`\n"
        user_text += f"   INSCRIT: {user['created_at'].strftime('%d/%m/%Y')}\n\n"
    
    if len(users) > 20:
        user_text += f"... ET {len(users) - 20} AUTRES UTILISATEURS"
    
    await update.message.reply_text(user_text, parse_mode='Markdown')

async def editproduct_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /editproduct pour modifier un produit"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    if len(context.args) < 1:
        # Afficher la liste des produits avec leurs IDs
        products = get_all_products()
        if not products:
            await update.message.reply_text("AUCUN PRODUIT TROUVÉ.")
            return
        
        product_text = "*LISTE DES PRODUITS À MODIFIER*\n\n"
        product_text += "USAGE: `/editproduct [ID] [CHAMP] [NOUVELLE_VALEUR]`\n\n"
        product_text += "*CHAMPS MODIFIABLES:* NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, MODEL\n\n"
        
        for i, product in enumerate(products[:10], 1):
            product_text += f"{i}. *{product['name'].upper()}*\n"
            product_text += f"   ID: `{str(product['_id'])}`\n"
            product_text += f"   PRIX: {product['price']}€\n\n"
        
        if len(products) > 10:
            product_text += f"... ET {len(products) - 10} AUTRES PRODUITS"
            
        await update.message.reply_text(product_text, parse_mode='Markdown')
        return
    
    if len(context.args) < 3:
        await update.message.reply_text(
            "*MODIFICATION DE PRODUIT*\n\n"
            "USAGE: `/editproduct [ID] [CHAMP] [NOUVELLE_VALEUR]`\n\n"
            "*EXEMPLES:*\n"
            "`/editproduct 6543210abcdef name \"NOUVEAU NOM\"`\n"
            "`/editproduct 6543210abcdef price 35.99`\n"
            "`/editproduct 6543210abcdef description \"NOUVELLE DESCRIPTION\"`\n\n"
            "*CHAMPS:* NAME, PRICE, DESCRIPTION, CATEGORY, BRAND, MODEL",
            parse_mode='Markdown'
        )
        return
    
    try:
        from database.db_functions import update_product
        from bson import ObjectId
        
        product_id = context.args[0]
        field = context.args[1].lower()
        new_value = " ".join(context.args[2:])
        
        # Vérifier les champs valides
        valid_fields = ['name', 'price', 'description', 'category', 'brand', 'model']
        if field not in valid_fields:
            await update.message.reply_text(f"CHAMP INVALIDE. UTILISEZ : {', '.join(valid_fields).upper()}")
            return
        
        # Conversion du prix en float si nécessaire
        if field == 'price':
            new_value = float(new_value)
        
        # Mettre à jour le produit
        success = update_product(product_id, {field: new_value})
        
        if success:
            await update.message.reply_text(
                f"*PRODUIT MODIFIÉ AVEC SUCCÈS*\n\n"
                f"ID: `{product_id}`\n"
                f"CHAMP: {field.upper()}\n"
                f"NOUVELLE VALEUR: {str(new_value).upper()}",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("ERREUR LORS DE LA MODIFICATION. VÉRIFIEZ L'ID DU PRODUIT.")
            
    except ValueError:
        await update.message.reply_text("VALEUR INVALIDE POUR LE PRIX. UTILISEZ UN NOMBRE DÉCIMAL.")
    except Exception as e:
        await update.message.reply_text(f"ERREUR : {str(e)}")

async def deleteproduct_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /deleteproduct pour supprimer un produit"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    if len(context.args) < 1:
        # Afficher la liste des produits
        products = get_all_products()
        if not products:
            await update.message.reply_text("AUCUN PRODUIT TROUVÉ.")
            return
        
        product_text = "*SUPPRESSION DE PRODUIT*\n\n"
        product_text += "USAGE: `/deleteproduct [ID]`\n\n"
        
        for i, product in enumerate(products[:10], 1):
            product_text += f"{i}. *{product['name'].upper()}*\n"
            product_text += f"   ID: `{str(product['_id'])}`\n"
            product_text += f"   PRIX: {product['price']}€\n\n"
        
        await update.message.reply_text(product_text, parse_mode='Markdown')
        return
    
    try:
        from database.db_functions import delete_product, get_all_products
        from bson import ObjectId
        
        product_id = context.args[0]
        
        # Récupérer les infos du produit avant suppression
        products = get_all_products()
        product_to_delete = None
        for product in products:
            if str(product['_id']) == product_id:
                product_to_delete = product
                break
        
        if not product_to_delete:
            await update.message.reply_text("PRODUIT NON TROUVÉ.")
            return
        
        # Supprimer le produit
        success = delete_product(product_id)
        
        if success:
            await update.message.reply_text(
                f"*PRODUIT SUPPRIMÉ AVEC SUCCÈS*\n\n"
                f"*{product_to_delete['name'].upper()}*\n"
                f"PRIX: {product_to_delete['price']}€\n"
                f"ID: `{product_id}`",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("ERREUR LORS DE LA SUPPRESSION.")
            
    except Exception as e:
        await update.message.reply_text(f"ERREUR : {str(e)}")

async def addimage_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Commande /addimage pour ajouter/modifier l'image d'un produit"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("ACCÈS REFUSÉ. VOUS N'ÊTES PAS ADMINISTRATEUR.")
        return
    
    if len(context.args) < 1:
        # Afficher la liste des produits
        products = get_all_products()
        if not products:
            await update.message.reply_text("AUCUN PRODUIT TROUVÉ.")
            return
        
        product_text = "*GESTION DES IMAGES*\n\n"
        product_text += "USAGE: `/addimage [ID_PRODUIT]`\n\n"
        
        for i, product in enumerate(products[:8], 1):
            has_image = "[IMAGE]" if product.get('image_url') else "[SANS IMAGE]"
            product_text += f"{i}. {has_image} *{product['name'].upper()}*\n"
            product_text += f"   ID: `{str(product['_id'])}`\n\n"
        
        await update.message.reply_text(product_text, parse_mode='Markdown')
        return
    
    try:
        product_id = context.args[0]
        
        # Vérifier que le produit existe
        products = get_all_products()
        product = None
        for p in products:
            if str(p['_id']) == product_id:
                product = p
                break
        
        if not product:
            await update.message.reply_text("PRODUIT NON TROUVÉ.")
            return
        
        # Stocker l'ID du produit pour la suite
        context.user_data['awaiting_image_for_product'] = product_id
        
        current_image = "AUCUNE IMAGE" if not product.get('image_url') else "IMAGE EXISTANTE"
        
        await update.message.reply_text(
            f"*AJOUT/MODIFICATION D'IMAGE*\n\n"
            f"PRODUIT: *{product['name'].upper()}*\n"
            f"ID: `{product_id}`\n"
            f"ÉTAT ACTUEL: {current_image}\n\n"
            f"*VEUILLEZ MAINTENANT ENVOYER L'IMAGE* QUE VOUS SOUHAITEZ ASSOCIER À CE PRODUIT.\n\n"
            f"L'IMAGE SERA AUTOMATIQUEMENT UPLOADÉE SUR CLOUDINARY ET ASSOCIÉE AU PRODUIT.",
            parse_mode='Markdown'
        )
        
    except Exception as e:
        await update.message.reply_text(f"ERREUR : {str(e)}")

async def handle_image_upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Gère l'upload d'images vers Cloudinary"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        return
    
    # Vérifier si on attend une image pour un produit
    if not context.user_data.get('awaiting_image_for_product'):
        return
    
    if not update.message.photo:
        await update.message.reply_text("VEUILLEZ ENVOYER UNE IMAGE (PHOTO).")
        return
    
    try:
        import cloudinary.uploader
        import io
        import requests
        
        product_id = context.user_data['awaiting_image_for_product']
        
        await update.message.reply_text("UPLOAD EN COURS SUR CLOUDINARY...")
        
        # Récupérer la plus haute qualité de l'image
        photo = update.message.photo[-1]
        
        # Télécharger le fichier depuis Telegram
        file = await context.bot.get_file(photo.file_id)
        file_bytes = await file.download_as_bytearray()
        
        # Upload vers Cloudinary
        result = cloudinary.uploader.upload(
            file_bytes,
            folder="anonyme_smartphone/products",
            public_id=f"product_{product_id}",
            overwrite=True,
            resource_type="image"
        )
        
        image_url = result['secure_url']
        
        # Mettre à jour le produit avec l'URL de l'image
        from database.db_functions import update_product
        success = update_product(product_id, {"image_url": image_url})
        
        if success:
            await update.message.reply_text(
                f"*IMAGE AJOUTÉE AVEC SUCCÈS*\n\n"
                f"URL: {image_url}\n"
                f"PRODUIT ID: `{product_id}`\n\n"
                f"L'IMAGE EST MAINTENANT ASSOCIÉE AU PRODUIT ET SERA AFFICHÉE DANS LE CATALOGUE.",
                parse_mode='Markdown'
            )
        else:
            await update.message.reply_text("ERREUR LORS DE LA MISE À JOUR DU PRODUIT.")
        
        # Nettoyer les données utilisateur
        context.user_data.pop('awaiting_image_for_product', None)
        
    except Exception as e:
        await update.message.reply_text(f"ERREUR LORS DE L'UPLOAD : {str(e)}")
        context.user_data.pop('awaiting_image_for_product', None)
