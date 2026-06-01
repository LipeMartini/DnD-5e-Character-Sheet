#!/bin/bash
# Build script para Linux (rodar via WSL ou máquina Linux)

echo "========================================"
echo "  D&D Companion - Build Script (Linux)"
echo "========================================"
echo

# Garante Python 3.10+ usando uv (gerenciador confiável da Astral)
echo "Verificando versão do Python..."
export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"

if ! command -v uv &>/dev/null; then
    echo "Instalando uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$HOME/.cargo/bin:$PATH"
fi

if ! command -v uv &>/dev/null; then
    echo "ERRO: Falha ao instalar uv. Verifique sua conexão e tente novamente."
    exit 1
fi

echo "Instalando Python 3.10 via uv..."
uv python install 3.10

PYTHON=$(uv python find 3.10 2>/dev/null)
if [ -z "$PYTHON" ]; then
    echo "ERRO: Python 3.10 nao encontrado apos instalacao."
    exit 1
fi

echo "Python: $($PYTHON --version)"

# Cria ambiente virtual isolado para o build (em $HOME para evitar limite de memória do tmpfs)
BUILD_VENV="$HOME/.dnd-build-venv"
if [ ! -f "$BUILD_VENV/bin/python" ]; then
    echo "Criando ambiente virtual..."
    uv venv "$BUILD_VENV" --python 3.10
    # Bootstrap pip no venv (uv venv não inclui pip por padrão no WSL1)
    "$BUILD_VENV/bin/python" -m ensurepip --upgrade
fi
source "$BUILD_VENV/bin/activate"
PYTHON="$BUILD_VENV/bin/python"
# uv pip causa 'Cannot allocate memory' no WSL1 por usar mmap; usa pip normal
PIP="$PYTHON -m pip --no-cache-dir"

# Adiciona ~/.local/bin ao PATH (onde pip instala scripts de usuário)
export PATH="$HOME/.local/bin:$PATH"

# Instala dependências do sistema necessárias para PyQt6
echo "Verificando dependências do sistema..."
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y \
        libpython3.10 \
        libgl1 \
        libglib2.0-0 \
        libdbus-1-3 \
        libxcb-cursor0 \
        libxcb-icccm4 \
        libxcb-image0 \
        libxcb-keysyms1 \
        libxcb-randr0 \
        libxcb-render-util0 \
        libxcb-shape0 \
        libxcb-xinerama0 \
        libxcb-xkb1 \
        libxkbcommon-x11-0 2>/dev/null
fi

# Verifica/instala PyInstaller
$PYTHON -c "import PyInstaller" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "PyInstaller nao encontrado. Instalando..."
    $PIP install pyinstaller
fi

# Instala PyQt6 com wheel pré-compilada (PyQt6 6.11+ não tem manylinux wheel)
echo "Instalando PyQt6..."
$PIP install 'PyQt6==6.7.1' --only-binary PyQt6,PyQt6-Qt6,PyQt6-sip

# Instala demais dependências do projeto
echo "Instalando dependências Python..."
$PIP install reportlab supabase

echo
echo "Criando executavel..."
echo

# Executa PyInstaller (separador de paths é : no Linux)
$PYTHON -m PyInstaller --name="DnD Companion" --onefile --windowed --add-data="data:data" --clean \
  --hidden-import=h11 \
  --hidden-import=h11._readers \
  --hidden-import=h11._writers \
  --hidden-import=h11._connection \
  --hidden-import=h11._events \
  --hidden-import=httpx \
  --hidden-import=httpx._transports.default \
  --hidden-import=httpx._transports.asgi \
  --hidden-import=httpcore \
  --hidden-import=httpcore._async.http11 \
  --hidden-import=httpcore._sync.http11 \
  --hidden-import=certifi \
  --hidden-import=anyio \
  --hidden-import=anyio._backends._asyncio \
  --hidden-import=sniffio \
  --hidden-import=supabase \
  --hidden-import=supabase_auth \
  --hidden-import=postgrest \
  --hidden-import=realtime \
  --hidden-import=storage3 \
  --hidden-import=websockets \
  --hidden-import=websockets.legacy.client \
  --hidden-import=pydantic \
  --hidden-import=jwt \
  --hidden-import=jwt.algorithms \
  --hidden-import=strenum \
  --hidden-import=yarl \
  main.py

