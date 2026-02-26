@echo off
echo ========================================
echo   Starting Flask Application
echo ========================================
echo.
echo Checking Python environment...
python --version
echo.
echo Starting server...
echo Server will be available at: http://127.0.0.1:5000
echo.
echo Press CTRL+C to stop the server
echo ========================================
echo.
python app.py
