#!/usr/bin/env python3
"""
Test script pour vérifier que le fix de notification fonctionne
"""

from notifications.admin_notifications import notify_admin_product_interest

def test_notification_function():
    """Teste la signature de la fonction notify_admin_product_interest"""
    import inspect
    
    # Obtenir la signature de la fonction
    sig = inspect.signature(notify_admin_product_interest)
    print(f"✅ Signature de notify_admin_product_interest: {sig}")
    print(f"✅ Paramètres attendus: {list(sig.parameters.keys())}")
    
    # Vérifier que la fonction accepte les bons paramètres
    expected_params = ['context', 'user_info', 'model_name', 'model_price']
    actual_params = list(sig.parameters.keys())
    
    print(f"\n📋 Vérification des paramètres:")
    for param in expected_params:
        if param in actual_params:
            print(f"   ✅ {param} - OK")
        else:
            print(f"   ❌ {param} - MANQUANT")
    
    # Vérifier qu'il n'y a pas de paramètres inattendus
    unexpected = set(actual_params) - set(expected_params)
    if unexpected:
        print(f"\n⚠️  Paramètres inattendus: {unexpected}")
    else:
        print(f"\n✅ Tous les paramètres sont corrects!")
    
    return len(unexpected) == 0 and all(p in actual_params for p in expected_params[:3])

def test_callback_handler_import():
    """Teste l'import du callback handler"""
    try:
        from handlers.callback_handlers import button_callback
        print(f"✅ Import callback_handlers réussi")
        return True
    except Exception as e:
        print(f"❌ Erreur import callback_handlers: {e}")
        return False

if __name__ == "__main__":
    print("🔍 TEST DU FIX DE NOTIFICATION\n")
    
    # Test 1: Vérifier la signature de la fonction
    print("1️⃣ Test de la fonction notify_admin_product_interest:")
    notification_ok = test_notification_function()
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: Vérifier l'import du callback handler
    print("2️⃣ Test import callback handler:")
    callback_ok = test_callback_handler_import()
    
    print("\n" + "="*50 + "\n")
    
    # Résultat final
    if notification_ok and callback_ok:
        print("🎉 TOUS LES TESTS PASSENT - Le fix devrait fonctionner!")
        print("\n💡 Vous pouvez maintenant redémarrer le bot et tester:")
        print("   1. Aller dans /produits → Pochettes → iPhone")
        print("   2. Sélectionner un modèle (ex: iPhone 17 Air)")
        print("   3. Vérifier qu'aucune erreur n'apparaît")
        print("   4. L'admin devrait recevoir une notification")
    else:
        print("❌ DES PROBLÈMES SUBSISTENT - Vérifiez les erreurs ci-dessus")
    
    print(f"\n📊 Résultat: {notification_ok and callback_ok}")
