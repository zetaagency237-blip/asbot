# Bot Telegram Anonyme Smartphone 📱

## Description
Bot Telegram pour la plateforme de vente d'accessoires smartphones et services techniques "Anonyme Smartphone".

## Fonctionnalités principales

### 🏠 Menu Principal
- **📱 PRODUITS** : Catalogue complet d'accessoires
- **🔧 SERVICES** : Services techniques spécialisés
- **👥 COMMUNAUTÉ** : Groupe Telegram de la communauté
- **ℹ️ À PROPOS** : Informations sur l'entreprise

### 📱 Catalogue Produits
1. **👜 Pochettes** - Protection pour smartphones
2. **🔌 Chargeurs MagSafe** - Chargeurs sans fil
3. **🎯 Autres Gadgets** - Accessoires divers
4. **📦 Packs** - Offres groupées

#### Marques supportées :
- 🍎 iPhone
- 📱 Samsung
- 🤖 Xiaomi
- 📲 Huawei

### 🔧 Services
1. **🔓 Déblocage** - Déblocage de téléphones
2. **📡 Désimlocage** - Libération opérateur
3. **🔄 Déclonage** - Services de déclonage
4. **⚠️ Cas Particuliers** - Situations spéciales

## Fonctionnement du Bot

### Première connexion
1. L'utilisateur tape `/start`
2. Le bot demande le prénom
3. Stockage de l'ID Telegram et du prénom en base de données
4. Authentification automatique
5. Affichage du menu principal

### Utilisateur existant
- Reconnaissance automatique
- Accès direct au menu principal

## Installation et Configuration

### Prérequis
```bash
pip install python-telegram-bot
```

### Configuration
1. Remplacez le token dans `main.py` par votre token BotFather
2. Modifiez les informations de contact dans le code
3. Personnalisez les messages selon vos besoins

### Lancement
```bash
python main.py
```

## Structure de la Base de Données

### Table `users`
- `user_id` : ID Telegram (clé primaire)
- `prenom` : Prénom de l'utilisateur
- `authenticated` : Statut d'authentification (1=oui, 0=non)
- `created_at` : Date de création du compte

## Sécurité
⚠️ **Important** : Ne partagez jamais votre token de bot publiquement !

## Support
Pour toute question ou problème :
- 💬 Telegram : @anonyme_smartphone
- 📧 Email : contact@anonymesmartphone.com

## Version
Version 1.0 - Bot Anonyme Smartphone
