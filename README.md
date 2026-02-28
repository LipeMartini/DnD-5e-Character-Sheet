# D&D 5e Character Builder

Um construtor de fichas de personagem para Dungeons & Dragons 5ª Edição desenvolvido em Python com interface gráfica moderna.

## 🎲 Funcionalidades

### Criação de Personagem
- **Informações Básicas**: Nome, raça, classe, nível, antecedente e alinhamento
- **Atributos**: Sistema completo de atributos (FOR, DES, CON, INT, SAB, CAR)
  - Rolagem automática de atributos (4d6, mantém os 3 maiores)
  - Rolagem individual por atributo
  - Cálculo automático de modificadores
- **Raças Disponíveis**: Human, Elf, Dwarf, Halfling, Dragonborn, Gnome, Half-Elf, Half-Orc, Tiefling
  - Bônus raciais aplicados automaticamente
  - Traços raciais
  - Idiomas
- **Classes Disponíveis**: Barbarian, Bard, Cleric, Druid, Fighter, Monk, Paladin, Ranger, Rogue, Sorcerer, Warlock, Wizard
  - Dado de vida específico por classe
  - Proficiências em testes de resistência
  - Seleção de perícias baseada na classe

### Ficha Completa
- Visualização completa de todas as estatísticas do personagem
- Estatísticas de combate (CA, Iniciativa, Deslocamento, PV)
- Atributos com modificadores
- Testes de resistência com indicação de proficiência
- Perícias com bônus calculados automaticamente
- Traços e características raciais
- Idiomas conhecidos

### Sistema de Rolagem de Dados
- **Rolagem Personalizada**: Suporta notação padrão de dados (ex: 2d6+3, 4d6kh3)
- **Rolagens Rápidas**: Botões para d4, d6, d8, d10, d12, d20, d100
- **Rolagens de Personagem**:
  - Iniciativa (com modificador de Destreza)
  - Testes de Resistência (com proficiências)
  - Testes de Perícia (com proficiências)
  - Rolagens de Ataque (com bônus de proficiência)
- **Histórico de Rolagens**: Mantém registro de todas as rolagens realizadas
- **Detecção de Críticos**: Identifica automaticamente acertos e falhas críticas

### Salvamento e Carregamento
- Salvar fichas em formato JSON
- Carregar fichas salvas anteriormente
- Criar novas fichas

## 🚀 Como Usar

### Instalação

1. Clone o repositório ou baixe os arquivos
2. Instale as dependências:
```bash
pip install -r requirements.txt
```

### Executar o Programa

```bash
python main.py
```

## 📁 Estrutura do Projeto

```
DnD Sheet/
├── main.py                      # Ponto de entrada da aplicação
├── requirements.txt             # Dependências do projeto
├── README.md                    # Este arquivo
├── models/                      # Modelos de dados
│   ├── __init__.py
│   ├── character.py            # Classe principal do personagem
│   ├── stats.py                # Sistema de atributos
│   ├── race.py                 # Raças e banco de dados de raças
│   ├── character_class.py      # Classes e banco de dados de classes
│   └── dice.py                 # Sistema de rolagem de dados
└── gui/                        # Interface gráfica
    ├── __init__.py
    ├── main_window.py          # Janela principal
    ├── character_creation_tab.py  # Aba de criação
    ├── character_sheet_tab.py     # Aba da ficha completa
    └── dice_roller_tab.py         # Aba de rolagem de dados
```

## 🎯 Arquitetura

O projeto foi desenvolvido com arquitetura modular e escalável, pensando em futuras expansões:

- **Separação de Responsabilidades**: Models separados da GUI
- **Banco de Dados de Raças e Classes**: Fácil adição de novas opções
- **Sistema de Dados Reutilizável**: Pode ser usado em outros contextos
- **Salvamento em JSON**: Formato legível e editável
- **Interface Responsiva**: Usa PyQt6 para interface moderna

## 🔮 Futuras Expansões

Este projeto foi desenvolvido com a possibilidade de expansão para:
- Sistema de mapas 2D
- Multiplayer online
- Controle de monstros pelo mestre
- Sistema de combate
- Gerenciamento de inventário expandido
- Sistema de magias
- Progressão de níveis automática

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **PyQt6**: Interface gráfica moderna
- **JSON**: Persistência de dados

## 📝 Regras de D&D 5e Implementadas

- Cálculo de modificadores de atributos
- Bônus de proficiência por nível
- Sistema de rolagem 4d6 (manter 3 maiores) para atributos
- Bônus raciais de atributos
- Proficiências de classe (perícias e testes de resistência)
- Cálculo de CA base
- Iniciativa baseada em Destreza
- Dados de vida por classe
- Testes de resistência e perícia com proficiências

## 📄 Licença

Este é um projeto de portfólio pessoal. Sinta-se livre para usar como referência ou base para seus próprios projetos.

---

Desenvolvido como projeto de portfólio para demonstrar habilidades em Python, POO, GUI e desenvolvimento de aplicações desktop.
# DnD-5e-Character-Sheet
