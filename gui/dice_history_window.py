from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QLabel, QLineEdit)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor
from datetime import datetime
import random
import re

class DiceHistoryWindow(QWidget):
    """Janela de histórico de rolagens com tema medieval"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rolagens")
        self.resize(500, 600)
        self.init_ui()
        self.apply_theme()
    
    def apply_theme(self):
        """Aplica tema medieval/pergaminho"""
        self.setStyleSheet("""
            QWidget {
                background-color: #F5EBDC;
                color: #281E14;
                font-family: 'Georgia', 'Times New Roman', serif;
            }
            
            QTextEdit {
                background-color: #FFF8DC;
                border: 3px solid #8B4513;
                border-radius: 8px;
                padding: 10px;
                font-size: 12px;
                color: #281E14;
            }
            
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                font-size: 11px;
                min-width: 100px;
                min-height: 30px;
            }
            
            QPushButton:hover {
                background-color: #A0522D;
                border-color: #8B4513;
            }
            
            QPushButton:pressed {
                background-color: #654321;
            }
            
            QLabel {
                background-color: transparent;
                font-size: 14px;
                font-weight: bold;
                color: #8B4513;
            }
        """)
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Título
        title = QLabel("🎲 ROLAGENS")
        title.setFont(QFont("Georgia", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("""
            background-color: #8B4513;
            color: #F5EBDC;
            padding: 10px;
            border-radius: 8px;
        """)
        layout.addWidget(title)
        
        # Área de histórico
        self.history_text = QTextEdit()
        self.history_text.setReadOnly(True)
        self.history_text.setFont(QFont("Georgia", 11))
        layout.addWidget(self.history_text)
        
        # Campo de rolagem manual (estilo chat)
        roll_input_layout = QHBoxLayout()
        roll_input_layout.setSpacing(5)
        
        self.manual_dice_input = QLineEdit()
        self.manual_dice_input.setPlaceholderText("Digite sua rolagem (ex: 1d8, 2d6+3, 4d6-2)...")
        self.manual_dice_input.setStyleSheet("""
            QLineEdit {
                background-color: white;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 8px;
                font-size: 12px;
            }
            QLineEdit:focus {
                border-color: #A0522D;
            }
        """)
        self.manual_dice_input.returnPressed.connect(self.roll_manual_dice)
        roll_input_layout.addWidget(self.manual_dice_input)
        
        roll_btn = QPushButton("🎲 Rolar")
        roll_btn.setFixedWidth(100)
        roll_btn.clicked.connect(self.roll_manual_dice)
        roll_input_layout.addWidget(roll_btn)
        
        layout.addLayout(roll_input_layout)
        
        # Botões
        button_layout = QHBoxLayout()
        
        clear_btn = QPushButton("Limpar")
        clear_btn.clicked.connect(self.clear_history)
        button_layout.addWidget(clear_btn)
        
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.hide)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        # Mensagem inicial
        self.add_entry("Histórico de rolagens iniciado.", "INFO")
    
    def add_entry(self, message: str, roll_type: str = "ROLL"):
        """Adiciona uma entrada ao histórico
        
        Args:
            message: Mensagem da rolagem
            roll_type: Tipo (ROLL, INFO, SKILL, SAVE, ATTACK, etc.)
        """
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Cores por tipo
        colors = {
            "INFO": "#666666",
            "ROLL": "#8B4513",
            "SKILL": "#2E7D32",
            "SAVE": "#1565C0",
            "ATTACK": "#C62828",
            "DAMAGE": "#D84315",
            "INITIATIVE": "#6A1B9A",
            "ABILITY": "#00838F",
        }
        
        color = colors.get(roll_type, "#8B4513")
        
        # Formatar entrada
        html = f"""
        <div style="margin-bottom: 10px; padding: 8px; background-color: #FFFAF0; border-left: 4px solid {color}; border-radius: 4px;">
            <span style="color: #999; font-size: 10px;">[{timestamp}]</span>
            <span style="color: {color}; font-weight: bold;"> {roll_type}:</span>
            <span style="color: #281E14;"> {message}</span>
        </div>
        <br>
        """
        
        # Adicionar ao histórico
        cursor = self.history_text.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.history_text.setTextCursor(cursor)
        self.history_text.insertHtml(html)
        
        # Auto-scroll para o final
        scrollbar = self.history_text.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def add_roll(self, roll_name: str, roll_value: int, modifier: int, total: int, roll_type: str = "ROLL"):
        """Adiciona uma rolagem formatada ao histórico"""
        mod_sign = '+' if modifier >= 0 else ''
        
        # Colorir o valor do dado se for crítico (20) ou falha crítica (1)
        if roll_value == 20:
            dice_display = f'<span style="color: #2E7D32; font-weight: bold;">{roll_value}</span>'
        elif roll_value == 1:
            dice_display = f'<span style="color: #C62828; font-weight: bold;">{roll_value}</span>'
        else:
            dice_display = str(roll_value)
        
        message = f"<b>{roll_name}</b>: 🎲 {dice_display} {mod_sign}{modifier} = <b>{total}</b>"
        self.add_entry(message, roll_type)
    
    def add_custom_roll(self, roll_name: str, formatted_result: str):
        """Adiciona uma rolagem customizada (manual) ao histórico"""
        self.add_entry(f"<b>{formatted_result}</b>", "MANUAL")
    
    def roll_manual_dice(self):
        """Rola dados manualmente a partir de uma expressão (ex: 1d8, 2d6+3)"""
        from PyQt6.QtWidgets import QMessageBox
        
        expression = self.manual_dice_input.text().strip()
        if not expression:
            return
        
        try:
            # Parse da expressão (ex: 2d6+3, 1d8, 4d6-2)
            pattern = r'(\d+)d(\d+)([\+\-]\d+)?'
            match = re.match(pattern, expression.lower().replace(' ', ''))
            
            if not match:
                QMessageBox.warning(
                    self,
                    "Formato Inválido",
                    f"Formato inválido: '{expression}'\n\n"
                    f"Use formatos como:\n"
                    f"• 1d8\n"
                    f"• 2d6+3\n"
                    f"• 4d6-2"
                )
                return
            
            num_dice = int(match.group(1))
            die_size = int(match.group(2))
            modifier = int(match.group(3)) if match.group(3) else 0
            
            # Validação
            if num_dice > 100 or num_dice < 1:
                QMessageBox.warning(self, "Erro", "Número de dados deve ser entre 1 e 100")
                return
            
            if die_size not in [2, 4, 6, 8, 10, 12, 20, 100]:
                QMessageBox.warning(self, "Erro", f"Tamanho de dado inválido: d{die_size}\n\nUse: d4, d6, d8, d10, d12, d20, d100")
                return
            
            # Rolar dados
            rolls = [random.randint(1, die_size) for _ in range(num_dice)]
            total = sum(rolls) + modifier
            
            # Formatar resultado
            rolls_str = " + ".join(str(r) for r in rolls)
            
            if modifier > 0:
                result = f"Manual - {expression}: 🎲 ({rolls_str}) + {modifier} = <b>{total}</b>"
            elif modifier < 0:
                result = f"Manual - {expression}: 🎲 ({rolls_str}) - {abs(modifier)} = <b>{total}</b>"
            else:
                result = f"Manual - {expression}: 🎲 ({rolls_str}) = <b>{total}</b>"
            
            # Adicionar ao histórico
            self.add_entry(result, "MANUAL")
            
            # Limpar campo
            self.manual_dice_input.clear()
            self.manual_dice_input.setFocus()
            
        except Exception as e:
            QMessageBox.warning(
                self,
                "Erro",
                f"Erro ao processar rolagem: {str(e)}\n\n"
                f"Use formatos como: 1d8, 2d6+3, 4d6-2"
            )
    
    def clear_history(self):
        """Limpa o histórico"""
        self.history_text.clear()
        self.add_entry("Histórico limpo.", "INFO")
    
    def show_and_raise(self):
        """Mostra a janela e traz para frente"""
        self.show()
        self.raise_()
        self.activateWindow()
