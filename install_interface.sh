#!/bin/bash

echo "🚀 Installation de l'interface Post Bridge"
echo "=========================================="
echo ""

# Vérifier si python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

echo "✓ Python3 trouvé: $(python3 --version)"
echo ""

# Installer les dépendances
echo "📦 Installation des dépendances..."
python3 -m pip install --user Flask==3.0.0 APScheduler==3.10.4 requests==2.31.0

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Installation terminée avec succès!"
    echo ""
    echo "Pour lancer l'interface:"
    echo "  python3 postbridge_app.py"
    echo ""
    echo "Puis ouvrez votre navigateur sur:"
    echo "  http://localhost:5000"
else
    echo ""
    echo "❌ Erreur lors de l'installation"
    echo ""
    echo "Essayez manuellement:"
    echo "  python3 -m pip install --user Flask APScheduler requests"
fi

