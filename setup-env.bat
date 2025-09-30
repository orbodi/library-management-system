@echo off
echo ========================================
echo Configuration de l'environnement local
echo ========================================
echo.

if exist .env (
    echo ⚠️  Le fichier .env existe déjà !
    echo.
    set /p OVERWRITE="Voulez-vous le remplacer ? (o/N): "
    if /i not "%OVERWRITE%"=="o" (
        echo ❌ Opération annulée.
        pause
        exit /b 0
    )
)

echo 📝 Copie de env.example vers .env...
copy env.example .env >nul

if errorlevel 1 (
    echo ❌ Erreur lors de la copie du fichier
    pause
    exit /b 1
)

echo ✅ Fichier .env créé avec succès !
echo.
echo 📋 Prochaines étapes:
echo   1. Ouvrez le fichier .env et vérifiez les paramètres
echo   2. Modifiez les valeurs si nécessaire (notamment les mots de passe)
echo   3. Pour Docker: docker-compose up -d
echo   4. Pour développement local: python manage.py runserver
echo.
pause
