from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QSpinBox, QPushButton, 
                             QGroupBox, QLabel, QListWidget, QMessageBox, QScrollArea, QWidget)
from PyQt6.QtCore import Qt
from models import Character, RaceDatabase, SubraceDatabase, ClassDatabase, BackgroundDatabase, DiceRoller
from models.expertise_rules import get_expertise_choices_for_level
from .expertise_selection_dialog import ExpertiseSelectionDialog

class CharacterCreationDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.character = Character()
        self.setWindowTitle("Criar Novo Personagem")
        self.setModal(True)
        self.resize(900, 700)
        self.init_ui()
    
    def init_ui(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll.setWidget(scroll_widget)
        
        main_layout = QVBoxLayout(self)
        main_layout.addWidget(scroll)
        
        layout = QVBoxLayout(scroll_widget)
        
        # Informações Básicas
        basic_group = QGroupBox("Informações Básicas")
        basic_layout = QFormLayout()
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Digite o nome do personagem")
        basic_layout.addRow("Nome:", self.name_input)
        
        self.race_combo = QComboBox()
        self.race_combo.addItem("Escolha uma Raça")  # Placeholder
        races = list(RaceDatabase.get_all_races().keys())
        self.race_combo.addItems(races)
        self.race_combo.currentTextChanged.connect(self.on_race_changed)
        basic_layout.addRow("Raça:", self.race_combo)
        
        self.subrace_combo = QComboBox()
        self.subrace_combo.currentTextChanged.connect(self.on_subrace_changed)
        basic_layout.addRow("Subraça:", self.subrace_combo)
        
        self.class_combo = QComboBox()
        self.class_combo.addItem("Escolha uma Classe")  # Placeholder
        classes = list(ClassDatabase.get_all_classes().keys())
        self.class_combo.addItems(classes)
        self.class_combo.currentTextChanged.connect(self.on_class_changed)
        basic_layout.addRow("Classe:", self.class_combo)

        self.background_combo = QComboBox()
        self.background_combo.addItem("Escolha um Antecedente")  # Placeholder
        backgrounds = list(BackgroundDatabase.get_all_backgrounds().keys())
        self.background_combo.addItems(backgrounds)
        self.background_combo.currentTextChanged.connect(self.on_background_changed)
        basic_layout.addRow("Antecedente:", self.background_combo)
        
        self.alignment_combo = QComboBox()
        alignments = ["Lawful Good", "Neutral Good", "Chaotic Good",
                     "Lawful Neutral", "Neutral", "Chaotic Neutral",
                     "Lawful Evil", "Neutral Evil", "Chaotic Evil"]
        self.alignment_combo.addItems(alignments)
        basic_layout.addRow("Alinhamento:", self.alignment_combo)
        
        basic_group.setLayout(basic_layout)
        layout.addWidget(basic_group)
        
        # Atributos
        stats_group = QGroupBox("Atributos")
        stats_layout = QVBoxLayout()
        
        roll_buttons = QHBoxLayout()
        roll_all_btn = QPushButton("Rolar Todos os Atributos")
        roll_all_btn.clicked.connect(self.roll_all_stats)
        roll_buttons.addWidget(roll_all_btn)
        stats_layout.addLayout(roll_buttons)
        
        stats_grid = QFormLayout()
        self.stat_inputs = {}
        
        stat_names = {
            'strength': 'Força',
            'dexterity': 'Destreza',
            'constitution': 'Constituição',
            'intelligence': 'Inteligência',
            'wisdom': 'Sabedoria',
            'charisma': 'Carisma'
        }
        
        for stat_name, pt_name in stat_names.items():
            stat_widget = QWidget()
            stat_layout = QHBoxLayout(stat_widget)
            stat_layout.setContentsMargins(0, 0, 0, 0)
            
            spin = QSpinBox()
            spin.setMinimum(1)
            spin.setMaximum(20)
            spin.setValue(10)
            spin.valueChanged.connect(self.update_stats_display)
            stat_layout.addWidget(spin)
            
            modifier_label = QLabel("(+0)")
            modifier_label.setMinimumWidth(50)
            stat_layout.addWidget(modifier_label)
            
            roll_btn = QPushButton("Rolar")
            roll_btn.clicked.connect(lambda checked, s=stat_name: self.roll_single_stat(s))
            stat_layout.addWidget(roll_btn)
            
            stat_layout.addStretch()
            
            stats_grid.addRow(f"{pt_name}:", stat_widget)
            
            self.stat_inputs[stat_name] = {
                'spin': spin,
                'modifier': modifier_label
            }
        
        stats_layout.addLayout(stats_grid)
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
        
        # Perícias
        skills_group = QGroupBox("Proficiências em Perícias")
        skills_layout = QVBoxLayout()
        
        self.available_skills_label = QLabel("Selecione suas perícias:")
        skills_layout.addWidget(self.available_skills_label)
        
        self.skills_list = QListWidget()
        self.skills_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        skills_layout.addWidget(self.skills_list)
        
        self.subrace_skills_label = QLabel("Perícias da Subraça:")
        self.subrace_skills_label.setVisible(False)
        skills_layout.addWidget(self.subrace_skills_label)
        
        self.subrace_skills_list = QListWidget()
        self.subrace_skills_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.subrace_skills_list.setVisible(False)
        skills_layout.addWidget(self.subrace_skills_list)

        self.background_skills_info = QLabel("Perícias do Antecedente: Nenhum")
        self.background_skills_info.setStyleSheet("font-weight: bold; color: #2E7D32; padding: 5px;")
        self.background_skills_info.setWordWrap(True)
        skills_layout.addWidget(self.background_skills_info)
        
        skills_group.setLayout(skills_layout)
        layout.addWidget(skills_group)
        
        # Botões de ação
        button_layout = QHBoxLayout()
        
        create_btn = QPushButton("Criar Personagem")
        create_btn.clicked.connect(self.create_character)
        create_btn.setStyleSheet("font-weight: bold; padding: 10px;")
        button_layout.addWidget(create_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def roll_single_stat(self, stat_name: str):
        total, rolls = DiceRoller.roll_ability_score()
        self.stat_inputs[stat_name]['spin'].setValue(total)
        setattr(self.character.base_stats, stat_name, total)
        self.character.recalculate_stats()
        self.update_stats_display()
        QMessageBox.information(
            self, 
            "Rolagem de Atributo",
            f"Rolou 4d6 (manteve os 3 maiores)\nResultados: {rolls}\nTotal: {total}"
        )

    def handle_initial_expertise(self):
        """Permite escolher Expertise disponível já no nível inicial."""
        if not self.character.character_class:
            return
        class_name = self.character.character_class.name
        level = self.character.level
        num_choices = get_expertise_choices_for_level(class_name, level)
        if num_choices <= 0:
            return
        eligible_skills = sorted([
            skill for skill in self.character.skill_proficiencies
            if skill not in self.character.skill_expertise
        ])
        if not eligible_skills:
            return
        dialog = ExpertiseSelectionDialog(
            self.character,
            num_choices,
            eligible_skills,
            parent=self,
            title="Selecionar perícias com Expertise",
        )
        if dialog.exec():
            for skill in dialog.get_selected_skills():
                if skill not in self.character.skill_expertise:
                    self.character.skill_expertise.append(skill)
    
    def roll_all_stats(self):
        results = []
        for stat_name in ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']:
            total, rolls = DiceRoller.roll_ability_score()
            self.stat_inputs[stat_name]['spin'].setValue(total)
            setattr(self.character.base_stats, stat_name, total)
            results.append(f"{stat_name.capitalize()}: {total} (rolagens: {rolls})")
        
        self.character.recalculate_stats()
        self.update_stats_display()
        
        QMessageBox.information(
            self,
            "Rolagem de Atributos",
            "Todos os atributos foram rolados!\n\n" + "\n".join(results)
        )
    
    def on_race_changed(self, race_name: str):
        # Ignora placeholder
        if race_name and race_name != "Escolha uma Raça":
            self.character.set_race(race_name)
            self.character.set_subrace('None')
            self.subrace_combo.clear()
            subraces = SubraceDatabase.get_subraces_for_race(race_name)
            if subraces:
                self.subrace_combo.addItems(list(subraces.keys()))
            self.update_stats_display()
    
    def on_subrace_changed(self, subrace_name: str):
        if subrace_name:
            self.character.set_subrace(subrace_name)
            self.update_stats_display()
            self.update_skills_list()
    
    def on_class_changed(self, class_name: str):
        # Ignora placeholder
        if class_name and class_name != "Escolha uma Classe":
            self.character.set_class(class_name)
            self.update_skills_list()
    
    def on_background_changed(self, background_name: str):
        # Ignora placeholder
        if background_name and background_name != "Escolha um Antecedente":
            self.character.set_background(background_name)
            self.update_skills_list()
    
    def update_skills_list(self):
        self.skills_list.clear()
        if self.character.character_class:
            available_skills = self.character.character_class.available_skills
            self.skills_list.addItems(available_skills)
            
            max_skills = self.character.character_class.skill_proficiencies_count
            self.available_skills_label.setText(
                f"Selecione {max_skills} perícias da classe:"
            )
        
        self.subrace_skills_list.clear()
        if self.character.subrace and self.character.subrace.skill_proficiencies_count > 0:
            self.subrace_skills_label.setVisible(True)
            self.subrace_skills_list.setVisible(True)
            
            all_skills = [
                'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception',
                'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine',
                'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion',
                'Sleight of Hand', 'Stealth', 'Survival'
            ]
            self.subrace_skills_list.addItems(all_skills)
            
            subrace_max = self.character.subrace.skill_proficiencies_count
            self.subrace_skills_label.setText(
                f"Selecione {subrace_max} perícias da subraça ({self.character.subrace.name}):"
            )
        else:
            self.subrace_skills_label.setVisible(False)
            self.subrace_skills_list.setVisible(False)
        
        if self.character.background:
            bg_skills = ", ".join(self.character.background.skill_proficiencies)
            self.background_skills_info.setText(
                f"✓ Perícias do Antecedente ({self.character.background.name}): {bg_skills}"
            )
        else:
            self.background_skills_info.setText("Perícias do Antecedente: Nenhum")
    
    def update_stats_display(self):
        for stat_name, widgets in self.stat_inputs.items():
            value = widgets['spin'].value()
            modifier = (value - 10) // 2
            sign = '+' if modifier >= 0 else ''
            widgets['modifier'].setText(f"({sign}{modifier})")
    
    def create_character(self):
        # Validações
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Aviso", "Por favor, digite um nome para o personagem.")
            return
        
        if not self.race_combo.currentText():
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma raça.")
            return
        
        # Validar que raça, classe e antecedente válidos foram selecionados
        if self.race_combo.currentText() == "Escolha uma Raça":
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma raça.")
            return
        
        if self.class_combo.currentText() == "Escolha uma Classe":
            QMessageBox.warning(self, "Aviso", "Por favor, selecione uma classe.")
            return
        
        if self.background_combo.currentText() == "Escolha um Antecedente":
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um antecedente.")
            return
        
        # Atualizar personagem com dados finais
        self.character.name = self.name_input.text()
        self.character.alignment = self.alignment_combo.currentText()
        
        for stat_name, widgets in self.stat_inputs.items():
            value = widgets['spin'].value()
            setattr(self.character.base_stats, stat_name, value)
        
        self.character.recalculate_stats()
        self.character.recalculate_max_hp()  # Calcula HP com o modificador de CON correto
        
        # Validar perícias da classe
        selected_class_skills = [item.text() for item in self.skills_list.selectedItems()]
        if self.character.character_class:
            max_skills = self.character.character_class.skill_proficiencies_count
            if len(selected_class_skills) != max_skills:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"Você deve selecionar exatamente {max_skills} perícias da classe."
                )
                return
        
        # Validar perícias da subraça
        selected_subrace_skills = [item.text() for item in self.subrace_skills_list.selectedItems()]
        if self.character.subrace and self.character.subrace.skill_proficiencies_count > 0:
            max_subrace_skills = self.character.subrace.skill_proficiencies_count
            if len(selected_subrace_skills) != max_subrace_skills:
                QMessageBox.warning(
                    self,
                    "Aviso",
                    f"Você deve selecionar exatamente {max_subrace_skills} perícias da subraça."
                )
                return
        
        # Adicionar perícias do background
        background_skills = []
        if self.character.background:
            background_skills = self.character.background.skill_proficiencies.copy()
        
        # Combinar todas as perícias
        self.character.skill_proficiencies = selected_class_skills + selected_subrace_skills + background_skills
        
        # Adicionar class features do nível 1
        if self.character.character_class:
            self.character.add_class_features(
                self.character.character_class.name,
                1
            )

        # Expertise inicial (ex: Rogue nível 1)
        self.handle_initial_expertise()
        
        self.character.update_derived_stats()
        
        # Sucesso!
        self.accept()
    
    def get_character(self):
        """Retorna o personagem criado"""
        return self.character
