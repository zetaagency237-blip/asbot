# 🚀 Déploiement sur Render - Anonyme Smartphone Bot

## 📋 Prérequis

- Compte [Render.com](https://render.com) (gratuit)
- Repository GitHub avec votre code
- Token Telegram Bot
- Base de données MongoDB Atlas
- Compte Cloudinary

## 🔧 Fichiers de Configuration

### ✅ Déjà créés :
- `requirements.txt` - Dépendances Python
- `runtime.txt` - Version Python (3.10.11)
- `Procfile` - Commande de démarrage
- `.env` - Variables d'environnement (à configurer sur Render)

## 📚 Guide de Déploiement Étape par Étape

### 1. **Préparer le Repository GitHub**
```bash
# Ajouter tous les fichiers
git add .
git commit -m "Prêt pour déploiement Render"
git push origin main
```

### 2. **Créer un Web Service sur Render**

1. Connectez-vous sur [Render.com](https://render.com)
2. Cliquez sur **"New +"** → **"Web Service"**
3. Connectez votre repository GitHub
4. Sélectionnez le repository de votre bot

### 3. **Configuration du Service**

| Champ | Valeur |
|-------|---------|
| **Name** | `anonyme-smartphone-bot` |
| **Region** | `Frankfurt (EU Central)` |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `python main.py` |

### 4. **Variables d'Environnement**

Dans l'onglet **"Environment"**, ajoutez :

```env
BOT_TOKEN=8424154788:AAEuobN21v6QHuvEsl5EaZQ2aptz0jncRfc
BOT_USERNAME=@anonyme_smartphone_bot
MONGODB_URI=mongodb+srv://thekyann_db_user:iE5Fg0i1hWffNGaw@cluster0.auysbl7.mongodb.net/
DATABASE_NAME=anonyme_smartphone
CLOUDINARY_URL=cloudinary://398734649392149:9AJGURM4X2oaDV01r3XIKt7pomI@dkpf8ovsd
CLOUDINARY_API_SECRET=9AJGURM4X2oaDV01r3XIKt7pomI
ADMIN_ID=1888960312
```

### 5. **Paramètres Avancés**

| Setting | Valeur | Description |
|---------|---------|-------------|
| **Auto-Deploy** | `Yes` | Redéploie automatiquement à chaque push |
| **Health Check Path** | `/health` | Optionnel |
| **Instance Type** | `Free` | Gratuit (512MB RAM) |

## 🔄 Webhook Telegram

⚠️ **Important** : Après le déploiement, configurez le webhook :

```python
# URL du webhook : https://votre-app.onrender.com
# Render fournira automatiquement l'URL HTTPS
```

## 📊 Monitoring et Logs

### Voir les Logs en Temps Réel :
1. Allez dans votre service Render
2. Onglet **"Logs"**
3. Surveillez le démarrage du bot

### Indicateurs de Succès :
```
✅ Application started successfully
✅ Bot configuré avec succès
✅ Base de données connectée
✅ Cloudinary configuré
✅ Bot démarré et en écoute...
```

## 🔧 Dépannage Fréquent

### **Bot ne démarre pas**
```bash
# Vérifiez les logs Render
# Variables d'environnement correctes ?
# MongoDB accessible ?
```

### **Images ne s'affichent pas**
```bash
# Cloudinary configuré ?
# CLOUDINARY_URL correct ?
# Quota Cloudinary OK ?
```

### **Base de données inaccessible**
```bash
# MongoDB Atlas : IP autorisées (0.0.0.0/0) ?
# Credentials corrects ?
# DATABASE_NAME existe ?
```

## 💰 Coûts

### **Plan Gratuit Render :**
- ✅ 512MB RAM
- ✅ Domaine HTTPS gratuit
- ✅ Auto-déploiement Git
- ⚠️ Se met en veille après 15min d'inactivité
- ⚠️ 750h/mois maximum

### **Upgrade Recommandé ($7/mois) :**
- 💪 Toujours actif (24/7)
- 💪 Plus de RAM et CPU
- 💪 Pas de limite d'heures

## 🚀 Mise en Production

### **Checklist Final :**
- [ ] ✅ Variables d'environnement configurées
- [ ] ✅ Repository GitHub à jour
- [ ] ✅ MongoDB Atlas accessible
- [ ] ✅ Cloudinary fonctionnel
- [ ] ✅ Token bot valide
- [ ] ✅ Admin ID correct
- [ ] ✅ Logs sans erreur
- [ ] ✅ Bot répond aux commandes

## 📞 Support

En cas de problème :
1. **Logs Render** - Premier réflexe
2. **Variables d'environnement** - Vérifier les valeurs
3. **MongoDB Atlas** - Tester la connexion
4. **Telegram BotFather** - Token valide ?

---

🎉 **Votre bot Telegram est maintenant hébergé professionnellement sur Render !**
