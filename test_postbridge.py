#!/usr/bin/env python3
"""
Script de test pour vérifier la connexion à l'API Post Bridge.
"""

import requests
import json


def test_api_connection():
    """Teste la connexion à l'API et affiche les comptes disponibles."""
    
    API_KEY = "pb_live_FdrG5jubHBJvtGLkgXvRof"
    BASE_URL = "https://api.post-bridge.com/v1"
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    print("=" * 60)
    print("🧪 TEST DE CONNEXION À POST BRIDGE")
    print("=" * 60)
    
    # Test 1: Récupérer les comptes sociaux
    print("\n1️⃣  Test: Récupération des comptes sociaux...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/social-accounts",
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            accounts = data.get('data', [])
            
            print(f"   ✅ Succès! {len(accounts)} compte(s) trouvé(s)\n")
            
            if accounts:
                print("   📋 Vos comptes connectés:")
                for acc in accounts:
                    print(f"      • {acc['platform'].upper()}: @{acc['username']} (ID: {acc['id']})")
            else:
                print("   ⚠️  Aucun compte connecté")
                print("   → Connectez vos comptes sur https://www.post-bridge.com/")
            
            # Compter les comptes Twitter/X
            twitter_accounts = [a for a in accounts if a['platform'] in ['twitter', 'x']]
            if twitter_accounts:
                print(f"\n   🐦 {len(twitter_accounts)} compte(s) Twitter/X disponible(s) pour poster")
            else:
                print("\n   ⚠️  Aucun compte Twitter/X trouvé")
                print("   → Vous devez connecter au moins un compte Twitter/X")
        
        elif response.status_code == 401:
            print("   ❌ Erreur 401: Clé API invalide")
            print("   → Vérifiez votre clé API dans postbridge_config.json")
        else:
            print(f"   ❌ Erreur {response.status_code}")
            print(f"   Réponse: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Récupérer les posts existants
    print("\n2️⃣  Test: Récupération des posts existants...")
    
    try:
        response = requests.get(
            f"{BASE_URL}/posts?limit=5",
            headers=headers
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            posts = data.get('data', [])
            meta = data.get('meta', {})
            total = meta.get('total', 0)
            
            print(f"   ✅ Succès! {total} post(s) trouvé(s) au total")
            
            if posts:
                print(f"\n   📝 Derniers posts (max 5):")
                for i, post in enumerate(posts[:5], 1):
                    caption = post['caption'][:50] + "..." if len(post['caption']) > 50 else post['caption']
                    status = post['status']
                    print(f"      {i}. [{status.upper()}] {caption}")
        else:
            print(f"   ❌ Erreur {response.status_code}")
    
    except Exception as e:
        print(f"   ⚠️  Erreur: {e}")
    
    print("\n" + "=" * 60)
    print("✅ TESTS TERMINÉS")
    print("=" * 60)
    
    print("\n💡 Prochaines étapes:")
    print("   1. Assurez-vous d'avoir au moins un compte Twitter/X connecté")
    print("   2. Lancez: python postbridge_poster.py --accounts NOM_COMPTE --max-posts 1")
    print("   3. Vérifiez le résultat sur https://www.post-bridge.com/")
    

if __name__ == '__main__':
    test_api_connection()

