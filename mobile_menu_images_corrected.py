"""
Fonction mobile_menu_images corrigée - à copier dans mobile_admin_handlers.py
"""

async def mobile_menu_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    """Menu de gestion des images des menus"""
    keyboard = [
        [InlineKeyboardButton("🏠 Logo d'accueil", callback_data="mobile_welcome_logo")],
        [InlineKeyboardButton("📚 Image Catalogue", callback_data="mobile_catalog_image")],
        [InlineKeyboardButton("🖼️ Images des catégories", callback_data="mobile_category_images")],
        [InlineKeyboardButton("🏷️ Images des marques", callback_data="mobile_brand_images")],
        [InlineKeyboardButton("📋 Voir toutes les images", callback_data="mobile_view_all_images")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_admin")]
    ]
    
    text = "🖼️ **GESTION IMAGES MENUS**\n\n" \
           "Gérez les images des différents menus :\n\n" \
           "• **Logo d'accueil** : Logo affiché dans le message de bienvenue\n" \
           "• **Catalogue** : Image principale du menu produits\n" \
           "• **Catégories** : Images pour pochettes, magsafe, etc.\n" \
           "• **Marques** : Images pour iPhone, Samsung, etc.\n" \
           "• **Voir tout** : État complet des images\n\n" \
           "💡 Envoyez simplement une photo après avoir sélectionné l'élément à modifier !"
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
