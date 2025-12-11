@echo off
echo ===================================
echo   Installation des dependances
echo ===================================
echo.

echo [1/2] Installation du backend...
cd backend
call npm install
if errorlevel 1 (
    echo Erreur lors de l'installation du backend
    pause
    exit /b 1
)
cd ..
echo.

echo [2/2] Installation du frontend...
cd frontend
call npm install
if errorlevel 1 (
    echo Erreur lors de l'installation du frontend
    pause
    exit /b 1
)
cd ..
echo.

echo ===================================
echo   Installation terminee avec succes
echo ===================================
echo.
echo Vous pouvez maintenant lancer: start-dashboard.bat
echo.
pause
