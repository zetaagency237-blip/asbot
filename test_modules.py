#!/usr/bin/env python3
"""
Script de test pour vérifier que tous les modules sont bien chargés
"""

def test_imports():
    """Teste l'importation de tous les modules"""
    print("🧪 Test des imports des modules...")
    
    try:
        # Test database
        from database.db_functions import init_database, get_user, add_user
        print("✅ database.db_functions - OK")
        
        # Test menus
        from menus.menu_functions import create_main_menu, create_products_menu
        print("✅ menus.menu_functions - OK")
        
        # Test handlers
        from handlers.basic_handlers import start_command, handle_message
        print("✅ handlers.basic_handlers - OK")
        
        from handlers.admin_handlers import admin_command, addproduct_command
        print("✅ handlers.admin_handlers - OK")
        
        from handlers.callback_handlers import button_callback
        print("✅ handlers.callback_handlers - OK")
        
        print("\n🎉 Tous les modules importés avec succès !")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return False

def test_config():
    """Teste la configuration"""
    print("\n🔧 Test de configuration...")
    
    try:
        from dotenv import load_dotenv
        import os
        
        load_dotenv()
        
        bot_token = os.getenv('BOT_TOKEN')
        mongodb_uri = os.getenv('MONGODB_URI')
        admin_id = os.getenv('ADMIN_ID')
        
        if bot_token and mongodb_uri and admin_id:
            print("✅ Configuration complète")
            return True
        else:
            print("⚠️ Configuration incomplète - vérifiez le .env")
            return False
            
    except Exception as e:
        print(f"❌ Erreur de configuration : {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("   TEST BOT ANONYME SMARTPHONE")
    print("=" * 50)
    
    imports_ok = test_imports()
    config_ok = test_config()
    
    print("\n" + "=" * 50)
    if imports_ok and config_ok:
        print("🚀 Le bot est prêt à démarrer !")
    else:
        print("⚠️ Il y a des problèmes à résoudre avant de démarrer")
    print("=" * 50)
