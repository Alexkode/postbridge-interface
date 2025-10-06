# ❓ FAQ - Questions Fréquentes

## 🔗 Comptes et Configuration

### Q: Si j'ajoute un compte sur Post Bridge, est-ce automatique dans l'interface ?

**R: OUI !** 🎉

Les comptes sont récupérés en temps réel via l'API. Pas besoin de :
- ❌ Redémarrer l'interface
- ❌ Configurer quoi que ce soit
- ❌ Modifier des fichiers

Simplement :
1. Ajoutez votre compte sur https://www.post-bridge.com/
2. Rechargez la page Configuration (F5)
3. Le compte apparaît automatiquement !

Vérifiez avec : `python3 test_postbridge.py`

### Q: Où dois-je gérer mes comptes Twitter ?

**R:** Sur https://www.post-bridge.com/ uniquement.

L'interface récupère automatiquement la liste de vos comptes connectés.

### Q: Est-ce que je peux poster sur certains comptes seulement ?

**R:** Actuellement, chaque post est publié sur **TOUS** vos comptes Twitter connectés sur Post Bridge.

Pour poster sur un seul compte :
1. Déconnectez temporairement les autres sur Post Bridge
2. Publiez votre post
3. Reconnectez les autres comptes

---

## 📂 Données et Fichiers

### Q: D'où viennent les tweets que je peux poster ?

**R:** Des comptes scrapés dans :
```
software_clean/scraped data/twitter scraped data/accounts/
```

Le chemin est configuré dans `postbridge_config.json`.

### Q: Est-ce que je peux changer le dossier des données ?

**R:** OUI ! Modifiez `postbridge_config.json` :

```json
{
  "scraped_data_path": "/votre/chemin/vers/accounts/"
}
```

### Q: Pourquoi certains comptes n'apparaissent pas dans l'interface ?

**R:** L'interface affiche uniquement les comptes qui ont :
1. Un dossier dans `scraped data/twitter scraped data/accounts/`
2. Un fichier `Account Posts.csv` dans `Account Posts/`

Vérifiez que le chemin dans `postbridge_config.json` est correct.

---

## 🤖 Automatisation

### Q: Comment fonctionne la planification automatique ?

**R:** L'algorithme :
1. Sélectionne les X meilleurs posts (par likes/vues)
2. Les planifie dans votre plage horaire (ex: 9h-18h)
3. Ajoute un délai aléatoire entre chaque (ex: 60-120 min)
4. Vérifie toutes les 5 minutes s'il y a des posts à publier
5. Publie automatiquement
6. Replanifie de nouveaux posts quand nécessaire

### Q: Dois-je laisser l'ordinateur allumé pour l'automatisation ?

**R:** OUI ! L'application doit rester en cours d'exécution.

**Options :**
- Laissez le terminal ouvert
- Utilisez `screen` ou `tmux` pour le détacher
- Configurez un service systemd
- Utilisez un serveur/VPS

### Q: Comment arrêter l'automatisation ?

**R:** 
1. **Temporaire** : Allez dans Configuration → Désactivez le toggle
2. **Définitif** : Appuyez sur `Ctrl+C` dans le terminal

### Q: Les posts sont planifiés mais ne se publient pas

**R:** Vérifiez :
1. ✅ L'automatisation est **activée** (toggle vert)
2. ✅ Vous êtes **dans la plage horaire** (ex: entre 9h et 18h)
3. ✅ Il y a des posts avec statut **"scheduled"** (pas "pending")
4. ✅ L'application est **toujours en cours** d'exécution
5. ✅ Vous avez une **connexion internet**

---

## 🎯 Utilisation

### Q: Combien de posts par jour est recommandé ?

**R:** Cela dépend de votre objectif :

- **Débutant/Naturel** : 3-5 posts/jour
- **Growth Modéré** : 5-10 posts/jour  
- **Growth Agressif** : 10-20 posts/jour

⚠️ Commencez doucement pour éviter les restrictions Twitter.

### Q: Quel est le meilleur délai entre posts ?

**R:** 
- **Minimum recommandé** : 30-60 minutes
- **Maximum recommandé** : 120-180 minutes
- **Sweet spot** : 60-120 minutes (aléatoire)

Les délais aléatoires donnent un comportement plus naturel.

### Q: Quelle plage horaire choisir ?

**R:** Analysez quand votre audience est active :

- **Business B2B** : 9h-17h (heures de bureau)
- **Grand public** : 8h-22h (large)
- **International** : 24h/24 (si audience mondiale)

Testez et ajustez selon vos statistiques !

### Q: Dois-je poster les retweets et réponses ?

