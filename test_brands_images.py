#!/usr/bin/env python3
"""
Diagnostic des images de marques
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import get_brands, get_brand_by_id

def test_brands_images():
    print("🧪 DIAGNOSTIC IMAGES DES MARQUES")
    print("=" * 45)
    
    # Récupérer toutes les marques
    brands = get_brands()
    
    print(f"\n🏷️ {len(brands)} marques trouvées :")
    
    for brand in brands:
        active = "✅" if brand.get('active', True) else "❌"
        image = "🖼️" if brand.get('image_url') else "📷"
        models_count = len(brand.get('models', []))
        
        print(f"   {active} {image} {brand['name']} (ID: {brand['id']}) - {models_count} modèles")
        
        if brand.get('image_url'):
            url = brand['image_url']
            print(f"      URL: {url}")
        
        # Test de récupération par ID
        test_brand = get_brand_by_id(brand['id'])
        if test_brand:
            print(f"      ✅ Récupération par ID OK")
            if test_brand.get('image_url'):
                print(f"      🖼️ Image via get_brand_by_id: {test_brand['image_url'][:50]}...")
        else:
            print(f"      ❌ Erreur récupération par ID")
    
    # Test spécifique pour iPhone
    print(f"\n📱 TEST SPÉCIFIQUE iPhone :")
    iphone = get_brand_by_id('iphone')
    if iphone:
        print(f"   ✅ iPhone trouvé: {iphone['name']}")
        print(f"   Image URL: {iphone.get('image_url', 'AUCUNE')}")
        print(f"   Actif: {iphone.get('active', 'Non défini')}")
        print(f"   Modèles: {len(iphone.get('models', []))}")
    else:
        print(f"   ❌ iPhone non trouvé!")
    
    print(f"\n🎯 Test terminé")

if __name__ == "__main__":
    test_brands_images()
