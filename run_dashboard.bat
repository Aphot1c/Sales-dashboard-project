@echo off
title Enterprise Sales Intelligence Dashboard
echo ========================================================
echo   Enterprise Sales Intelligence Dashboard (BCA Capstone)
echo ========================================================
echo.

:: Check if port 8501 is already listening
netstat -ano | findstr :8501 | findstr LISTENING >nul
if %errorlevel% == 0 (
    echo [INFO] Dashboard is already active on port 8501!
    echo Opening dashboard in your browser...
    start http://localhost:8501
    goto end
)

echo Starting Streamlit application server...
echo URL: http://localhost:8501
echo.
py -m streamlit run app.py

:end
pause
