#!/bin/bash

echo "========================================"
echo "Configuration de l'environnement local"
echo "========================================"
echo ""

if [ -f .env ]; then
    echo "⚠️  Le fichier .env existe déjà !"
    echo ""
    read -p "Voulez-vous le remplacer ? (o/N): " OVERWRITE
    if [ "$OVERWRITE" != "o" ] && [ "$OVERWRITE" != "O" ]; then
        echo "❌ Opération annulée."
        exit 0
    fi
fi

echo "📝 Copie de env.example vers .env..."
cp env.example .env

if [ $? -eq 0 ]; then
    echo "✅ Fichier .env créé avec succès !"
    echo ""
    echo "📋 Prochaines étapes:"
    echo "  1. Ouvrez le fichier .env et vérifiez les paramètres"
    echo "  2. Modifiez les valeurs si nécessaire"
    echo "  3. Lancez le serveur: python manage.py runserver"
    echo ""
else
    echo "❌ Erreur lors de la copie du fichier"
    exit 1
fi
