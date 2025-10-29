"""
Fonctions de base de données pour MongoDB
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Charger les variables d'environnement
load_dotenv()

# Configuration MongoDB
MONGODB_URI = os.getenv('MONGODB_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# Connexion MongoDB
client = MongoClient(MONGODB_URI)
db = client[DATABASE_NAME]
users_collection = db.users
products_collection = db.products

def init_database():
    """Initialise la base de données MongoDB"""
    try:
        # Créer les index pour optimiser les requêtes
        users_collection.create_index("user_id", unique=True)
        products_collection.create_index("category")
        products_collection.create_index("brand")
        print("Base de données MongoDB initialisée avec succès")
        
        # Initialiser les structures
        init_categories_and_brands()
        
        # Ajouter quelques produits de démonstration si la collection est vide
        if products_collection.count_documents({}) == 0:
            add_demo_products()
            
    except Exception as e:
        print(f"Erreur lors de l'initialisation de la base de données : {e}")

def init_categories_and_brands():
    """Initialise les catégories et marques avec héritage"""
    categories_collection = db.categories
    brands_collection = db.brands
    
    # Structure des catégories avec héritage et images
    categories = [
        {
            "id": "pochettes",
            "name": "Pochettes",
            "parent": None,
            "subcategories": [],
            "image_url": "",
            "description": "Pochettes et coques de protection pour tous modèles",
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "magsafe", 
            "name": "Chargeurs MagSafe",
            "parent": None,
            "subcategories": [],
            "image_url": "",
            "description": "Chargeurs sans fil et accessoires MagSafe",
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "gadgets",
            "name": "Autres Gadgets", 
            "parent": None,
            "subcategories": [],
            "image_url": "",
            "description": "Supports, câbles et accessoires divers",
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "packs",
            "name": "Packs",
            "parent": None,
            "subcategories": [],
            "image_url": "",
            "description": "Packs complets à prix réduit",
            "active": True,
            "created_at": datetime.now()
        }
    ]
    
    # Structure des marques avec modèles et images
    brands = [
        {
            "id": "iphone",
            "name": "iPhone",
            "image_url": "",
            "description": "Accessoires premium pour iPhone Apple",
            "models": [
                {"id": "iphone_17_pro_max", "name": "iPhone 17 Pro Max"},
                {"id": "iphone_17_pro", "name": "iPhone 17 Pro"},
                {"id": "iphone_17_air", "name": "iPhone 17 Air"},
                {"id": "iphone_17", "name": "iPhone 17"},
                {"id": "iphone_16_pro_max", "name": "iPhone 16 Pro Max"},
                {"id": "iphone_16_pro", "name": "iPhone 16 Pro"},
                {"id": "iphone_16", "name": "iPhone 16"},
                {"id": "iphone_15_pro_max", "name": "iPhone 15 Pro Max"},
                {"id": "iphone_15_pro", "name": "iPhone 15 Pro"},
                {"id": "iphone_15", "name": "iPhone 15"}
            ],
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "samsung",
            "name": "Samsung",
            "image_url": "",
            "description": "Accessoires pour la gamme Galaxy Samsung",
            "models": [
                {"id": "galaxy_s25_ultra", "name": "Galaxy S25 Ultra"},
                {"id": "galaxy_s25_plus", "name": "Galaxy S25+"},
                {"id": "galaxy_s25", "name": "Galaxy S25"},
                {"id": "galaxy_s24_ultra", "name": "Galaxy S24 Ultra"},
                {"id": "galaxy_s24_plus", "name": "Galaxy S24+"},
                {"id": "galaxy_s24", "name": "Galaxy S24"},
                {"id": "galaxy_a55", "name": "Galaxy A55"},
                {"id": "galaxy_a35", "name": "Galaxy A35"},
                {"id": "galaxy_z_fold_6", "name": "Galaxy Z Fold 6"},
                {"id": "galaxy_z_flip_6", "name": "Galaxy Z Flip 6"}
            ],
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "xiaomi",
            "name": "Xiaomi",
            "image_url": "",
            "description": "Accessoires pour Xiaomi, Redmi et Poco",
            "models": [
                {"id": "xiaomi_15_pro", "name": "Xiaomi 15 Pro"},
                {"id": "xiaomi_15", "name": "Xiaomi 15"},
                {"id": "redmi_note_14", "name": "Redmi Note 14"},
                {"id": "redmi_note_13", "name": "Redmi Note 13"},
                {"id": "xiaomi_14_ultra", "name": "Xiaomi 14 Ultra"},
                {"id": "xiaomi_14", "name": "Xiaomi 14"},
                {"id": "poco_x6_pro", "name": "Poco X6 Pro"},
                {"id": "poco_x6", "name": "Poco X6"},
                {"id": "poco_f6", "name": "Poco F6"}
            ],
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "huawei",
            "name": "Huawei",
            "image_url": "",
            "description": "Accessoires pour Huawei Pura, P et Mate",
            "models": [
                {"id": "pura_80_pro", "name": "Pura 80 Pro"},
                {"id": "pura_80", "name": "Pura 80"},
                {"id": "p70_pro", "name": "P70 Pro"},
                {"id": "p70", "name": "P70"},
                {"id": "mate_70_pro", "name": "Mate 70 Pro"},
                {"id": "mate_70", "name": "Mate 70"},
                {"id": "nova_12", "name": "Nova 12"},
                {"id": "nova_11", "name": "Nova 11"}
            ],
            "active": True,
            "created_at": datetime.now()
        },
        {
            "id": "pixel",
            "name": "Google Pixel",
            "image_url": "",
            "description": "Accessoires officiels Google Pixel",
            "models": [
                {"id": "pixel_9_pro_xl", "name": "Pixel 9 Pro XL"},
                {"id": "pixel_9_pro", "name": "Pixel 9 Pro"},
                {"id": "pixel_9", "name": "Pixel 9"},
                {"id": "pixel_8_pro", "name": "Pixel 8 Pro"},
                {"id": "pixel_8", "name": "Pixel 8"},
                {"id": "pixel_7_pro", "name": "Pixel 7 Pro"},
                {"id": "pixel_7", "name": "Pixel 7"},
                {"id": "pixel_fold", "name": "Pixel Fold"}
            ],
            "active": True,
            "created_at": datetime.now()
        }
    ]
    
    try:
        # Vérifier et ajouter les catégories si elles n'existent pas
        if categories_collection.count_documents({}) == 0:
            categories_collection.insert_many(categories)
            print("✅ Catégories initialisées")
        
        # Vérifier et ajouter les marques si elles n'existent pas
        if brands_collection.count_documents({}) == 0:
            brands_collection.insert_many(brands)
            print("✅ Marques et modèles initialisés")
            
    except Exception as e:
        print(f"Erreur lors de l'initialisation des structures : {e}")

def add_demo_products():
    """Ajoute des produits de démonstration"""
    demo_products = [
        {
            "name": "Pochette Cuir Premium iPhone 17 Pro Max",
            "category": "pochettes",
            "brand": "iphone",
            "model": "iPhone 17 Pro Max",
            "price": 34.99,
            "image_url": "",
            "description": "Pochette en cuir véritable avec protection renforcée pour iPhone 17 Pro Max",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Pochette Silicone iPhone 17 Air",
            "category": "pochettes", 
            "brand": "iphone",
            "model": "iPhone 17 Air",
            "price": 24.99,
            "image_url": "",
            "description": "Pochette silicone ultra-fine pour iPhone 17 Air",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Pochette Premium iPhone 17 Pro",
            "category": "pochettes", 
            "brand": "iphone",
            "model": "iPhone 17 Pro",
            "price": 29.99,
            "image_url": "",
            "description": "Pochette premium avec protection avancée",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Chargeur MagSafe 4ème génération",
            "category": "magsafe",
            "brand": "iphone",
            "model": "iPhone 17 Pro Max",
            "price": 49.00,
            "image_url": "",
            "description": "Chargeur sans fil MagSafe nouvelle génération compatible iPhone 17",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Support Voiture Galaxy S25 Ultra",
            "category": "gadgets",
            "brand": "samsung",
            "model": "Galaxy S25 Ultra",
            "price": 24.99,
            "image_url": "",
            "description": "Support magnétique ultra-résistant pour Galaxy S25 Ultra",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Pack Protection Xiaomi 15 Pro",
            "category": "packs",
            "brand": "xiaomi",
            "model": "Xiaomi 15 Pro",
            "price": 44.99,
            "image_url": "",
            "description": "Pack complet nouvelle génération : coque + verre trempé + chargeur rapide",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Pochette Galaxy S25 Ultra",
            "category": "pochettes",
            "brand": "samsung",
            "model": "Galaxy S25 Ultra",
            "price": 27.99,
            "image_url": "",
            "description": "Pochette résistante pour Galaxy S25 Ultra avec compartiment S Pen",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Chargeur Rapide Xiaomi 15",
            "category": "magsafe",
            "brand": "xiaomi",
            "model": "Xiaomi 15",
            "price": 39.99,
            "image_url": "",
            "description": "Chargeur sans fil rapide 67W pour Xiaomi 15",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Support Bureau Huawei Pura 80",
            "category": "gadgets",
            "brand": "huawei",
            "model": "Pura 80 Pro",
            "price": 22.99,
            "image_url": "",
            "description": "Support de bureau ajustable pour Huawei Pura 80 Pro",
            "created_at": datetime.now(),
            "active": True
        },
        {
            "name": "Pochette Premium Google Pixel 9 Pro XL",
            "category": "pochettes",
            "brand": "pixel",
            "model": "Pixel 9 Pro XL",
            "price": 32.99,
            "image_url": "",
            "description": "Pochette premium avec protection avancée pour Pixel 9 Pro XL",
            "created_at": datetime.now(),
            "active": True
        }
    ]
    
    try:
        products_collection.insert_many(demo_products)
        print("Produits de démonstration ajoutés avec succès")
    except Exception as e:
        print(f"Erreur lors de l'ajout des produits de démonstration : {e}")

# === FONCTIONS DE GESTION DYNAMIQUE POUR SMARTPHONE ===

def get_categories():
    """Récupère toutes les catégories actives"""
    try:
        categories_collection = db.categories
        return list(categories_collection.find({"active": True}))
    except Exception as e:
        print(f"Erreur récupération catégories : {e}")
        return []

def get_brands():
    """Récupère toutes les marques actives"""
    try:
        brands_collection = db.brands
        return list(brands_collection.find({"active": True}))
    except Exception as e:
        print(f"Erreur récupération marques : {e}")
        return []

def add_new_category(category_id, category_name, parent=None):
    """Ajoute une nouvelle catégorie"""
    try:
        categories_collection = db.categories
        new_category = {
            "id": category_id,
            "name": category_name,
            "parent": parent,
            "subcategories": [],
            "active": True,
            "created_at": datetime.now()
        }
        result = categories_collection.insert_one(new_category)
        print(f"✅ Catégorie {category_name} ajoutée")
        return result.inserted_id
    except Exception as e:
        print(f"Erreur ajout catégorie : {e}")
        return None

def add_new_brand(brand_id, brand_name, models=[]):
    """Ajoute une nouvelle marque"""
    try:
        brands_collection = db.brands
        new_brand = {
            "id": brand_id,
            "name": brand_name,
            "models": models,
            "active": True,
            "created_at": datetime.now()
        }
        result = brands_collection.insert_one(new_brand)
        print(f"✅ Marque {brand_name} ajoutée")
        return result.inserted_id
    except Exception as e:
        print(f"Erreur ajout marque : {e}")
        return None

def add_model_to_brand(brand_id, model_id, model_name):
    """Ajoute un modèle à une marque existante"""
    try:
        brands_collection = db.brands
        result = brands_collection.update_one(
            {"id": brand_id},
            {"$push": {"models": {"id": model_id, "name": model_name}}}
        )
        if result.modified_count > 0:
            print(f"✅ Modèle {model_name} ajouté à {brand_id}")
            return True
        return False
    except Exception as e:
        print(f"Erreur ajout modèle : {e}")
        return False

def get_brand_models(brand_id):
    """Récupère les modèles d'une marque"""
    try:
        brands_collection = db.brands
        brand = brands_collection.find_one({"id": brand_id})
        return brand.get("models", []) if brand else []
    except Exception as e:
        print(f"Erreur récupération modèles : {e}")
        return []

