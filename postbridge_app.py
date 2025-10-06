#!/usr/bin/env python3
"""
Interface web pour gérer les publications automatiques via Post Bridge.
"""

from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file
import json
import csv
import os
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3
from typing import List, Dict
from postbridge_poster import PostBridgePoster
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialiser le poster Post Bridge
poster = PostBridgePoster()

# Base de données SQLite
DB_PATH = 'postbridge_app.db'

# Scheduler pour l'automatisation
scheduler = BackgroundScheduler()
scheduler.start()


def init_db():
    """Initialise la base de données."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Table des posts sélectionnés
    c.execute('''
        CREATE TABLE IF NOT EXISTS selected_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            account_name TEXT NOT NULL,
            tweet_id TEXT NOT NULL,
            tweet_text TEXT,
            tweet_date TEXT,
            has_media BOOLEAN,
            media_paths TEXT,
            views_count INTEGER,
            likes_count INTEGER,
            retweets_count INTEGER,
            status TEXT DEFAULT 'pending',
            scheduled_at TEXT,
            posted_at TEXT,
            post_bridge_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(account_name, tweet_id)
        )
    ''')
    
    # Table de configuration
    c.execute('''
        CREATE TABLE IF NOT EXISTS config (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Configuration par défaut
    default_config = {
        'daily_posts_count': '5',
        'min_delay_minutes': '30',
        'max_delay_minutes': '120',
        'start_hour': '9',
        'end_hour': '18',
        'enabled': 'false',
        'timezone': 'Europe/Paris'
    }
    
    for key, value in default_config.items():
        c.execute('INSERT OR IGNORE INTO config (key, value) VALUES (?, ?)', (key, value))
    
    conn.commit()
    conn.close()


def get_config():
    """Récupère la configuration."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT key, value FROM config')
    config = dict(c.fetchall())
    conn.close()
    return config


def update_config(key, value):
    """Met à jour une valeur de configuration."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE config SET value = ?, updated_at = CURRENT_TIMESTAMP WHERE key = ?', (value, key))
    conn.commit()
    conn.close()


def load_account_tweets(account_name):
    """Charge les tweets d'un compte depuis le CSV."""
    base_path = Path(poster.config['scraped_data_path']) / account_name
    
    # Essayer structure directe
    csv_path_direct = base_path / 'Account Posts' / 'Account Posts.csv'
    media_base_dir = base_path / 'Account Posts'
    
    # Essayer structure avec session
    session_folders = [f for f in base_path.iterdir() if f.is_dir() and f.name.startswith('session_')]
    
    csv_path = None
    if csv_path_direct.exists():
        csv_path = csv_path_direct
    elif session_folders:
        # Prendre la session la plus récente
        latest_session = sorted(session_folders, reverse=True)[0]
        csv_path_session = latest_session / 'Account Posts' / 'Account Posts.csv'
        if csv_path_session.exists():
            csv_path = csv_path_session
            media_base_dir = latest_session / 'Account Posts'
    
    if not csv_path or not csv_path.exists():
        return []
    
    csv_path = str(csv_path)
    
    tweets = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parser les médias
            images_str = row.get('Tweet Images Downloaded Filepaths', '')
            videos_str = row.get('Tweet Videos Downloaded Filepaths', '')
            
            media_paths = []
            for media_str in [images_str, videos_str]:
                if media_str and media_str.strip():
                    # Format simple: "Account Posts Media/filename" ou "Account Posts Media/filename.jpg"
                    if 'Account Posts Media/' in media_str:
                        # Chemin relatif
                        relative_path = media_str.strip()
                        absolute_path = media_base_dir / relative_path
                        
                        # Vérifier si le fichier existe tel quel
                        if absolute_path.exists():
                            media_paths.append(str(absolute_path))
                        else:
                            # Si pas d'extension ou fichier non trouvé, chercher avec extensions
                            base_name = absolute_path.name
                            parent_dir = absolute_path.parent
                            
                            if parent_dir.exists():
                                # Chercher exactement ce nom de fichier avec différentes extensions
                                found = False
                                for ext in ['', '.jpg', '.jpeg', '.png', '.gif', '.webp', '.mp4', '.mov', '.avi']:
                                    potential_file = parent_dir / (base_name + ext)
                                    if potential_file.exists():
                                        media_paths.append(str(potential_file))
                                        found = True
                                        break
                                
                                # Si toujours pas trouvé, chercher si le nom existe comme préfixe
                                if not found:
                                    try:
                                        for file in parent_dir.iterdir():
                                            if file.name.startswith(base_name) and file.is_file():
                                                media_paths.append(str(file))
                                                break
                                    except:
                                        pass
                    else:
                        # Format avec liste/dict Python
                        try:
                            import ast
                            media_list = ast.literal_eval(media_str)
                            if isinstance(media_list, list):
                                for item in media_list:
                                    if isinstance(item, dict) and 'downloaded_filepath' in item:
                                        media_paths.append(item['downloaded_filepath'])
                        except:
                            pass
            
            tweet = {
                'tweet_id': row.get('Tweet ID', ''),
                'tweet_text': row.get('Tweet Text', ''),
                'tweet_date': row.get('Tweet Date and Time (UTC)', ''),
                'tweet_type': row.get('Tweet Type (Original / Retweet / Quote / Reply)', ''),
                'has_media': len(media_paths) > 0,
                'media_paths': media_paths,
                'media_count': len(media_paths),
                'views_count': int(row.get('Tweet Views Count', 0) or 0),
                'likes_count': int(row.get('Tweet Likes Count', 0) or 0),
                'retweets_count': int(row.get('Tweet Retweets Count', 0) or 0),
                'replies_count': int(row.get('Tweet Replies Count', 0) or 0),
            }
            tweets.append(tweet)
    
    return tweets


