#!/usr/bin/env python3
"""
Script pour poster automatiquement des tweets via l'API Post Bridge.
"""

import json
import csv
import os
import requests
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import ast


class PostBridgePoster:
    """Gestionnaire pour poster des tweets via l'API Post Bridge."""
    
    def __init__(self, config_path: str = "postbridge_config.json"):
        """Initialise le poster avec la configuration."""
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.api_key = self.config['api_key']
        self.api_base_url = self.config['api_base_url']
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        self.social_accounts = None
    
    def get_social_accounts(self) -> List[Dict]:
        """Récupère les comptes sociaux depuis Post Bridge."""
        print("🔍 Récupération des comptes sociaux...")
        
        response = requests.get(
            f"{self.api_base_url}/social-accounts",
            headers=self.headers
        )
        
        if response.status_code == 200:
            data = response.json()
            self.social_accounts = data['data']
            
            # Filtrer uniquement les comptes Twitter/X
            twitter_accounts = [acc for acc in self.social_accounts if acc['platform'] in ['twitter', 'x']]
            
            print(f"✅ {len(twitter_accounts)} compte(s) Twitter trouvé(s):")
            for acc in twitter_accounts:
                print(f"   - @{acc['username']} (ID: {acc['id']})")
            
            return twitter_accounts
        else:
            print(f"❌ Erreur lors de la récupération des comptes: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return []
    
    def upload_media(self, file_path: str) -> Optional[str]:
        """Upload un fichier média et retourne son ID."""
        if not os.path.exists(file_path):
            print(f"⚠️  Fichier média introuvable: {file_path}")
            return None
        
        # Déterminer le type MIME
        ext = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.mp4': 'video/mp4',
            '.mov': 'video/quicktime'
        }
        
        mime_type = mime_types.get(ext)
        if not mime_type:
            print(f"⚠️  Type de fichier non supporté: {ext}")
            return None
        
        # Obtenir la taille du fichier
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        
        print(f"   📤 Upload de {file_name} ({file_size} bytes)...")
        
        # Étape 1: Créer l'URL d'upload
        create_response = requests.post(
            f"{self.api_base_url}/media/create-upload-url",
            headers=self.headers,
            json={
                'mime_type': mime_type,
                'size_bytes': file_size,
                'name': file_name
            }
        )
        
        if create_response.status_code not in [200, 201]:
            print(f"   ❌ Erreur création URL: {create_response.status_code}")
            print(f"      {create_response.text}")
            return None
        
        upload_data = create_response.json()
        media_id = upload_data['media_id']
        upload_url = upload_data['upload_url']
        
        # Étape 2: Upload le fichier
        with open(file_path, 'rb') as f:
            upload_response = requests.put(
                upload_url,
                headers={'Content-Type': mime_type},
                data=f
            )
        
        if upload_response.status_code in [200, 201]:
            print(f"   ✅ Média uploadé: {media_id}")
            return media_id
        else:
            print(f"   ❌ Erreur upload: {upload_response.status_code}")
            return None
    
    def parse_media_paths(self, media_string: str) -> List[str]:
        """Parse une chaîne de médias (format liste Python) en liste de chemins."""
        if not media_string or media_string == '[]':
            return []
        
        try:
            # Essayer de parser comme une liste Python
            media_list = ast.literal_eval(media_string)
            if isinstance(media_list, list):
                paths = []
                for item in media_list:
                    if isinstance(item, dict) and 'downloaded_filepath' in item:
                        paths.append(item['downloaded_filepath'])
                    elif isinstance(item, str):
                        paths.append(item)
                return paths
        except:
            pass
        
        return []
    
    def create_post(self, 
                    caption: str, 
                    media_ids: List[str] = None,
                    social_account_ids: List[int] = None,
                    scheduled_at: Optional[str] = None) -> Dict:
        """Crée un post sur Post Bridge."""
        
        if not social_account_ids:
            print("⚠️  Aucun compte social spécifié")
            return None
        
        post_data = {
            'caption': caption,
            'social_accounts': social_account_ids
        }
        
        if media_ids:
            post_data['media'] = media_ids
        
        if scheduled_at:
            post_data['scheduled_at'] = scheduled_at
        
        response = requests.post(
            f"{self.api_base_url}/posts",
            headers=self.headers,
            json=post_data
        )
        
        if response.status_code in [200, 201]:
            return response.json()
        else:
            print(f"❌ Erreur création post: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return None
    
    def should_post_tweet(self, tweet: Dict) -> bool:
        """Détermine si un tweet doit être posté selon les filtres."""
        filters = self.config['filters']
        
        # Type de tweet
        tweet_type = tweet.get('Tweet Type (Original / Retweet / Quote / Reply)', '')
        if filters['skip_retweets'] and tweet_type == 'Retweet':
            return False
        if filters['skip_replies'] and tweet_type == 'Reply':
            return False
        if filters['skip_quotes'] and tweet_type == 'Quote':
            return False
        
        # Nombre de likes minimum
        try:
            likes = int(tweet.get('Tweet Likes Count', 0) or 0)
            if likes < filters['min_likes']:
                return False
        except (ValueError, TypeError):
            pass
        
        return True
    
    def load_tweets_from_csv(self, csv_path: str) -> List[Dict]:
        """Charge les tweets depuis un fichier CSV."""
        tweets = []
        
        if not os.path.exists(csv_path):
            print(f"⚠️  Fichier CSV introuvable: {csv_path}")
            return tweets
        
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                tweets.append(row)
        
        return tweets
    
    def process_account_tweets(self, 
                               account_name: str,
                               twitter_account_ids: List[int],
                               max_posts: Optional[int] = None) -> int:
        """Traite tous les tweets d'un compte."""
        
        csv_path = os.path.join(
            self.config['scraped_data_path'],
            account_name,
            'Account Posts',
            'Account Posts.csv'
        )
        
        if not os.path.exists(csv_path):
            print(f"⚠️  Aucun CSV trouvé pour {account_name}")
            return 0
        
        print(f"\n📊 Traitement de @{account_name}...")
        tweets = self.load_tweets_from_csv(csv_path)
        print(f"   {len(tweets)} tweets trouvés dans le CSV")
        
        posted_count = 0
        
        for i, tweet in enumerate(tweets):
            if max_posts and posted_count >= max_posts:
                break
            
            # Vérifier si le tweet doit être posté
            if not self.should_post_tweet(tweet):
                continue
            
            # Récupérer le texte
            caption = tweet.get('Tweet Text', '').strip()
            if not caption:
                continue
            
            # Limiter la longueur (Twitter a une limite)
            if len(caption) > 280:
                caption = caption[:277] + "..."
            
            print(f"\n📝 Tweet {i+1}/{len(tweets)}")
            print(f"   Texte: {caption[:100]}{'...' if len(caption) > 100 else ''}")
            
            # Traiter les médias
            media_ids = []
            
            # Images
            images_str = tweet.get('Tweet Images Downloaded Filepaths', '')
            image_paths = self.parse_media_paths(images_str)
            
            # Vidéos
            videos_str = tweet.get('Tweet Videos Downloaded Filepaths', '')
            video_paths = self.parse_media_paths(videos_str)
            
            all_media_paths = image_paths + video_paths
            
            if all_media_paths:
                print(f"   📎 {len(all_media_paths)} média(s) trouvé(s)")
                for media_path in all_media_paths[:4]:  # Max 4 médias par tweet
                    media_id = self.upload_media(media_path)
                    if media_id:
                        media_ids.append(media_id)
                    # Pause pour éviter le rate limiting
                    time.sleep(1)
            
            # Créer le post
            print(f"   🚀 Publication du post...")
            result = self.create_post(
                caption=caption,
                media_ids=media_ids if media_ids else None,
                social_account_ids=twitter_account_ids
            )
            
            if result:
                print(f"   ✅ Post publié avec succès! ID: {result.get('id')}")
                posted_count += 1
                
                # Pause entre les posts
                time.sleep(2)
            else:
                print(f"   ❌ Échec de la publication")
        
        print(f"\n✅ {posted_count} tweet(s) publié(s) pour @{account_name}")
        return posted_count
    
    def run(self, 
            accounts: List[str] = None,
            max_posts_per_account: int = None):
        """Lance le processus de publication."""
        
        print("=" * 60)
        print("🚀 POST BRIDGE AUTO POSTER")
        print("=" * 60)
        
        # Récupérer les comptes Twitter sur Post Bridge
        twitter_accounts = self.get_social_accounts()
        
        if not twitter_accounts:
            print("\n❌ Aucun compte Twitter trouvé sur Post Bridge.")
            print("   Veuillez d'abord connecter vos comptes sur https://www.post-bridge.com/")
            return
        
        # Extraire les IDs des comptes
        twitter_account_ids = [acc['id'] for acc in twitter_accounts]
        
        # Déterminer quels comptes traiter
        if accounts:
            accounts_to_process = accounts
        else:
            # Lister tous les comptes disponibles
            scraped_path = Path(self.config['scraped_data_path'])
            accounts_to_process = [
                d.name for d in scraped_path.iterdir() 
                if d.is_dir() and d.name != 'Combined Files'
            ]
        
        print(f"\n📂 {len(accounts_to_process)} compte(s) à traiter")
        
        # Limite de posts par compte
        if max_posts_per_account is None:
            max_posts_per_account = self.config['filters'].get('max_posts_per_account')
        
        # Traiter chaque compte
        total_posted = 0
        for account_name in accounts_to_process:
            posted = self.process_account_tweets(
                account_name,
                twitter_account_ids,
                max_posts_per_account
            )
            total_posted += posted
        
        print("\n" + "=" * 60)
        print(f"✅ TERMINÉ! {total_posted} tweet(s) publié(s) au total")
        print("=" * 60)


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Poster automatiquement des tweets via Post Bridge"
    )
    parser.add_argument(
        '--accounts',
        nargs='+',
        help='Liste des comptes à traiter (ex: alecttrona thedankoe)'
    )
    parser.add_argument(
        '--max-posts',
        type=int,
        help='Nombre maximum de posts par compte'
    )
    parser.add_argument(
        '--config',
        default='postbridge_config.json',
        help='Chemin vers le fichier de configuration'
    )
    
    args = parser.parse_args()
    
    poster = PostBridgePoster(args.config)
    poster.run(
        accounts=args.accounts,
        max_posts_per_account=args.max_posts
    )


if __name__ == '__main__':
    main()