def get_products_by_category(category):
    """Récupère les produits par catégorie depuis MongoDB"""
    try:
        products = list(products_collection.find({"category": category}))
        return products
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        return []

def get_products_by_category_and_brand(category, brand):
    """Récupère les produits par catégorie et marque depuis MongoDB"""
    try:
        products = list(products_collection.find({
            "category": category,
            "brand": brand,
            "active": True
        }))
        return products
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        return []

def get_products_by_category_brand_model(category, brand, model):
    """Récupère les produits par catégorie, marque et modèle"""
    try:
        return list(products_collection.find({
            "category": category,
            "brand": brand,
            "model": model
        }).limit(10))
    except Exception as e:
        print(f"Erreur lors de la récupération des produits: {e}")
        return []

def toggle_category_status(category_id):
    """Active/désactive une catégorie"""
    try:
        categories_collection = db.categories
        category = categories_collection.find_one({"id": category_id})
        if category:
            new_status = not category.get("active", True)
            result = categories_collection.update_one(
                {"id": category_id},
                {"$set": {"active": new_status}}
            )
            return new_status if result.modified_count > 0 else None
        return None
    except Exception as e:
        print(f"Erreur toggle catégorie : {e}")
        return None

def toggle_brand_status(brand_id):
    """Active/désactive une marque"""
    try:
        brands_collection = db.brands
        brand = brands_collection.find_one({"id": brand_id})
        if brand:
            new_status = not brand.get("active", True)
            result = brands_collection.update_one(
                {"id": brand_id},
                {"$set": {"active": new_status}}
            )
            return new_status if result.modified_count > 0 else None
        return None
    except Exception as e:
        print(f"Erreur toggle marque : {e}")
        return None

