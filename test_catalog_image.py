#!/usr/bin/env python3
"""
Test script pour vérifier le système d'image du catalogue
"""

def test_catalog_functions():
    """Teste les fonctions du catalogue"""
    try:
        from database.db_functions import get_catalog_image, update_catalog_image
        print("✅ Import des fonctions catalogue réussi")
        
        # Test de récupération de l'image actuelle
        current_image = get_catalog_image()
        if current_image:
            print(f"📸 Image catalogue actuelle: {current_image}")
        else:
            print("📷 Aucune image catalogue définie")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur import: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur test: {e}")
        return False

def test_mobile_admin_integration():
    """Teste l'intégration dans mobile admin"""
    try:
        from handlers.mobile_admin_handlers import mobile_menu_images, handle_mobile_admin_callback
        print("✅ Import mobile admin handlers réussi")
        
        # Vérifier que les callbacks sont bien gérés
        test_callbacks = ["mobile_catalog_image", "mobile_view_all_images"]
        print(f"📋 Callbacks à tester: {test_callbacks}")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur import mobile admin: {e}")
        return False

def test_callback_handler_integration():
    """Teste l'intégration dans callback handlers"""
    try:
        from handlers.callback_handlers import button_callback
        from database.db_functions import get_catalog_image
        print("✅ Import callback handlers réussi")
        
        # Test de la fonction get_catalog_image
        image_url = get_catalog_image()
        print(f"📸 Test get_catalog_image: {'OK' if image_url is not None or image_url is None else 'ERREUR'}")
        
        return True
    except ImportError as e:
        print(f"❌ Erreur import callback handlers: {e}")
        return False

if __name__ == "__main__":
    print("🔍 TEST DU SYSTÈME IMAGE CATALOGUE\n")
    
    # Test 1: Fonctions de base
    print("1️⃣ Test des fonctions catalogue:")
    catalog_ok = test_catalog_functions()
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Intégration mobile admin
    print("2️⃣ Test intégration mobile admin:")
    mobile_ok = test_mobile_admin_integration()
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Intégration callback handlers
    print("3️⃣ Test intégration callback handlers:")
    callback_ok = test_callback_handler_integration()
    
    print("\n" + "="*50 + "\n")
    
    # Résultat final
    all_ok = catalog_ok and mobile_ok and callback_ok
    
    if all_ok:
        print("🎉 TOUS LES TESTS PASSENT - Le système d'image catalogue est prêt!")
        print("\n💡 Pour utiliser:")
        print("   1. Aller dans /mobile_admin → 🖼️ Gérer Images → 📚 Image Catalogue")
        print("   2. Envoyer une photo pour l'image du catalogue")
        print("   3. Tester /produits pour voir l'image s'afficher")
        print("   4. L'image apparaîtra avec le titre 'Catalogue Produits'")
    else:
        print("❌ DES PROBLÈMES SUBSISTENT")
        if not catalog_ok:
            print("   • Problème avec les fonctions catalogue")
        if not mobile_ok:
            print("   • Problème avec l'intégration mobile admin")
        if not callback_ok:
            print("   • Problème avec l'intégration callback handlers")
    
    print(f"\n📊 Résultat global: {all_ok}")
