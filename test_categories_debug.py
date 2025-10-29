#!/usr/bin/env python3
"""
Test de diagnostic pour le problème des images de catégories
"""

import asyncio
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import get_categories, get_category_by_id

def test_categories():
    """Test des fonctions de catégories"""
    try:
        print("🧪 Test des catégories...")
        
        # Obtenir toutes les catégories
        categories = get_categories()
        print(f"📱 Nombre de catégories: {len(categories)}")
        
        for cat in categories:
            print(f"  - ID: {cat['id']}, Nom: {cat['name']}, Image: {cat.get('image_url', 'Aucune')}")
        
        # Chercher spécifiquement "pochette"
        pochette_found = False
        for cat in categories:
            if 'pochette' in cat['name'].lower():
                pochette_found = True
                print(f"\n✅ Pochette trouvée: {cat}")
                
                # Test get_category_by_id
                cat_by_id = get_category_by_id(cat['id'])
                if cat_by_id:
                    print(f"✅ get_category_by_id fonctionne: {cat_by_id['name']}")
                else:
                    print(f"❌ get_category_by_id échoue pour ID: {cat['id']}")
        
        if not pochette_found:
            print("❌ Aucune catégorie 'pochette' trouvée")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    test_categories()
