@echo off
echo 🐳 Démarrage de la bibliothèque en ligne avec Docker...
echo.

REM Vérifier si Docker est installé
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker n'est pas installé. Veuillez l'installer depuis https://www.docker.com/
    pause
    exit /b 1
)

REM Vérifier si Docker Compose est installé
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose n'est pas installé.
    pause
    exit /b 1
)

echo ✅ Docker et Docker Compose sont installés
echo.

REM Construire l'image
echo 📦 Construction de l'image Docker...
docker-compose build

if errorlevel 1 (
    echo ❌ Erreur lors de la construction
    pause
    exit /b 1
)

echo ✅ Image construite avec succès
echo.

REM Démarrer les conteneurs
echo 🚀 Démarrage des conteneurs...
docker-compose up -d

if errorlevel 1 (
    echo ❌ Erreur lors du démarrage
    pause
    exit /b 1
)

echo ✅ Conteneurs démarrés
echo.
echo ⏳ Attente du démarrage complet...
timeout /t 5 /nobreak >nul

echo.
echo ✅ Application démarrée avec succès!
echo.
echo 📍 Accédez à l'application sur: http://localhost:8000
echo 📍 Interface admin: http://localhost:8000/admin
echo.
echo 📋 Commandes utiles:
echo   - Voir les logs: docker-compose logs -f
echo   - Arrêter: docker-compose down
echo   - Créer un superutilisateur: docker-compose exec web python manage.py createsuperuser
echo.
pause
