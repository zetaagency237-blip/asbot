"""
Test simple pour vérifier la fonction get_products_by_category_and_brand
"""
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import get_products_by_category_and_brand, init_database

def test_products():
    """Test de récupération des produits"""
    print("=== TEST DES PRODUITS ===")
    
    # Initialiser la base de données
    print("1. Initialisation de la base de données...")
    try:
        init_database()
        print("   ✅ Base de données initialisée")
    except Exception as e:
        print(f"   ❌ Erreur : {e}")
        return
    
    # Tester différentes combinaisons
    test_cases = [
        ("pochettes", "iphone"),
        ("magsafe", "iphone"), 
        ("gadgets", "samsung"),
        ("packs", "xiaomi"),
        ("pochettes", "huawei")
    ]
    
    print("\n2. Test de récupération des produits...")
    for category, brand in test_cases:
        print(f"\n   Catégorie: {category} | Marque: {brand}")
        try:
            products = get_products_by_category_and_brand(category, brand)
            print(f"   ✅ {len(products)} produits trouvés")
            
            for i, product in enumerate(products[:2], 1):
                print(f"      {i}. {product['name']} - {product['price']}€")
                if product.get('description'):
                    print(f"         {product['description'][:30]}...")
                    
        except Exception as e:
            print(f"   ❌ Erreur : {e}")
    
    print("\n=== FIN DU TEST ===")

if __name__ == "__main__":
    test_products()
