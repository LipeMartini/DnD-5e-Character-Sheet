#!/bin/bash
# Build script para Linux (rodar via WSL ou máquina Linux)

echo "========================================"
echo "  D&D Companion - Build Script (Linux)"
echo "========================================"
echo

# Garante Python 3.10+ (PyQt6 6.7+ requer Python >= 3.9)
echo "Verificando versão do Python..."
if ! python3.10 --version &>/dev/null; then
    echo "Instalando Python 3.10 via deadsnakes PPA..."
    sudo apt-get install -y software-properties-common
    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt-get update -qq
    sudo apt-get install -y python3.10
    sudo apt-get install -y python3.10-distutils 2>/dev/null || true
    # Baixa get-pip.py para arquivo (evita erro de pipe)
    curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
    python3.10 /tmp/get-pip.py --user
fi

if ! python3.10 --version &>/dev/null; then
    echo "ERRO: Python 3.10 nao foi instalado. Instale manualmente e rode novamente."
    exit 1
fi

PYTHON=python3.10
PIP="$PYTHON -m pip"

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
    $PIP install --user pyinstaller
fi

# Instala dependências do projeto
echo "Instalando dependências Python..."
$PIP install --user -r requirements.txt

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
  --hidden-import=supabase_auth._async.client \
  --hidden-import=supabase_auth._sync.client \
  --hidden-import=postgrest \
  --hidden-import=realtime \
  --hidden-import=storage3 \
  --hidden-import=websockets \
  --hidden-import=websockets.legacy.client \
  --hidden-import=pydantic \
  --hidden-import=pyjwt \
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