# === FONCTIONS DE GESTION DES IMAGES DE MENUS ===

def update_category_image(category_id, image_url):
    """Met à jour l'image d'une catégorie"""
    try:
        categories_collection = db.categories
        result = categories_collection.update_one(
            {"id": category_id},
            {"$set": {"image_url": image_url}}
        )
        if result.modified_count > 0:
            print(f"✅ Image de la catégorie {category_id} mise à jour")
            return True
        return False
    except Exception as e:
        print(f"Erreur mise à jour image catégorie : {e}")
        return False

def update_brand_image(brand_id, image_url):
    """Met à jour l'image d'une marque"""
    try:
        brands_collection = db.brands
        result = brands_collection.update_one(
            {"id": brand_id},
            {"$set": {"image_url": image_url}}
        )
        if result.modified_count > 0:
            print(f"✅ Image de la marque {brand_id} mise à jour")
            return True
        return False
    except Exception as e:
        print(f"Erreur mise à jour image marque : {e}")
        return False

def get_category_by_id(category_id):
    """Récupère une catégorie par son ID"""
    try:
        categories_collection = db.categories
        return categories_collection.find_one({"id": category_id})
    except Exception as e:
        print(f"Erreur récupération catégorie : {e}")
        return None

def get_brand_by_id(brand_id):
    """Récupère une marque par son ID"""
    try:
        brands_collection = db.brands
        return brands_collection.find_one({"id": brand_id})
    except Exception as e:
        print(f"Erreur récupération marque : {e}")
        return None

