@echo off
echo ========================================
echo   D&D Character Sheet - Installer Build
echo ========================================
echo.

REM Verifica se PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo [ERRO] PyInstaller nao encontrado. Instalando...
    pip install pyinstaller
    echo.
)

echo [1/3] Limpando builds anteriores...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "installer_output" rmdir /s /q "installer_output"
echo.

echo [2/3] Criando executavel com PyInstaller...
echo.
pyinstaller "DnD Character Sheet.spec" --clean

if not exist "dist\DnD Character Sheet.exe" (
    echo.
    echo [ERRO] Falha ao criar executavel!
    pause
    exit /b 1
)

echo.
echo [3/3] Criando instalador com Inno Setup...
echo.

REM Verifica se Inno Setup está instalado
if exist "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" (
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
) else if exist "C:\Program Files\Inno Setup 6\ISCC.exe" (
    "C:\Program Files\Inno Setup 6\ISCC.exe" installer.iss
) else (
    echo.
    echo [AVISO] Inno Setup nao encontrado!
    echo.
    echo Por favor, instale o Inno Setup de: https://jrsoftware.org/isdl.php
    echo Depois execute manualmente: ISCC.exe installer.iss
    echo.
    echo O executavel standalone esta disponivel em: dist\DnD Character Sheet.exe
    pause
    exit /b 0
)

echo.
echo ========================================
echo   Build concluido com sucesso!
echo ========================================
echo.
echo Executavel: dist\DnD Character Sheet.exe
echo Instalador: installer_output\DnD_Character_Sheet_Setup.exe
echo.
pause
