# 🚀 Post Bridge Auto Poster

Outil simple pour poster automatiquement vos tweets scrapés sur Twitter via l'API Post Bridge.

## 📋 Prérequis

1. **Compte Post Bridge** : Créez un compte sur [post-bridge.com](https://www.post-bridge.com/)
2. **Connecter vos comptes Twitter** : Connectez vos comptes Twitter/X sur Post Bridge
3. **Clé API** : Récupérez votre clé API depuis votre tableau de bord Post Bridge

## ⚙️ Configuration

Modifiez le fichier `postbridge_config.json` selon vos besoins :

```json
{
  "api_key": "pb_live_VOTRE_CLE_API",
  "api_base_url": "https://api.post-bridge.com/v1",
  "scraped_data_path": "/chemin/vers/scraped data/twitter scraped data/accounts",
  "post_schedule": {
    "enabled": false,
    "interval_hours": 2
  },
  "filters": {
    "skip_retweets": true,      // Ignorer les retweets
    "skip_replies": true,        // Ignorer les réponses
    "skip_quotes": false,        // Poster les citations
    "min_likes": 0,              // Minimum de likes requis
    "max_posts_per_account": null // Limite par compte (null = illimité)
  }
}
```

## 🚀 Utilisation

### Mode simple - Poster tous les comptes

```bash
python postbridge_poster.py
```

### Poster des comptes spécifiques

```bash
python postbridge_poster.py --accounts alecttrona thedankoe matt_gray_
```

### Limiter le nombre de posts par compte

```bash
python postbridge_poster.py --max-posts 5
```

### Combiner les options

```bash
python postbridge_poster.py --accounts alecttrona --max-posts 3
```

## 📊 Fonctionnalités

✅ **Upload automatique des médias** (images et vidéos)  
✅ **Filtrage intelligent** (retweets, réponses, likes minimum)  
✅ **Gestion des limites** (max posts par compte)  
✅ **Support multi-comptes** (poster sur plusieurs comptes Twitter)  
✅ **Gestion des erreurs** (fichiers manquants, API)  
✅ **Progression détaillée** (logs de chaque étape)

## 📝 Structure des données

Le script attend des fichiers CSV dans cette structure :

```
scraped data/twitter scraped data/accounts/
├── alecttrona/
│   └── Account Posts/
│       ├── Account Posts.csv
│       └── Account Posts Media/
│           ├── image1.jpg
│           └── video1.mp4
├── thedankoe/
│   └── Account Posts/
│       └── Account Posts.csv
...
```

## ⚠️ Limitations

- **Médias** : Maximum 4 médias par tweet
- **Texte** : Maximum 280 caractères (tronqué automatiquement)
- **Types de fichiers supportés** : JPG, PNG, MP4, MOV
- **Rate limiting** : Pauses automatiques entre les uploads et posts

## 🔍 Vérification des comptes

Pour vérifier quels comptes Twitter sont connectés sur Post Bridge :

```python
from postbridge_poster import PostBridgePoster

poster = PostBridgePoster()
poster.get_social_accounts()
```

## 📞 Support

Pour toute question sur l'API Post Bridge, consultez la documentation officielle :
- [Documentation API](https://api.post-bridge.com/)
- [Site web](https://www.post-bridge.com/)

## 🛠️ Dépannage

### "Aucun compte Twitter trouvé"
→ Connectez vos comptes Twitter sur post-bridge.com

### "Erreur 401 Unauthorized"
→ Vérifiez votre clé API dans `postbridge_config.json`

### "Fichier média introuvable"
→ Vérifiez que les chemins dans le CSV correspondent aux fichiers réels

### "Type de fichier non supporté"
→ Seuls JPG, PNG, MP4 et MOV sont supportés

