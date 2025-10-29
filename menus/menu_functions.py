"""
Fonctions pour créer les menus interactifs
"""
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.db_functions import is_admin

def create_main_menu(user_id=None):
    """Crée le menu principal (maintenant simplifié pour les commandes)"""
    keyboard = []
    
    # Ajouter le bouton admin si c'est l'administrateur
    if user_id and is_admin(user_id):
        keyboard.append([InlineKeyboardButton("Administration", callback_data="admin_menu")])
    
    # Si pas d'admin, retourner None pour ne pas afficher de clavier
    if not keyboard:
        return None
        
    return InlineKeyboardMarkup(keyboard)

def create_products_menu():
    """Crée le menu des produits dynamiquement depuis la base de données"""
    from database.db_functions import get_categories
    
    categories = get_categories()
    keyboard = []
    
    for category in categories:
        if category.get('active', True):
            # Utiliser l'ID de la catégorie comme callback_data au lieu des noms fixes
            keyboard.append([InlineKeyboardButton(category['name'], callback_data=f"category_{category['id']}")])
    
    keyboard.append([InlineKeyboardButton("Retour", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

def create_services_menu():
    """Crée le menu des services"""
    keyboard = [
        [InlineKeyboardButton("Déblocage", callback_data="deblocage")],
        [InlineKeyboardButton("Désimlocage", callback_data="desimlockage")],
        [InlineKeyboardButton("Déclonage", callback_data="declonage")],
        [InlineKeyboardButton("Cas Particuliers", callback_data="cas_particulier")],
        [InlineKeyboardButton("Retour", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_brands_menu():
    """Crée le menu des marques dynamiquement depuis la base de données"""
    from database.db_functions import get_brands
    
    brands = get_brands()
    keyboard = []
    
    for brand in brands:
        if brand.get('active', True):
            keyboard.append([InlineKeyboardButton(brand['name'], callback_data=brand['id'])])
    
    keyboard.append([InlineKeyboardButton("Retour", callback_data="produits")])
    return InlineKeyboardMarkup(keyboard)

def create_models_menu(brand_id):
    """Crée le menu des modèles dynamiquement depuis la base de données"""
    from database.db_functions import get_brand_models
    
    models = get_brand_models(brand_id)
    keyboard = []
    
    for model in models:
        keyboard.append([InlineKeyboardButton(model['name'], callback_data=f"model_{model['id']}")])
    
    # Bouton retour vers les marques
    keyboard.append([InlineKeyboardButton("Retour aux marques", callback_data="back_to_brands")])
    
    return InlineKeyboardMarkup(keyboard)

def create_admin_menu():
    """Crée le menu d'administration"""
    keyboard = [
        [InlineKeyboardButton("Gestion Utilisateurs", callback_data="admin_users")],
        [InlineKeyboardButton("Gestion Produits", callback_data="admin_products")],
        [InlineKeyboardButton("Gestion Images", callback_data="admin_images")],
        [InlineKeyboardButton("Statistiques", callback_data="admin_stats")],
        [InlineKeyboardButton("Diffusion Message", callback_data="admin_broadcast")],
        [InlineKeyboardButton("Retour", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_product_admin_menu():
    """Crée le menu d'administration des produits"""
    keyboard = [
        [
            InlineKeyboardButton("Ajouter", callback_data="add_product"),
            InlineKeyboardButton("Lister", callback_data="list_products")
        ],
        [
            InlineKeyboardButton("Modifier", callback_data="edit_product"),
            InlineKeyboardButton("Supprimer", callback_data="delete_product_menu")
        ],
        [InlineKeyboardButton("Retour Admin", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_image_admin_menu():
    """Crée le menu d'administration des images"""
    keyboard = [
        [
            InlineKeyboardButton("Ajouter Image", callback_data="add_image"),
            InlineKeyboardButton("Modifier Image", callback_data="modify_image")
        ],
        [
            InlineKeyboardButton("Images Produits", callback_data="list_images"),
            InlineKeyboardButton("Supprimer Image", callback_data="delete_image")
        ],
        [InlineKeyboardButton("Retour Admin", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
