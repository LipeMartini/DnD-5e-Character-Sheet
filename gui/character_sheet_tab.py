from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLabel, QGroupBox, QScrollArea, QGridLayout, 
                             QPushButton, QSpinBox, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette, QColor
from models import Character
from .dice_history_window import DiceHistoryWindow
from .inventory_window import InventoryWindow

class CharacterSheetTab(QWidget):
    character_updated = pyqtSignal()
    
    def __init__(self, character: Character):
        super().__init__()
        self.character = character
        self.dice_history = DiceHistoryWindow()
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
        
        # ========== LINHA MÉDIA: Skills (esquerda) + Combat Column (direita) ==========
        middle_row = QHBoxLayout()
        middle_row.setSpacing(15)
        
        # Perícias (65% - esquerda)
        skills_group = self.create_skills_section()
        middle_row.addWidget(skills_group, 65)
        
        # Coluna de Combate (35% - direita): TR + Ataques
        combat_column = self.create_combat_column()
        middle_row.addWidget(combat_column, 35)
        
        layout.addLayout(middle_row)
        
        # ========== LINHA INFERIOR: Traits + Languages + Equipment ==========
        bottom_row = QHBoxLayout()
        bottom_row.setSpacing(15)
        
        traits_group = self.create_traits_section()
        bottom_row.addWidget(traits_group)
        
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
        """Cria coluna de combate com TR compactos e ataques"""
        column_widget = QWidget()
        column_layout = QVBoxLayout(column_widget)
        column_layout.setSpacing(15)
        column_layout.setContentsMargins(0, 0, 0, 0)
        
        # Testes de Resistência (compactos)
        saves_compact = self.create_saves_compact()
        column_layout.addWidget(saves_compact)
        
        # Ataques
        attacks_section = self.create_attacks_section()
        column_layout.addWidget(attacks_section)
        
        # Espaço reservado para magias (futuro)
        spells_placeholder = QGroupBox("MAGIAS")
        spells_placeholder.setStyleSheet("QGroupBox { min-height: 100px; }")
        spells_layout = QVBoxLayout()
        placeholder_label = QLabel("Espaço reservado\npara magias")
        placeholder_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        placeholder_label.setStyleSheet("color: #999; font-style: italic;")
        spells_layout.addWidget(placeholder_label)
        spells_placeholder.setLayout(spells_layout)
        column_layout.addWidget(spells_placeholder)
        
        column_layout.addStretch()
        
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
        
        self.traits_label = QLabel("Nenhum traço")
        self.traits_label.setWordWrap(True)
        self.traits_label.setStyleSheet("background-color: transparent; padding: 5px;")
        traits_layout.addWidget(self.traits_label)
        
        traits_group.setLayout(traits_layout)
        return traits_group
    
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
        
        # Traços
        if self.character.traits:
            self.traits_label.setText("\n".join(f"• {trait}" for trait in self.character.traits))
        else:
            self.traits_label.setText("Nenhum traço")
        
        # Idiomas
        if self.character.languages:
            self.languages_label.setText(", ".join(self.character.languages))
        else:
            self.languages_label.setText("Nenhum idioma")
        
        # Ataques
        self.update_attacks_display()
    
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
        attack_roll_btn.clicked.connect(lambda: self.roll_attack(weapon))
        buttons_layout.addWidget(attack_roll_btn)
        
        damage_roll_btn = QPushButton("🎲 Dano")
        damage_roll_btn.setMaximumHeight(25)
        damage_roll_btn.clicked.connect(lambda: self.roll_damage(weapon))
        buttons_layout.addWidget(damage_roll_btn)
        
        weapon_layout.addLayout(buttons_layout)
        
        return weapon_frame
    
    def roll_attack(self, weapon):
        """Rola ataque com uma arma"""
        from models import DiceRoller
        
        # roll_d20() retorna (total, d20_value)
        attack_bonus = weapon.get_attack_bonus(self.character)
        total, d20_value = DiceRoller.roll_d20(attack_bonus)
        
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
        
        # Atualizar display
        self.update_display()
        self.character_updated.emit()
        
        # Adicionar ao histórico
        method = "Média" if use_average else "Rolagem"
        self.dice_history.add_entry(
            f"<b>Subiu para o nível {self.character.level}!</b> HP ganho: +{hp_gained} ({method})",
            "INFO"
        )
        self.dice_history.show_and_raise()
    
    def roll_initiative(self):
        """Rola iniciativa"""
        total, roll = self.character.roll_initiative()
        self.dice_history.add_roll("Iniciativa", roll, self.character.initiative, total, "INITIATIVE")
        self.dice_history.show_and_raise()
    
    def roll_save(self, ability: str):
        """Rola teste de resistência"""
        total, roll = self.character.roll_saving_throw(ability)
        modifier = self.character.stats.get_modifier(ability)
        if ability in self.character.saving_throw_proficiencies:
            modifier += self.character.proficiency_bonus
        
        ability_names = {
            'strength': 'Força',
            'dexterity': 'Destreza',
            'constitution': 'Constituição',
            'intelligence': 'Inteligência',
            'wisdom': 'Sabedoria',
            'charisma': 'Carisma'
        }
        
        self.dice_history.add_roll(f"TR {ability_names[ability]}", roll, modifier, total, "SAVE")
        self.dice_history.show_and_raise()
    
    def roll_skill(self, skill_name: str, ability: str):
        """Rola teste de perícia"""
        total, roll = self.character.roll_skill_check(skill_name, ability)
        modifier = self.character.stats.get_modifier(ability)
        if skill_name in self.character.skill_proficiencies:
            modifier += self.character.proficiency_bonus
        
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
        
        self.dice_history.add_roll(skill_names_pt.get(skill_name, skill_name), roll, modifier, total, "SKILL")
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
