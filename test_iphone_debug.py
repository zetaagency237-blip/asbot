import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from database.db_functions import get_brand_by_id, get_brands
    
    print("=== TEST IMAGE iPHONE ===")
    
    # Test direct iPhone
    brand = get_brand_by_id('iphone')
    
    with open("iphone_test_result.txt", "w", encoding="utf-8") as f:
        f.write("=== TEST IMAGE iPHONE ===\n\n")
        
        if brand:
            f.write(f"✅ iPhone trouvé: {brand['name']}\n")
            f.write(f"ID: {brand['id']}\n")
            f.write(f"Image URL: {brand.get('image_url', 'AUCUNE')}\n")
            f.write(f"Actif: {brand.get('active', True)}\n")
            f.write(f"Modèles: {len(brand.get('models', []))}\n")
            
            if brand.get('image_url'):
                f.write(f"✅ IMAGE PRÉSENTE\n")
                f.write(f"URL complète: {brand['image_url']}\n")
            else:
                f.write(f"❌ PAS D'IMAGE\n")
        else:
            f.write(f"❌ iPhone non trouvé!\n")
        
        # Liste toutes les marques
        f.write(f"\n--- TOUTES LES MARQUES ---\n")
        brands = get_brands()
        for i, b in enumerate(brands, 1):
            img = "🖼️" if b.get('image_url') else "📷"
            f.write(f"{i}. {img} {b['name']} (ID: {b['id']})\n")
            if b.get('image_url'):
                f.write(f"   URL: {b['image_url']}\n")
        
        f.write(f"\n=== FIN TEST ===\n")
    
    print("Résultat écrit dans iphone_test_result.txt")

except Exception as e:
    with open("iphone_test_result.txt", "w", encoding="utf-8") as f:
        f.write(f"ERREUR: {str(e)}\n")
        f.write(f"Type: {type(e)}\n")
    print(f"Erreur: {e}")
