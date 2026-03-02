from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem,
                             QTextEdit, QLineEdit, QCheckBox, QGroupBox, QMessageBox,
                             QScrollArea)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models import SpellDatabase, Spell

class SpellManagementWindow(QDialog):
    """Janela para gerenciar magias conhecidas/preparadas"""
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.setWindowTitle("Gerenciamento de Magias")
        self.setMinimumSize(900, 700)
        
        # Verifica se é conjurador
        if not self.character.is_spellcaster():
            QMessageBox.warning(self, "Aviso", "Este personagem não é um conjurador!")
            self.reject()
            return
        
        # Determina tipo de interface
        self.spellcasting_type = self.character.get_spellcasting_type()
        
        self.init_ui()
        self.load_spells()
    
    def init_ui(self):
        """Inicializa a interface"""
        layout = QVBoxLayout(self)
        
        # ========== HEADER COM INFORMAÇÕES ==========
        header = self.create_header()
        layout.addWidget(header)
        
        # ========== TABS POR NÍVEL DE MAGIA ==========
        self.tabs = QTabWidget()
        
        # Tab de Cantrips
        cantrips_tab = self.create_spell_level_tab(0)
        self.tabs.addTab(cantrips_tab, "Cantrips")
        
        # Tabs de níveis 1-9
        for level in range(1, 10):
            tab = self.create_spell_level_tab(level)
            self.tabs.addTab(tab, f"Nível {level}")
        
        layout.addWidget(self.tabs)
        
        # ========== BOTÕES DE AÇÃO ==========
        buttons_layout = QHBoxLayout()
        
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_header(self):
        """Cria header com informações do personagem"""
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        
        # Nome e classe
        title = QLabel(f"{self.character.name} - {self.character.character_class.name}")
        title.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #654321;")
        header_layout.addWidget(title)
        
        # Informações de conjuração
        info_layout = QHBoxLayout()
        
        ability_name = self.character.spellcasting.spellcasting_ability.upper()[:3]
        spell_dc = self.character.spellcasting.spell_save_dc
        spell_attack = self.character.spellcasting.spell_attack_bonus
        
        info_label = QLabel(
            f"Habilidade: {ability_name} | "
            f"CD de Magia: {spell_dc} | "
            f"Bônus de Ataque: +{spell_attack}"
        )
        info_label.setFont(QFont("Georgia", 10))
        info_label.setStyleSheet("color: #654321;")
        info_layout.addWidget(info_label)
        
        # Informação de preparação (se aplicável)
        if self.character.can_prepare_spells():
            max_prepared = self.character.get_max_prepared_spells()
            current_prepared = len(self.character.spellcasting.prepared_spells)
            
            prepared_label = QLabel(f"Magias Preparadas: {current_prepared}/{max_prepared}")
            prepared_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
            prepared_label.setStyleSheet("color: #228B22;")
            info_layout.addWidget(prepared_label)
        
        info_layout.addStretch()
        header_layout.addLayout(info_layout)
        
        return header_widget
    
    def create_spell_level_tab(self, level):
        """Cria tab para um nível específico de magia"""
        tab_widget = QWidget()
        tab_layout = QHBoxLayout(tab_widget)
        
        # Cria interface baseada no tipo de conjurador
        if self.spellcasting_type == 'wizard':
            return self.create_wizard_tab(level, tab_widget, tab_layout)
        elif self.spellcasting_type == 'prepared':
            return self.create_prepared_tab(level, tab_widget, tab_layout)
        else:  # known
            return self.create_known_tab(level, tab_widget, tab_layout)
    
    def create_wizard_tab(self, level, tab_widget, tab_layout):
        """Interface para Wizard: Spellbook + Preparação"""
        
        # ========== COLUNA ESQUERDA: LISTA DE MAGIAS DISPONÍVEIS ==========
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        
        # Busca
        search_layout = QHBoxLayout()
        search_label = QLabel("Buscar:")
        search_input = QLineEdit()
        search_input.setPlaceholderText("Digite o nome da magia...")
        search_input.textChanged.connect(lambda text: self.filter_spells(level, text))
        search_layout.addWidget(search_label)
        search_layout.addWidget(search_input)
        left_layout.addLayout(search_layout)
        
        # Lista de magias disponíveis
        available_label = QLabel("Magias Disponíveis:")
        available_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        left_layout.addWidget(available_label)
        
        available_list = QListWidget()
        available_list.itemClicked.connect(lambda item: self.show_spell_details(item, level))
        left_layout.addWidget(available_list)
        
        # Botão adicionar
        add_btn = QPushButton("➡️ Adicionar à Lista")
        add_btn.clicked.connect(lambda: self.add_spell_to_known(level))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: #228B22;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #32CD32;
            }
        """)
        left_layout.addWidget(add_btn)
        
        tab_layout.addWidget(left_column, 1)
        
        # ========== COLUNA CENTRAL: DETALHES DA MAGIA ==========
        center_column = QWidget()
        center_layout = QVBoxLayout(center_column)
        
        details_label = QLabel("Detalhes da Magia:")
        details_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        center_layout.addWidget(details_label)
        
        details_text = QTextEdit()
        details_text.setReadOnly(True)
        details_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 10px;
                font-family: Georgia;
            }
        """)
        center_layout.addWidget(details_text)
        
        tab_layout.addWidget(center_column, 1)
        
        # ========== COLUNA DIREITA: MAGIAS CONHECIDAS/PREPARADAS ==========
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        
        # Label dinâmico (Conhecidas vs Preparadas)
        if level == 0:
            known_label = QLabel("Cantrips Conhecidos:")
        elif self.character.can_prepare_spells():
            known_label = QLabel("Magias Conhecidas:")
        else:
            known_label = QLabel("Magias Conhecidas:")
        
        known_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        right_layout.addWidget(known_label)
        
        known_list = QListWidget()
        known_list.itemClicked.connect(lambda item: self.show_spell_details(item, level))
        right_layout.addWidget(known_list)
        
        # Botão remover
        remove_btn = QPushButton("❌ Remover da Lista")
        remove_btn.clicked.connect(lambda: self.remove_spell_from_known(level))
        remove_btn.setStyleSheet("""
            QPushButton {
                background-color: #DC143C;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #FF6347;
            }
        """)
        right_layout.addWidget(remove_btn)
        
        # Se pode preparar magias (Wizard/Cleric) e não é cantrip
        if self.character.can_prepare_spells() and level > 0:
            right_layout.addSpacing(20)
            
            prepared_label = QLabel("Magias Preparadas:")
            prepared_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
            right_layout.addWidget(prepared_label)
            
            prepared_list = QListWidget()
            prepared_list.itemClicked.connect(lambda item: self.show_spell_details(item, level))
            right_layout.addWidget(prepared_list)
            
            # Botões preparar/despreparar
            prep_buttons = QHBoxLayout()
            
            prepare_btn = QPushButton("📖 Preparar")
            prepare_btn.clicked.connect(lambda: self.prepare_spell(level))
            prepare_btn.setStyleSheet("""
                QPushButton {
                    background-color: #4169E1;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #6495ED;
                }
            """)
            prep_buttons.addWidget(prepare_btn)
            
            unprepare_btn = QPushButton("📕 Despreparar")
            unprepare_btn.clicked.connect(lambda: self.unprepare_spell(level))
            unprepare_btn.setStyleSheet("""
                QPushButton {
                    background-color: #FF8C00;
                    color: white;
                    border-radius: 5px;
                    padding: 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #FFA500;
                }
            """)
            prep_buttons.addWidget(unprepare_btn)
            
            right_layout.addLayout(prep_buttons)
        
        tab_layout.addWidget(right_column, 1)
        
        # Armazena referências para atualização
        if not hasattr(self, 'spell_widgets'):
            self.spell_widgets = {}
        
        self.spell_widgets[level] = {
            'available_list': available_list,
            'known_list': known_list,
            'details_text': details_text,
            'search_input': search_input,
        }
        
        if self.character.can_prepare_spells() and level > 0:
            self.spell_widgets[level]['prepared_list'] = prepared_list
        
        return tab_widget
    
    def load_spells(self):
        """Carrega todas as magias do banco de dados"""
        all_spells = SpellDatabase.get_all_spells()
        class_name = self.character.character_class.name
        
        # Filtra magias por classe
        class_spells = {name: spell for name, spell in all_spells.items() 
                       if class_name in spell.classes}
        
        # Organiza por nível
        for level in range(10):
            level_spells = {name: spell for name, spell in class_spells.items() 
                           if spell.level == level}
            
            if level in self.spell_widgets:
                self.update_spell_lists(level, level_spells)
    
    def update_spell_lists(self, level, available_spells):
        """Atualiza as listas de magias para um nível"""
        widgets = self.spell_widgets[level]
        
        # Limpa listas
        widgets['available_list'].clear()
        widgets['known_list'].clear()
        
        # Lista de magias conhecidas/cantrips
        if level == 0:
            known_spells = self.character.spellcasting.known_cantrips
        else:
            known_spells = self.character.spellcasting.known_spells
        
        # Popula lista de disponíveis (excluindo já conhecidas)
        for spell_name in sorted(available_spells.keys()):
            if spell_name not in known_spells:
                item = QListWidgetItem(spell_name)
                item.setData(Qt.ItemDataRole.UserRole, available_spells[spell_name])
                widgets['available_list'].addItem(item)
        
        # Popula lista de conhecidas
        for spell_name in sorted(known_spells):
            if spell_name in available_spells:
                item = QListWidgetItem(spell_name)
                item.setData(Qt.ItemDataRole.UserRole, available_spells[spell_name])
                widgets['known_list'].addItem(item)
        
        # Popula lista de preparadas (se aplicável)
        if 'prepared_list' in widgets:
            widgets['prepared_list'].clear()
            prepared_spells = self.character.spellcasting.prepared_spells
            
            for spell_name in sorted(prepared_spells):
                spell = SpellDatabase.get_spell(spell_name)
                if spell and spell.level == level:
                    item = QListWidgetItem(spell_name)
                    item.setData(Qt.ItemDataRole.UserRole, spell)
                    widgets['prepared_list'].addItem(item)
    
    def filter_spells(self, level, search_text):
        """Filtra magias por texto de busca"""
        widgets = self.spell_widgets[level]
        available_list = widgets['available_list']
        
        for i in range(available_list.count()):
            item = available_list.item(i)
            item.setHidden(search_text.lower() not in item.text().lower())
    
    def show_spell_details(self, item, level):
        """Mostra detalhes de uma magia"""
        spell = item.data(Qt.ItemDataRole.UserRole)
        if not spell:
            return
        
        widgets = self.spell_widgets[level]
        details_text = widgets['details_text']
        
        # Formata detalhes
        details = f"""<h2 style='color: #654321;'>{spell.name}</h2>
<p><b>Nível:</b> {spell.get_level_text()}<br>
<b>Escola:</b> {spell.school}<br>
<b>Tempo de Conjuração:</b> {spell.casting_time}<br>
<b>Alcance:</b> {spell.range}<br>
<b>Componentes:</b> {spell.components}<br>
<b>Duração:</b> {spell.duration}</p>

<p><b>Descrição:</b><br>{spell.description.replace(chr(10), '<br>')}</p>
"""
        
        if spell.ritual:
            details += "<p><i>✨ Esta magia pode ser conjurada como ritual.</i></p>"
        
        if spell.concentration:
            details += "<p><i>🧠 Requer concentração.</i></p>"
        
        details_text.setHtml(details)
    
    def add_spell_to_known(self, level):
        """Adiciona magia à lista de conhecidas"""
        widgets = self.spell_widgets[level]
        available_list = widgets['available_list']
        
        current_item = available_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione uma magia para adicionar.")
            return
        
        spell = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Adiciona à lista apropriada
        if level == 0:
            self.character.spellcasting.known_cantrips.append(spell.name)
        else:
            self.character.spellcasting.known_spells.append(spell.name)
        
        # Recarrega listas
        self.load_spells()
    
    def remove_spell_from_known(self, level):
        """Remove magia da lista de conhecidas"""
        widgets = self.spell_widgets[level]
        known_list = widgets['known_list']
        
        current_item = known_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione uma magia para remover.")
            return
        
        spell_name = current_item.text()
        
        # Remove da lista apropriada
        if level == 0:
            if spell_name in self.character.spellcasting.known_cantrips:
                self.character.spellcasting.known_cantrips.remove(spell_name)
        else:
            if spell_name in self.character.spellcasting.known_spells:
                self.character.spellcasting.known_spells.remove(spell_name)
            
            # Remove também de preparadas se estiver lá
            if spell_name in self.character.spellcasting.prepared_spells:
                self.character.spellcasting.prepared_spells.remove(spell_name)
        
        # Recarrega listas
        self.load_spells()
    
    def prepare_spell(self, level):
        """Prepara uma magia"""
        widgets = self.spell_widgets[level]
        known_list = widgets['known_list']
        
        current_item = known_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione uma magia para preparar.")
            return
        
        spell_name = current_item.text()
        
        # Verifica limite de magias preparadas
        max_prepared = self.character.get_max_prepared_spells()
        current_prepared = len(self.character.spellcasting.prepared_spells)
        
        if current_prepared >= max_prepared:
            QMessageBox.warning(
                self, 
                "Limite Atingido", 
                f"Você já preparou o máximo de {max_prepared} magias.\n"
                "Despreparare uma magia primeiro."
            )
            return
        
        # Adiciona à lista de preparadas
        if spell_name not in self.character.spellcasting.prepared_spells:
            self.character.spellcasting.prepared_spells.append(spell_name)
        
        # Recarrega listas
        self.load_spells()
    
    def unprepare_spell(self, level):
        """Desprep ara uma magia"""
        widgets = self.spell_widgets[level]
        
        if 'prepared_list' not in widgets:
            return
        
        prepared_list = widgets['prepared_list']
        current_item = prepared_list.currentItem()
        
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione uma magia para despreparar.")
            return
        
        spell_name = current_item.text()
        
        # Remove da lista de preparadas
        if spell_name in self.character.spellcasting.prepared_spells:
            self.character.spellcasting.prepared_spells.remove(spell_name)
        
        # Recarrega listas
        self.load_spells()
