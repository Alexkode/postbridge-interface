#!/bin/bash

clear
echo "╔══════════════════════════════════════════════════════════╗"
echo "║       🚀 POST BRIDGE AUTO POSTER - INTERFACE WEB 🚀      ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Vérifier si les dépendances sont installées
echo "🔍 Vérification des dépendances..."

if ! python3 -c "import flask" 2>/dev/null; then
    echo "❌ Flask n'est pas installé"
    echo ""
    echo "Installation..."
    pip3 install --user Flask APScheduler requests 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "⚠️  Veuillez installer manuellement les dépendances:"
        echo "   pip3 install --user Flask APScheduler requests"
        echo ""
        exit 1
    fi
fi

echo "✅ Dépendances OK"
echo ""
echo "🌐 Lancement de l'interface..."
echo ""
echo "┌─────────────────────────────────────────────────────────┐"
echo "│  Interface disponible sur: http://localhost:5000        │"
echo "│  Appuyez sur Ctrl+C pour arrêter                        │"
echo "└─────────────────────────────────────────────────────────┘"
echo ""

# Lancer l'application
python3 postbridge_app.py

