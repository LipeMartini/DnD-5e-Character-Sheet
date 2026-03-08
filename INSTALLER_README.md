# Guia de Criação do Instalador - D&D Character Sheet

Este guia explica como criar o instalador do aplicativo para distribuição.

## Pré-requisitos

### 1. Python e Dependências
```bash
pip install pyinstaller
```

### 2. Inno Setup (para criar o instalador)
- Baixe e instale: https://jrsoftware.org/isdl.php
- Versão recomendada: 6.x ou superior

## Processo de Build

### Opção 1: Build Automático (Recomendado)

Execute o script que faz tudo automaticamente:

```bash
build_installer.bat
```

Este script irá:
1. Limpar builds anteriores
2. Criar o executável com PyInstaller
3. Criar o instalador com Inno Setup

**Resultado:**
- `dist\DnD Character Sheet.exe` - Executável standalone
- `installer_output\DnD_Character_Sheet_Setup.exe` - Instalador completo

### Opção 2: Build Manual

#### Passo 1: Criar o Executável
```bash
pyinstaller "DnD Character Sheet.spec" --clean
```

#### Passo 2: Criar o Instalador
```bash
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer.iss
```

## Arquivos de Configuração

### `DnD Character Sheet.spec`
- Configuração do PyInstaller
- Define quais arquivos incluir no executável
- Inclui a pasta `data` com as magias

### `installer.iss`
- Script do Inno Setup
- Define como o instalador será criado
- Configura ícones, atalhos e desinstalação

## Distribuição

### Para o Site
Faça upload do arquivo:
```
installer_output\DnD_Character_Sheet_Setup.exe
```

### Tamanho Estimado
- Executável standalone: ~50-100 MB
- Instalador: ~50-100 MB (compactado)

## Personalização

### Adicionar Ícone
1. Crie/obtenha um arquivo `.ico` (256x256 recomendado)
2. Salve como `icon.ico` na raiz do projeto
3. Edite `DnD Character Sheet.spec`:
   ```python
   exe = EXE(
       ...
       icon='icon.ico',  # Adicione esta linha
       ...
   )
   ```
4. Edite `installer.iss`:
   ```ini
   SetupIconFile=icon.ico
   ```

### Alterar Versão
Edite o arquivo `installer.iss`:
```ini
#define MyAppVersion "1.0.0"  ; Altere aqui
```

### Adicionar Licença
1. Crie um arquivo `LICENSE.txt`
2. Edite `installer.iss`:
   ```ini
   LicenseFile=LICENSE.txt
   ```

## Troubleshooting

### PyInstaller não encontrado
```bash
pip install pyinstaller
```

### Inno Setup não encontrado
- Instale de: https://jrsoftware.org/isdl.php
- Ou execute apenas: `pyinstaller "DnD Character Sheet.spec"`
- E distribua o executável em `dist\`

### Executável muito grande
- Já está otimizado com `--optimize=2` e `upx=True`
- Tamanho normal para aplicações PyQt5

### Erro ao executar o .exe
- Teste primeiro o executável em `dist\`
- Verifique se a pasta `data` está incluída
- Execute em modo console para ver erros:
  ```python
  # Em DnD Character Sheet.spec, mude:
  console=True  # temporariamente para debug
  ```

## Checklist de Release

- [ ] Testar o aplicativo localmente
- [ ] Atualizar versão em `installer.iss`
- [ ] Executar `build_installer.bat`
- [ ] Testar o executável em `dist\`
- [ ] Testar o instalador
- [ ] Fazer upload do instalador para o site
- [ ] Atualizar link de download no site

## Suporte

Para problemas ou dúvidas, consulte:
- PyInstaller: https://pyinstaller.org/
- Inno Setup: https://jrsoftware.org/ishelp/
