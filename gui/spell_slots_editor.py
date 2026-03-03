from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QSpinBox, QGroupBox, QFormLayout,
                             QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class SpellSlotsEditor(QDialog):
    """Dialog para editar spell slots manualmente"""
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.slot_spinboxes = {}
        
        self.setWindowTitle("Editar Spell Slots")
        self.setModal(True)
        self.resize(400, 500)
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("Editar Spell Slots")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(
            "Ajuste manualmente seus spell slots disponíveis.\n"
            "Útil para Natural Recovery, itens mágicos, ou correções."
        )
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #666; padding: 5px;")
        layout.addWidget(desc)
        
        # Verifica se é conjurador
        if not self.character.is_spellcaster():
            no_spells = QLabel("Este personagem não é um conjurador.")
            no_spells.setStyleSheet("color: #999; font-style: italic; padding: 20px;")
            no_spells.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(no_spells)
            
            close_btn = QPushButton("Fechar")
            close_btn.clicked.connect(self.reject)
            layout.addWidget(close_btn)
            return
        
        # Grupo de spell slots
        slots_group = QGroupBox("Spell Slots Disponíveis")
        slots_layout = QFormLayout()
        
        # Cria spinboxes para cada nível de spell slot
        for level in range(1, 10):
            max_slots = self.character.spellcasting.get_max_slots(level)
            
            if max_slots > 0:
                current_slots = self.character.spellcasting.get_available_slots(level)
                
                # Layout horizontal para cada nível
                slot_layout = QHBoxLayout()
                
                # SpinBox para slots disponíveis
                spinbox = QSpinBox()
                spinbox.setMinimum(0)
                spinbox.setMaximum(max_slots)
                spinbox.setValue(current_slots)
                spinbox.setStyleSheet("""
                    QSpinBox {
                        background-color: #FFF8DC;
                        border: 2px solid #8B4513;
                        border-radius: 4px;
                        padding: 5px;
                        min-width: 60px;
                    }
                """)
                
                self.slot_spinboxes[level] = spinbox
                slot_layout.addWidget(spinbox)
                
                # Label mostrando máximo
                max_label = QLabel(f"/ {max_slots}")
                max_label.setStyleSheet("color: #666; font-weight: bold;")
                slot_layout.addWidget(max_label)
                
                slot_layout.addStretch()
                
                # Botões rápidos
                restore_btn = QPushButton("Restaurar")
                restore_btn.setToolTip(f"Restaurar para {max_slots} slots")
                restore_btn.clicked.connect(lambda checked, lv=level, mx=max_slots: self.slot_spinboxes[lv].setValue(mx))
                restore_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 3px 8px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                """)
                slot_layout.addWidget(restore_btn)
                
                deplete_btn = QPushButton("Esgotar")
                deplete_btn.setToolTip("Esgotar todos os slots")
                deplete_btn.clicked.connect(lambda checked, lv=level: self.slot_spinboxes[lv].setValue(0))
                deplete_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #f44336;
                        color: white;
                        border: none;
                        border-radius: 3px;
                        padding: 3px 8px;
                        font-size: 10px;
                    }
                    QPushButton:hover {
                        background-color: #da190b;
                    }
                """)
                slot_layout.addWidget(deplete_btn)
                
                # Adiciona ao form
                slots_layout.addRow(f"Nível {level}:", slot_layout)
        
        slots_group.setLayout(slots_layout)
        layout.addWidget(slots_group)
        
        # Botões de ação rápida
        quick_actions_layout = QHBoxLayout()
        
        restore_all_btn = QPushButton("🔄 Restaurar Todos")
        restore_all_btn.setToolTip("Restaurar todos os spell slots para o máximo")
        restore_all_btn.clicked.connect(self.restore_all_slots)
        restore_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: 2px solid #1976D2;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1976D2;
            }
        """)
        quick_actions_layout.addWidget(restore_all_btn)
        
        layout.addLayout(quick_actions_layout)
        
        layout.addStretch()
        
        # Botões principais
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Salvar")
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_changes)
        buttons_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #696969;
                color: white;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
        """)
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
    
    def restore_all_slots(self):
        """Restaura todos os spell slots para o máximo"""
        for level, spinbox in self.slot_spinboxes.items():
            max_slots = self.character.spellcasting.get_max_slots(level)
            spinbox.setValue(max_slots)
    
    def save_changes(self):
        """Salva as mudanças nos spell slots"""
        # Atualiza os spell slots do personagem
        for level, spinbox in self.slot_spinboxes.items():
            new_value = spinbox.value()
            # Atualiza diretamente os current_spell_slots
            self.character.spellcasting.current_spell_slots[level] = new_value
        
        self.accept()