**R:** **NON**, généralement :

Le contenu original performe mieux. Dans `postbridge_config.json` :

```json
{
  "filters": {
    "skip_retweets": true,    ← Ignorer RT
    "skip_replies": true,      ← Ignorer réponses
    "skip_quotes": false,      ← Garder citations
    "min_likes": 100          ← Minimum 100 likes
  }
}
```

---

## 🛠️ Technique

### Q: Comment installer les dépendances ?

**R:** 
```bash
pip3 install --user Flask APScheduler requests
```

Ou utilisez :
```bash
cd postbridge_interface
./install_interface.sh
```

### Q: L'interface ne démarre pas (port 5000 occupé)

**R:**
```bash
# Trouver le processus
lsof -i :5000

# Tuer le processus
kill -9 <PID>

# Ou changer le port dans postbridge_app.py (ligne finale)
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Q: Où sont stockées les données de l'interface ?

**R:** Dans `postbridge_app.db` (SQLite) :
- Posts sélectionnés
- Statuts (pending, scheduled, posted)
- Configuration

Pour réinitialiser : supprimez simplement `postbridge_app.db`

### Q: Comment voir les logs ?

**R:** Les logs s'affichent dans le terminal où tourne l'application.

Pour sauvegarder les logs :
```bash
python3 postbridge_app.py 2>&1 | tee app.log
```

---

## 🔐 Sécurité

### Q: Ma clé API est-elle sécurisée ?

**R:** La clé est stockée localement dans `postbridge_config.json`.

**Bonnes pratiques :**
- ✅ Ne partagez pas ce fichier
- ✅ Ne commitez pas dans Git (ajoutez au .gitignore)
- ✅ L'interface est locale (localhost uniquement)
- ❌ N'exposez pas l'interface publiquement sans authentification

### Q: Est-ce que je peux exposer l'interface sur internet ?

**R:** **NON recommandé** sans sécurisation.

L'interface actuelle n'a pas d'authentification. Si vous voulez l'exposer :
1. Ajoutez une authentification (login/password)
2. Utilisez HTTPS (certificat SSL)
3. Configurez un reverse proxy (nginx)
4. Utilisez un VPN ou IP whitelist

---

## 📊 Performance

### Q: Combien de tweets puis-je sélectionner ?

**R:** Techniquement illimité, mais recommandé :
- **Buffer minimal** : 20-30 tweets
- **Buffer optimal** : 50-100 tweets
- **Buffer maximal** : 200-500 tweets

### Q: L'interface est lente avec beaucoup de tweets

**R:** L'interface charge tous les tweets d'un compte en une fois.

**Solutions :**
1. Filtrez les tweets (min likes, type original)
2. Parcourez un compte à la fois
3. Sélectionnez progressivement

### Q: Combien de temps garde-t-on les posts publiés ?

**R:** Indéfiniment dans `postbridge_app.db`.

Pour nettoyer l'historique :
```bash
sqlite3 postbridge_app.db "DELETE FROM selected_posts WHERE status='posted'"
```

---

## 🆘 Support

### Q: Comment tester ma connexion Post Bridge ?

**R:**
```bash
cd postbridge_interface
python3 test_postbridge.py
```

### Q: Où trouver plus de documentation ?

**R:**
- `README.md` - Documentation principale
- `docs/DEMARRAGE_RAPIDE.md` - Guide rapide
- `docs/POSTBRIDGE_INTERFACE_GUIDE.md` - Guide complet
- `docs/AJOUT_COMPTES_POSTBRIDGE.md` - Gestion des comptes

### Q: Comment signaler un bug ?

**R:** Vérifiez d'abord les logs dans le terminal, puis :
1. Testez la connexion : `python3 test_postbridge.py`
2. Vérifiez la configuration : `cat postbridge_config.json`
3. Consultez la FAQ et la documentation

---

## 💡 Astuces Pro

### Q: Comment optimiser mes publications ?

**R:**

1. **Contenu** :
   - Priorisez les tweets avec médias
   - Sélectionnez les tweets avec bon engagement
   - Variez les sources (plusieurs comptes)

2. **Timing** :
   - Testez différentes plages horaires
   - Analysez vos stats Twitter
   - Ajustez selon votre audience

3. **Volume** :
   - Commencez à 3-5 posts/jour
   - Augmentez progressivement
   - Surveillez les réactions

4. **Qualité** :
   - Filtrez par likes minimum (100+)
   - Évitez les RT et réponses
   - Gardez le contenu original

---

**D'autres questions ?** Consultez la documentation complète dans le dossier `docs/` !


