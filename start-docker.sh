#!/bin/bash

echo "🐳 Démarrage de la bibliothèque en ligne avec Docker..."
echo ""

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer depuis https://www.docker.com/"
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

echo "✅ Docker et Docker Compose sont installés"
echo ""

# Construire l'image
echo "📦 Construction de l'image Docker..."
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Image construite avec succès"
else
    echo "❌ Erreur lors de la construction"
    exit 1
fi

echo ""

# Démarrer les conteneurs
echo "🚀 Démarrage des conteneurs..."
docker-compose up -d

if [ $? -eq 0 ]; then
    echo "✅ Conteneurs démarrés"
else
    echo "❌ Erreur lors du démarrage"
    exit 1
fi

echo ""
echo "⏳ Attente du démarrage complet..."
sleep 5

echo ""
echo "✅ Application démarrée avec succès!"
echo ""
echo "📍 Accédez à l'application sur: http://localhost:8000"
echo "📍 Interface admin: http://localhost:8000/admin"
echo ""
echo "📋 Commandes utiles:"
echo "  - Voir les logs: docker-compose logs -f"
echo "  - Arrêter: docker-compose down"
echo "  - Créer un superutilisateur: docker-compose exec web python manage.py createsuperuser"
echo ""
