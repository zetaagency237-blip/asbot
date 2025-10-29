#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test pour vérifier les fonctions d'images
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db_functions import (
    get_catalog_image, update_catalog_image,
    get_welcome_logo, update_welcome_logo
)

def test_image_functions():
    """Test les fonctions d'images"""
    
    print("🔍 TEST DES FONCTIONS D'IMAGES")
    print("=" * 50)
    
    # Test du logo d'accueil
    print("\n🏠 LOGO D'ACCUEIL:")
    welcome_logo = get_welcome_logo()
    print(f"   État actuel: {'✅ Présent' if welcome_logo else '❌ Absent'}")
    if welcome_logo:
        print(f"   URL: {welcome_logo}")
    
    # Test de l'image du catalogue  
    print("\n📚 IMAGE CATALOGUE:")
    catalog_image = get_catalog_image()
    print(f"   État actuel: {'✅ Présente' if catalog_image else '❌ Absente'}")
    if catalog_image:
        print(f"   URL: {catalog_image}")
    
    # Test de mise à jour (avec URL factice)
    print("\n🧪 TEST MISE À JOUR:")
    test_url = "https://res.cloudinary.com/test/image/upload/v1234567890/test.jpg"
    
    # Test logo d'accueil
    success_logo = update_welcome_logo(test_url)
    print(f"   Logo d'accueil: {'✅ Succès' if success_logo else '❌ Échec'}")
    
    # Vérifier si ça a marché
    new_welcome_logo = get_welcome_logo()
    print(f"   Récupération: {'✅ OK' if new_welcome_logo == test_url else '❌ KO'}")
    
    # Test catalogue
    success_catalog = update_catalog_image(test_url + "_catalog")
    print(f"   Image catalogue: {'✅ Succès' if success_catalog else '❌ Échec'}")
    
    # Vérifier si ça a marché
    new_catalog_image = get_catalog_image()
    print(f"   Récupération: {'✅ OK' if new_catalog_image == test_url + '_catalog' else '❌ KO'}")
    
    print("\n" + "=" * 50)
    print("🏁 TEST TERMINÉ")

if __name__ == "__main__":
    test_image_functions()
