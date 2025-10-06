# 📁 Structures de Dossiers Supportées

L'interface Post Bridge supporte **deux structures de dossiers** pour s'adapter à différentes versions du scraper.

## ✅ Structures Supportées

### 1️⃣ Structure Directe (Ancienne)

```
software/scraped data/twitter scraped data/accounts/
└── nom_du_compte/
    └── Account Posts/
        ├── Account Posts.csv
        └── Account Posts Media/
```

**Exemple :**
```
alecttrona/
└── Account Posts/
    ├── Account Posts.csv
    └── Account Posts Media/
        ├── image1.jpg
        └── video1.mp4
```

### 2️⃣ Structure avec Sessions (Nouvelle) ✨

```
software_clean/scraped data/twitter scraped data/accounts/
└── nom_du_compte/
    └── session_DD-MM-YYYY_HH-MM/
        └── Account Posts/
            ├── Account Posts.csv
            └── Account Posts Media/
```

**Exemple :**
```
SeekWiser_/
└── session_04-10-2025_03-48/
    └── Account Posts/
        ├── Account Posts.csv
        └── Account Posts Media/
            ├── tweet1.jpg
            └── tweet2.mp4
```

## 🔄 Détection Automatique

L'interface **détecte automatiquement** quelle structure vous utilisez :

1. **Vérifie d'abord** la structure directe
2. **Si non trouvée**, cherche les dossiers `session_*`
3. **Prend la session la plus récente** (tri par date)

## 📊 Vos Comptes Actuels

**Structure détectée : Sessions** ✅

| Compte | Tweets | Session |
|--------|--------|---------|
| @DearS_o_n | 7,212 | session_02-10-2025_07-45 |
| @Dearme2_ | 3,880 | session_02-10-2025_21-02 |
| @Mind_Essentials | 8,712 | session_05-10-2025_16-15 |
| @PathOfMen_ | 2,974 | session_02-10-2025_14-08 |
| @SeekWiser_ | 7,328 | session_04-10-2025_03-48 |
| @TheRich_Gospel | 4,382 | session_03-10-2025_04-15 |
| @jackfriks | 19,323 | session_05-10-2025_10-37 |

**Total : 7 comptes - 53,811 tweets disponibles !** 🎉

## 🧪 Tester la Détection

```bash
cd postbridge_interface
python3 test_synchro.py
```

Ce script affichera :
- ✅ Comptes détectés
- 📊 Nombre de tweets
- 🏗️ Type de structure (directe ou session)
- 📁 Chemin exact du CSV

## 🔧 Avantages de la Structure avec Sessions

### ✅ Multi-Sessions
- Gardez plusieurs sessions de scraping
- Historique des données
- Possibilité de comparer

### ✅ Organisation
- Dates claires dans les noms
- Facile de retrouver une session spécifique
- Pas de mélange de données

### ✅ Automatique
- L'interface prend toujours la **session la plus récente**
- Pas besoin de configuration manuelle
- Transparent pour l'utilisateur

## 📝 Exemple Pratique

### Scénario : Plusieurs Sessions

```
SeekWiser_/
├── session_01-10-2025_10-00/    ← Ancienne session
│   └── Account Posts/
│       └── Account Posts.csv
├── session_03-10-2025_15-30/    ← Session intermédiaire
│   └── Account Posts/
│       └── Account Posts.csv
└── session_04-10-2025_03-48/    ← Session la plus récente ✅
    └── Account Posts/
        └── Account Posts.csv
```

**L'interface utilisera automatiquement** : `session_04-10-2025_03-48`

## 🔄 Migration Entre Structures

### De Structure Directe → Structure avec Sessions

Si vous migrez de l'ancienne structure, **aucune action requise** !

L'interface continuera à fonctionner car elle vérifie :
1. D'abord la structure directe (ancienne)
2. Puis la structure avec sessions (nouvelle)

### Mélanger les Deux Structures

**Oui, c'est possible !** Vous pouvez avoir :

```
accounts/
├── ancien_compte/              ← Structure directe
│   └── Account Posts/
│       └── Account Posts.csv
└── nouveau_compte/             ← Structure avec sessions
    └── session_05-10-2025_10-00/
        └── Account Posts/
            └── Account Posts.csv
```

L'interface détectera les deux automatiquement ! ✅

## 🛠️ Configuration du Chemin

Le chemin est configuré dans `postbridge_config.json` :

```json
{
  "scraped_data_path": "/home/cytech/Projects/scraperX/scraper/software_clean/scraped data/twitter scraped data/accounts"
}
```

**Actuellement configuré sur :** `software_clean` ✅

## ⚠️ Points d'Attention

### ✅ Obligatoire
- Fichier `Account Posts.csv` **requis**
- Doit contenir au moins 1 ligne (header + data)

### ✅ Optionnel
- Dossier `Account Posts Media/` (pour les images/vidéos)
- Peut être vide si pas de médias

### ❌ Ignoré
- Dossiers nommés `Combined Files`
- Dossiers sans CSV
- Sessions vides

## 🔍 Dépannage

### "Mon compte n'apparaît pas"

**Vérifications :**

1. **Structure correcte ?**
```bash
# Vérifier ce qui existe
ls -la "software_clean/.../accounts/NOM_COMPTE/"

# Doit montrer soit :
# - Account Posts/             (structure directe)
# - session_XX/                (structure session)
```

2. **CSV existe ?**
```bash
# Structure directe
ls "software_clean/.../accounts/NOM_COMPTE/Account Posts/Account Posts.csv"

# Structure session
ls "software_clean/.../accounts/NOM_COMPTE/session_*/Account Posts/Account Posts.csv"
```

3. **Tester la détection**
```bash
python3 test_synchro.py
```

### "Ancienne session utilisée"

Si l'interface utilise une ancienne session au lieu de la plus récente :

**Cause :** Tri alphabétique incorrect

**Solution :** Le tri par date est automatique. Si problème persiste, renommez les sessions avec un format cohérent : `session_DD-MM-YYYY_HH-MM`

## 💡 Conseils

1. **Format de date cohérent** : `DD-MM-YYYY_HH-MM`
2. **Sessions nommées clairement** : Commencez par `session_`
3. **Nettoyez les vieilles sessions** si vous manquez d'espace
4. **Gardez au moins une session** par compte

## 🎯 Résumé

✅ **Deux structures supportées** (directe + sessions)  
✅ **Détection automatique** sans configuration  
✅ **Session la plus récente** utilisée automatiquement  
✅ **Compatible** avec anciennes et nouvelles versions  
✅ **Flexible** - mélangez les structures si besoin  

---

**L'interface s'adapte automatiquement à votre structure ! 🎉**

