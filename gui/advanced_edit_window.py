from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QWidget, QLabel, QPushButton, QSpinBox, QGroupBox,
                             QFormLayout, QCheckBox, QScrollArea, QMessageBox,
                             QComboBox, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from models.pact_boons import PactBoonDatabase
from models.eldritch_invocations import EldritchInvocationDatabase

class AdvancedEditWindow(QDialog):
    """Janela de edição avançada para customização manual do personagem"""
    
    character_updated = pyqtSignal()
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.setWindowTitle("Edição Avançada")
        self.setMinimumSize(700, 600)
        self.pact_boon_combo: QComboBox | None = None
        self.invocation_list_widget: QListWidget | None = None
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

        # Aba de Warlock (Pact Boon + Invocations)
        warlock_tab = self.create_warlock_tab()
        self.tabs.addTab(warlock_tab, "🔮 Warlock")
        
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
        
        skills_group = QGroupBox("Perícias: Proficiência x Expertise (excludentes)")
        skills_layout = QVBoxLayout()
        
        # Dicionários de checkboxes
        self.skill_prof_checkboxes = {}
        self.skill_expert_checkboxes = {}
        
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
                row = QHBoxLayout()
                label = QLabel(skill_translations.get(skill, skill))
                label.setFont(QFont("Georgia", 10))
                prof_cb = QCheckBox("Proficiente")
                expert_cb = QCheckBox("Expertise")
                # Ligações para exclusividade mútua
                prof_cb.toggled.connect(lambda checked, s=skill: self.on_prof_toggled(s, checked))
                expert_cb.toggled.connect(lambda checked, s=skill: self.on_expert_toggled(s, checked))
                
                self.skill_prof_checkboxes[skill] = prof_cb
                self.skill_expert_checkboxes[skill] = expert_cb
                
                row.addWidget(label)
                row.addStretch(1)
                row.addWidget(prof_cb)
                row.addWidget(expert_cb)
                skills_layout.addLayout(row)
        
        skills_group.setLayout(skills_layout)
        scroll_layout.addWidget(skills_group)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Info
        info_label = QLabel("💡 Dica: Expertise dobra o bônus de proficiência e é mutuamente excludente com a proficiência simples.")
        info_label.setWordWrap(True)
        info_label.setStyleSheet("color: #666; font-style: italic; padding: 10px;")
        layout.addWidget(info_label)
        
        return tab

    def create_warlock_tab(self):
        """Cria aba dedicada a opções específicas de Warlock."""
        tab = QWidget()
        layout = QVBoxLayout(tab)

        if not self.character.character_class or self.character.character_class.name != "Warlock":
            info_label = QLabel(
                "Esta aba é liberada apenas para personagens Warlock."
            )
            info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            info_label.setWordWrap(True)
            info_label.setStyleSheet(
                "color: #777; font-style: italic; background-color: #FFF8DC; "
                "border: 1px dashed #BCAAA4; padding: 15px;"
            )
            layout.addStretch()
            layout.addWidget(info_label)
            layout.addStretch()
            return tab

        # Pact Boon
        boon_group = QGroupBox("Pact Boon")
        boon_layout = QFormLayout()
        self.pact_boon_combo = QComboBox()
        self.pact_boon_combo.addItem("— Nenhum —", None)
        for boon in PactBoonDatabase.get_all_boons():
            self.pact_boon_combo.addItem(boon.name, boon.name)
        boon_layout.addRow("Selecione:", self.pact_boon_combo)

        boon_hint = QLabel(
            "💡 Você pode redefinir seu Pact Boon aqui se estiver usando regras de "
            "reescolha entre aventuras."
        )
        boon_hint.setWordWrap(True)
        boon_hint.setStyleSheet("color: #555;")
        boon_layout.addRow(boon_hint)
        boon_group.setLayout(boon_layout)
        layout.addWidget(boon_group)

        # Invocations
        invocation_group = QGroupBox("Eldritch Invocations")
        invocation_vbox = QVBoxLayout()

        instructions = QLabel(
            "Marque as invocações que seu personagem conhece. Esta seção é útil para "
            "refazer escolhas ao subir de nível."
        )
        instructions.setWordWrap(True)
        invocation_vbox.addWidget(instructions)

        self.invocation_list_widget = QListWidget()
        self.invocation_list_widget.setStyleSheet("background-color: #FFFAF0;")
        self.invocation_list_widget.setSelectionMode(QListWidget.SelectionMode.NoSelection)

        invocations = list(EldritchInvocationDatabase.get_all_invocations().values())
        invocations.sort(key=lambda inv: (inv.min_level, inv.name))

        for invocation in invocations:
            subtitle = f"Nível {invocation.min_level}+"
            if invocation.required_pacts:
                subtitle += f" • Requer: {', '.join(invocation.required_pacts)}"
            item = QListWidgetItem(f"{invocation.name} ({subtitle})")
            item.setData(Qt.ItemDataRole.UserRole, invocation.name)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            tooltip = (
                f"<b>{invocation.name}</b><br><br>{invocation.description}<br><br>"
                f"<i>Fonte: {invocation.source}</i>"
            )
            item.setToolTip(tooltip)
            self.invocation_list_widget.addItem(item)

        invocation_vbox.addWidget(self.invocation_list_widget)

        reminder = QLabel(
            "⚠️ Respeite os requisitos oficiais (nível, patrono, Pact Boon) ao marcar "
            "novas invocações."
        )
        reminder.setWordWrap(True)
        reminder.setStyleSheet("color: #B71C1C; font-style: italic;")
        invocation_vbox.addWidget(reminder)

        invocation_group.setLayout(invocation_vbox)
        layout.addWidget(invocation_group)

        layout.addStretch()
        return tab

    def on_prof_toggled(self, skill: str, checked: bool):
        """Garante exclusividade: proficiência simples x expertise"""
        expert_cb = self.skill_expert_checkboxes.get(skill)
        if checked and expert_cb and expert_cb.isChecked():
            expert_cb.blockSignals(True)
            expert_cb.setChecked(False)
            expert_cb.blockSignals(False)
    
    def on_expert_toggled(self, skill: str, checked: bool):
        """Garante exclusividade: proficiência simples x expertise"""
        prof_cb = self.skill_prof_checkboxes.get(skill)
        if checked and prof_cb and prof_cb.isChecked():
            prof_cb.blockSignals(True)
            prof_cb.setChecked(False)
            prof_cb.blockSignals(False)
    
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
        
        # Perícias (proficiente x expertise)
        for skill, cb in self.skill_prof_checkboxes.items():
            is_expert = skill in getattr(self.character, 'skill_expertise', [])
            is_prof = (skill in self.character.skill_proficiencies) and not is_expert
            cb.setChecked(is_prof)
        for skill, cb in self.skill_expert_checkboxes.items():
            cb.setChecked(skill in getattr(self.character, 'skill_expertise', []))

        # Pact Boon e Invocações
        if self.pact_boon_combo:
            index = self.pact_boon_combo.findData(self.character.pact_boon)
            self.pact_boon_combo.setCurrentIndex(index if index >= 0 else 0)

        if self.invocation_list_widget:
            known = set(self.character.eldritch_invocations)
            for row in range(self.invocation_list_widget.count()):
                item = self.invocation_list_widget.item(row)
                name = item.data(Qt.ItemDataRole.UserRole)
                item.setCheckState(
                    Qt.CheckState.Checked if name in known else Qt.CheckState.Unchecked
                )
    
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
        
        # Perícias (salva listas exclusivas)
        self.character.skill_proficiencies = [
            skill for skill, cb in self.skill_prof_checkboxes.items()
            if cb.isChecked()
        ]
        self.character.skill_expertise = [
            skill for skill, cb in self.skill_expert_checkboxes.items()
            if cb.isChecked()
        ]

        # Pact Boon e Invocações
        if self.pact_boon_combo:
            self.character.pact_boon = self.pact_boon_combo.currentData()

        if self.invocation_list_widget:
            self.character.eldritch_invocations = []
            for row in range(self.invocation_list_widget.count()):
                item = self.invocation_list_widget.item(row)
                if item.checkState() == Qt.CheckState.Checked:
                    name = item.data(Qt.ItemDataRole.UserRole)
                    if name:
                        self.character.eldritch_invocations.append(name)

        
        # Recalcula estatísticas derivadas (CA, iniciativa, velocidade, etc.)
        self.character.update_derived_stats()
        
        # Aplica valor manual de speed DEPOIS do recálculo (se o usuário alterou manualmente)
        # Iniciativa é calculada automaticamente baseada em DEX + feat Alert
        self.character.speed = self.speed_spin.value()
        
        # Emite sinal de atualização
        self.character_updated.emit()
        
        QMessageBox.information(self, "Sucesso", "Alterações salvas com sucesso!")
        self.accept()
