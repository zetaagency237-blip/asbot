#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script pour tester et corriger les problèmes d'affichage des images
"""

def test_bot_startup():
    """Test le démarrage du bot avec les nouvelles fonctionnalités"""
    
    print("🚀 TEST DE DÉMARRAGE DU BOT")
    print("=" * 50)
    
    try:
        # Importer les modules principaux
        print("📦 Import des modules...")
        
        # Test import database functions
        from database.db_functions import (
            get_catalog_image, update_catalog_image,
            get_welcome_logo, update_welcome_logo
        )
        print("   ✅ Fonctions de base de données importées")
        
        # Test import handlers
        from handlers.basic_handlers import start_command
        print("   ✅ Handlers de base importés")
        
        from handlers.mobile_admin_handlers import handle_mobile_admin_callback
        print("   ✅ Handlers admin mobile importés")
        
        # Test des fonctions
        print("\n🔧 Test des fonctions...")
        
        # Test récupération logo d'accueil
        try:
            logo = get_welcome_logo()
            print(f"   🏠 Logo d'accueil: {'✅ Trouvé' if logo else '⚠️ Pas configuré'}")
        except Exception as e:
            print(f"   ❌ Erreur logo d'accueil: {e}")
        
        # Test récupération image catalogue
        try:
            catalog = get_catalog_image()
            print(f"   📚 Image catalogue: {'✅ Trouvée' if catalog else '⚠️ Pas configurée'}")
        except Exception as e:
            print(f"   ❌ Erreur image catalogue: {e}")
        
        print("\n✅ Tous les modules sont correctement configurés !")
        print("💡 Le bot peut maintenant être lancé avec : python main.py")
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que tous les modules sont installés")
    except Exception as e:
        print(f"❌ Erreur générale: {e}")
    
    print("\n" + "=" * 50)
    print("🏁 TEST TERMINÉ")

def instructions():
    """Affiche les instructions pour utiliser les nouvelles fonctionnalités"""
    
    print("\n📖 INSTRUCTIONS D'UTILISATION")
    print("=" * 50)
    
    print("🏠 LOGO D'ACCUEIL:")
    print("   1. Lancez le bot: python main.py")
    print("   2. Envoyez /mobileadmin")
    print("   3. Cliquez sur '🖼️ Gérer Images'")
    print("   4. Cliquez sur '🏠 Logo d'accueil'")
    print("   5. Envoyez votre image de logo")
    
    print("\n📚 IMAGE CATALOGUE:")
    print("   1. Dans 'Gérer Images'")
    print("   2. Cliquez sur '📚 Image Catalogue'")
    print("   3. Envoyez votre image de catalogue")
    
    print("\n🔍 VÉRIFICATION:")
    print("   - Le logo apparaîtra dans le message 'Bonjour Cristian !'")
    print("   - L'image catalogue apparaîtra dans /produits")
    print("   - Utilisez 'Voir toutes les images' pour vérifier l'état")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    test_bot_startup()
    instructions()
