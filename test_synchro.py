#!/usr/bin/env python3
"""
Script de test pour vérifier la synchronisation automatique des comptes.
"""

import os
from pathlib import Path
import json

print("=" * 60)
print("🔍 TEST DE SYNCHRONISATION DES COMPTES")
print("=" * 60)
print()

# Charger la config
with open('postbridge_config.json', 'r') as f:
    config = json.load(f)

scraped_path = Path(config['scraped_data_path'])

print(f"📂 Chemin configuré:")
print(f"   {scraped_path}")
print()

# Vérifier si le chemin existe
if not scraped_path.exists():
    print("❌ ERREUR : Le chemin n'existe pas !")
    print(f"   Créez le dossier : {scraped_path}")
    exit(1)

print("✅ Le chemin existe")
print()

# Lister tous les dossiers
print("📋 Comptes trouvés dans le dossier :")
print()

accounts = []
for d in scraped_path.iterdir():
    if d.is_dir() and d.name != 'Combined Files':
        # Vérifier structure directe
        csv_path_direct = d / 'Account Posts' / 'Account Posts.csv'
        
        # Vérifier structure avec session
        session_folders = [f for f in d.iterdir() if f.is_dir() and f.name.startswith('session_')]
        
        csv_path = None
        structure_type = None
        
        if csv_path_direct.exists():
            csv_path = csv_path_direct
            structure_type = "directe"
        elif session_folders:
            latest_session = sorted(session_folders, reverse=True)[0]
            csv_path_session = latest_session / 'Account Posts' / 'Account Posts.csv'
            if csv_path_session.exists():
                csv_path = csv_path_session
                structure_type = f"session ({latest_session.name})"
        
        if csv_path:
            # Compter les tweets
            import csv
            with open(csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                tweet_count = sum(1 for row in reader)
            
            print(f"   ✅ @{d.name}")
            print(f"      📊 {tweet_count} tweets disponibles")
            print(f"      🏗️  Structure: {structure_type}")
            print(f"      📁 {csv_path}")
            accounts.append(d.name)
        else:
            print(f"   ⚠️  @{d.name}")
            print(f"      ❌ Aucun CSV trouvé")
            if session_folders:
                print(f"      📂 {len(session_folders)} session(s) trouvée(s) mais sans CSV")
        
        print()

print("=" * 60)
print(f"✅ TOTAL : {len(accounts)} compte(s) disponible(s)")
print("=" * 60)
print()

if accounts:
    print("🎯 Ces comptes apparaîtront dans l'interface :")
    for account in sorted(accounts):
        print(f"   • @{account}")
    print()
    print("💡 Pour les voir dans l'interface :")
    print("   1. Lancez : python3 postbridge_app.py")
    print("   2. Ouvrez : http://localhost:5000")
    print("   3. Ils seront listés sur la page d'accueil !")
else:
    print("⚠️  Aucun compte trouvé")
    print()
    print("Pour qu'un compte apparaisse, il faut :")
    print("   1. Un dossier dans :")
    print(f"      {scraped_path}")
    print("   2. Qui contient :")
    print("      Account Posts/Account Posts.csv")
    print()
    print("Exemple de structure correcte :")
    print("   software_clean/scraped data/twitter scraped data/accounts/")
    print("   └── nom_du_compte/")
    print("       └── Account Posts/")
    print("           ├── Account Posts.csv")
    print("           └── Account Posts Media/")

print()
print("=" * 60)
print("🔄 La synchronisation est AUTOMATIQUE !")
print("   Ajoutez un nouveau dossier → Rechargez la page (F5)")
print("=" * 60)