if [ $? -ne 0 ]; then
    echo "ERRO: Build falhou."
    exit 1
fi

echo
echo "========================================"
echo "  Build concluido!"
echo "========================================"
echo
echo "O executavel esta em: dist/DnD Companion"
echo

# Torna o executável executável
chmod +x "dist/DnD Companion"
echo "Permissao de execucao aplicada."

echo
echo "========================================"
echo "  Gerando AppImage..."
echo "========================================"
echo

APPDIR="$(pwd)/AppDir"
APPIMAGE_OUT="DnD_Companion-x86_64.AppImage"

# Limpa e recria o AppDir
rm -rf "$APPDIR"
mkdir -p "$APPDIR/usr/bin"

# Copia o executável
cp "dist/DnD Companion" "$APPDIR/usr/bin/dnd-companion"

# Cria o arquivo .desktop (obrigatório para AppImage)
cat > "$APPDIR/dnd-companion.desktop" << 'EOF'
[Desktop Entry]
Name=DnD Companion
Exec=dnd-companion
Icon=dnd-companion
Type=Application
Categories=Game;
Comment=D&D 5e Character Sheet and Session Manager
EOF

# Cria ícone placeholder (PNG 256x256 simples via Python)
"$PYTHON" - << 'PYEOF'
try:
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new("RGBA", (256, 256), (139, 69, 19, 255))
    draw = ImageDraw.Draw(img)
    draw.ellipse([20, 20, 236, 236], fill=(180, 50, 50, 255))
    draw.text((128, 128), "D&D", fill=(255, 255, 255, 255), anchor="mm")
    img.save("AppDir/dnd-companion.png")
except Exception:
    # Sem Pillow disponível: cria ícone mínimo vazio (1x1)
    import struct, zlib
    def png1x1(r,g,b):
        def chunk(t,d): c=zlib.crc32(t+d)&0xffffffff; return struct.pack('>I',len(d))+t+d+struct.pack('>I',c)
        sig=b'\x89PNG\r\n\x1a\n'
        ihdr=chunk(b'IHDR',struct.pack('>IIBBBBB',1,1,8,2,0,0,0))
        raw=b'\x00'+bytes([r,g,b])
        idat=chunk(b'IDAT',zlib.compress(raw))
        iend=chunk(b'IEND',b'')
        return sig+ihdr+idat+iend
    open("AppDir/dnd-companion.png","wb").write(png1x1(139,69,19))
PYEOF

# Link simbólico obrigatório para appimagetool
ln -sf "usr/bin/dnd-companion" "$APPDIR/AppRun"
chmod +x "$APPDIR/AppRun"

# Baixa appimagetool se não estiver disponível
APPIMAGETOOL="$HOME/.local/bin/appimagetool"
if [ ! -f "$APPIMAGETOOL" ]; then
    echo "Baixando appimagetool..."
    mkdir -p "$HOME/.local/bin"
    wget -q "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" \
        -O "$APPIMAGETOOL"
    chmod +x "$APPIMAGETOOL"
fi

# Gera o AppImage (APPIMAGE_EXTRACT_AND_RUN=1 contorna a falta de FUSE no WSL1)
APPIMAGE_EXTRACT_AND_RUN=1 ARCH=x86_64 "$APPIMAGETOOL" "$APPDIR" "$APPIMAGE_OUT" 2>&1

if [ -f "$APPIMAGE_OUT" ]; then
    echo
    echo "========================================"
    echo "  AppImage gerado: $APPIMAGE_OUT"
    echo "========================================"
else
    echo "AVISO: AppImage nao foi gerado. O executavel ainda esta em dist/DnD Companion"
fi
