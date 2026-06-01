from PyQt6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from models import Character
from models.character_exporter import CharacterExporter
from models.character_pdf_exporter import CharacterPDFExporter
from .character_creation_dialog import CharacterCreationDialog
from .character_sheet_tab import CharacterSheetTab
from .session_dialog import SessionDialog, SessionCodeDialog
from .session_panel import SessionPanel
from services.session_service import SessionService

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.character = Character()
        self._session_service = SessionService(self)
        self._session_panel = None
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
        self.save_btn.clicked.connect(self.save_json)
        button_layout.addWidget(self.save_btn)
        
        self.load_btn = QPushButton("Carregar Ficha")
        self.load_btn.clicked.connect(self.load_json)
        button_layout.addWidget(self.load_btn)
        
        self.session_btn = QPushButton("⚔️ Sessão")
        self.session_btn.clicked.connect(self.open_session)
        button_layout.addWidget(self.session_btn)

        button_layout.addStretch()
        
        main_layout.addLayout(button_layout)
        
        self.sheet_tab = CharacterSheetTab(self.character)
        self.sheet_tab.character_updated.connect(self.on_character_updated)
        
        main_layout.addWidget(self.sheet_tab)
        
        # Mostrar diálogo de boas-vindas ao iniciar se não houver personagem
        if not self.character.name:
            self.show_welcome_dialog()
    
    def open_session(self):
        """Abre o diálogo para criar ou entrar em uma sessão."""
        if self._session_service.is_active:
            if self._session_panel:
                self._session_panel.show()
                self._session_panel.raise_()
            return

        char_name = self.character.name or ""
        dialog = SessionDialog(character_name=char_name, parent=self)
        if not dialog.exec():
            return

        try:
            if dialog.mode == "create":
                code = self._session_service.create_session(
                    dm_name=dialog.player_name,
                    character_name=dialog.character_name,
                )
                SessionCodeDialog(code, self).exec()
            else:
                self._session_service.join_session(
                    code=dialog.join_code,
                    player_name=dialog.player_name,
                    character_name=dialog.character_name,
                )
        except Exception as e:
            QMessageBox.critical(self, "Erro na Sessão", str(e))
            return

        self._session_panel = SessionPanel(self._session_service, self)
        self._session_panel.show()
        self.session_btn.setText("⚔️ Sessão Ativa")
        self.session_btn.setStyleSheet("background-color:#2E7D32; color:white; font-weight:bold;")

        # Conecta o painel ao DiceHistoryWindow para publicar rolagens locais
        if hasattr(self.sheet_tab, 'dice_history') and self.sheet_tab.dice_history:
            self.sheet_tab.dice_history.session_panel = self._session_panel

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
            previous_name = self.character.name
            self.load_json()
            # Se o usuário cancelou ou falhou ao carregar, oferece criação
            if not self.character.name or self.character.name == previous_name:
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
    