def get_user(user_id):
    """Récupère les informations d'un utilisateur depuis MongoDB"""
    try:
        user = users_collection.find_one({"user_id": user_id})
        return user
    except Exception as e:
        print(f"Erreur lors de la récupération de l'utilisateur : {e}")
        return None

def add_user(user_id, prenom):
    """Ajoute un nouvel utilisateur dans MongoDB"""
    try:
        user_data = {
            "user_id": user_id,
            "prenom": prenom,
            "authenticated": True,
            "created_at": datetime.now(),
            "last_activity": datetime.now()
        }
        
        # Utiliser upsert pour insérer ou mettre à jour
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": user_data},
            upsert=True
        )
        print(f"Utilisateur {prenom} (ID: {user_id}) ajouté/mis à jour avec succès")
    except Exception as e:
        print(f"Erreur lors de l'ajout de l'utilisateur : {e}")

def update_user_activity(user_id):
    """Met à jour la dernière activité de l'utilisateur"""
    try:
        users_collection.update_one(
            {"user_id": user_id},
            {"$set": {"last_activity": datetime.now()}}
        )
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'activité : {e}")

def add_product(name, category, brand, model, price, image_url, description):
    """Ajoute un produit dans MongoDB"""
    try:
        product_data = {
            "name": name,
            "category": category,
            "brand": brand,
            "model": model,
            "price": price,
            "image_url": image_url,
            "description": description,
            "created_at": datetime.now(),
            "active": True
        }
        
        result = products_collection.insert_one(product_data)
        print(f"Produit {name} ajouté avec succès (ID: {result.inserted_id})")
        return result.inserted_id
    except Exception as e:
        print(f"Erreur lors de l'ajout du produit : {e}")
        return None

