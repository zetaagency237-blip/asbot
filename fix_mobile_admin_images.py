#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour corriger les problèmes d'encodage dans mobile_admin_handlers.py
"""

def fix_mobile_admin_file():
    """Corrige les caractères d'encodage problématiques"""
    
    file_path = r"c:\Users\INGENIEUR\Desktop\ASbot\handlers\mobile_admin_handlers.py"
    
    try:
        # Lire le fichier
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Corrections des caractères corrompus
        corrections = [
            ('� Image Catalogue', '📚 Image Catalogue'),
            ('�🖼️ Images des catégories', '🖼️ Images des catégories'),
        ]
        
        for old, new in corrections:
            content = content.replace(old, new)
        
        # Ajouter le logo d'accueil dans le menu
        old_keyboard = '''    keyboard = [
        [InlineKeyboardButton("📚 Image Catalogue", callback_data="mobile_catalog_image")],
        [InlineKeyboardButton("🖼️ Images des catégories", callback_data="mobile_category_images")],
        [InlineKeyboardButton("🏷️ Images des marques", callback_data="mobile_brand_images")],
        [InlineKeyboardButton("📋 Voir toutes les images", callback_data="mobile_view_all_images")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_admin")]
    ]'''
        
        new_keyboard = '''    keyboard = [
        [InlineKeyboardButton("🏠 Logo d'accueil", callback_data="mobile_welcome_logo")],
        [InlineKeyboardButton("📚 Image Catalogue", callback_data="mobile_catalog_image")],
        [InlineKeyboardButton("🖼️ Images des catégories", callback_data="mobile_category_images")],
        [InlineKeyboardButton("🏷️ Images des marques", callback_data="mobile_brand_images")],
        [InlineKeyboardButton("📋 Voir toutes les images", callback_data="mobile_view_all_images")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="mobile_admin")]
    ]'''
        
        content = content.replace(old_keyboard, new_keyboard)
        
        # Mettre à jour le texte descriptif
        old_text = '''           "• **Catalogue** : Image principale du menu produits\\n" \\
           "• **Catégories** : Images pour pochettes, magsafe, etc.\\n" \\
           "• **Marques** : Images pour iPhone, Samsung, etc.\\n" \\
           "• **Voir tout** : État complet des images\\n\\n" \\'''
        
        new_text = '''           "• **Logo d'accueil** : Logo affiché dans le message de bienvenue\\n" \\
           "• **Catalogue** : Image principale du menu produits\\n" \\
           "• **Catégories** : Images pour pochettes, magsafe, etc.\\n" \\
           "• **Marques** : Images pour iPhone, Samsung, etc.\\n" \\
           "• **Voir tout** : État complet des images\\n\\n" \\'''
        
        content = content.replace(old_text, new_text)
        
        # Écrire le fichier corrigé
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print("✅ Fichier mobile_admin_handlers.py corrigé avec succès !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction : {e}")
        return False

if __name__ == "__main__":
    fix_mobile_admin_file()
