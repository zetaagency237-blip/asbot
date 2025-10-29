# GUIDE ADMIN - GESTION DES IMAGES ET PRODUITS

## 🔧 NOUVELLES COMMANDES ADMINISTRATEUR

### 📱 GESTION DES PRODUITS

#### ✏️ Modifier un produit
```
/editproduct [ID] [champ] [nouvelle_valeur]
```

**Exemples :**
- `/editproduct 6543210abc name "Nouveau nom"`
- `/editproduct 6543210abc price 35.99`
- `/editproduct 6543210abc description "Nouvelle description"`

**Champs modifiables :**
- `name` : Nom du produit
- `price` : Prix (nombre décimal)
- `description` : Description
- `category` : Catégorie (pochettes, magsafe, gadgets, packs)
- `brand` : Marque (iphone, samsung, xiaomi, huawei)
- `model` : Modèle

#### 🗑️ Supprimer un produit
```
/deleteproduct [ID]
```

**Exemple :**
- `/deleteproduct 6543210abcdef`

### 🖼️ GESTION DES IMAGES (CLOUDINARY)

#### 📤 Ajouter/Modifier une image
1. Utilisez la commande :
   ```
   /addimage [ID_produit]
   ```

2. Le bot vous confirmera le produit et demandera l'image

3. **Envoyez l'image** (photo) directement dans le chat

4. L'image sera automatiquement :
   - ✅ Uploadée sur Cloudinary
   - ✅ Associée au produit
   - ✅ Affichée dans le catalogue

**Exemple complet :**
```
Vous : /addimage 6543210abc
Bot : 🖼️ Produit: Coque iPhone... Veuillez envoyer l'image
Vous : [Envoyer la photo]
Bot : ✅ Image ajoutée avec succès !
```

#### 📋 Voir l'état des images
- Via le menu admin : `/admin` > 🖼️ Gestion Images > 📋 Images Produits
- Affiche quels produits ont des images ou non

#### 🗑️ Supprimer une image
Pour retirer l'image d'un produit (sans la supprimer de Cloudinary) :
```
/editproduct [ID] image_url ""
```

### 📊 AUTRES COMMANDES ADMIN

#### 📋 Lister tous les produits avec infos
```
/editproduct
```
(sans arguments - affiche la liste avec IDs)

#### 👥 Lister tous les utilisateurs
```
/listusers
```

#### 📊 Voir les statistiques
```
/stats
```

#### 💬 Diffuser un message
```
/broadcast Votre message ici
```

## 🔧 CONFIGURATION CLOUDINARY

Assurez-vous d'avoir ces variables dans votre fichier `.env` :

```
CLOUDINARY_URL=cloudinary://api_key:api_secret@cloud_name
CLOUDINARY_CLOUD_NAME=votre_cloud_name
CLOUDINARY_API_KEY=votre_api_key
CLOUDINARY_API_SECRET=votre_api_secret
```

## 🎯 WORKFLOW RECOMMANDÉ

### Pour ajouter un produit complet :

1. **Créer le produit :**
   ```
   /addproduct "Coque iPhone 15" pochettes iphone "15 Pro" 29.99 "Coque premium en silicone"
   ```

2. **Ajouter l'image :**
   ```
   /addimage [ID_retourné]
   ```
   Puis envoyer l'image

3. **Vérifier dans le catalogue :**
   Le produit apparaîtra avec son image dans le menu /produits

### Pour modifier un produit existant :

1. **Voir la liste :**
   ```
   /editproduct
   ```

2. **Modifier ce qui est nécessaire :**
   ```
   /editproduct [ID] price 25.99
   /editproduct [ID] description "Nouvelle description"
   ```

3. **Ajouter/changer l'image si nécessaire :**
   ```
   /addimage [ID]
   ```

## 🚀 FONCTIONNALITÉS AVANCÉES

- **Images automatiques** : Les images sont affichées automatiquement dans le catalogue
- **Upload sécurisé** : Toutes les images sont stockées sur Cloudinary
- **Gestion complète** : Modification, suppression, ajout via commandes simples
- **Interface intuitive** : Menus et commandes faciles à utiliser

## ⚠️ NOTES IMPORTANTES

- Seul l'administrateur (ID configuré dans .env) peut utiliser ces commandes
- Les images restent sur Cloudinary même après suppression du produit
- La modification d'image remplace l'ancienne par la nouvelle
- Les IDs des produits sont générés automatiquement par MongoDB
