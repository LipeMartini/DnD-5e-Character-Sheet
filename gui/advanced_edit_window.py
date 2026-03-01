from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QWidget, QLabel, QPushButton, QSpinBox, QGroupBox,
                             QFormLayout, QCheckBox, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class AdvancedEditWindow(QDialog):
    """Janela de edição avançada para customização manual do personagem"""
    
    character_updated = pyqtSignal()
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.setWindowTitle("Edição Avançada")
        self.setMinimumSize(700, 600)
        self.init_ui()
        self.apply_theme()
        self.load_values()
    
    def apply_theme(self):
        """Aplica tema medieval/pergaminho"""
        self.setStyleSheet("""
            QDialog {
                background-color: #F5E6D3;
            }
            QTabWidget::pane {
                border: 2px solid #8B4513;
                background-color: #FFF8DC;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #D2B48C;
                color: #654321;
                border: 2px solid #8B4513;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 15px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #FFF8DC;
                color: #654321;
            }
            QGroupBox {
                border: 2px solid #8B4513;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #FFF8DC;
                font-weight: bold;
                color: #654321;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
            QSpinBox {
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFAF0;
                min-width: 80px;
            }
            QCheckBox {
                color: #654321;
                spacing: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border: 2px solid #8B4513;
                border-radius: 3px;
                background-color: #FFFAF0;
            }
            QCheckBox::indicator:checked {
                background-color: #8B4513;
            }
            QLabel {
                color: #654321;
            }
        """)
    
    def init_ui(self):
        """Inicializa a interface"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("⚙️ EDIÇÃO AVANÇADA")
        title.setFont(QFont("Georgia", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #654321; padding: 10px;")
        layout.addWidget(title)
        
        # Aviso
        warning = QLabel("⚠️ Use com cuidado! Alterações manuais podem sobrescrever valores calculados automaticamente.")
        warning.setWordWrap(True)
        warning.setStyleSheet("color: #D32F2F; font-style: italic; padding: 5px; background-color: #FFE6E6; border-radius: 5px;")
        layout.addWidget(warning)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Aba de Atributos
        stats_tab = self.create_stats_tab()
        self.tabs.addTab(stats_tab, "📊 Atributos")
        
        # Aba de HP e Combate
        combat_tab = self.create_combat_tab()
        self.tabs.addTab(combat_tab, "⚔️ HP e Combate")
        
        # Aba de Perícias
        skills_tab = self.create_skills_tab()
        self.tabs.addTab(skills_tab, "🎯 Perícias")
        
        layout.addWidget(self.tabs)
        
        # Botões
        button_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Salvar Alterações")
        save_btn.clicked.connect(self.save_changes)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("❌ Cancelar")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def create_stats_tab(self):
        """Cria aba de edição de atributos"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Grupo de atributos base
        base_stats_group = QGroupBox("Atributos Base (antes de bônus raciais)")
        base_stats_layout = QFormLayout()
        
        self.base_stat_spins = {}
        stat_names = {
            'strength': 'Força (FOR)',
            'dexterity': 'Destreza (DEX)',
            'constitution': 'Constituição (CON)',
            'intelligence': 'Inteligência (INT)',
            'wisdom': 'Sabedoria (WIS)',
            'charisma': 'Carisma (CHA)'
        }
        
        for stat_key, stat_label in stat_names.items():
            spin = QSpinBox()
            spin.setRange(1, 30)
            spin.setValue(10)
            self.base_stat_spins[stat_key] = spin
            base_stats_layout.addRow(stat_label, spin)
        
        base_stats_group.setLayout(base_stats_layout)
        layout.addWidget(base_stats_group)
        
        # Grupo de atributos finais (com bônus)
        final_stats_group = QGroupBox("Atributos Finais (com bônus raciais)")
        final_stats_layout = QFormLayout()
        
        self.final_stat_spins = {}
        
        for stat_key, stat_label in stat_names.items():
            spin = QSpinBox()
            spin.setRange(1, 30)
            spin.setValue(10)
            self.final_stat_spins[stat_key] = spin
            final_stats_layout.addRow(stat_label, spin)
        
        final_stats_group.setLayout(final_stats_layout)
        layout.addWidget(final_stats_group)
        
        # Info
        info_label = QLabel("💡 Dica: Normalmente você só precisa editar os atributos base. Os finais são calculados automaticamente com bônus raciais.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return tab
    
    def create_combat_tab(self):
        """Cria aba de HP e combate"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # HP
        hp_group = QGroupBox("Pontos de Vida")
        hp_layout = QFormLayout()
        
        self.max_hp_spin = QSpinBox()
        self.max_hp_spin.setRange(1, 999)
        hp_layout.addRow("HP Máximo:", self.max_hp_spin)
        
        self.current_hp_spin = QSpinBox()
        self.current_hp_spin.setRange(0, 999)
        hp_layout.addRow("HP Atual:", self.current_hp_spin)
        
        self.temp_hp_spin = QSpinBox()
        self.temp_hp_spin.setRange(0, 999)
        hp_layout.addRow("HP Temporário:", self.temp_hp_spin)
        
        hp_group.setLayout(hp_layout)
        layout.addWidget(hp_group)
        
        # Combate
        combat_group = QGroupBox("Estatísticas de Combate")
        combat_layout = QFormLayout()
        
        self.speed_spin = QSpinBox()
        self.speed_spin.setRange(0, 120)
        self.speed_spin.setSuffix(" ft")
        combat_layout.addRow("Deslocamento:", self.speed_spin)
        
        self.initiative_spin = QSpinBox()
        self.initiative_spin.setRange(-10, 20)
        self.initiative_spin.setPrefix("+ " if self.initiative_spin.value() >= 0 else "")
        combat_layout.addRow("Iniciativa (modificador):", self.initiative_spin)
        
        combat_group.setLayout(combat_layout)
        layout.addWidget(combat_group)
        
        # Info
        info_label = QLabel("💡 Dica: O deslocamento pode ser alterado por magias, equipamentos ou habilidades especiais.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(info_label)
        
        layout.addStretch()
        
        return tab
    
    def create_skills_tab(self):
        """Cria aba de edição de perícias"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Scroll area para as perícias
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        skills_group = QGroupBox("Proficiências em Perícias")
        skills_layout = QVBoxLayout()
        
        self.skill_checkboxes = {}
        
        # Perícias organizadas por atributo
        skills_by_ability = {
            'Força': ['Athletics'],
            'Destreza': ['Acrobatics', 'Sleight of Hand', 'Stealth'],
            'Inteligência': ['Arcana', 'History', 'Investigation', 'Nature', 'Religion'],
            'Sabedoria': ['Animal Handling', 'Insight', 'Medicine', 'Perception', 'Survival'],
            'Carisma': ['Deception', 'Intimidation', 'Performance', 'Persuasion']
        }
        
        skill_translations = {
            'Athletics': 'Atletismo',
            'Acrobatics': 'Acrobacia',
            'Sleight of Hand': 'Prestidigitação',
            'Stealth': 'Furtividade',
            'Arcana': 'Arcanismo',
            'History': 'História',
            'Investigation': 'Investigação',
            'Nature': 'Natureza',
            'Religion': 'Religião',
            'Animal Handling': 'Lidar com Animais',
            'Insight': 'Intuição',
            'Medicine': 'Medicina',
            'Perception': 'Percepção',
            'Survival': 'Sobrevivência',
            'Deception': 'Enganação',
            'Intimidation': 'Intimidação',
            'Performance': 'Performance',
            'Persuasion': 'Persuasão'
        }
        
        for ability, skills in skills_by_ability.items():
            # Separador
            separator = QLabel(f"━━ {ability.upper()} ━━")
            separator.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
            separator.setStyleSheet("color: #8B4513; background-color: transparent;")
            skills_layout.addWidget(separator)
            
            for skill in skills:
                checkbox = QCheckBox(skill_translations.get(skill, skill))
                checkbox.setFont(QFont("Georgia", 10))
                self.skill_checkboxes[skill] = checkbox
                skills_layout.addWidget(checkbox)
        
        skills_group.setLayout(skills_layout)
        scroll_layout.addWidget(skills_group)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Info
        info_label = QLabel("💡 Dica: Marque as perícias nas quais o personagem é proficiente. Isso adiciona o bônus de proficiência aos testes.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(info_label)
        
        return tab
    
    def load_values(self):
        """Carrega valores atuais do personagem"""
        # Atributos base
        for stat_key, spin in self.base_stat_spins.items():
            value = getattr(self.character.base_stats, stat_key)
            spin.setValue(value)
        
        # Atributos finais
        for stat_key, spin in self.final_stat_spins.items():
            value = getattr(self.character.stats, stat_key)
            spin.setValue(value)
        
        # HP e Combate
        self.max_hp_spin.setValue(self.character.max_hit_points)
        self.current_hp_spin.setValue(self.character.current_hit_points)
        self.temp_hp_spin.setValue(self.character.temporary_hit_points)
        self.speed_spin.setValue(self.character.speed)
        self.initiative_spin.setValue(self.character.initiative)
        
        # Perícias
        for skill, checkbox in self.skill_checkboxes.items():
            checkbox.setChecked(skill in self.character.skill_proficiencies)
    
    def save_changes(self):
        """Salva as alterações no personagem"""
        # Confirmar
        reply = QMessageBox.question(
            self, "Confirmar Alterações",
            "Deseja salvar todas as alterações? Isso pode sobrescrever valores calculados automaticamente.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply != QMessageBox.StandardButton.Yes:
            return
        
        # Atributos base
        for stat_key, spin in self.base_stat_spins.items():
            setattr(self.character.base_stats, stat_key, spin.value())
        
        # Atributos finais
        for stat_key, spin in self.final_stat_spins.items():
            setattr(self.character.stats, stat_key, spin.value())
        
        # HP
        self.character.max_hit_points = self.max_hp_spin.value()
        self.character.current_hit_points = self.current_hp_spin.value()
        self.character.temporary_hit_points = self.temp_hp_spin.value()
        
        # Perícias
        self.character.skill_proficiencies = [
            skill for skill, checkbox in self.skill_checkboxes.items()
            if checkbox.isChecked()
        ]
        
        # Recalcula estatísticas derivadas (isso pode sobrescrever speed e initiative)
        self.character.update_derived_stats()
        
        # Aplica valores manuais de speed e initiative DEPOIS do recálculo
        self.character.speed = self.speed_spin.value()
        self.character.initiative = self.initiative_spin.value()
        
        # Emite sinal de atualização
        self.character_updated.emit()
        
        QMessageBox.information(self, "Sucesso", "Alterações salvas com sucesso!")
        self.accept()
