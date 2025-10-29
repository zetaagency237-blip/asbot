#!/usr/bin/env python3
"""
Diagnostic des menus et callbacks utilisateur
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import get_categories, get_brands
from menus.menu_functions import create_products_menu, create_brands_menu

def test_menus():
    print("🧪 DIAGNOSTIC DES MENUS UTILISATEUR")
    print("=" * 50)
    
    # Test des catégories
    print("\n📂 CATÉGORIES :")
    try:
        categories = get_categories()
        if categories:
            for i, cat in enumerate(categories, 1):
                active = "✅" if cat.get('active', True) else "❌"
                image = "🖼️" if cat.get('image_url') else "📷"
                print(f"   {i}. {active} {image} {cat['name']} (ID: {cat['id']})")
        else:
            print("   ❌ Aucune catégorie trouvée")
    except Exception as e:
        print(f"   ❌ Erreur catégories: {e}")
    
    # Test des marques
    print("\n🏷️ MARQUES :")
    try:
        brands = get_brands()
        if brands:
            for i, brand in enumerate(brands, 1):
                active = "✅" if brand.get('active', True) else "❌"
                image = "🖼️" if brand.get('image_url') else "📷"
                models_count = len(brand.get('models', []))
                print(f"   {i}. {active} {image} {brand['name']} (ID: {brand['id']}) - {models_count} modèles")
                
                # Afficher les modèles
                for model in brand.get('models', [])[:3]:  # Max 3 modèles pour éviter spam
                    print(f"      └─ {model['name']}")
                if len(brand.get('models', [])) > 3:
                    print(f"      └─ ... et {len(brand.get('models', [])) - 3} autres")
        else:
            print("   ❌ Aucune marque trouvée")
    except Exception as e:
        print(f"   ❌ Erreur marques: {e}")
    
    # Test du menu produits
    print("\n📱 MENU PRODUITS :")
    try:
        menu = create_products_menu()
        print(f"   ✅ Menu créé avec {len(menu.inline_keyboard)} boutons")
        for row in menu.inline_keyboard:
            for button in row:
                print(f"      └─ '{button.text}' → callback: '{button.callback_data}'")
    except Exception as e:
        print(f"   ❌ Erreur menu produits: {e}")
    
    # Test du menu marques
    print("\n🏷️ MENU MARQUES :")
    try:
        menu = create_brands_menu()
        print(f"   ✅ Menu créé avec {len(menu.inline_keyboard)} boutons")
        for row in menu.inline_keyboard:
            for button in row:
                print(f"      └─ '{button.text}' → callback: '{button.callback_data}'")
    except Exception as e:
        print(f"   ❌ Erreur menu marques: {e}")
    
    # Test de la connexion DB
    print("\n💾 CONNEXION BASE DE DONNÉES :")
    try:
        from database.db_functions import db
        collections = db.list_collection_names()
        print(f"   ✅ Connexion OK - Collections: {collections}")
    except Exception as e:
        print(f"   ❌ Erreur connexion DB: {e}")

if __name__ == "__main__":
    test_menus()
