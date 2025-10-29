#!/usr/bin/env python3
"""
Test de diagnostic pour les images de catégories
"""

import asyncio
import os
from dotenv import load_dotenv
from database.db_functions import get_categories, get_category_by_id, update_category_image

# Charger les variables d'environnement
load_dotenv()

def test_categories():
    """Test les fonctions de catégories"""
    print("🧪 Test des catégories et images...\n")
    
    # 1. Lister toutes les catégories
    categories = get_categories()
    print(f"📱 Catégories trouvées: {len(categories)}")
    
    for i, cat in enumerate(categories, 1):
        print(f"{i}. ID: {cat['id']} | Nom: {cat['name']} | Image: {cat.get('image_url', 'Aucune')}")
        
        # Test de récupération par ID
        retrieved = get_category_by_id(cat['id'])
        if retrieved:
            print(f"   ✅ Récupération par ID: OK")
        else:
            print(f"   ❌ Récupération par ID: ÉCHEC")
    
    # 2. Test de mise à jour d'image sur la première catégorie
    if categories:
        test_cat = categories[0]
        print(f"\n🧪 Test de mise à jour image sur '{test_cat['name']}'...")
        
        # Test avec une URL factice
        test_url = "https://test.example.com/image.jpg"
        success = update_category_image(test_cat['id'], test_url)
        
        if success:
            print("✅ Mise à jour image: SUCCÈS")
            # Vérifier que c'est bien sauvé
            updated_cat = get_category_by_id(test_cat['id'])
            if updated_cat and updated_cat.get('image_url') == test_url:
                print("✅ Vérification sauvegarde: OK")
            else:
                print("❌ Vérification sauvegarde: ÉCHEC")
        else:
            print("❌ Mise à jour image: ÉCHEC")

if __name__ == "__main__":
    test_categories()
