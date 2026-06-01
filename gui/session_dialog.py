"""
Diálogo para criar ou entrar em uma sessão compartilhada.
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QWidget, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QClipboard


STYLE = """
QDialog {
    background-color: #F5EBDC;
    color: #281E14;
    font-family: 'Georgia', 'Times New Roman', serif;
}
QTabWidget::pane {
    border: 2px solid #8B4513;
    border-radius: 6px;
    background-color: #FFF8DC;
}
QTabBar::tab {
    background: #D2B48C;
    color: #281E14;
    padding: 8px 20px;
    border: 1px solid #8B4513;
    font-family: 'Georgia', serif;
    font-weight: bold;
}
QTabBar::tab:selected {
    background: #8B4513;
    color: #F5EBDC;
}
QLabel {
    background: transparent;
    color: #281E14;
    font-size: 13px;
}
QLineEdit {
    background: white;
    border: 2px solid #8B4513;
    border-radius: 5px;
    padding: 7px 10px;
    font-size: 13px;
    color: #281E14;
}
QLineEdit:focus { border-color: #A0522D; }
QPushButton {
    background-color: #8B4513;
    color: #F5EBDC;
    border: 2px solid #654321;
    border-radius: 5px;
    padding: 8px 18px;
    font-weight: bold;
    font-size: 12px;
    min-height: 34px;
}
QPushButton:hover  { background-color: #A0522D; }
QPushButton:pressed { background-color: #654321; }
QPushButton#secondary {
    background-color: transparent;
    color: #8B4513;
    border: 2px solid #8B4513;
}
QPushButton#secondary:hover { background-color: #D2B48C; }
"""


class SessionDialog(QDialog):
    """
    Diálogo com duas abas:
      • Criar Sessão (DM)
      • Entrar na Sessão (jogador)

    Após exec() com resultado Accepted, use:
      dialog.mode          – "create" | "join"
      dialog.player_name
      dialog.character_name
      dialog.join_code     – preenchido apenas se mode == "join"
    """

    def __init__(self, character_name: str = "", parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sessão Compartilhada")
        self.setMinimumWidth(420)
        self.setStyleSheet(STYLE)

        self.mode:           str = ""
        self.player_name:    str = ""
        self.character_name: str = ""
        self.join_code:      str = ""

        self._prefill_character = character_name
        self._build_ui()

    # ------------------------------------------------------------------
    # UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("⚔️  Sessão Compartilhada")
        title.setFont(QFont("Georgia", 15, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "background:#8B4513; color:#F5EBDC; padding:10px; border-radius:8px;"
        )
        layout.addWidget(title)

        tabs = QTabWidget()
        tabs.addTab(self._create_tab(), "🏰  Criar Sessão")
        tabs.addTab(self._join_tab(),   "🚪  Entrar na Sessão")
        layout.addWidget(tabs)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setObjectName("secondary")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

    def _create_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        layout.addWidget(QLabel("Seu nome (Mestre):"))
        self._create_name = QLineEdit()
        self._create_name.setPlaceholderText("Nome do Mestre")
        if self._prefill_character:
            self._create_name.setText(self._prefill_character)
        layout.addWidget(self._create_name)

        layout.addWidget(QLabel("Nome do personagem (opcional):"))
        self._create_char = QLineEdit()
        self._create_char.setPlaceholderText("Nome do personagem")
        layout.addWidget(self._create_char)

        layout.addStretch()

        btn = QPushButton("🏰  Criar Sessão")
        btn.clicked.connect(self._on_create)
        layout.addWidget(btn)
        return w

    def _join_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(10)
        layout.setContentsMargins(16, 16, 16, 16)

        layout.addWidget(QLabel("Código da sessão:"))
        self._join_code_input = QLineEdit()
        self._join_code_input.setPlaceholderText("Ex: X7K2M9")
        self._join_code_input.setMaxLength(6)
        font = self._join_code_input.font()
        font.setPointSize(16)
        font.setBold(True)
        self._join_code_input.setFont(font)
        self._join_code_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self._join_code_input)

        layout.addWidget(QLabel("Seu nome:"))
        self._join_name = QLineEdit()
        self._join_name.setPlaceholderText("Nome do jogador")
        if self._prefill_character:
            self._join_name.setText(self._prefill_character)
        layout.addWidget(self._join_name)

        layout.addWidget(QLabel("Nome do personagem (opcional):"))
        self._join_char = QLineEdit()
        self._join_char.setPlaceholderText("Nome do personagem")
        layout.addWidget(self._join_char)

        layout.addStretch()

        btn = QPushButton("🚪  Entrar na Sessão")
        btn.clicked.connect(self._on_join)
        layout.addWidget(btn)
        return w

    # ------------------------------------------------------------------
    # Handlers
    # ------------------------------------------------------------------

    def _on_create(self):
        name = self._create_name.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Digite seu nome para criar a sessão.")
            return
        self.mode           = "create"
        self.player_name    = name
        self.character_name = self._create_char.text().strip()
        self.accept()

    def _on_join(self):
        code = self._join_code_input.text().strip().upper()
        name = self._join_name.text().strip()
        if not code:
            QMessageBox.warning(self, "Aviso", "Digite o código da sessão.")
            return
        if not name:
            QMessageBox.warning(self, "Aviso", "Digite seu nome.")
            return
        self.mode           = "join"
        self.player_name    = name
        self.character_name = self._join_char.text().strip()
        self.join_code      = code
        self.accept()


# ---------------------------------------------------------------------------
# Diálogo de confirmação / exibição do código gerado
# ---------------------------------------------------------------------------

class SessionCodeDialog(QDialog):
    """Exibe o código da sessão criada e permite copiar."""

    def __init__(self, code: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Sessão Criada!")
        self.setMinimumWidth(360)
        self.setStyleSheet(STYLE)
        self._build_ui(code)

    def _build_ui(self, code: str):
        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(24, 24, 24, 24)

        lbl = QLabel("Sessão criada com sucesso!")
        lbl.setFont(QFont("Georgia", 13, QFont.Weight.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        info = QLabel("Compartilhe este código com os jogadores:")
        info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(info)

        code_lbl = QLabel(code)
        code_lbl.setFont(QFont("Georgia", 36, QFont.Weight.Bold))
        code_lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        code_lbl.setStyleSheet(
            "color:#8B4513; background:#FFF8DC; border:3px solid #8B4513;"
            "border-radius:10px; padding:16px;"
        )
        layout.addWidget(code_lbl)

        copy_btn = QPushButton("📋  Copiar Código")
        copy_btn.clicked.connect(lambda: self._copy(code))
        layout.addWidget(copy_btn)

        ok_btn = QPushButton("Continuar")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn)

    def _copy(self, code: str):
        QApplication.clipboard().setText(code)
        QMessageBox.information(self, "Copiado", f"Código '{code}' copiado para a área de transferência.")
