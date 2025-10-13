#!/bin/bash

echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║         📊 VÉRIFICATION DES MODIFICATIONS 📊                  ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo ""

DB_PATH="/home/cytech/Projects/scraperX/scraper/postbridge_interface/postbridge.db"

if [ ! -f "$DB_PATH" ]; then
    echo "❌ Base de données non trouvée !"
    echo "   Lancez Flask une première fois pour initialiser la base."
    exit 1
fi

echo "✅ Base de données trouvée !"
echo ""

echo "📊 STATISTIQUES"
echo "═══════════════════════════════════════════════════════════════"

# Nombre total de modifications
TOTAL=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM tweet_edits;" 2>/dev/null || echo "0")
echo "   Total de modifications : $TOTAL"

# Nombre de comptes modifiés
ACCOUNTS=$(sqlite3 "$DB_PATH" "SELECT COUNT(DISTINCT account_name) FROM tweet_edits;" 2>/dev/null || echo "0")
echo "   Comptes modifiés : $ACCOUNTS"

# Nombre de tweets sélectionnés
SELECTED=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM selected_posts;" 2>/dev/null || echo "0")
echo "   Tweets sélectionnés : $SELECTED"

echo ""
echo "📝 DERNIÈRES MODIFICATIONS"
echo "═══════════════════════════════════════════════════════════════"

sqlite3 "$DB_PATH" "
SELECT 
    account_name as 'Compte',
    SUBSTR(edited_text, 1, 50) || '...' as 'Texte modifié',
    updated_at as 'Date'
FROM tweet_edits 
ORDER BY updated_at DESC 
LIMIT 5;" 2>/dev/null || echo "   Aucune modification trouvée"

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Menu interactif
echo "ACTIONS DISPONIBLES :"
echo "  1) Voir toutes les modifications"
echo "  2) Voir les modifications d'un compte spécifique"
echo "  3) Exporter les modifications en CSV"
echo "  4) Quitter"
echo ""

read -p "Votre choix (1-4) : " choice

case $choice in
    1)
        echo ""
        echo "📋 TOUTES LES MODIFICATIONS"
        echo "═══════════════════════════════════════════════════════════════"
        sqlite3 -header -column "$DB_PATH" "
        SELECT 
            account_name,
            tweet_id,
            SUBSTR(original_text, 1, 30) as original,
            SUBSTR(edited_text, 1, 30) as edited,
            updated_at
        FROM tweet_edits 
        ORDER BY updated_at DESC;"
        ;;
    2)
        read -p "Nom du compte (ex: jaynitx) : " account
        echo ""
        echo "📋 MODIFICATIONS DE @$account"
        echo "═══════════════════════════════════════════════════════════════"
        sqlite3 -header -column "$DB_PATH" "
        SELECT 
            tweet_id,
            original_text,
            edited_text,
            updated_at
        FROM tweet_edits 
        WHERE account_name='$account'
        ORDER BY updated_at DESC;"
        ;;
    3)
        OUTPUT="modifications_$(date +%Y%m%d_%H%M%S).csv"
        sqlite3 -header -csv "$DB_PATH" "
        SELECT * FROM tweet_edits ORDER BY updated_at DESC;" > "$OUTPUT"
        echo ""
        echo "✅ Export réussi : $OUTPUT"
        ;;
    4)
        echo "👋 Au revoir !"
        exit 0
        ;;
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""


