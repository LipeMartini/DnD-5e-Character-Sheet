from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QTextEdit, QComboBox,
                             QRadioButton, QButtonGroup, QGroupBox, QMessageBox,
                             QListWidgetItem)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from models.feats import get_available_feats, ABILITY_SCORE_IMPROVEMENT
from .magic_initiate_dialog import MagicInitiateDialog

class FeatDialog(QDialog):
    """Dialog para seleção de Feat (incluindo ASI)"""
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.selected_feat = None
        self.asi_choice = None  # Para ASI: {"type": "single", "stat": "strength"} ou {"type": "double", "stat1": "str", "stat2": "dex"}
        self.half_feat_choice = None  # Para feats que concedem +1 em atributo específico
        self.magic_initiate_choice = None
        
        self.setWindowTitle("Escolher Feat ou ASI")
        self.setModal(True)
        self.setMinimumSize(700, 500)
        
        self.setup_ui()
        self.load_feats()
    
    def setup_ui(self):
        """Configura a interface do dialog"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Escolha um Feat ou Ability Score Improvement")
        title.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        title.setStyleSheet("color: #8B4513; padding: 10px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Layout horizontal: lista de feats + detalhes
        content_layout = QHBoxLayout()
        
        # Lista de feats (esquerda)
        left_layout = QVBoxLayout()
        
        feats_label = QLabel("Feats Disponíveis:")
        feats_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        left_layout.addWidget(feats_label)
        
        self.feats_list = QListWidget()
        self.feats_list.setFont(QFont("Georgia", 10))
        self.feats_list.setStyleSheet("""
            QListWidget {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #D2B48C;
            }
            QListWidget::item:selected {
                background-color: #DEB887;
                color: #000000;
            }
        """)
        self.feats_list.currentItemChanged.connect(self.on_feat_selected)
        left_layout.addWidget(self.feats_list)
        
        content_layout.addLayout(left_layout, 1)
        
        # Painel de detalhes (direita)
        right_layout = QVBoxLayout()
        
        details_label = QLabel("Detalhes:")
        details_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        right_layout.addWidget(details_label)
        
        # Nome do feat
        self.feat_name_label = QLabel("")
        self.feat_name_label.setFont(QFont("Georgia", 12, QFont.Weight.Bold))
        self.feat_name_label.setStyleSheet("color: #8B4513; padding: 5px;")
        right_layout.addWidget(self.feat_name_label)
        
        # Descrição
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        self.description_text.setFont(QFont("Georgia", 9))
        self.description_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFF8DC;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        right_layout.addWidget(self.description_text)
        
        # Painel de escolha de ASI (inicialmente oculto)
        self.asi_panel = QGroupBox("Escolha de Atributos")
        self.asi_panel.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        self.asi_panel.setStyleSheet("""
            QGroupBox {
                border: 2px solid #8B4513;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #FFF8DC;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
        """)
        self.asi_panel.setVisible(False)
        
        asi_layout = QVBoxLayout()
        
        # Radio buttons para escolher tipo de ASI
        self.asi_type_group = QButtonGroup()
        
        self.single_stat_radio = QRadioButton("+2 em um atributo")
        self.single_stat_radio.setFont(QFont("Georgia", 9))
        self.single_stat_radio.setChecked(True)
        self.single_stat_radio.toggled.connect(self.on_asi_type_changed)
        self.asi_type_group.addButton(self.single_stat_radio)
        asi_layout.addWidget(self.single_stat_radio)
        
        # Dropdown para +2
        self.single_stat_combo = QComboBox()
        self.single_stat_combo.setFont(QFont("Georgia", 9))
        self.populate_stat_combo(self.single_stat_combo)
        asi_layout.addWidget(self.single_stat_combo)
        
        self.double_stat_radio = QRadioButton("+1 em dois atributos")
        self.double_stat_radio.setFont(QFont("Georgia", 9))
        self.double_stat_radio.toggled.connect(self.on_asi_type_changed)
        self.asi_type_group.addButton(self.double_stat_radio)
        asi_layout.addWidget(self.double_stat_radio)
        
        # Dropdowns para +1 +1
        double_layout = QHBoxLayout()
        self.double_stat1_combo = QComboBox()
        self.double_stat1_combo.setFont(QFont("Georgia", 9))
        self.populate_stat_combo(self.double_stat1_combo)
        self.double_stat1_combo.setEnabled(False)
        double_layout.addWidget(self.double_stat1_combo)
        
        double_layout.addWidget(QLabel("e"))
        
        self.double_stat2_combo = QComboBox()
        self.double_stat2_combo.setFont(QFont("Georgia", 9))
        self.populate_stat_combo(self.double_stat2_combo)
        self.double_stat2_combo.currentIndexChanged.connect(lambda: self.double_stat2_combo.setCurrentIndex(1) if self.double_stat2_combo.currentIndex() == 0 else None)
        self.double_stat2_combo.setEnabled(False)
        double_layout.addWidget(self.double_stat2_combo)
        
        asi_layout.addLayout(double_layout)
        
        self.asi_panel.setLayout(asi_layout)
        right_layout.addWidget(self.asi_panel)

        # Painel para Half Feats (um atributo específico)
        self.half_feat_panel = QGroupBox("Aumento de Atributo do Feat")
        self.half_feat_panel.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        self.half_feat_panel.setStyleSheet(self.asi_panel.styleSheet())
        self.half_feat_panel.setVisible(False)

        half_layout = QVBoxLayout()
        self.half_feat_label = QLabel("Selecione o atributo para receber +1")
        self.half_feat_label.setFont(QFont("Georgia", 9))
        half_layout.addWidget(self.half_feat_label)

        self.half_feat_combo = QComboBox()
        self.half_feat_combo.setFont(QFont("Georgia", 9))
        half_layout.addWidget(self.half_feat_combo)

        self.half_feat_panel.setLayout(half_layout)
        right_layout.addWidget(self.half_feat_panel)
        
        content_layout.addLayout(right_layout, 1)
        
        layout.addLayout(content_layout)
        
        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        
        self.select_button = QPushButton("Selecionar")
        self.select_button.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        self.select_button.setStyleSheet("""
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
            QPushButton:disabled {
                background-color: #999999;
            }
        """)
        self.select_button.clicked.connect(self.accept_selection)
        self.select_button.setEnabled(False)
        buttons_layout.addWidget(self.select_button)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.setFont(QFont("Georgia", 10))
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #666666;
                color: #FFFFFF;
                border: 2px solid #444444;
                border-radius: 5px;
                padding: 8px 20px;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #888888;
            }
        """)
        cancel_button.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_button)
        
        layout.addLayout(buttons_layout)
    
    def populate_stat_combo(self, combo):
        """Popula combo box com atributos"""
        stats = [
            ("Força (Strength)", "strength"),
            ("Destreza (Dexterity)", "dexterity"),
            ("Constituição (Constitution)", "constitution"),
            ("Inteligência (Intelligence)", "intelligence"),
            ("Sabedoria (Wisdom)", "wisdom"),
            ("Carisma (Charisma)", "charisma")
        ]
        
        for display_name, stat_name in stats:
            current_value = getattr(self.character.stats, stat_name)
            combo.addItem(f"{display_name} ({current_value})", stat_name)
    
    def load_feats(self):
        """Carrega lista de feats disponíveis"""
        available_feats = get_available_feats(self.character, include_asi=True)
        
        for feat in available_feats:
            item = QListWidgetItem(feat.name)
            item.setData(Qt.ItemDataRole.UserRole, feat)
            
            # ASI em destaque
            if feat.is_asi:
                item.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
            
            self.feats_list.addItem(item)
        
        # Seleciona ASI por padrão
        if self.feats_list.count() > 0:
            self.feats_list.setCurrentRow(0)
    
    def on_feat_selected(self, current, previous):
        """Callback quando um feat é selecionado"""
        if not current:
            self.select_button.setEnabled(False)
            return
        
        feat = current.data(Qt.ItemDataRole.UserRole)
        
        # Atualiza detalhes
        self.feat_name_label.setText(feat.name)
        
        description_html = f"""
        <p style="margin-bottom: 10px;"><b>Descrição:</b><br>{feat.description}</p>
        <p><b>Efeito Mecânico:</b><br>{feat.mechanical_effect.replace(chr(10), '<br>')}</p>
        """
        
        if feat.prerequisites:
            prereq_text = ", ".join([f"{k} {v}+" for k, v in feat.prerequisites.items()])
            description_html += f"<p style='color: #8B4513;'><b>Pré-requisitos:</b> {prereq_text}</p>"
        
        self.description_text.setHtml(description_html)
        
        # Mostra/oculta painel de ASI
        self.asi_panel.setVisible(feat.is_asi)

        # Configura painel de half feat quando aplicável
        if not feat.is_asi and feat.ability_increase_options:
            self.half_feat_panel.setVisible(True)
            self.populate_half_feat_combo(feat)
        else:
            self.half_feat_panel.setVisible(False)
        
        self.select_button.setEnabled(True)
    
    def on_asi_type_changed(self):
        """Callback quando tipo de ASI muda"""
        is_single = self.single_stat_radio.isChecked()
        
        self.single_stat_combo.setEnabled(is_single)
        self.double_stat1_combo.setEnabled(not is_single)
        self.double_stat2_combo.setEnabled(not is_single)
    
    def accept_selection(self):
        """Aceita a seleção e valida"""
        current_item = self.feats_list.currentItem()
        if not current_item:
            return
        
        feat = current_item.data(Qt.ItemDataRole.UserRole)
        
        # Se for ASI, valida escolha de atributos
        if feat.is_asi:
            if self.single_stat_radio.isChecked():
                stat_name = self.single_stat_combo.currentData()
                current_value = getattr(self.character.stats, stat_name)
                
                if current_value >= 20:
                    QMessageBox.warning(
                        self,
                        "Limite de Atributo",
                        f"O atributo já está no máximo (20). Escolha outro atributo."
                    )
                    return
                
                if current_value == 19:
                    reply = QMessageBox.question(
                        self,
                        "Confirmar",
                        f"O atributo está em 19. Aumentar em +2 resultará em apenas +1 (máximo 20). Continuar?",
                        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                    )
                    if reply == QMessageBox.StandardButton.No:
                        return
                
                self.asi_choice = {
                    "type": "single",
                    "stat": stat_name
                }
            else:
                stat1_name = self.double_stat1_combo.currentData()
                stat2_name = self.double_stat2_combo.currentData()
                
                if stat1_name == stat2_name:
                    QMessageBox.warning(
                        self,
                        "Atributos Iguais",
                        "Você deve escolher dois atributos diferentes."
                    )
                    return
                
                current_value1 = getattr(self.character.stats, stat1_name)
                current_value2 = getattr(self.character.stats, stat2_name)
                
                if current_value1 >= 20 or current_value2 >= 20:
                    QMessageBox.warning(
                        self,
                        "Limite de Atributo",
                        "Um dos atributos já está no máximo (20). Escolha outros atributos."
                    )
                    return
                
                self.asi_choice = {
                    "type": "double",
                    "stat1": stat1_name,
                    "stat2": stat2_name
                }
            self.half_feat_choice = None
        else:
            self.asi_choice = None
            if feat.ability_increase_options:
                stat_choice = self.half_feat_combo.currentData()
                if stat_choice is None:
                    QMessageBox.warning(
                        self,
                        "Seleção obrigatória",
                        "Escolha um atributo para receber o bônus de +1 do feat."
                    )
                    return
                current_value = getattr(self.character.stats, stat_choice, 0)
                if current_value >= 20:
                    QMessageBox.warning(
                        self,
                        "Limite de Atributo",
                        "O atributo selecionado já está no máximo (20). Escolha outro atributo."
                    )
                    return
                self.half_feat_choice = stat_choice
            else:
                self.half_feat_choice = None

            if feat.name == "Magic Initiate":
                magic_dialog = MagicInitiateDialog(self)
                if magic_dialog.exec():
                    self.magic_initiate_choice = magic_dialog.get_selection()
                else:
                    QMessageBox.warning(
                        self,
                        "Seleção obrigatória",
                        "É necessário escolher a classe e magias para Magic Initiate."
                    )
                    return
            else:
                self.magic_initiate_choice = None
        
        self.selected_feat = feat
        self.accept()
    
    def get_selected_feat(self):
        """Retorna o feat selecionado"""
        return self.selected_feat
    
    def get_asi_choice(self):
        """Retorna a escolha de ASI (se aplicável)"""
        return self.asi_choice

    def get_half_feat_ability(self):
        """Retorna o atributo escolhido para feats que concedem +1"""
        return self.half_feat_choice

    def get_magic_initiate_choice(self):
        """Retorna a seleção de magias para Magic Initiate (se aplicável)."""
        return self.magic_initiate_choice

    def populate_half_feat_combo(self, feat):
        """Popula combo de half feat com atributos elegíveis"""
        self.half_feat_combo.clear()
        options = feat.ability_increase_options or []
        for stat in options:
            display = {
                "strength": "Força (Strength)",
                "dexterity": "Destreza (Dexterity)",
                "constitution": "Constituição (Constitution)",
                "intelligence": "Inteligência (Intelligence)",
                "wisdom": "Sabedoria (Wisdom)",
                "charisma": "Carisma (Charisma)",
            }.get(stat, stat.capitalize())
            current = getattr(self.character.stats, stat, 0)
            self.half_feat_combo.addItem(f"{display} ({current})", stat)
