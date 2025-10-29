"""
Fonctions pour créer les menus interactifs
"""def create_admin_menu():
    """Crée le menu d'administration"""
    keyboard = [
        [InlineKeyboardButton("GESTION UTILISATEURS", callback_data="admin_users")],
        [InlineKeyboardButton("GESTION PRODUITS", callback_data="admin_products")],
        [InlineKeyboardButton("GESTION IMAGES", callback_data="admin_images")],
        [InlineKeyboardButton("STATISTIQUES", callback_data="admin_stats")],
        [InlineKeyboardButton("DIFFUSION MESSAGE", callback_data="admin_broadcast")],
        [InlineKeyboardButton("RETOUR", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)ram import InlineKeyboardButton, InlineKeyboardMarkup
from database.db_functions import is_admin

def create_main_menu(user_id=None):
    """Crée le menu principal (maintenant simplifié pour les commandes)"""
    keyboard = []
    
    # Ajouter le bouton admin si c'est l'administrateur
    if user_id and is_admin(user_id):
        keyboard.append([InlineKeyboardButton("ADMINISTRATION", callback_data="admin_menu")])
    
    # Si pas d'admin, retourner None pour ne pas afficher de clavier
    if not keyboard:
        return None
        
    return InlineKeyboardMarkup(keyboard)

def create_products_menu():
    """Crée le menu des produits"""
    keyboard = [
        [InlineKeyboardButton("POCHETTES", callback_data="pochettes")],
        [InlineKeyboardButton("CHARGEURS MAGSAFE", callback_data="magsafe")],
        [InlineKeyboardButton("AUTRES GADGETS", callback_data="gadgets")],
        [InlineKeyboardButton("PACKS", callback_data="packs")],
        [InlineKeyboardButton("RETOUR", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_services_menu():
    """Crée le menu des services"""
    keyboard = [
        [InlineKeyboardButton("DÉBLOCAGE", callback_data="deblocage")],
        [InlineKeyboardButton("DÉSIMLOCAGE", callback_data="desimlockage")],
        [InlineKeyboardButton("DÉCLONAGE", callback_data="declonage")],
        [InlineKeyboardButton("CAS PARTICULIERS", callback_data="cas_particulier")],
        [InlineKeyboardButton("RETOUR", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_brands_menu():
    """Crée le menu des marques"""
    keyboard = [
        [InlineKeyboardButton("IPHONE", callback_data="iphone")],
        [InlineKeyboardButton("SAMSUNG", callback_data="samsung")],
        [InlineKeyboardButton("XIAOMI", callback_data="xiaomi")],
        [InlineKeyboardButton("HUAWEI", callback_data="huawei")],
        [InlineKeyboardButton("RETOUR", callback_data="produits")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_admin_menu():
    """Crée le menu d'administration"""
    keyboard = [
        [InlineKeyboardButton("👥 Gestion Utilisateurs", callback_data="admin_users")],
        [InlineKeyboardButton("📱 Gestion Produits", callback_data="admin_products")],
        [InlineKeyboardButton("�️ Gestion Images", callback_data="admin_images")],
        [InlineKeyboardButton("�📊 Statistiques", callback_data="admin_stats")],
        [InlineKeyboardButton("💬 Diffusion Message", callback_data="admin_broadcast")],
        [InlineKeyboardButton("⬅️ Retour", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_product_admin_menu():
    """Crée le menu d'administration des produits"""
    keyboard = [
        [
            InlineKeyboardButton("➕ Ajouter", callback_data="add_product"),
            InlineKeyboardButton("📋 Lister", callback_data="list_products")
        ],
        [
            InlineKeyboardButton("✏️ Modifier", callback_data="edit_product"),
            InlineKeyboardButton("🗑️ Supprimer", callback_data="delete_product_menu")
        ],
        [InlineKeyboardButton("⬅️ Retour Admin", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_image_admin_menu():
    """Crée le menu d'administration des images"""
    keyboard = [
        [
            InlineKeyboardButton("🖼️ Ajouter Image", callback_data="add_image"),
            InlineKeyboardButton("📸 Modifier Image", callback_data="modify_image")
        ],
        [
            InlineKeyboardButton("📋 Images Produits", callback_data="list_images"),
            InlineKeyboardButton("🗑️ Supprimer Image", callback_data="delete_image")
        ],
        [InlineKeyboardButton("⬅️ Retour Admin", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)
