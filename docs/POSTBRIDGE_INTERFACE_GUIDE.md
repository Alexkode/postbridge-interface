# 🚀 Interface Web Post Bridge - Guide Complet

Interface web complète pour automatiser vos publications Twitter via Post Bridge avec sélection manuelle, planification intelligente et automatisation.

## 📋 Installation

### 1. Installer les dépendances

```bash
source venv/bin/activate
pip install -r requirements_postbridge.txt
```

### 2. Lancer l'interface

```bash
python postbridge_app.py
```

L'interface sera accessible sur : **http://localhost:5000**

## 🎯 Fonctionnalités Principales

### 🏠 Page d'Accueil

- **Tableau de bord** avec statistiques en temps réel
  - Posts en attente
  - Posts planifiés
  - Posts publiés
  - Statut de l'automatisation
  
- **Liste des comptes disponibles** pour parcourir les tweets scrapés
- **Actions rapides** pour accéder à la file d'attente et aux paramètres

### 📱 Parcourir les Tweets

1. **Cliquez sur un compte** pour voir tous ses tweets
2. **Filtres disponibles** :
   - Type de tweet (Original, Retweet, Quote, Reply)
   - Avec ou sans média
   - Nombre minimum de likes
   - Recherche textuelle
3. **Sélection visuelle** : cliquez sur "Sélectionner" pour ajouter à la file
4. **Preview complet** : voir le texte, les stats, et les médias de chaque tweet

### 📋 File d'Attente

- **Vue d'ensemble** de tous les posts sélectionnés
- **Statuts** :
  - ⏳ En attente : sélectionné mais pas encore planifié
  - 📅 Planifié : date/heure de publication définie
  - ✓ Publié : post publié avec succès
  - ❌ Erreur : échec de publication
- **Actions** :
  - Poster maintenant (bypass la planification)
  - Retirer de la file

### ⚙️ Configuration

#### Template de Publication Journalier

**Activation/Désactivation** : Toggle pour activer l'automatisation

**Paramètres** :
- **Nombre de posts par jour** : Ex: 5 posts/jour
- **Délai minimum** : Ex: 30 minutes (temps min entre 2 posts)
- **Délai maximum** : Ex: 120 minutes (temps max entre 2 posts)
- **Heure de début** : Ex: 9h (début de publication)
- **Heure de fin** : Ex: 18h (fin de publication)

**Comment ça marche** :
1. L'algorithme sélectionne les posts avec le plus de likes/vues
2. Planifie automatiquement dans la plage horaire
3. Ajoute un délai aléatoire entre min et max
4. Respecte les heures de début/fin
5. Replanifie automatiquement de nouveaux posts

## 🔄 Workflow Complet

### Scénario 1 : Sélection Manuelle Simple

```
1. Parcourez un compte → Sélectionnez des tweets
2. Allez dans la file d'attente
3. Cliquez sur "Poster maintenant" pour chaque tweet
```

### Scénario 2 : Automatisation Complète

```
1. Parcourez plusieurs comptes et sélectionnez 50+ tweets
2. Allez dans Configuration
3. Configurez le template :
   - 5 posts/jour
   - Délai : 60-120 min
   - Plage : 9h-18h
4. Activez l'automatisation
5. Les posts seront planifiés et publiés automatiquement !
```

### Scénario 3 : Mix Manuel + Auto

```
1. Sélectionnez des tweets
2. Activez l'automatisation
3. L'algorithme planifie automatiquement les meilleurs posts
4. Vous pouvez forcer la publication de certains posts manuellement
```

## 📊 Exemple de Configuration

### Configuration Aggressive (Growth Rapide)

```
Posts par jour: 10
Délai min: 30 minutes
Délai max: 90 minutes
Heures: 8h - 20h
```

### Configuration Modérée (Recommended)

```
Posts par jour: 5
Délai min: 60 minutes
Délai max: 180 minutes
Heures: 9h - 18h
```

### Configuration Douce (Natural)

```
Posts par jour: 3
Délai min: 120 minutes
Délai max: 240 minutes
Heures: 10h - 17h
```

## 🎨 Captures d'Écran

### Page d'Accueil
- Dashboard avec stats colorées
- Liste des comptes disponibles
- Accès rapide aux fonctionnalités

### Page de Parcours
- Grille de tweets avec preview
- Filtres multiples
- Sélection en un clic

### File d'Attente
- Liste chronologique des posts
- Statuts visuels (badges colorés)
- Actions rapides

### Configuration
- Interface simple et claire
- Toggle d'activation
- Validation en temps réel

## 🔧 Fonctionnalités Avancées

### Planification Intelligente

- **Priorisation** : Les tweets avec le plus d'engagement sont publiés en premier
- **Randomisation** : Délais aléatoires pour un comportement naturel
- **Gestion horaire** : Respecte strictement la plage horaire définie
- **Auto-remplissage** : Planifie automatiquement de nouveaux posts

### Base de Données SQLite

Toutes les données sont stockées dans `postbridge_app.db` :
- Posts sélectionnés et leur statut
- Configuration du template
- Historique des publications

### Scheduler APScheduler

- **Job en arrière-plan** : Vérifie toutes les 5 minutes
- **Publication automatique** : Poste les tweets planifiés
- **Replanification** : Ajoute automatiquement de nouveaux posts

## 📱 Compatibilité

- ✅ Desktop (Chrome, Firefox, Safari, Edge)
- ✅ Tablette
- ✅ Mobile (design responsive)

## ⚠️ Notes Importantes

1. **Gardez l'application en cours d'exécution** pour que l'automatisation fonctionne
2. **Vérifiez vos comptes Post Bridge** avant d'activer l'automatisation
3. **Testez avec peu de posts** d'abord pour valider la configuration
4. **Surveillez la file d'attente** régulièrement

## 🔒 Sécurité

- La clé API est stockée dans `postbridge_config.json`
- L'interface est locale (localhost) par défaut
- Base de données locale SQLite

## 🆘 Dépannage

### L'interface ne démarre pas
```bash
# Vérifier les dépendances
pip install -r requirements_postbridge.txt

# Vérifier le port 5000
lsof -i :5000  # Si occupé, tuer le processus
```

### Les posts ne se publient pas automatiquement
- Vérifier que l'automatisation est activée (toggle vert)
- Vérifier qu'il y a des posts "en attente" dans la file
- Vérifier que vous êtes dans la plage horaire définie
- Vérifier les logs dans le terminal

### Erreur de connexion Post Bridge
- Vérifier la clé API dans `postbridge_config.json`
- Vérifier que les comptes Twitter sont connectés sur Post Bridge
- Tester avec `python test_postbridge.py`

## 🚀 Démarrage Rapide

```bash
# 1. Installer
pip install -r requirements_postbridge.txt

# 2. Lancer
python postbridge_app.py

# 3. Ouvrir
# http://localhost:5000

# 4. Commencer !
# - Parcourir les comptes
# - Sélectionner des tweets
# - Configurer l'automatisation
# - Activer et profiter !
```

## 💡 Conseils Pro

1. **Sélectionnez 20-30 tweets** pour avoir un bon buffer
2. **Variez les comptes sources** pour du contenu diversifié
3. **Priorisez les tweets avec médias** (plus d'engagement)
4. **Évitez les retweets et réponses** (activez les filtres)
5. **Testez différentes plages horaires** pour trouver le meilleur timing

## 📞 Support

Pour toute question :
- Documentation Post Bridge : https://www.post-bridge.com/
- Fichier de config : `postbridge_config.json`
- Logs : Dans le terminal où tourne `postbridge_app.py`

---

**Bon posting ! 🎉**

