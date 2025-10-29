"""
Script pour réinitialiser la base de données avec la nouvelle structure
"""
import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import products_collection, users_collection, add_demo_products

def reset_database():
    """Réinitialise la base de données"""
    print("=== RÉINITIALISATION DE LA BASE DE DONNÉES ===")
    
    try:
        # Supprimer tous les produits existants
        result = products_collection.delete_many({})
        print(f"✅ {result.deleted_count} anciens produits supprimés")
        
        # Ajouter les nouveaux produits de démonstration
        add_demo_products()
        print("✅ Nouveaux produits de démonstration ajoutés")
        
        # Vérifier le nombre de produits
        count = products_collection.count_documents({})
        print(f"✅ Total produits dans la base : {count}")
        
        # Afficher quelques produits pour vérification
        print("\n📋 ÉCHANTILLON DE PRODUITS :")
        products = list(products_collection.find().limit(3))
        for i, product in enumerate(products, 1):
            print(f"{i}. {product['name']} ({product['brand']} - {product['model']})")
        
        print("\n=== RÉINITIALISATION TERMINÉE ===")
        
    except Exception as e:
        print(f"❌ Erreur : {e}")

if __name__ == "__main__":
    reset_database()
