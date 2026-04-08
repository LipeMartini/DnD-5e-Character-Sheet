"""
Dialog para seleção de Fighting Style
"""

from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QListWidget, QTextEdit, QListWidgetItem)
from PyQt6.QtCore import Qt
from models.fighting_styles import get_available_fighting_styles, FightingStyle


class FightingStyleDialog(QDialog):
    """Dialog para escolher um Fighting Style"""
    
    def __init__(self, class_name: str, parent=None):
        super().__init__(parent)
        self.class_name = class_name
        self.selected_style = None
        self.available_styles = get_available_fighting_styles(class_name)
        
        self.setWindowTitle("Escolher Fighting Style")
        self.setModal(True)
        self.resize(600, 500)
        
        self.init_ui()
    
    def init_ui(self):
        """Inicializa a interface"""
        layout = QVBoxLayout()
        
        # Título
        title = QLabel(f"<h2>Escolha seu Fighting Style</h2>")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Descrição
        desc = QLabel(f"Como {self.class_name}, você pode escolher um estilo de luta que define sua especialização em combate.")
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        # Container horizontal para lista e detalhes
        content_layout = QHBoxLayout()
        
        # Lista de estilos disponíveis
        list_container = QVBoxLayout()
        list_label = QLabel("<b>Estilos Disponíveis:</b>")
        list_container.addWidget(list_label)
        
        self.style_list = QListWidget()
        self.style_list.currentItemChanged.connect(self.on_style_selected)
        
        for style in self.available_styles:
            item = QListWidgetItem(style.name)
            item.setData(Qt.ItemDataRole.UserRole, style)
            self.style_list.addItem(item)
        
        list_container.addWidget(self.style_list)
        content_layout.addLayout(list_container, 1)
        
        # Painel de detalhes
        details_container = QVBoxLayout()
        details_label = QLabel("<b>Detalhes:</b>")
        details_container.addWidget(details_label)
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setPlaceholderText("Selecione um estilo para ver os detalhes...")
        details_container.addWidget(self.details_text)
        
        content_layout.addLayout(details_container, 2)
        
        layout.addLayout(content_layout)
        
        # Botões
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        self.select_button = QPushButton("Selecionar")
        self.select_button.clicked.connect(self.accept)
        self.select_button.setEnabled(False)
        button_layout.addWidget(self.select_button)
        
        cancel_button = QPushButton("Cancelar")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Seleciona o primeiro item por padrão
        if self.style_list.count() > 0:
            self.style_list.setCurrentRow(0)
    
    def on_style_selected(self, current, previous):
        """Atualiza os detalhes quando um estilo é selecionado"""
        if current:
            style = current.data(Qt.ItemDataRole.UserRole)
            self.selected_style = style.name
            
            # Monta o texto de detalhes
            details_html = f"""
            <h3>{style.name}</h3>
            <p><b>Descrição:</b><br>{style.description}</p>
            """
            
            self.details_text.setHtml(details_html)
            self.select_button.setEnabled(True)
        else:
            self.selected_style = None
            self.details_text.clear()
            self.select_button.setEnabled(False)
    
    def get_selected_style(self) -> str:
        """Retorna o nome do estilo selecionado"""
        return self.selected_style