def get_available_accounts():
    """Liste tous les comptes disponibles."""
    scraped_path = Path(poster.config['scraped_data_path'])
    accounts = []
    
    for d in scraped_path.iterdir():
        if d.is_dir() and d.name != 'Combined Files':
            # Vérifier structure directe: nom_compte/Account Posts/Account Posts.csv
            csv_path_direct = d / 'Account Posts' / 'Account Posts.csv'
            
            # Vérifier structure avec session: nom_compte/session_XX/Account Posts/Account Posts.csv
            session_folders = [f for f in d.iterdir() if f.is_dir() and f.name.startswith('session_')]
            
            if csv_path_direct.exists():
                accounts.append(d.name)
            elif session_folders:
                # Prendre la session la plus récente
                latest_session = sorted(session_folders, reverse=True)[0]
                csv_path_session = latest_session / 'Account Posts' / 'Account Posts.csv'
                if csv_path_session.exists():
                    accounts.append(d.name)
    
    return sorted(accounts)


def schedule_next_posts():
    """Planifie les prochains posts selon la configuration."""
    config = get_config()
    
    if config.get('enabled') != 'true':
        return
    
    daily_count = int(config.get('daily_posts_count', 5))
    min_delay = int(config.get('min_delay_minutes', 30))
    max_delay = int(config.get('max_delay_minutes', 120))
    start_hour = int(config.get('start_hour', 9))
    end_hour = int(config.get('end_hour', 18))
    
    # Récupérer les posts en attente
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, account_name, tweet_id, tweet_text, media_paths 
        FROM selected_posts 
        WHERE status = 'pending' 
        ORDER BY likes_count DESC, views_count DESC 
        LIMIT ?
    ''', (daily_count,))
    
    posts = c.fetchall()
    
    # Planifier chaque post
    now = datetime.now()
    current_time = now.replace(hour=start_hour, minute=0, second=0, microsecond=0)
    
    if current_time < now:
        current_time = now + timedelta(minutes=random.randint(min_delay, max_delay))
    
    for post_id, account_name, tweet_id, tweet_text, media_paths_str in posts:
        # Vérifier qu'on est dans la plage horaire
        if current_time.hour >= end_hour:
            # Reporter au lendemain
            current_time = current_time.replace(hour=start_hour, minute=0) + timedelta(days=1)
        
        # Mettre à jour la planification
        c.execute('''
            UPDATE selected_posts 
            SET scheduled_at = ?, status = 'scheduled' 
            WHERE id = ?
        ''', (current_time.isoformat(), post_id))
        
        # Ajouter un délai aléatoire pour le prochain post
        delay = random.randint(min_delay, max_delay)
        current_time += timedelta(minutes=delay)
    
    conn.commit()
    conn.close()


def post_scheduled_tweets():
    """Poste les tweets planifiés dont l'heure est arrivée."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    now = datetime.now()
    
    c.execute('''
        SELECT id, account_name, tweet_id, tweet_text, media_paths 
        FROM selected_posts 
        WHERE status = 'scheduled' 
        AND scheduled_at <= ? 
        ORDER BY scheduled_at
        LIMIT 5
    ''', (now.isoformat(),))
    
    posts = c.fetchall()
    
    # Récupérer les comptes Twitter de Post Bridge
    twitter_accounts = poster.get_social_accounts()
    twitter_account_ids = [acc['id'] for acc in twitter_accounts]
    
    for post_id, account_name, tweet_id, tweet_text, media_paths_str in posts:
        try:
            # Upload des médias
            media_ids = []
            if media_paths_str:
                media_paths = json.loads(media_paths_str)
                for media_path in media_paths[:4]:
                    media_id = poster.upload_media(media_path)
                    if media_id:
                        media_ids.append(media_id)
            
            # Créer le post
            result = poster.create_post(
                caption=tweet_text[:280],
                media_ids=media_ids if media_ids else None,
                social_account_ids=twitter_account_ids
            )
            
            if result:
                c.execute('''
                    UPDATE selected_posts 
                    SET status = 'posted', posted_at = ?, post_bridge_id = ?
                    WHERE id = ?
                ''', (now.isoformat(), result.get('id'), post_id))
                print(f"✅ Post publié: {post_id} - {tweet_text[:50]}")
            else:
                c.execute('''
                    UPDATE selected_posts 
                    SET status = 'error'
                    WHERE id = ?
                ''', (post_id,))
                print(f"❌ Erreur post: {post_id}")
        
        except Exception as e:
            print(f"❌ Exception: {e}")
            c.execute('UPDATE selected_posts SET status = ? WHERE id = ?', ('error', post_id))
    
    conn.commit()
    conn.close()
    
    # Replanifier de nouveaux posts
    schedule_next_posts()


# Routes Flask

@app.route('/')
def index():
    """Page d'accueil."""
    accounts = get_available_accounts()
    config = get_config()
    
    # Statistiques
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM selected_posts WHERE status = ?', ('pending',))
    pending_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM selected_posts WHERE status = ?', ('scheduled',))
    scheduled_count = c.fetchone()[0]
    
    c.execute('SELECT COUNT(*) FROM selected_posts WHERE status = ?', ('posted',))
    posted_count = c.fetchone()[0]
    
    conn.close()
    
    return render_template('postbridge_home.html',
                         accounts=accounts,
                         config=config,
                         stats={
                             'pending': pending_count,
                             'scheduled': scheduled_count,
                             'posted': posted_count
                         })


@app.route('/browse/<account_name>')
def browse_account(account_name):
    """Parcourir les tweets d'un compte."""
    tweets = load_account_tweets(account_name)
    
    # Vérifier quels tweets sont déjà sélectionnés
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT tweet_id FROM selected_posts WHERE account_name = ?', (account_name,))
    selected_ids = set(row[0] for row in c.fetchall())
    conn.close()
    
    for tweet in tweets:
        tweet['is_selected'] = tweet['tweet_id'] in selected_ids
    
    return render_template('postbridge_browse.html',
                         account_name=account_name,
                         tweets=tweets)


@app.route('/api/select_post', methods=['POST'])
def select_post():
    """Sélectionne un post pour publication."""
    data = request.json
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    try:
        c.execute('''
            INSERT INTO selected_posts 
            (account_name, tweet_id, tweet_text, tweet_date, has_media, media_paths, 
             views_count, likes_count, retweets_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['account_name'],
            data['tweet_id'],
            data['tweet_text'],
            data.get('tweet_date', ''),
            data.get('has_media', False),
            json.dumps(data.get('media_paths', [])),
            data.get('views_count', 0),
            data.get('likes_count', 0),
            data.get('retweets_count', 0)
        ))
        conn.commit()
        return jsonify({'success': True})
    except sqlite3.IntegrityError:
        return jsonify({'success': False, 'error': 'Post déjà sélectionné'})
    finally:
        conn.close()


