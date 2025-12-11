@echo off
echo ===================================
echo   Spotify Analytics Dashboard
echo ===================================
echo.

echo [1/3] Verification de MongoDB...
net start | findstr /i "MongoDB" >nul
if errorlevel 1 (
    echo MongoDB n'est pas demarre. Demarrage...
    net start MongoDB
) else (
    echo MongoDB est deja en cours d'execution
)
echo.

echo [2/3] Demarrage du backend...
cd backend
start "Backend Server" cmd /k "npm start"
timeout /t 3 >nul
cd ..
echo.

echo [3/3] Demarrage du frontend...
cd frontend
start "Frontend Dev Server" cmd /k "npm run dev"
cd ..
echo.

echo ===================================
echo   Dashboard en cours de demarrage
echo ===================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
pause >nul
