# 🚀 Démarrage Rapide - Interface Post Bridge

## ⚡ Installation des Dépendances

Il y a un problème avec le venv existant. Voici comment installer les dépendances :

### Option 1 : Installation Système (Recommandé)

```bash
# Installer pip si nécessaire
sudo apt install python3-pip

# Installer les dépendances
pip3 install --user Flask APScheduler requests

# Ou avec sudo si nécessaire
sudo pip3 install Flask APScheduler requests
```

### Option 2 : Nouveau Virtual Environment

```bash
# Créer un nouveau venv propre
cd /home/cytech/Projects/scraperX/scraper
python3 -m venv pb_venv

# Activer
source pb_venv/bin/activate

# Installer
pip install Flask APScheduler requests
```

## 🎯 Lancer l'Interface

```bash
cd /home/cytech/Projects/scraperX/scraper

# Lancer l'application
python3 postbridge_app.py
```

L'interface sera disponible sur : **http://localhost:5000**

## 📱 Utilisation Rapide

### 1. Page d'Accueil (Dashboard)
- Voir les statistiques
- Accéder aux comptes disponibles
- Aller dans la configuration

### 2. Parcourir un Compte
- Cliquez sur un compte (ex: @alecttrona)
- Utilisez les filtres pour trouver les meilleurs tweets
- Cliquez sur "Sélectionner" pour ajouter à la file

### 3. Configurer l'Automatisation
- Allez dans "Configuration"
- Réglez les paramètres :
  ```
  Posts par jour: 5
  Délai min: 30 min
  Délai max: 120 min
  Heures: 9h - 18h
  ```
- Activez le toggle
- Cliquez sur "Sauvegarder et Planifier"

### 4. C'est Tout !
L'application va maintenant :
- Planifier automatiquement les posts
- Les publier dans la plage horaire
- Replanifier de nouveaux posts automatiquement

## 🎨 Fonctionnalités Principales

### ✅ Sélection Manuelle
- Parcourez les comptes scrapés
- Filtrez par type, médias, likes
- Preview complet avant sélection

### 📅 Planification Automatique
- Template journalier configurable
- Délais aléatoires entre posts
- Respect des plages horaires
- Priorisation par engagement

### 📊 File d'Attente
- Vue d'ensemble des posts
- Statuts en temps réel
- Actions manuelles possibles

### ⚙️ Configuration
- Nombre de posts/jour
- Délais entre posts
- Plages horaires
- Activation/désactivation

## 🔧 Dépannage

### "ModuleNotFoundError: No module named 'flask'"
```bash
pip3 install --user Flask APScheduler requests
```

### "Address already in use"
```bash
# Tuer le processus sur le port 5000
lsof -i :5000
kill -9 <PID>
```

### Les posts ne se publient pas
1. Vérifier que l'automatisation est activée (toggle vert)
2. Vérifier qu'il y a des posts dans la file
3. Vérifier la plage horaire
4. Regarder les logs dans le terminal

## 📞 Support

- Guide complet : `POSTBRIDGE_INTERFACE_GUIDE.md`
- Configuration API : `postbridge_config.json`
- Test connexion : `python3 test_postbridge.py`

## 🎉 C'est Parti !

```bash
# 1. Installer
pip3 install --user Flask APScheduler requests

# 2. Lancer
python3 postbridge_app.py

# 3. Ouvrir
# http://localhost:5000

# 4. Profiter !
```

**Note** : Gardez le terminal ouvert tant que vous voulez que l'automatisation fonctionne !