@app.route('/api/deselect_post', methods=['POST'])
def deselect_post():
    """Désélectionne un post."""
    data = request.json
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM selected_posts WHERE account_name = ? AND tweet_id = ?',
             (data['account_name'], data['tweet_id']))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})


@app.route('/queue')
def queue():
    """Affiche la file d'attente des posts."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT id, account_name, tweet_text, status, scheduled_at, posted_at, 
               likes_count, views_count, media_paths
        FROM selected_posts 
        ORDER BY 
            CASE status 
                WHEN 'scheduled' THEN 1 
                WHEN 'pending' THEN 2 
                WHEN 'posted' THEN 3 
                ELSE 4 
            END,
            scheduled_at, likes_count DESC
    ''')
    
    posts = []
    for row in c.fetchall():
        posts.append({
            'id': row[0],
            'account_name': row[1],
            'tweet_text': row[2],
            'status': row[3],
            'scheduled_at': row[4],
            'posted_at': row[5],
            'likes_count': row[6],
            'views_count': row[7],
            'has_media': bool(row[8] and row[8] != '[]')
        })
    
    conn.close()
    
    return render_template('postbridge_queue.html', posts=posts)


@app.route('/api/remove_from_queue/<int:post_id>', methods=['POST'])
def remove_from_queue(post_id):
    """Retire un post de la file d'attente."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('DELETE FROM selected_posts WHERE id = ?', (post_id,))
    conn.commit()
    conn.close()
    
    return jsonify({'success': True})


