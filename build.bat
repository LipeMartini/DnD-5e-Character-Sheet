@echo off
echo ========================================
echo   D&D Character Sheet - Build Script
echo ========================================
echo.

REM Verifica se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
    echo.
)

echo Criando executavel...
echo.

REM Executa PyInstaller
pyinstaller --name="DnD Companion" --onefile --windowed --add-data="data;data" --clean ^
  --hidden-import=h11 ^
  --hidden-import=h11._readers ^
  --hidden-import=h11._writers ^
  --hidden-import=h11._connection ^
  --hidden-import=h11._events ^
  --hidden-import=httpx ^
  --hidden-import=httpx._transports.default ^
  --hidden-import=httpx._transports.asgi ^
  --hidden-import=httpcore ^
  --hidden-import=httpcore._async.http11 ^
  --hidden-import=httpcore._sync.http11 ^
  --hidden-import=certifi ^
  --hidden-import=anyio ^
  --hidden-import=anyio._backends._asyncio ^
  --hidden-import=sniffio ^
  --hidden-import=supabase ^
  --hidden-import=supabase_auth ^
  --hidden-import=supabase_auth._async.client ^
  --hidden-import=supabase_auth._sync.client ^
  --hidden-import=postgrest ^
  --hidden-import=realtime ^
  --hidden-import=storage3 ^
  --hidden-import=websockets ^
  --hidden-import=websockets.legacy.client ^
  --hidden-import=pydantic ^
  --hidden-import=pyjwt ^
  --hidden-import=strenum ^
  --hidden-import=yarl ^
  main.py

echo.
echo ========================================
echo   Build concluido!
echo ========================================
echo.
echo O executavel esta em: dist\DnD Companion.exe
echo.
pause
