from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QFileDialog, QMessageBox, QMenu)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from models import Character
from models.character_exporter import CharacterExporter
from models.character_pdf_exporter import CharacterPDFExporter
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
        self.save_btn.clicked.connect(self.show_save_menu)
        button_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Carregar Ficha")
        self.load_btn.clicked.connect(self.show_load_menu)
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
            self.show_load_menu()
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
            
            # Verificar se precisa escolher Fighting Style (Fighter nível 1)
            self.sheet_tab.check_and_select_fighting_style(self.character.level)
            
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
    
    def show_save_menu(self):
        """Mostra menu de opções para salvar ficha"""
        if not self.character.name:
            QMessageBox.warning(self, "Aviso", "Por favor, dê um nome ao personagem antes de salvar.")
            return
        
        menu = QMenu(self)
        
        json_action = QAction("Salvar como JSON", self)
        json_action.triggered.connect(self.save_json)
        menu.addAction(json_action)
        
        xml_action = QAction("Salvar como XML", self)
        xml_action.triggered.connect(self.save_xml)
        menu.addAction(xml_action)
        
        pdf_action = QAction("Exportar como PDF", self)
        pdf_action.triggered.connect(self.export_pdf)
        menu.addAction(pdf_action)
        
        # Mostra o menu na posição do botão
        menu.exec(self.save_btn.mapToGlobal(self.save_btn.rect().bottomLeft()))
    
    def show_load_menu(self):
        """Mostra menu de opções para carregar ficha"""
        menu = QMenu(self)
        
        json_action = QAction("Carregar de JSON", self)
        json_action.triggered.connect(self.load_json)
        menu.addAction(json_action)
        
        xml_action = QAction("Carregar de XML", self)
        xml_action.triggered.connect(self.load_xml)
        menu.addAction(xml_action)
        
        # Mostra o menu na posição do botão
        menu.exec(self.load_btn.mapToGlobal(self.load_btn.rect().bottomLeft()))
    
    def save_json(self):
        """Salva personagem em JSON"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Ficha como JSON",
            f"{self.character.name}.json",
            "JSON Files (*.json)"
        )
        
        if filepath:
            try:
                CharacterExporter.export_to_json(self.character, filepath)
                QMessageBox.information(self, "Sucesso", f"Ficha salva em:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar ficha:\n{str(e)}")
    
    def save_xml(self):
        """Salva personagem em XML"""
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar Ficha como XML",
            f"{self.character.name}.xml",
            "XML Files (*.xml)"
        )
        
        if filepath:
            try:
                CharacterExporter.export_to_xml(self.character, filepath)
                QMessageBox.information(self, "Sucesso", f"Ficha salva em:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao salvar ficha:\n{str(e)}")
    
    def export_pdf(self):
        """Exporta personagem para PDF"""
        if not CharacterPDFExporter.is_available():
            reply = QMessageBox.question(
                self,
                "Biblioteca não instalada",
                "A exportação para PDF requer a biblioteca 'reportlab'.\n\n"
                "Deseja instalar agora? (Execute: pip install reportlab)",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                QMessageBox.information(
                    self,
                    "Instalação",
                    "Por favor, execute o seguinte comando no terminal:\n\n"
                    "pip install reportlab\n\n"
                    "Após a instalação, reinicie o aplicativo."
                )
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self,
            "Exportar Ficha como PDF",
            f"{self.character.name}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if filepath:
            try:
                CharacterPDFExporter.export_to_pdf(self.character, filepath)
                QMessageBox.information(self, "Sucesso", f"Ficha exportada para PDF em:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao exportar para PDF:\n{str(e)}")
    
    def load_json(self):
        """Carrega personagem de JSON"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Carregar Ficha de JSON",
            "",
            "JSON Files (*.json)"
        )
        
        if filepath:
            try:
                self.character = CharacterExporter.import_from_json(filepath)
                self.sheet_tab.set_character(self.character)
                self.on_character_updated()
                QMessageBox.information(self, "Sucesso", f"Ficha carregada de:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar ficha:\n{str(e)}")
    
    def load_xml(self):
        """Carrega personagem de XML"""
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Carregar Ficha de XML",
            "",
            "XML Files (*.xml)"
        )
        
        if filepath:
            try:
                self.character = CharacterExporter.import_from_xml(filepath)
                self.sheet_tab.set_character(self.character)
                self.on_character_updated()
                QMessageBox.information(self, "Sucesso", f"Ficha carregada de:\n{filepath}")
            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Erro ao carregar ficha:\n{str(e)}")
