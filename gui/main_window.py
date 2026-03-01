from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from models import Character
from .character_creation_dialog import CharacterCreationDialog
from .character_sheet_tab import CharacterSheetTab

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.character = Character()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("D&D 5e Character Builder")
        self.setGeometry(100, 100, 1200, 800)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        
        button_layout = QHBoxLayout()
        
        self.new_char_btn = QPushButton("Nova Ficha")
        self.new_char_btn.clicked.connect(self.new_character)
        button_layout.addWidget(self.new_char_btn)
        
        self.save_btn = QPushButton("Salvar Ficha")
        self.save_btn.clicked.connect(self.save_character)
        button_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Carregar Ficha")
        self.load_btn.clicked.connect(self.load_character)
        button_layout.addWidget(self.load_btn)
        
        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        self.sheet_tab = CharacterSheetTab(self.character)
        self.sheet_tab.character_updated.connect(self.on_character_updated)
        
        main_layout.addWidget(self.sheet_tab)
        
        # Mostrar diálogo de boas-vindas ao iniciar se não houver personagem
        if not self.character.name:
            self.show_welcome_dialog()
    
    def on_character_updated(self):
        """Atualiza a ficha quando o personagem é modificado"""
        self.sheet_tab.update_display()
    
    def show_welcome_dialog(self):
        """Mostra diálogo de boas-vindas para escolher entre criar ou carregar personagem"""
        msg = QMessageBox(self)
        msg.setWindowTitle("Bem-vindo ao D&D 5e Character Builder!")
        msg.setText("O que você gostaria de fazer?")
        msg.setInformativeText("Escolha uma opção para começar:")
        
        create_btn = msg.addButton("Criar Novo Personagem", QMessageBox.ButtonRole.AcceptRole)
        load_btn = msg.addButton("Carregar Ficha Existente", QMessageBox.ButtonRole.AcceptRole)
        
        msg.exec()
        clicked = msg.clickedButton()
        
        if clicked == create_btn:
            self.show_character_creation()
        elif clicked == load_btn:
            self.load_character()
            # Se não carregou nenhum personagem, mostra criação
            if not self.character.name:
                self.show_character_creation()
    
    def show_character_creation(self):
        """Mostra o diálogo de criação de personagem"""
        dialog = CharacterCreationDialog(self)
        if dialog.exec():
            self.character = dialog.get_character()
            self.sheet_tab.set_character(self.character)
            self.on_character_updated()
            QMessageBox.information(
                self,
                "Personagem Criado!",
                f"Bem-vindo, {self.character.name}!\n\n"
                f"Raça: {self.character.race.name if self.character.race else 'N/A'}\n"
                f"Classe: {self.character.character_class.name if self.character.character_class else 'N/A'}\n"
                f"Nível: {self.character.level}\n"
                f"HP: {self.character.max_hit_points}"
            )
    
    def new_character(self):
        reply = QMessageBox.question(
            self, 
            'Nova Ficha',
            'Deseja criar uma nova ficha? Alterações não salvas serão perdidas.',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.show_character_creation()
    
    def save_character(self):
        if not self.character.name:
            QMessageBox.warning(self, "Aviso", "Por favor, dê um nome ao personagem antes de salvar.")
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Ficha de Personagem",
            f"{self.character.name}.json",
            "JSON Files (*.json)"
        )
        
        if filepath:
            try:
                self.character.save_to_file(filepath)
                QMessageBox.information(self, "Sucesso", f"Ficha salva em:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar ficha:\n{str(e)}")
    
    def load_character(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Carregar Ficha de Personagem",
            "",
            "JSON Files (*.json)"
        )
        
        if filepath:
            try:
                self.character = Character.load_from_file(filepath)
                self.sheet_tab.set_character(self.character)
                self.on_character_updated()
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar ficha:\n{str(e)}")
