from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, 
                             QPushButton, QTabWidget, QLabel, QWidget)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

class NotesWindow(QDialog):
    """Janela flutuante para anotações do personagem"""
    
    notes_updated = pyqtSignal()
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.note_fields = {}
        
        # Configurar janela
        self.setWindowTitle(f"Anotações - {character.name}")
        self.setModal(False)  # Não-modal para permitir interação com ficha
        self.resize(600, 500)
        
        # Permitir que a janela fique sempre no topo (opcional)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        
        self.init_ui()
        self.load_notes()
    
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel(f"📝 Anotações de {self.character.name}")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #8B4513; padding: 10px;")
        layout.addWidget(title)
        
        # Tabs para diferentes categorias de notas
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #8B4513;
                border-radius: 5px;
                background-color: #FFF8DC;
            }
            QTabBar::tab {
                background-color: #D2B48C;
                color: #654321;
                padding: 8px 15px;
                margin-right: 2px;
                border: 2px solid #8B4513;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #FFF8DC;
                color: #8B4513;
            }
            QTabBar::tab:hover {
                background-color: #DEB887;
            }
        """)
        
        # Criar abas de notas
        self.create_note_tab("Geral", "📋", "Anotações gerais sobre o personagem")
        self.create_note_tab("Combate", "⚔️", "Estratégias, táticas e lembretes de combate")
        self.create_note_tab("Roleplay", "🎭", "Personalidade, objetivos, relacionamentos")
        self.create_note_tab("História", "📖", "Backstory, eventos importantes, missões")
        self.create_note_tab("Itens", "🎒", "Itens especiais, desejos, equipamentos futuros")
        self.create_note_tab("Sessão", "🗓️", "Notas da sessão atual, lembretes rápidos")
        
        layout.addWidget(self.tabs)
        
        # Informação útil
        info = QLabel("💡 Dica: Esta janela pode ficar aberta enquanto você joga!")
        info.setStyleSheet("color: #666; font-style: italic; padding: 5px;")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)
        
        # Botões
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
        save_btn.clicked.connect(self.save_notes)
        buttons_layout.addWidget(save_btn)
        
        close_btn = QPushButton("Fechar")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #696969;
                color: white;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #808080;
            }
        """)
        close_btn.clicked.connect(self.close)
        buttons_layout.addWidget(close_btn)
        
        layout.addLayout(buttons_layout)
    
    def create_note_tab(self, name: str, icon: str, placeholder: str):
        """Cria uma aba de notas"""
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)
        
        # Campo de texto
        text_edit = QTextEdit()
        text_edit.setPlaceholderText(placeholder)
        text_edit.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 10px;
                font-family: 'Segoe UI', Arial;
                font-size: 11pt;
                line-height: 1.5;
            }
        """)
        
        # Armazenar referência ao campo
        self.note_fields[name] = text_edit
        
        tab_layout.addWidget(text_edit)
        
        # Adicionar aba
        self.tabs.addTab(tab, f"{icon} {name}")
    
    def load_notes(self):
        """Carrega notas salvas do personagem"""
        if not hasattr(self.character, 'notes') or not self.character.notes:
            return
        
        for category, text in self.character.notes.items():
            if category in self.note_fields:
                self.note_fields[category].setPlainText(text)
    
    def save_notes(self):
        """Salva notas no personagem"""
        # Inicializar dicionário de notas se não existir
        if not hasattr(self.character, 'notes'):
            self.character.notes = {}
        
        # Salvar texto de cada aba
        for category, text_edit in self.note_fields.items():
            self.character.notes[category] = text_edit.toPlainText()
        
        self.notes_updated.emit()
        
        # Feedback visual
        from PyQt6.QtWidgets import QMessageBox
        QMessageBox.information(
            self,
            "Notas Salvas",
            "Suas anotações foram salvas com sucesso!"
        )
    
    def closeEvent(self, event):
        """Salva automaticamente ao fechar"""
        self.save_notes()
        event.accept()
