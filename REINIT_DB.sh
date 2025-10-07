#!/bin/bash
# Script pour réinitialiser la base de données

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║       🔄 RÉINITIALISATION DE LA BASE DE DONNÉES 🔄            ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

cd /home/cytech/Projects/scraperX/scraper/postbridge_interface

# Sauvegarder l'ancienne DB si elle existe
if [ -f postbridge.db ]; then
    echo "📦 Sauvegarde de l'ancienne base..."
    mv postbridge.db postbridge.db.backup_$(date +%Y%m%d_%H%M%S)
    echo "✅ Sauvegardée dans postbridge.db.backup_*"
else
    echo "ℹ️  Pas de base existante"
fi

echo ""
echo "🗑️  Suppression effectuée"
echo ""
echo "⚡ MAINTENANT:"
echo "   1. Relancez Flask → python3 postbridge_app.py"
echo "   2. Flask créera automatiquement la nouvelle DB"
echo "   3. Toutes les tables seront correctes ! ✅"
echo ""
echo "═══════════════════════════════════════════════════════════════"