def is_admin(user_id):
    """Vérifie si l'utilisateur est administrateur"""
    return user_id == ADMIN_ID

def get_all_users():
    """Récupère tous les utilisateurs"""
    try:
        users = list(users_collection.find())
        return users
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs : {e}")
        return []

def get_all_products():
    """Récupère tous les produits"""
    try:
        products = list(products_collection.find())
        return products
    except Exception as e:
        print(f"Erreur lors de la récupération des produits : {e}")
        return []

def delete_product(product_id):
    """Supprime un produit"""
    try:
        from bson import ObjectId
        result = products_collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0
    except Exception as e:
        print(f"Erreur lors de la suppression du produit : {e}")
        return False

def update_product(product_id, updates):
    """Met à jour un produit"""
    try:
        from bson import ObjectId
        result = products_collection.update_one(
            {"_id": ObjectId(product_id)},
            {"$set": updates}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Erreur lors de la mise à jour du produit : {e}")
        return False

def get_user_stats():
    """Récupère les statistiques des utilisateurs"""
    try:
        total_users = users_collection.count_documents({})
        today_users = users_collection.count_documents({
            "created_at": {"$gte": datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)}
        })
        return {"total": total_users, "today": today_users}
    except Exception as e:
        print(f"Erreur lors de la récupération des stats : {e}")
        return {"total": 0, "today": 0}

def get_catalog_image():
    """Récupère l'URL de l'image du catalogue depuis la base de données"""
    try:
        # Chercher dans une collection spéciale pour les images du système
        system_images = db.system_images
        catalog_img = system_images.find_one({"type": "catalog"})
        
        if catalog_img and catalog_img.get('image_url'):
            return catalog_img['image_url']
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image catalogue : {e}")
        return None

def update_catalog_image(image_url):
    """Met à jour l'image du catalogue"""
    try:
        system_images = db.system_images
        result = system_images.update_one(
            {"type": "catalog"},
            {"$set": {"image_url": image_url, "updated_at": datetime.now()}},
            upsert=True
        )
        print(f"✅ Image catalogue mise à jour: {image_url}")
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'image catalogue : {e}")
        return False

def get_welcome_logo():
    """Récupère l'URL du logo d'accueil depuis la base de données"""
    try:
        system_images = db.system_images
        logo_img = system_images.find_one({"type": "welcome_logo"})
        
        if logo_img and logo_img.get('image_url'):
            return logo_img['image_url']
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération du logo d'accueil : {e}")
        return None

def update_welcome_logo(image_url):
    """Met à jour le logo d'accueil"""
    try:
        system_images = db.system_images
        result = system_images.update_one(
            {"type": "welcome_logo"},
            {"$set": {"image_url": image_url, "updated_at": datetime.now()}},
            upsert=True
        )
        print(f"✅ Logo d'accueil mis à jour: {image_url}")
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour du logo d'accueil : {e}")
        return False

def get_services_image():
    """Récupère l'URL de l'image des services depuis la base de données"""
    try:
        system_images = db.system_images
        services_img = system_images.find_one({"type": "services"})
        
        if services_img and services_img.get('image_url'):
            return services_img['image_url']
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image services : {e}")
        return None

def update_services_image(image_url):
    """Met à jour l'image des services"""
    try:
        system_images = db.system_images
        result = system_images.update_one(
            {"type": "services"},
            {"$set": {"image_url": image_url, "updated_at": datetime.now()}},
            upsert=True
        )
        print(f"✅ Image services mise à jour: {image_url}")
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'image services : {e}")
        return False

def get_service_image(service_type):
    """Récupère l'URL de l'image d'un sous-service spécifique"""
    try:
        system_images = db.system_images
        service_img = system_images.find_one({"type": f"service_{service_type}"})
        
        if service_img and service_img.get('image_url'):
            return service_img['image_url']
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération de l'image service {service_type} : {e}")
        return None

def update_service_image(service_type, image_url):
    """Met à jour l'image d'un sous-service spécifique"""
    try:
        system_images = db.system_images
        result = system_images.update_one(
            {"type": f"service_{service_type}"},
            {"$set": {"image_url": image_url, "updated_at": datetime.now()}},
            upsert=True
        )
        print(f"✅ Image service {service_type} mise à jour: {image_url}")
        return True
    except Exception as e:
        print(f"Erreur lors de la mise à jour de l'image service {service_type} : {e}")
        return False
