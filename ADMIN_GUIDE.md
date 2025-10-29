# 🔧 GUIDE D'ADMINISTRATION - Bot Anonyme Smartphone

## ⚙️ Commandes d'Administration

### 📋 Commandes principales

#### `/admin`
Accède au panneau d'administration principal avec menu interactif.

#### `/stats`
Affiche les statistiques complètes :
- Nombre total d'utilisateurs
- Nouveaux utilisateurs du jour
- Nombre de produits total et actifs

#### `/listusers`
Liste tous les utilisateurs enregistrés avec leurs informations :
- Prénom
- ID Telegram
- Date d'inscription

---

## 📱 Gestion des Produits

#### `/addproduct`
Ajoute un nouveau produit au catalogue.

**Syntaxe :**
```
/addproduct "nom" catégorie marque "modèle" prix "description"
```

**Exemple :**
```
/addproduct "Coque Premium" pochettes iphone "15 Pro" 29.99 "Coque en cuir véritable avec protection MagSafe"
```

**Paramètres :**
- **nom** : Nom du produit (entre guillemets si espaces)
- **catégorie** : `pochettes`, `magsafe`, `gadgets`, `packs`
- **marque** : `iphone`, `samsung`, `xiaomi`, `huawei`
- **modèle** : Modèle du téléphone (entre guillemets)
- **prix** : Prix en euros (format : 29.99)
- **description** : Description du produit

---

## 💬 Communication

#### `/broadcast`
Envoie un message à tous les utilisateurs enregistrés.

**Syntaxe :**
```
/broadcast Votre message ici
```

**Exemple :**
```
/broadcast 🎉 Nouvelle collection iPhone 16 disponible ! Remise de 20% ce week-end.
```

⚠️ **Attention :** Cette commande envoie le message à TOUS les utilisateurs. Utilisez avec précaution !

---

## 🔐 Sécurité

### Configuration de l'ID Administrateur

1. **Trouvez votre ID Telegram :**
   - Envoyez `/start` au bot @userinfobot
   - Notez votre ID numérique

2. **Configurez dans le fichier `.env` :**
   ```
   ADMIN_ID=123456789
   ```

3. **Redémarrez le bot** pour appliquer les changements.

---

## 📊 Menu Interactif (via `/admin`)

### 👥 Gestion Utilisateurs
- Voir la liste des utilisateurs
- Statistiques d'inscription

### 📱 Gestion Produits  
- ➕ Ajouter un produit
- 📋 Voir tous les produits
- ✏️ Modifier un produit (à venir)
- 🗑️ Supprimer un produit (à venir)

### 📊 Statistiques
- Nombre d'utilisateurs total et du jour
- Nombre de produits
- Mise à jour en temps réel

### 💬 Diffusion
- Instructions pour envoyer des messages groupés

---

## 🚀 Exemples d'Utilisation

### Ajouter plusieurs produits :

```bash
# Pochette iPhone
/addproduct "Pochette Cuir iPhone" pochettes iphone "15 Pro Max" 35.99 "Protection premium en cuir véritable"

# Chargeur MagSafe
/addproduct "Chargeur MagSafe 15W" magsafe iphone "12+" 49.99 "Chargeur sans fil rapide compatible MagSafe"

# Gadget Samsung
/addproduct "Support Voiture" gadgets samsung "Galaxy S24" 24.99 "Support magnétique ajustable pour voiture"

# Pack Xiaomi
/addproduct "Pack Protection Xiaomi" packs xiaomi "14 Pro" 45.99 "Coque + verre trempé + chargeur + câble"
```

### Envoyer des annonces :

```bash
# Promotion
/broadcast 🔥 SOLDES ! -30% sur tous les accessoires iPhone jusqu'à dimanche !

# Nouveau produit
/broadcast 📱 Nouveauté : Coques iPhone 16 maintenant disponibles. Commandez dès maintenant !

# Service
/broadcast 🔧 Service déblocage disponible 24h/24. Contactez-nous pour plus d'infos.
```

---

## 📝 Notes Importantes

- ✅ Seul l'administrateur configuré peut utiliser ces commandes
- ✅ Toutes les données sont stockées dans MongoDB Atlas
- ✅ Les images peuvent être ajoutées via Cloudinary (URL)
- ✅ Le bot fonctionne 24h/24 une fois déployé

---

## 🆘 Support

Pour toute question technique :
- 📧 Email : contact@anonymesmartphone.com
- 💬 Telegram : @anonyme_smartphone
