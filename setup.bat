@echo off
chcp 65001 >nul
setlocal

echo ========================================================
echo MSLX Tools: setup
echo ========================================================

echo [1/5] Starting Qdrant...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: docker-compose failed. Check Docker Desktop.
    exit /b 1
)

echo [2/5] Creating Python virtual environment...
if not exist ".venv" (
    python -m venv .venv
    if errorlevel 1 (
        echo ERROR: failed to create .venv.
        exit /b 1
    )
)

echo [3/5] Installing Python dependencies...
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip install failed.
    exit /b 1
)

echo [4/5] Creating .env from template...
if not exist ".env" (
    copy .env.example .env >nul
    echo Created .env. Fill OPENROUTER_API_KEY and check Mobile SMARTS paths.
) else (
    echo .env already exists, skipping.
)

echo [5/5] Building Mobile SMARTS syntax checker...
powershell -NoProfile -ExecutionPolicy Bypass -File ".\MobileSmartsSyntaxChecker\build.ps1"
if errorlevel 1 (
    echo WARNING: syntax checker build failed.
    echo Check .\MobileSmartsSyntaxChecker\README.md and build it manually.
) else (
    echo Syntax checker built successfully.
)

echo ========================================================
echo Setup completed.
echo ========================================================
echo Next steps:
echo 1. Open .env and fill OPENROUTER_API_KEY.
echo 2. Check MOBILESMARTS_DIR points to folder with Cleverence.Parsing.dll.
echo 3. Configure your AI client MCP server to run server.py.
echo ========================================================
pause
