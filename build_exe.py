"""
Script para criar executável do D&D Companion
Usa PyInstaller para empacotar o aplicativo em um único arquivo .exe
"""

import PyInstaller.__main__
import os
import sys

# Diretório base do projeto
base_dir = os.path.dirname(os.path.abspath(__file__))

# Configurações do PyInstaller
PyInstaller.__main__.run([
    'main.py',                          # Script principal
    '--name=DnD Companion',       # Nome do executável
    '--onefile',                        # Criar um único arquivo
    '--windowed',                       # Sem console (GUI apenas)
    '--clean',                          # Limpar cache antes de compilar
    
    # Adicionar dados necessários
    '--add-data=data;data',             # Incluir pasta data
    
    # Otimizações
    '--optimize=2',                     # Otimização máxima
    
    # Diretório de saída
    '--distpath=dist',
    '--workpath=build',
    '--specpath=.',
])

print("\n" + "="*60)
print("Executável criado com sucesso!")
print(f"Localização: {os.path.join(base_dir, 'dist', 'DnD Companion.exe')}")
print("="*60)
