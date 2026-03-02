from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLabel, QGroupBox, QScrollArea, QGridLayout, 
                             QPushButton, QSpinBox, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from models import Character
from .dice_history_window import DiceHistoryWindow
from .inventory_window import InventoryWindow
from .advanced_edit_window import AdvancedEditWindow

class CharacterSheetTab(QWidget):
    character_updated = pyqtSignal()
    
    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.dice_history = DiceHistoryWindow()
        
        # Estado de vantagem/desvantagem
        self.advantage_active = False
        self.disadvantage_active = False
        
        self.init_ui()
        self.apply_theme()
    
    def apply_theme(self):
        """Aplica tema medieval/pergaminho"""
        palette = QPalette()
        
        # Cores de pergaminho
        parchment = QColor(245, 235, 220)  # Bege claro
        parchment_dark = QColor(220, 200, 170)  # Bege escuro
        text_color = QColor(40, 30, 20)  # Marrom escuro
        accent = QColor(139, 69, 19)  # Marrom médio
        
        palette.setColor(QPalette.ColorRole.Window, parchment)
        palette.setColor(QPalette.ColorRole.WindowText, text_color)
        palette.setColor(QPalette.ColorRole.Base, parchment_dark)
        palette.setColor(QPalette.ColorRole.AlternateBase, parchment)
        palette.setColor(QPalette.ColorRole.Text, text_color)
        
        self.setPalette(palette)
        
        # Stylesheet global para o tema
        self.setStyleSheet("""
            QWidget {
                background-color: #F5EBDC;
                color: #281E14;
                font-family: 'Georgia', 'Times New Roman', serif;
            }
            
            QGroupBox {
                border: 2px solid #8B4513;
                border-radius: 8px;
                margin-top: 12px;
                padding-top: 15px;
                background-color: #F5EBDC;
                font-weight: bold;
                font-size: 13px;
            }
            
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 5px 15px;
                background-color: #8B4513;
                color: #F5EBDC;
                border-radius: 4px;
            }
            
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
                min-width: 80px;
                min-height: 30px;
            }
            
            QPushButton:hover {
                background-color: #A0522D;
                border-color: #8B4513;
            }
            
            QPushButton:pressed {
                background-color: #654321;
            }
            
            QSpinBox {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 4px;
                padding: 3px;
                min-width: 60px;
            }
            
            QLabel {
                background-color: transparent;
            }
            
            QScrollArea {
                border: none;
                background-color: #F5EBDC;
            }
            
            .stat-box {
                background-color: #FFF8DC;
                border: 3px solid #8B4513;
                border-radius: 10px;
                padding: 10px;
            }
            
            .modifier-label {
                font-size: 24px;
                font-weight: bold;
                color: #8B4513;
            }
            
            .score-label {
                font-size: 16px;
                color: #654321;
            }
        """)
    
    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
        # Container centralizado com largura máxima
        container = QWidget()
        container.setMaximumWidth(1400)  # Largura máxima da ficha
        container.setStyleSheet("background-color: transparent;")
        
        layout = QVBoxLayout(scroll_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(container)
        
        # Layout interno do container
        layout = QVBoxLayout(container)
        layout.setSpacing(15)
        
        # ========== CABEÇALHO ==========
        header = self.create_header()
        layout.addWidget(header)
        
        # ========== LINHA SUPERIOR: Stats + Combat Info ==========
        top_row = QHBoxLayout()
        top_row.setSpacing(15)
        
        # Atributos (esquerda)
        stats_group = self.create_stats_section()
        top_row.addWidget(stats_group, 1)
        
        # Info de Combate (centro)
        combat_group = self.create_combat_section()
        top_row.addWidget(combat_group, 1)
        
        # HP e Dados de Vida (direita)
        hp_group = self.create_hp_section()
        top_row.addWidget(hp_group, 1)
        
        layout.addLayout(top_row)
        
        # ========== LINHA MÉDIA: 3 Colunas Iguais (33% cada) ==========
        middle_row = QHBoxLayout()
        middle_row.setSpacing(15)
        
        # Coluna 1: Perícias (33%)
        skills_group = self.create_skills_section()
        middle_row.addWidget(skills_group, 33)
        
        # Coluna 2: Vantagem/Desvantagem + TRs + Ataques (33%)
        combat_column = self.create_combat_column()
        middle_row.addWidget(combat_column, 33)
        
        # Coluna 3: Magias (33% - placeholder)
        spells_column = self.create_spells_column()
        middle_row.addWidget(spells_column, 33)
        
        layout.addLayout(middle_row)
        
        # ========== LINHA INFERIOR: Traits + Class Features + Languages ==========
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(15)
        
        traits_group = self.create_traits_section()
        bottom_row.addWidget(traits_group)
        
        features_group = self.create_class_features_section()
        bottom_row.addWidget(features_group)
        
        languages_group = self.create_languages_section()
        bottom_row.addWidget(languages_group)
        
        layout.addLayout(bottom_row)
        
        layout.addStretch()
        
        self.update_display()
    
    def create_header(self):
        """Cria o cabeçalho com nome e informações do personagem"""
        header_frame = QFrame()
        header_frame.setStyleSheet("""
            QFrame {
                background-color: #8B4513;
                border: 3px solid #654321;
                border-radius: 10px;
                padding: 15px;
            }
        """)
        
        header_layout = QVBoxLayout(header_frame)
        
        # Linha superior com botões
        top_header = QHBoxLayout()
        
        # Botão de histórico de rolagens
        history_btn = QPushButton("📜 Histórico")
        history_btn.setStyleSheet("""
            QPushButton {
                background-color: #654321;
                color: #F5EBDC;
                border: 2px solid #4A2511;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #7D5A3F;
            }
        """)
        history_btn.clicked.connect(self.show_dice_history)
        top_header.addWidget(history_btn)
        
        # Botão de inventário
        inventory_btn = QPushButton("🎒 Inventário")
        inventory_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B6914;
                color: #F5EBDC;
                border: 2px solid #6B5010;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #A0791A;
            }
        """)
        inventory_btn.clicked.connect(self.open_inventory)
        top_header.addWidget(inventory_btn)
        
        # Botão de edição avançada
        edit_btn = QPushButton("⚙️ Edição Avançada")
        edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #5D4037;
                color: #F5EBDC;
                border: 2px solid #3E2723;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #6D4C41;
            }
        """)
        edit_btn.clicked.connect(self.open_advanced_edit)
        top_header.addWidget(edit_btn)
        
        top_header.addStretch()
        
        # Botão de subir de nível
        level_up_btn = QPushButton("⬆️ Subir de Nível")
        level_up_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: #F5EBDC;
                border: 2px solid #1B5E20;
                border-radius: 5px;
                padding: 5px 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        level_up_btn.clicked.connect(self.level_up_character)
        top_header.addWidget(level_up_btn)
        
        header_layout.addLayout(top_header)
        
        self.name_label = QLabel("NOME DO PERSONAGEM")
        name_font = QFont("Georgia", 20, QFont.Weight.Bold)
        self.name_label.setFont(name_font)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: #F5EBDC; background-color: transparent;")
        header_layout.addWidget(self.name_label)
        
        self.info_label = QLabel("Raça | Classe | Nível | Background")
        info_font = QFont("Georgia", 12)
        self.info_label.setFont(info_font)
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("color: #FFF8DC; background-color: transparent;")
        header_layout.addWidget(self.info_label)
        
        return header_frame
    
    def create_stats_section(self):
        """Cria seção de atributos com visual de escudo"""
        stats_group = QGroupBox("ATRIBUTOS")
        stats_layout = QVBoxLayout()
        stats_layout.setSpacing(10)
        
        self.stat_widgets = {}
        stat_names = {
            'strength': 'FORÇA',
            'dexterity': 'DESTREZA',
            'constitution': 'CONSTITUIÇÃO',
            'intelligence': 'INTELIGÊNCIA',
            'wisdom': 'SABEDORIA',
            'charisma': 'CARISMA'
        }
        
        for stat_name, pt_name in stat_names.items():
            stat_frame = QFrame()
            stat_frame.setStyleSheet("""
                QFrame {
                    background-color: #FFF8DC;
                    border: 3px solid #8B4513;
                    border-radius: 8px;
                    padding: 8px;
                }
            """)
            
            stat_layout = QHBoxLayout(stat_frame)
            stat_layout.setContentsMargins(10, 5, 10, 5)
            
            # Nome do atributo
            name_label = QLabel(pt_name)
            name_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
            name_label.setStyleSheet("color: #654321; background-color: transparent;")
            stat_layout.addWidget(name_label)
            
            stat_layout.addStretch()
            
            # Valor
            score_label = QLabel("10")
            score_label.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
            score_label.setStyleSheet("color: #281E14; background-color: transparent;")
            score_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            score_label.setMinimumWidth(40)
            stat_layout.addWidget(score_label)
            
            # Modificador
            mod_label = QLabel("+0")
            mod_label.setFont(QFont("Georgia", 18, QFont.Weight.Bold))
            mod_label.setStyleSheet("color: #8B4513; background-color: transparent;")
            mod_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            mod_label.setMinimumWidth(50)
            stat_layout.addWidget(mod_label)
            
            stats_layout.addWidget(stat_frame)
            
            self.stat_widgets[stat_name] = {
                'score': score_label,
                'modifier': mod_label
            }
        
        stats_group.setLayout(stats_layout)
        return stats_group
    
    def create_combat_section(self):
        """Cria seção de informações de combate"""
        combat_group = QGroupBox("COMBATE")
        combat_layout = QVBoxLayout()
        combat_layout.setSpacing(15)
        
        # AC
        ac_frame = self.create_stat_display("CLASSE DE ARMADURA", "10")
        self.ac_label = ac_frame.findChild(QLabel, "value")
        combat_layout.addWidget(ac_frame)
        
        # Iniciativa
        init_frame = self.create_stat_display("INICIATIVA", "+0")
        self.initiative_label = init_frame.findChild(QLabel, "value")
        
        # Botão de rolar iniciativa
        init_container = QWidget()
        init_layout = QHBoxLayout(init_container)
        init_layout.setContentsMargins(0, 0, 0, 0)
        init_layout.addWidget(init_frame)
        
        roll_init_btn = QPushButton("🎲")
        roll_init_btn.setMaximumWidth(40)
        roll_init_btn.clicked.connect(self.roll_initiative)
        init_layout.addWidget(roll_init_btn)
        
        combat_layout.addWidget(init_container)
        
        # Velocidade
        speed_frame = self.create_stat_display("DESLOCAMENTO", "30 ft")
        self.speed_label = speed_frame.findChild(QLabel, "value")
        combat_layout.addWidget(speed_frame)
        
        # Bônus de Proficiência
        prof_frame = self.create_stat_display("BÔNUS DE PROFICIÊNCIA", "+2")
        self.prof_bonus_label = prof_frame.findChild(QLabel, "value")
        combat_layout.addWidget(prof_frame)
        
        combat_layout.addStretch()
        combat_group.setLayout(combat_layout)
        return combat_group
    
    def create_stat_display(self, title, default_value):
        """Cria um display de estatística com título e valor"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 6px;
                padding: 8px;
            }
        """)
        
        layout = QVBoxLayout(frame)
        layout.setSpacing(5)
        
        title_label = QLabel(title)
        title_label.setFont(QFont("Georgia", 9, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #654321; background-color: transparent;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)
        
        value_label = QLabel(default_value)
        value_label.setObjectName("value")
        value_label.setFont(QFont("Georgia", 16, QFont.Weight.Bold))
        value_label.setStyleSheet("color: #8B4513; background-color: transparent;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(value_label)
        
        return frame
    
    def create_hp_section(self):
        """Cria seção de HP com controles"""
        hp_group = QGroupBox("PONTOS DE VIDA")
        hp_layout = QVBoxLayout()
        hp_layout.setSpacing(10)
        
        # HP Atual/Máximo
        hp_display = QFrame()
        hp_display.setStyleSheet("""
            QFrame {
                background-color: #FFF8DC;
                border: 3px solid #8B4513;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        
        hp_display_layout = QVBoxLayout(hp_display)
        
        self.hp_label = QLabel("0 / 0")
        self.hp_label.setFont(QFont("Georgia", 24, QFont.Weight.Bold))
        self.hp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.hp_label.setStyleSheet("color: #DC143C; background-color: transparent;")
        hp_display_layout.addWidget(self.hp_label)
        
        self.temp_hp_label = QLabel("HP Temp: 0")
        self.temp_hp_label.setFont(QFont("Georgia", 11))
        self.temp_hp_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temp_hp_label.setStyleSheet("color: #1E90FF; background-color: transparent;")
        self.temp_hp_label.setVisible(False)
        hp_display_layout.addWidget(self.temp_hp_label)
        
        hp_layout.addWidget(hp_display)
        
        # Controles de Dano
        damage_layout = QHBoxLayout()
        self.damage_spin = QSpinBox()
        self.damage_spin.setMaximum(999)
        self.damage_spin.setPrefix("Dano: ")
        self.damage_spin.setMinimumWidth(200)
        self.damage_spin.setStyleSheet("""
            QSpinBox {
                border: 2px solid #654321;
                border-radius: 5px;
                min-width: 100px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        damage_layout.addWidget(self.damage_spin)
        
        damage_btn = QPushButton("Aplicar")
        damage_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                min-width: 100px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        damage_btn.clicked.connect(self.apply_damage)
        damage_layout.addWidget(damage_btn)
        
        hp_layout.addLayout(damage_layout)
        
        # Controles de Cura
        heal_layout = QHBoxLayout()
        self.heal_spin = QSpinBox()
        self.heal_spin.setMaximum(999)
        self.heal_spin.setPrefix("Cura: ")
        self.heal_spin.setMinimumWidth(200)
        self.heal_spin.setStyleSheet("""
            QSpinBox {
                border: 2px solid #654321;
                border-radius: 5px;
                min-width: 100px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        heal_layout.addWidget(self.heal_spin)
        
        heal_btn = QPushButton("Curar")
        heal_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                min-width: 100px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        heal_btn.clicked.connect(self.apply_healing)
        heal_layout.addWidget(heal_btn)
        
        hp_layout.addLayout(heal_layout)
        
        # Botões de Descanso
        short_rest_btn = QPushButton("Descanso Curto")
        short_rest_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                min-width: 150px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        short_rest_btn.clicked.connect(self.short_rest)
        hp_layout.addWidget(short_rest_btn)
        
        long_rest_btn = QPushButton("Descanso Longo")
        long_rest_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                min-width: 150px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        long_rest_btn.clicked.connect(self.long_rest)
        hp_layout.addWidget(long_rest_btn)
        
        hp_layout.addStretch()
        hp_group.setLayout(hp_layout)
        return hp_group
    
    def create_saves_section(self):
        """Cria seção de testes de resistência com botões de rolagem"""
        saves_group = QGroupBox("TESTES DE RESISTÊNCIA")
        saves_layout = QVBoxLayout()
        saves_layout.setSpacing(5)
        
        self.save_widgets = {}
        save_names = {
            'strength': 'Força',
            'dexterity': 'Destreza',
            'constitution': 'Constituição',
            'intelligence': 'Inteligência',
            'wisdom': 'Sabedoria',
            'charisma': 'Carisma'
        }
        
        for save_name, pt_name in save_names.items():
            save_layout = QHBoxLayout()
            
            # Indicador de proficiência
            prof_label = QLabel("○")
            prof_label.setFont(QFont("Georgia", 12))
            prof_label.setStyleSheet("color: #8B4513; background-color: transparent;")
            save_layout.addWidget(prof_label)
            
            # Nome
            name_label = QLabel(pt_name)
            name_label.setFont(QFont("Georgia", 11))
            name_label.setStyleSheet("background-color: transparent;")
            save_layout.addWidget(name_label)
            
            save_layout.addStretch()
            
            # Bônus
            bonus_label = QLabel("+0")
            bonus_label.setFont(QFont("Georgia", 12, QFont.Weight.Bold))
            bonus_label.setStyleSheet("color: #8B4513; background-color: transparent;")
            bonus_label.setMinimumWidth(40)
            save_layout.addWidget(bonus_label)
            
            # Botão de rolar
            roll_btn = QPushButton("🎲")
            roll_btn.setMaximumWidth(35)
            roll_btn.clicked.connect(lambda checked, s=save_name: self.roll_save(s))
            save_layout.addWidget(roll_btn)
            
            saves_layout.addLayout(save_layout)
            
            self.save_widgets[save_name] = {
                'prof': prof_label,
                'bonus': bonus_label
            }
        
        saves_group.setLayout(saves_layout)
        return saves_group
    
    def create_combat_column(self):
        """Cria coluna de combate com vantagem/desvantagem, TRs e ataques"""
        column_widget = QWidget()
        column_layout = QVBoxLayout(column_widget)
        column_layout.setSpacing(15)
        column_layout.setContentsMargins(0, 0, 0, 0)
        
        # Botões de Vantagem/Desvantagem
        adv_group = QGroupBox("VANTAGEM/DESVANTAGEM")
        adv_layout = QVBoxLayout()
        adv_layout.setSpacing(8)
        
        self.advantage_btn_column = QPushButton("⬆️ Vantagem")
        self.advantage_btn_column.setCheckable(True)
        self.advantage_btn_column.setStyleSheet("""
            QPushButton {
                background-color: #455A64;
                color: #F5EBDC;
                border: 2px solid #263238;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
            QPushButton:checked {
                background-color: #2E7D32;
                border-color: #1B5E20;
            }
        """)
        self.advantage_btn_column.clicked.connect(self.toggle_advantage_column)
        adv_layout.addWidget(self.advantage_btn_column)
        
        self.disadvantage_btn_column = QPushButton("⬇️ Desvantagem")
        self.disadvantage_btn_column.setCheckable(True)
        self.disadvantage_btn_column.setStyleSheet("""
            QPushButton {
                background-color: #455A64;
                color: #F5EBDC;
                border: 2px solid #263238;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #546E7A;
            }
            QPushButton:checked {
                background-color: #C62828;
                border-color: #8B0000;
            }
        """)
        self.disadvantage_btn_column.clicked.connect(self.toggle_disadvantage_column)
        adv_layout.addWidget(self.disadvantage_btn_column)
        
        adv_group.setLayout(adv_layout)
        column_layout.addWidget(adv_group)
        
        # Testes de Resistência (compactos)
        saves_compact = self.create_saves_compact()
        column_layout.addWidget(saves_compact)
        
        # Ataques
        attacks_section = self.create_attacks_section()
        column_layout.addWidget(attacks_section)
        
        column_layout.addStretch()
        
        return column_widget
    
    def create_spells_column(self):
        """Cria coluna de magias com spell slots e lista de magias"""
        column_widget = QWidget()
        column_layout = QVBoxLayout(column_widget)
        column_layout.setSpacing(10)
        column_layout.setContentsMargins(0, 0, 0, 0)
        
        # ========== SPELL SLOTS ==========
        slots_group = QGroupBox("ESPAÇOS DE MAGIA")
        slots_layout = QVBoxLayout()
        slots_layout.setSpacing(5)
        
        # Container para spell slots (será atualizado dinamicamente)
        self.spell_slots_container = QWidget()
        self.spell_slots_layout = QVBoxLayout(self.spell_slots_container)
        self.spell_slots_layout.setContentsMargins(0, 0, 0, 0)
        self.spell_slots_layout.setSpacing(3)
        
        slots_layout.addWidget(self.spell_slots_container)
        slots_group.setLayout(slots_layout)
        column_layout.addWidget(slots_group)
        
        # ========== MAGIAS CONHECIDAS/PREPARADAS ==========
        spells_group = QGroupBox("MAGIAS")
        spells_layout = QVBoxLayout()
        spells_layout.setSpacing(5)
        
        # Botão para gerenciar magias
        manage_spells_btn = QPushButton("⚙️ Gerenciar Magias")
        manage_spells_btn.clicked.connect(self.open_spell_management)
        manage_spells_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: white;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        spells_layout.addWidget(manage_spells_btn)
        
        # Container para lista de magias (será atualizado dinamicamente)
        self.spells_list_container = QWidget()
        self.spells_list_layout = QVBoxLayout(self.spells_list_container)
        self.spells_list_layout.setContentsMargins(0, 0, 0, 0)
        self.spells_list_layout.setSpacing(3)
        
        # Scroll area para magias
        scroll = QScrollArea()
        scroll.setWidget(self.spells_list_container)
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        spells_layout.addWidget(scroll)
        
        spells_group.setLayout(spells_layout)
        column_layout.addWidget(spells_group, 1)  # Stretch factor para ocupar espaço
        
        return column_widget
    
    def create_saves_compact(self):
        """Cria versão compacta dos testes de resistência"""
        saves_group = QGroupBox("TESTES DE RESISTÊNCIA")
        saves_layout = QVBoxLayout()
        saves_layout.setSpacing(3)
        
        self.save_widgets = {}
        save_names = {
            'strength': 'FOR',
            'dexterity': 'DEX',
            'constitution': 'CON',
            'intelligence': 'INT',
            'wisdom': 'WIS',
            'charisma': 'CHA'
        }
        
        for save_name, abbrev in save_names.items():
            save_layout = QHBoxLayout()
            
            # Indicador de proficiência (menor)
            prof_label = QLabel("○")
            prof_label.setFont(QFont("Georgia", 9))
            prof_label.setStyleSheet("color: #8B4513; background-color: transparent;")
            save_layout.addWidget(prof_label)
            
            # Nome abreviado
            name_label = QLabel(abbrev)
            name_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
            name_label.setStyleSheet("background-color: transparent;")
            name_label.setMinimumWidth(35)
            save_layout.addWidget(name_label)
            
            # Bônus
            bonus_label = QLabel("+0")
            bonus_label.setFont(QFont("Georgia", 11, QFont.Weight.Bold))
            bonus_label.setStyleSheet("color: #8B4513; background-color: transparent;")
            bonus_label.setMinimumWidth(30)
            save_layout.addWidget(bonus_label)
            
            save_layout.addStretch()
            
            # Botão de rolar
            roll_btn = QPushButton("🎲")
            roll_btn.setMaximumWidth(30)
            roll_btn.clicked.connect(lambda checked, s=save_name: self.roll_save(s))
            save_layout.addWidget(roll_btn)
            
            saves_layout.addLayout(save_layout)
            
            self.save_widgets[save_name] = {
                'prof': prof_label,
                'bonus': bonus_label
            }
        
        saves_group.setLayout(saves_layout)
        return saves_group
    
    def create_attacks_section(self):
        """Cria seção de ataques com armas equipadas"""
        attacks_group = QGroupBox("ATAQUES")
        attacks_layout = QVBoxLayout()
        attacks_layout.setSpacing(8)
        
        # Container para lista de ataques
        self.attacks_container = QWidget()
        self.attacks_list_layout = QVBoxLayout(self.attacks_container)
        self.attacks_list_layout.setSpacing(8)
        self.attacks_list_layout.setContentsMargins(0, 0, 0, 0)
        
        attacks_layout.addWidget(self.attacks_container)
        
        # Botão para adicionar ataque (abre inventário)
        add_attack_btn = QPushButton("+ Adicionar Ataque")
        add_attack_btn.setStyleSheet("""
            QPushButton {
                background-color: #2E7D32;
                color: #F5EBDC;
                border: 2px solid #1B5E20;
                border-radius: 5px;
                padding: 6px 10px;
                font-weight: bold;
                font-size: 10px;
            }
            QPushButton:hover {
                background-color: #388E3C;
            }
        """)
        add_attack_btn.clicked.connect(self.open_inventory)
        attacks_layout.addWidget(add_attack_btn)
        
        attacks_layout.addStretch()
        attacks_group.setLayout(attacks_layout)
        return attacks_group
    
    def create_skills_section(self):
        """Cria seção de perícias com botões de rolagem, agrupadas por atributo"""
        skills_group = QGroupBox("PERÍCIAS")
        skills_layout = QVBoxLayout()
        skills_layout.setSpacing(3)
        
        self.skills_widgets = {}
        
        # Perícias organizadas por atributo
        skills_by_ability = {
            'strength': [
                ('Athletics', 'Atletismo'),
            ],
            'dexterity': [
                ('Acrobatics', 'Acrobacia'),
                ('Sleight of Hand', 'Prestidigitação'),
                ('Stealth', 'Furtividade'),
            ],
            'intelligence': [
                ('Arcana', 'Arcanismo'),
                ('History', 'História'),
                ('Investigation', 'Investigação'),
                ('Nature', 'Natureza'),
                ('Religion', 'Religião'),
            ],
            'wisdom': [
                ('Animal Handling', 'Lidar com Animais'),
                ('Insight', 'Intuição'),
                ('Medicine', 'Medicina'),
                ('Perception', 'Percepção'),
                ('Survival', 'Sobrevivência'),
            ],
            'charisma': [
                ('Deception', 'Enganação'),
                ('Intimidation', 'Intimidação'),
                ('Performance', 'Performance'),
                ('Persuasion', 'Persuasão'),
            ],
        }
        
        ability_names = {
            'strength': 'FORÇA',
            'dexterity': 'DESTREZA',
            'intelligence': 'INTELIGÊNCIA',
            'wisdom': 'SABEDORIA',
            'charisma': 'CARISMA',
        }
        
        # Criar perícias agrupadas
        for ability, skills in skills_by_ability.items():
            # Separador de categoria
            separator = QLabel(f"━━ {ability_names[ability]} ━━")
            separator.setFont(QFont("Georgia", 9, QFont.Weight.Bold))
            separator.setStyleSheet("color: #8B4513; background-color: transparent;")
            separator.setAlignment(Qt.AlignmentFlag.AlignCenter)
            skills_layout.addWidget(separator)
            
            # Adicionar perícias deste atributo
            for skill_name, pt_name in skills:
                self._add_skill_row(skills_layout, skill_name, ability, pt_name)
            
            # Espaço entre grupos
            skills_layout.addSpacing(5)
        
        skills_group.setLayout(skills_layout)
        return skills_group
    
    def _add_skill_row(self, layout, skill_name, ability, pt_name):
        """Método auxiliar para adicionar uma linha de perícia"""
        skill_layout = QHBoxLayout()
        
        # Indicador de proficiência
        prof_label = QLabel("○")
        prof_label.setFont(QFont("Georgia", 10))
        prof_label.setStyleSheet("color: #8B4513; background-color: transparent;")
        skill_layout.addWidget(prof_label)
        
        # Nome
        name_label = QLabel(pt_name)
        name_label.setFont(QFont("Georgia", 10))
        name_label.setStyleSheet("background-color: transparent;")
        skill_layout.addWidget(name_label)
        
        skill_layout.addStretch()
        
        # Bônus
        bonus_label = QLabel("+0")
        bonus_label.setFont(QFont("Georgia", 11, QFont.Weight.Bold))
        bonus_label.setStyleSheet("color: #8B4513; background-color: transparent;")
        bonus_label.setMinimumWidth(35)
        skill_layout.addWidget(bonus_label)
        
        # Botão de rolar
        roll_btn = QPushButton("🎲")
        roll_btn.setMaximumWidth(30)
        roll_btn.clicked.connect(lambda checked, s=skill_name, a=ability: self.roll_skill(s, a))
        skill_layout.addWidget(roll_btn)
        
        layout.addLayout(skill_layout)
        
        self.skills_widgets[skill_name] = {
            'prof': prof_label,
            'bonus': bonus_label,
            'ability': ability
        }
    
    def create_traits_section(self):
        """Cria seção de traços e características"""
        traits_group = QGroupBox("TRAÇOS E CARACTERÍSTICAS")
        traits_layout = QVBoxLayout()
        
        # Container para os traços (será atualizado dinamicamente)
        self.traits_container = QWidget()
        self.traits_container_layout = QVBoxLayout(self.traits_container)
        self.traits_container_layout.setContentsMargins(0, 0, 0, 0)
        self.traits_container_layout.setSpacing(3)
        
        traits_layout.addWidget(self.traits_container)
        
        traits_group.setLayout(traits_layout)
        return traits_group
    
    def create_class_features_section(self):
        """Cria seção de features de classe"""
        features_group = QGroupBox("FEATURES DE CLASSE")
        features_layout = QVBoxLayout()
        
        # Container para as features (será atualizado dinamicamente)
        self.features_container = QWidget()
        self.features_container_layout = QVBoxLayout(self.features_container)
        self.features_container_layout.setContentsMargins(0, 0, 0, 0)
        self.features_container_layout.setSpacing(3)
        
        features_layout.addWidget(self.features_container)
        
        features_group.setLayout(features_layout)
        return features_group
    
    def create_languages_section(self):
        """Cria seção de idiomas"""
        languages_group = QGroupBox("IDIOMAS E PROFICIÊNCIAS")
        languages_layout = QVBoxLayout()
        
        self.languages_label = QLabel("Nenhum idioma")
        self.languages_label.setWordWrap(True)
        self.languages_label.setStyleSheet("background-color: transparent; padding: 5px;")
        languages_layout.addWidget(self.languages_label)
        
        languages_group.setLayout(languages_layout)
        return languages_group
    
    def update_display(self):
        """Atualiza todos os displays com os dados do personagem"""
        # Header
        if self.character.name:
            self.name_label.setText(self.character.name.upper())
        else:
            self.name_label.setText("NOME DO PERSONAGEM")
        
        race_name = self.character.race.name if self.character.race else "Raça"
        class_name = self.character.character_class.name if self.character.character_class else "Classe"
        bg_name = self.character.background.name if self.character.background else "Background"
        self.info_label.setText(f"{race_name} | {class_name} | Nível {self.character.level} | {bg_name}")
        
        # Atributos
        for stat_name, widgets in self.stat_widgets.items():
            score = getattr(self.character.stats, stat_name)
            modifier = self.character.stats.get_modifier(stat_name)
            
            widgets['score'].setText(str(score))
            sign = '+' if modifier >= 0 else ''
            widgets['modifier'].setText(f"{sign}{modifier}")
        
        # Combate
        self.ac_label.setText(str(self.character.armor_class))
        
        init_sign = '+' if self.character.initiative >= 0 else ''
        self.initiative_label.setText(f"{init_sign}{self.character.initiative}")
        
        self.speed_label.setText(f"{self.character.speed} ft")
        self.prof_bonus_label.setText(f"+{self.character.proficiency_bonus}")
        
        # HP
        current = self.character.current_hit_points
        maximum = self.character.max_hit_points
        self.hp_label.setText(f"{current} / {maximum}")
        
        if maximum > 0:
            hp_percent = (current / maximum) * 100
            if hp_percent > 50:
                color = "#228B22"  # Verde
            elif hp_percent > 25:
                color = "#FF8C00"  # Laranja
            else:
                color = "#DC143C"  # Vermelho
            self.hp_label.setStyleSheet(f"color: {color}; background-color: transparent;")
        
        if self.character.temporary_hit_points > 0:
            self.temp_hp_label.setText(f"HP Temp: {self.character.temporary_hit_points}")
            self.temp_hp_label.setVisible(True)
        else:
            self.temp_hp_label.setVisible(False)
        
        # Testes de Resistência
        for save_name, widgets in self.save_widgets.items():
            modifier = self.character.stats.get_modifier(save_name)
            
            if save_name in self.character.saving_throw_proficiencies:
                modifier += self.character.proficiency_bonus
                widgets['prof'].setText("●")
                widgets['prof'].setStyleSheet("color: #228B22; background-color: transparent; font-weight: bold;")
            else:
                widgets['prof'].setText("○")
                widgets['prof'].setStyleSheet("color: #8B4513; background-color: transparent;")
            
            sign = '+' if modifier >= 0 else ''
            widgets['bonus'].setText(f"{sign}{modifier}")
        
        # Perícias
        for skill_name, widgets in self.skills_widgets.items():
            ability = widgets['ability']
            modifier = self.character.stats.get_modifier(ability)
            
            if skill_name in self.character.skill_proficiencies:
                modifier += self.character.proficiency_bonus
                widgets['prof'].setText("●")
                widgets['prof'].setStyleSheet("color: #228B22; background-color: transparent; font-weight: bold;")
            else:
                widgets['prof'].setText("○")
                widgets['prof'].setStyleSheet("color: #8B4513; background-color: transparent;")
            
            sign = '+' if modifier >= 0 else ''
            widgets['bonus'].setText(f"{sign}{modifier}")
        
        # Traços (com tooltips)
        self.update_traits_display()
        
        # Features de Classe (com tooltips)
        self.update_class_features_display()
        
        # Idiomas
        if self.character.languages:
            self.languages_label.setText(", ".join(self.character.languages))
        else:
            self.languages_label.setText("Nenhum idioma")
        
        # Ataques
        self.update_attacks_display()
        
        # Spell Slots e Magias
        self.update_spell_slots_display()
        self.update_spells_display()
    
    def update_traits_display(self):
        """Atualiza a exibição de traços com tooltips informativos"""
        from models import get_trait_description
        
        # Limpa traços existentes
        while self.traits_container_layout.count():
            child = self.traits_container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.character.traits:
            no_traits = QLabel("Nenhum traço")
            no_traits.setStyleSheet("color: #999; font-style: italic; padding: 5px;")
            self.traits_container_layout.addWidget(no_traits)
            return
        
        # Adiciona cada traço com ícone informativo
        for trait in self.character.traits:
            trait_layout = QHBoxLayout()
            trait_layout.setContentsMargins(0, 0, 0, 0)
            trait_layout.setSpacing(5)
            
            # Bullet point e nome do traço
            trait_label = QLabel(f"• {trait}")
            trait_label.setFont(QFont("Georgia", 10))
            trait_label.setStyleSheet("background-color: transparent; color: #654321;")
            trait_layout.addWidget(trait_label)
            
            trait_layout.addStretch()
            
            # Ícone informativo com tooltip
            info_icon = QLabel("ℹ️")
            info_icon.setFont(QFont("Georgia", 10))
            info_icon.setStyleSheet("""
                background-color: transparent; 
                color: #4A90E2;
                padding: 2px;
            """)
            info_icon.setCursor(Qt.CursorShape.WhatsThisCursor)
            
            # Define o tooltip com a descrição
            description = get_trait_description(trait)
            info_icon.setToolTip(f"<b>{trait}</b><br><br>{description}")
            
            trait_layout.addWidget(info_icon)
            
            # Container para o layout
            trait_widget = QWidget()
            trait_widget.setLayout(trait_layout)
            trait_widget.setStyleSheet("background-color: transparent;")
            
            self.traits_container_layout.addWidget(trait_widget)
    
    def update_class_features_display(self):
        """Atualiza a exibição de features de classe com tooltips informativos"""
        # Limpa features existentes
        while self.features_container_layout.count():
            child = self.features_container_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        if not self.character.class_features:
            no_features = QLabel("Nenhuma feature")
            no_features.setStyleSheet("color: #999; font-style: italic; padding: 5px;")
            self.features_container_layout.addWidget(no_features)
            return
        
        # Adiciona cada feature com ícone informativo
        for feature_name in self.character.class_features:
            feature_layout = QHBoxLayout()
            feature_layout.setContentsMargins(0, 0, 0, 0)
            feature_layout.setSpacing(5)
            
            # Bullet point e nome da feature
            feature_label = QLabel(f"• {feature_name}")
            feature_label.setFont(QFont("Georgia", 10))
            feature_label.setStyleSheet("background-color: transparent; color: #654321;")
            feature_layout.addWidget(feature_label)
            
            feature_layout.addStretch()
            
            # Ícone informativo com tooltip
            info_icon = QLabel("ℹ️")
            info_icon.setFont(QFont("Georgia", 10))
            info_icon.setStyleSheet("""
                background-color: transparent; 
                color: #4A90E2;
                padding: 2px;
            """)
            info_icon.setCursor(Qt.CursorShape.WhatsThisCursor)
            
            # Define o tooltip com a descrição
            description = self.character.get_class_feature_description(feature_name)
            info_icon.setToolTip(f"<b>{feature_name}</b><br><br>{description}")
            
            feature_layout.addWidget(info_icon)
            
            # Container para o layout
            feature_widget = QWidget()
            feature_widget.setLayout(feature_layout)
            feature_widget.setStyleSheet("background-color: transparent;")
            
            self.features_container_layout.addWidget(feature_widget)
    
    def update_spell_slots_display(self):
        """Atualiza a exibição de spell slots"""
        # Limpa spell slots existentes
        while self.spell_slots_layout.count():
            child = self.spell_slots_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Verifica se personagem é conjurador
        if not self.character.is_spellcaster():
            no_spells = QLabel("Não é conjurador")
            no_spells.setStyleSheet("color: #999; font-style: italic; padding: 5px;")
            self.spell_slots_layout.addWidget(no_spells)
            return
        
        # Exibe spell slots por nível
        for level in range(1, 10):
            max_slots = self.character.spellcasting.get_max_slots(level)
            if max_slots == 0:
                continue
            
            current_slots = self.character.spellcasting.get_available_slots(level)
            
            # Layout horizontal para o nível
            slot_layout = QHBoxLayout()
            slot_layout.setSpacing(5)
            
            # Label do nível
            level_label = QLabel(f"Nível {level}:")
            level_label.setFont(QFont("Georgia", 9, QFont.Weight.Bold))
            level_label.setStyleSheet("color: #654321;")
            slot_layout.addWidget(level_label)
            
            # Círculos de spell slots
            for i in range(max_slots):
                slot_circle = QLabel("●" if i < current_slots else "○")
                slot_circle.setFont(QFont("Arial", 10))
                slot_circle.setStyleSheet("color: #4A90E2;" if i < current_slots else "color: #999;")
                slot_layout.addWidget(slot_circle)
            
            slot_layout.addStretch()
            
            # Widget container
            slot_widget = QWidget()
            slot_widget.setLayout(slot_layout)
            self.spell_slots_layout.addWidget(slot_widget)
    
    def update_spells_display(self):
        """Atualiza a exibição de magias conhecidas/preparadas"""
        # Limpa magias existentes
        while self.spells_list_layout.count():
            child = self.spells_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Verifica se personagem é conjurador
        if not self.character.is_spellcaster():
            return
        
        # Determina qual lista usar (conhecidas ou preparadas)
        if self.character.can_prepare_spells():
            spell_list = self.character.spellcasting.prepared_spells
            list_type = "Preparadas"
        else:
            spell_list = self.character.spellcasting.known_spells
            list_type = "Conhecidas"
        
        # Adiciona cantrips
        cantrips = self.character.spellcasting.known_cantrips
        if cantrips:
            cantrip_header = QLabel("Cantrips:")
            cantrip_header.setFont(QFont("Georgia", 9, QFont.Weight.Bold))
            cantrip_header.setStyleSheet("color: #654321; margin-top: 5px;")
            self.spells_list_layout.addWidget(cantrip_header)
            
            for cantrip_name in cantrips:
                spell_label = QLabel(f"• {cantrip_name}")
                spell_label.setFont(QFont("Georgia", 9))
                spell_label.setStyleSheet("color: #654321; padding-left: 10px;")
                spell_label.setWordWrap(True)
                self.spells_list_layout.addWidget(spell_label)
        
        # Adiciona magias por nível
        if spell_list:
            from models import SpellDatabase
            
            # Agrupa magias por nível
            spells_by_level = {}
            for spell_name in spell_list:
                spell = SpellDatabase.get_spell(spell_name)
                if spell and spell.level > 0:
                    if spell.level not in spells_by_level:
                        spells_by_level[spell.level] = []
                    spells_by_level[spell.level].append(spell_name)
            
            # Exibe por nível
            for level in sorted(spells_by_level.keys()):
                level_header = QLabel(f"Nível {level}:")
                level_header.setFont(QFont("Georgia", 9, QFont.Weight.Bold))
                level_header.setStyleSheet("color: #654321; margin-top: 5px;")
                self.spells_list_layout.addWidget(level_header)
                
                for spell_name in spells_by_level[level]:
                    spell_label = QLabel(f"• {spell_name}")
                    spell_label.setFont(QFont("Georgia", 9))
                    spell_label.setStyleSheet("color: #654321; padding-left: 10px;")
                    spell_label.setWordWrap(True)
                    self.spells_list_layout.addWidget(spell_label)
        
        # Se não tem magias
        if not cantrips and not spell_list:
            no_spells = QLabel(f"Nenhuma magia {list_type.lower()}")
            no_spells.setStyleSheet("color: #999; font-style: italic; padding: 5px;")
            self.spells_list_layout.addWidget(no_spells)
        
        self.spells_list_layout.addStretch()
    
    def open_spell_management(self):
        """Abre janela de gerenciamento de magias"""
        from gui.spell_management_window import SpellManagementWindow
        
        dialog = SpellManagementWindow(self.character, self)
        if dialog.exec():
            # Atualiza display após fechar a janela
            self.update_spell_slots_display()
            self.update_spells_display()
            
            # Salva personagem automaticamente
            if hasattr(self.parent(), 'save_character'):
                self.parent().save_character()
    
    # ========== MÉTODOS DE VANTAGEM/DESVANTAGEM ==========
    
    def toggle_advantage_column(self):
        """Ativa/desativa vantagem"""
        self.advantage_active = self.advantage_btn_column.isChecked()
        
        # Se vantagem foi ativada, desativa desvantagem
        if self.advantage_active and self.disadvantage_active:
            self.disadvantage_active = False
            self.disadvantage_btn_column.setChecked(False)
    
    def toggle_disadvantage_column(self):
        """Ativa/desativa desvantagem"""
        self.disadvantage_active = self.disadvantage_btn_column.isChecked()
        
        # Se desvantagem foi ativada, desativa vantagem
        if self.disadvantage_active and self.advantage_active:
            self.advantage_active = False
            self.advantage_btn_column.setChecked(False)
    
    # ========== MÉTODOS DE INVENTÁRIO E ATAQUES ==========
    
    def open_inventory(self):
        """Abre a janela de inventário"""
        inventory_window = InventoryWindow(self.character, self)
        inventory_window.inventory_updated.connect(self.on_inventory_updated)
        inventory_window.exec()
    
    def on_inventory_updated(self):
        """Callback quando inventário é atualizado"""
        self.character.update_derived_stats()
        self.update_display()
        self.character_updated.emit()
    
    def open_advanced_edit(self):
        """Abre a janela de edição avançada"""
        edit_window = AdvancedEditWindow(self.character, self)
        edit_window.character_updated.connect(self.on_advanced_edit_updated)
        edit_window.exec()
    
    def on_advanced_edit_updated(self):
        """Callback quando edição avançada é aplicada"""
        self.update_display()
        self.character_updated.emit()
    
    def update_attacks_display(self):
        """Atualiza a exibição de ataques com armas equipadas"""
        # Limpa ataques existentes
        while self.attacks_list_layout.count():
            child = self.attacks_list_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Adiciona armas equipadas
        equipped_weapons = self.character.inventory.get_equipped_weapons()
        
        if not equipped_weapons:
            no_weapons_label = QLabel("Nenhuma arma equipada")
            no_weapons_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_weapons_label.setStyleSheet("color: #999; font-style: italic; padding: 10px;")
            self.attacks_list_layout.addWidget(no_weapons_label)
        else:
            for weapon in equipped_weapons:
                attack_widget = self.create_attack_widget(weapon)
                self.attacks_list_layout.addWidget(attack_widget)
    
    def create_attack_widget(self, weapon):
        """Cria widget para uma arma"""
        weapon_frame = QFrame()
        weapon_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        
        weapon_layout = QVBoxLayout(weapon_frame)
        weapon_layout.setSpacing(3)
        
        # Nome da arma com ícone e indicador de proficiência
        icon = "⚔️" if weapon.weapon_range == "melee" else "🏹"
        is_proficient = self.character.is_proficient_with_weapon(weapon)
        prof_indicator = "✓ " if is_proficient else ""
        
        name_label = QLabel(f"{prof_indicator}{icon} {weapon.name}")
        name_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        
        # Cor diferente se não for proficiente
        color = "#8B4513" if is_proficient else "#999999"
        name_label.setStyleSheet(f"background-color: transparent; color: {color};")
        weapon_layout.addWidget(name_label)
        
        # Bônus de ataque e dano
        attack_bonus = weapon.get_attack_bonus(self.character)
        damage_bonus = weapon.get_damage_bonus(self.character)
        
        info_label = QLabel(f"Atq {'+' if attack_bonus >= 0 else ''}{attack_bonus}  |  Dano {weapon.damage_dice}{'+' if damage_bonus >= 0 else ''}{damage_bonus}")
        info_label.setFont(QFont("Georgia", 9))
        info_label.setStyleSheet("background-color: transparent; color: #654321;")
        weapon_layout.addWidget(info_label)
        
        # Botões de rolagem
        buttons_layout = QHBoxLayout()
        
        attack_roll_btn = QPushButton("🎲 Ataque")
        attack_roll_btn.setMaximumHeight(25)
        attack_roll_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        attack_roll_btn.clicked.connect(lambda: self.roll_attack(weapon))
        buttons_layout.addWidget(attack_roll_btn)
        
        damage_roll_btn = QPushButton("🎲 Dano")
        damage_roll_btn.setMaximumHeight(25)
        damage_roll_btn.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        damage_roll_btn.clicked.connect(lambda: self.roll_damage(weapon))
        buttons_layout.addWidget(damage_roll_btn)
        
        weapon_layout.addLayout(buttons_layout)
        
        return weapon_frame
    
    def roll_attack(self, weapon):
        """Rola ataque com uma arma"""
        from models import DiceRoller
        
        attack_bonus = weapon.get_attack_bonus(self.character)
        
        # Rola com vantagem/desvantagem se ativo
        if self.advantage_active:
            total1, roll1 = DiceRoller.roll_d20(attack_bonus)
            total2, roll2 = DiceRoller.roll_d20(attack_bonus)
            if total1 >= total2:
                total, d20_value = total1, roll1
            else:
                total, d20_value = total2, roll2
            roll_display = f"{roll1}, {roll2} (maior)"
        elif self.disadvantage_active:
            total1, roll1 = DiceRoller.roll_d20(attack_bonus)
            total2, roll2 = DiceRoller.roll_d20(attack_bonus)
            if total1 <= total2:
                total, d20_value = total1, roll1
            else:
                total, d20_value = total2, roll2
            roll_display = f"{roll1}, {roll2} (menor)"
        else:
            total, d20_value = DiceRoller.roll_d20(attack_bonus)
            roll_display = str(d20_value)
        
        # Se tem vantagem/desvantagem, mostra os dois dados
        if self.advantage_active or self.disadvantage_active:
            mod_sign = '+' if attack_bonus >= 0 else ''
            message = f"<b>Ataque - {weapon.name}</b>: 🎲 {roll_display} {mod_sign}{attack_bonus} = <b>{total}</b>"
            self.dice_history.add_entry(message, "ATTACK")
        else:
            self.dice_history.add_roll(f"Ataque - {weapon.name}", d20_value, attack_bonus, total, "ATTACK")
        
        self.dice_history.show_and_raise()
    
    def roll_damage(self, weapon):
        """Rola dano com uma arma"""
        from models import DiceRoller
        
        # roll() retorna (total, list_of_rolls)
        damage_total, damage_rolls = DiceRoller.roll(weapon.damage_dice)
        damage_bonus = weapon.get_damage_bonus(self.character)
        total = damage_total + damage_bonus
        
        damage_type = weapon.damage_type
        rolls_str = "+".join(str(r) for r in damage_rolls)
        message = f"<b>{weapon.name}</b>: 🎲 [{rolls_str}] {'+' if damage_bonus >= 0 else ''}{damage_bonus} = <b>{total}</b> de dano {damage_type}"
        
        self.dice_history.add_entry(message, "DAMAGE")
        self.dice_history.show_and_raise()
    
    # ========== MÉTODOS DE ROLAGEM ==========
    
    def show_dice_history(self):
        """Mostra a janela de histórico de rolagens"""
        self.dice_history.show_and_raise()
    
    def level_up_character(self):
        """Sobe de nível do personagem"""
        if not self.character.character_class:
            QMessageBox.warning(self, "Aviso", "Personagem precisa ter uma classe para subir de nível.")
            return
        
        # Diálogo customizado para escolher método de HP
        msg = QMessageBox(self)
        msg.setWindowTitle("Subir de Nível")
        msg.setText(f"Deseja subir para o nível {self.character.level + 1}?")
        
        hit_die = self.character.character_class.hit_die
        con_mod = self.character.stats.get_modifier('constitution')
        avg_hp = (hit_die // 2) + 1 + con_mod
        
        msg.setInformativeText(
            f"Escolha o método de ganho de HP:\n\n"
            f"Dado de Vida: d{hit_die}\n"
            f"Modificador CON: {'+' if con_mod >= 0 else ''}{con_mod}\n\n"
            f"🎲 Rolar: 1d{hit_die} + {con_mod}\n"
            f"📊 Média: {avg_hp} HP garantido"
        )
        
        # Definir tamanho mínimo para a janela
        msg.setStyleSheet("""
            QMessageBox {
                min-width: 400px;
            }
            QPushButton {
                min-width: 120px;
                padding: 8px 15px;
                font-size: 11px;
            }
        """)
        
        roll_btn = msg.addButton("🎲 Rolar Dado", QMessageBox.ButtonRole.AcceptRole)
        avg_btn = msg.addButton("📊 Pegar Média", QMessageBox.ButtonRole.AcceptRole)
        cancel_btn = msg.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        clicked = msg.clickedButton()
        
        if clicked == roll_btn:
            use_average = False
        elif clicked == avg_btn:
            use_average = True
        else:
            return
        
        # Subir de nível
        old_level = self.character.level
        hp_gained = self.character.level_up(use_average)
        new_level = self.character.level
        
        # Adicionar class features do novo nível
        new_features = []
        if self.character.character_class:
            new_features = self.character.add_class_features(
                self.character.character_class.name,
                new_level
            )
        
        # Atualizar display
        self.update_display()
        self.character_updated.emit()
        
        # Adicionar ao histórico
        method = "Média" if use_average else "Rolagem"
        self.dice_history.add_entry(
            f"<b>Subiu para o nível {new_level}!</b> HP ganho: +{hp_gained} ({method})",
            "INFO"
        )
        self.dice_history.show_and_raise()
        
        # Mostrar features ganhas (se houver)
        if new_features:
            features_text = "\n".join([f"• {feature}" for feature in new_features])
            QMessageBox.information(
                self,
                f"Nível {new_level} - Novas Features!",
                f"Você ganhou as seguintes features de classe:\n\n{features_text}\n\n"
                f"Confira a seção de Features de Classe na ficha para mais detalhes."
            )
    
    def roll_initiative(self):
        """Rola iniciativa"""
        total, roll = self.character.roll_initiative()
        self.dice_history.add_roll("Iniciativa", roll, self.character.initiative, total, "INITIATIVE")
        self.dice_history.show_and_raise()
    
    def roll_save(self, ability: str):
        """Rola teste de resistência"""
        from models import DiceRoller
        
        modifier = self.character.stats.get_modifier(ability)
        if ability in self.character.saving_throw_proficiencies:
            modifier += self.character.proficiency_bonus
        
        # Rola com vantagem/desvantagem se ativo
        if self.advantage_active:
            total1, roll1 = DiceRoller.roll_d20(modifier)
            total2, roll2 = DiceRoller.roll_d20(modifier)
            if total1 >= total2:
                total, roll = total1, roll1
            else:
                total, roll = total2, roll2
            roll_display = f"{roll1}, {roll2} (maior)"
        elif self.disadvantage_active:
            total1, roll1 = DiceRoller.roll_d20(modifier)
            total2, roll2 = DiceRoller.roll_d20(modifier)
            if total1 <= total2:
                total, roll = total1, roll1
            else:
                total, roll = total2, roll2
            roll_display = f"{roll1}, {roll2} (menor)"
        else:
            total, roll = DiceRoller.roll_d20(modifier)
            roll_display = str(roll)
        
        ability_names = {
            'strength': 'Força',
            'dexterity': 'Destreza',
            'constitution': 'Constituição',
            'intelligence': 'Inteligência',
            'wisdom': 'Sabedoria',
            'charisma': 'Carisma'
        }
        
        # Se tem vantagem/desvantagem, mostra os dois dados
        if self.advantage_active or self.disadvantage_active:
            mod_sign = '+' if modifier >= 0 else ''
            message = f"<b>TR {ability_names[ability]}</b>: 🎲 {roll_display} {mod_sign}{modifier} = <b>{total}</b>"
            self.dice_history.add_entry(message, "SAVE")
        else:
            self.dice_history.add_roll(f"TR {ability_names[ability]}", roll, modifier, total, "SAVE")
        
        self.dice_history.show_and_raise()
    
    def roll_skill(self, skill_name: str, ability: str):
        """Rola teste de perícia"""
        from models import DiceRoller
        
        modifier = self.character.stats.get_modifier(ability)
        if skill_name in self.character.skill_proficiencies:
            modifier += self.character.proficiency_bonus
        
        # Rola com vantagem/desvantagem se ativo
        if self.advantage_active:
            total1, roll1 = DiceRoller.roll_d20(modifier)
            total2, roll2 = DiceRoller.roll_d20(modifier)
            if total1 >= total2:
                total, roll = total1, roll1
            else:
                total, roll = total2, roll2
            roll_display = f"{roll1}, {roll2} (maior)"
        elif self.disadvantage_active:
            total1, roll1 = DiceRoller.roll_d20(modifier)
            total2, roll2 = DiceRoller.roll_d20(modifier)
            if total1 <= total2:
                total, roll = total1, roll1
            else:
                total, roll = total2, roll2
            roll_display = f"{roll1}, {roll2} (menor)"
        else:
            total, roll = DiceRoller.roll_d20(modifier)
            roll_display = str(roll)
        
        skill_names_pt = {
            'Acrobatics': 'Acrobacia',
            'Animal Handling': 'Lidar com Animais',
            'Arcana': 'Arcanismo',
            'Athletics': 'Atletismo',
            'Deception': 'Enganação',
            'History': 'História',
            'Insight': 'Intuição',
            'Intimidation': 'Intimidação',
            'Investigation': 'Investigação',
            'Medicine': 'Medicina',
            'Nature': 'Natureza',
            'Perception': 'Percepção',
            'Performance': 'Performance',
            'Persuasion': 'Persuasão',
            'Religion': 'Religião',
            'Sleight of Hand': 'Prestidigitação',
            'Stealth': 'Furtividade',
            'Survival': 'Sobrevivência'
        }
        
        skill_name_pt = skill_names_pt.get(skill_name, skill_name)
        
        # Se tem vantagem/desvantagem, mostra os dois dados
        if self.advantage_active or self.disadvantage_active:
            mod_sign = '+' if modifier >= 0 else ''
            message = f"<b>{skill_name_pt}</b>: 🎲 {roll_display} {mod_sign}{modifier} = <b>{total}</b>"
            self.dice_history.add_entry(message, "SKILL")
        else:
            self.dice_history.add_roll(skill_name_pt, roll, modifier, total, "SKILL")
        
        self.dice_history.show_and_raise()
    
    # ========== MÉTODOS DE HP ==========
    
    def apply_damage(self):
        """Aplica dano ao personagem"""
        damage = self.damage_spin.value()
        if damage <= 0:
            QMessageBox.warning(self, "Aviso", "Digite um valor de dano maior que 0.")
            return
        
        self.character.take_damage(damage)
        self.damage_spin.setValue(0)
        self.update_display()
        self.character_updated.emit()
        
        if self.character.current_hit_points == 0:
            QMessageBox.critical(
                self,
                "Personagem Inconsciente!",
                f"{self.character.name} caiu para 0 HP!\nO personagem está inconsciente e fazendo testes de morte."
            )
    
    def apply_healing(self):
        """Aplica cura ao personagem"""
        healing = self.heal_spin.value()
        if healing <= 0:
            return
        
        old_hp = self.character.current_hit_points
        self.character.heal(healing)
        actual_healing = self.character.current_hit_points - old_hp
        
        self.heal_spin.setValue(0)
        self.update_display()
        self.character_updated.emit()
    
    def short_rest(self):
        """Descanso curto"""
        info = self.character.short_rest()
        QMessageBox.information(
            self,
            "Descanso Curto",
            f"Descanso curto iniciado.\n\n{info}\n\nVocê pode rolar dados de vida para recuperar HP.\nCada dado de vida recupera 1d{self.character.character_class.hit_die if self.character.character_class else 6} + modificador de CON."
        )
    
    def long_rest(self):
        """Descanso longo"""
        result = QMessageBox.question(
            self,
            "Descanso Longo",
            "Tem certeza que deseja fazer um descanso longo?\n\nIsso irá restaurar todo o HP e metade dos dados de vida.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if result == QMessageBox.StandardButton.Yes:
            message = self.character.long_rest()
            self.update_display()
            self.character_updated.emit()
            
            QMessageBox.information(
                self,
                "Descanso Longo Completo",
                f"{message}\n\nHP: {self.character.current_hit_points}/{self.character.max_hit_points}"
            )
    
    def set_character(self, character: Character):
        """Define um novo personagem"""
        self.character = character
        self.update_display()
