#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de correction définitive pour le menu des images
"""

def fix_mobile_menu_images():
    """Corrige définitivement la fonction mobile_menu_images"""
    
    file_path = r"c:\Users\INGENIEUR\Desktop\ASbot\handlers\mobile_admin_handlers.py"
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Fonction corrigée complète
        old_function = """async def mobile_menu_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    \"\"\"Menu de gestion des images des menus\"\"\"
    keyboard = [
        [InlineKeyboardButton("� Image Catalogue", callback_data="mobile_catalog_image")],
        [InlineKeyboardButton("�🖼️ Images des catégories", callback_data="mobile_category_images")],
        [InlineKeyboardButton("🏷️ Images des marques", callback_data="mobile_brand_images")],
        [InlineKeyboardButton("📋 Voir toutes les images", callback_data="mobile_view_all_images")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_admin")]
    ]
    
    text = "🖼️ **GESTION IMAGES MENUS**\\n\\n" \\
           "Gérez les images des différents menus :\\n\\n" \\
           "• **Catalogue** : Image principale du menu produits\\n" \\
           "• **Catégories** : Images pour pochettes, magsafe, etc.\\n" \\
           "• **Marques** : Images pour iPhone, Samsung, etc.\\n" \\
           "• **Voir tout** : État complet des images\\n\\n" \\
           "💡 Envoyez simplement une photo après avoir sélectionné l'élément à modifier !"
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))"""
        
        new_function = """async def mobile_menu_images(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    \"\"\"Menu de gestion des images des menus\"\"\"
    keyboard = [
        [InlineKeyboardButton("🏠 Logo d'accueil", callback_data="mobile_welcome_logo")],
        [InlineKeyboardButton("📚 Image Catalogue", callback_data="mobile_catalog_image")],
        [InlineKeyboardButton("🖼️ Images des catégories", callback_data="mobile_category_images")],
        [InlineKeyboardButton("🏷️ Images des marques", callback_data="mobile_brand_images")],
        [InlineKeyboardButton("📋 Voir toutes les images", callback_data="mobile_view_all_images")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_admin")]
    ]
    
    text = "🖼️ **GESTION IMAGES MENUS**\\n\\n" \\
           "Gérez les images des différents menus :\\n\\n" \\
           "• **Logo d'accueil** : Logo affiché dans le message de bienvenue\\n" \\
           "• **Catalogue** : Image principale du menu produits\\n" \\
           "• **Catégories** : Images pour pochettes, magsafe, etc.\\n" \\
           "• **Marques** : Images pour iPhone, Samsung, etc.\\n" \\
           "• **Voir tout** : État complet des images\\n\\n" \\
           "💡 Envoyez simplement une photo après avoir sélectionné l'élément à modifier !"
    
    if query:
        await query.edit_message_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text(text, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))"""
        
        # Remplacer la fonction
        content = content.replace(old_function, new_function)
        
        # Aussi corriger les caractères isolés
        content = content.replace('        [InlineKeyboardButton("� Image Catalogue"', '        [InlineKeyboardButton("📚 Image Catalogue"')
        content = content.replace('        [InlineKeyboardButton("�🖼️ Images des catégories"', '        [InlineKeyboardButton("🖼️ Images des catégories"')
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Menu des images corrigé avec le logo d'accueil !")
        print("🏠 Le bouton 'Logo d'accueil' est maintenant disponible")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        return False

if __name__ == "__main__":
    fix_mobile_menu_images()