@app.route('/settings')
def settings():
    """Page de configuration."""
    config = get_config()
    
    # Récupérer les comptes Post Bridge
    twitter_accounts = poster.get_social_accounts()
    
    return render_template('postbridge_settings.html',
                         config=config,
                         twitter_accounts=twitter_accounts)


@app.route('/api/update_settings', methods=['POST'])
def update_settings():
    """Met à jour la configuration."""
    data = request.json
    
    for key, value in data.items():
        update_config(key, str(value))
    
    # Replanifier les posts si activé
    if data.get('enabled') == 'true':
        schedule_next_posts()
    
    return jsonify({'success': True})


@app.route('/api/schedule_now', methods=['POST'])
def schedule_now():
    """Force la planification immédiate."""
    schedule_next_posts()
    return jsonify({'success': True})


@app.route('/api/post_now/<int:post_id>', methods=['POST'])
def post_now(post_id):
    """Poste immédiatement un post spécifique."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('UPDATE selected_posts SET scheduled_at = ?, status = ? WHERE id = ?',
             (datetime.now().isoformat(), 'scheduled', post_id))
    conn.commit()
    conn.close()
    
    post_scheduled_tweets()
    
    return jsonify({'success': True})


@app.route('/media/<path:filepath>')
def serve_media(filepath):
    """Sert les fichiers médias."""
    try:
        # Décoder le chemin et le servir
        import urllib.parse
        decoded_path = urllib.parse.unquote(filepath)
        if os.path.exists(decoded_path):
            return send_file(decoded_path)
        else:
            return "File not found", 404
    except Exception as e:
        print(f"Erreur serving media: {e}")
        return "Error", 500


if __name__ == '__main__':
    init_db()
    
    # Lancer le job de vérification toutes les 5 minutes
    scheduler.add_job(
        post_scheduled_tweets,
        'interval',
        minutes=5,
        id='post_scheduled_tweets'
    )
    
    print("🚀 Démarrage de l'interface Post Bridge")
    print("📍 Accédez à http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)

