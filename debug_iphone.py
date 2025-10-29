#!/usr/bin/env python3
"""
Test du callback iPhone pour debug
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import get_brand_by_id, get_category_by_id

def test_iphone_callback():
    print("🧪 TEST CALLBACK iPhone")
    print("=" * 30)
    
    # Simuler les données du callback iPhone
    data = "iphone"
    category_id = "pochettes"  # Valeur par défaut
    
    print(f"\n📋 Données de test :")
    print(f"   Brand ID: {data}")
    print(f"   Category ID: {category_id}")
    
    # Test de récupération de la marque
    print(f"\n🏷️ Test get_brand_by_id('{data}'):")
    brand = get_brand_by_id(data)
    if brand:
        print(f"   ✅ Marque trouvée: {brand['name']}")
        print(f"   ID: {brand['id']}")
        print(f"   Image URL: {brand.get('image_url', 'AUCUNE')}")
        print(f"   Actif: {brand.get('active', True)}")
        
        if brand.get('image_url'):
            print(f"   🖼️ URL complète: {brand['image_url']}")
            print(f"   🔗 URL valide: {'https://' in brand['image_url'] or 'http://' in brand['image_url']}")
        else:
            print(f"   📷 Pas d'image définie")
    else:
        print(f"   ❌ Marque '{data}' non trouvée!")
    
    # Test de récupération de la catégorie
    print(f"\n📂 Test get_category_by_id('{category_id}'):")
    category = get_category_by_id(category_id)
    if category:
        print(f"   ✅ Catégorie trouvée: {category['name']}")
        print(f"   ID: {category['id']}")
    else:
        print(f"   ❌ Catégorie '{category_id}' non trouvée!")
    
    # Simuler la logique du handler
    print(f"\n🔄 Simulation du handler :")
    if brand and category:
        brand_name = brand['name']
        category_name = category['name']
        text = f"*{brand_name}* - {category_name}\n\nSélectionnez le modèle :"
        print(f"   Texte généré: {text}")
        
        if brand.get('image_url'):
            print(f"   📸 Tentative d'affichage d'image: OUI")
            print(f"   URL à utiliser: {brand['image_url']}")
        else:
            print(f"   📸 Tentative d'affichage d'image: NON (pas d'URL)")
    
    print(f"\n🎯 Test terminé")

if __name__ == "__main__":
    test_iphone_callback()
