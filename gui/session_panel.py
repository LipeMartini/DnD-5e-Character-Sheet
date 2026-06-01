"""
Painel flutuante da sessão compartilhada.

Exibe:
  • Lista de jogadores conectados
  • Histórico de rolagens em tempo real
  • Chat da sessão
"""

import random
import re

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QListWidget, QListWidgetItem,
    QTabWidget, QSplitter, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QTextCursor, QColor

from services.session_service import SessionService


STYLE = """
QWidget {
    background-color: #F5EBDC;
    color: #281E14;
    font-family: 'Georgia', 'Times New Roman', serif;
}
QTabWidget::pane {
    border: 2px solid #8B4513;
    border-radius: 4px;
    background: #FFF8DC;
}
QTabBar::tab {
    background: #D2B48C;
    color: #281E14;
    padding: 6px 14px;
    border: 1px solid #8B4513;
    font-weight: bold;
    font-size: 11px;
}
QTabBar::tab:selected {
    background: #8B4513;
    color: #F5EBDC;
}
QTextEdit, QListWidget {
    background: #FFFAF0;
    border: 2px solid #8B4513;
    border-radius: 6px;
    padding: 6px;
    font-size: 12px;
}
QLineEdit {
    background: white;
    border: 2px solid #8B4513;
    border-radius: 5px;
    padding: 6px 10px;
    font-size: 12px;
}
QLineEdit:focus { border-color: #A0522D; }
QPushButton {
    background-color: #8B4513;
    color: #F5EBDC;
    border: 2px solid #654321;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: bold;
    font-size: 11px;
    min-height: 30px;
}
QPushButton:hover  { background-color: #A0522D; }
QPushButton:pressed { background-color: #654321; }
QPushButton#danger {
    background-color: #8B1A1A;
    border-color: #5C0000;
}
QPushButton#danger:hover { background-color: #A52A2A; }
QLabel#header {
    background: #8B4513;
    color: #F5EBDC;
    padding: 8px;
    border-radius: 6px;
    font-size: 13px;
    font-weight: bold;
}
QLabel#code_badge {
    background: #654321;
    color: #F5EBDC;
    border-radius: 5px;
    padding: 4px 10px;
    font-size: 12px;
    font-weight: bold;
    letter-spacing: 2px;
}
"""

# Cores por tipo de rolagem (mesmas do DiceHistoryWindow)
ROLL_COLORS = {
    "INFO":       "#666666",
    "ROLL":       "#8B4513",
    "SKILL":      "#2E7D32",
    "SAVE":       "#1565C0",
    "ATTACK":     "#C62828",
    "DAMAGE":     "#D84315",
    "INITIATIVE": "#6A1B9A",
    "ABILITY":    "#00838F",
    "MANUAL":     "#4A4A4A",
    "SPELL":      "#5C35A0",
}


class SessionPanel(QWidget):
    """
    Janela flutuante que mostra o estado da sessão ao vivo.

    Parâmetros
    ----------
    session_service : SessionService
        Instância já conectada (create_session ou join_session já chamado).
    """

    def __init__(self, session_service: SessionService, parent=None):
        super().__init__(parent)
        self.service = session_service
        self.setWindowTitle("Sessão Compartilhada")
        self.setWindowFlags(Qt.WindowType.Window)
        self.resize(480, 620)
        self.setStyleSheet(STYLE)

        self._my_name = session_service.player_name or ""
        self._build_ui()
        self._connect_signals()
        self._load_history()

    # ------------------------------------------------------------------
    # Construção da UI
    # ------------------------------------------------------------------

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setSpacing(8)
        root.setContentsMargins(12, 12, 12, 12)

        # Cabeçalho
        header_row = QHBoxLayout()
        header_lbl = QLabel(f"⚔️  Sessão Ativa")
        header_lbl.setObjectName("header")
        header_row.addWidget(header_lbl, stretch=1)

        code_lbl = QLabel(self.service.session_code or "")
        code_lbl.setObjectName("code_badge")
        header_row.addWidget(code_lbl)
        root.addLayout(header_row)

        # Tabs: Rolagens | Chat | Jogadores
        self._tabs = QTabWidget()
        self._tabs.addTab(self._build_rolls_tab(),   "🎲 Rolagens")
        self._tabs.addTab(self._build_chat_tab(),    "💬 Chat")
        self._tabs.addTab(self._build_players_tab(), "👥 Jogadores")
        root.addWidget(self._tabs, stretch=1)

        # Rodapé
        leave_btn = QPushButton("Sair da Sessão")
        leave_btn.setObjectName("danger")
        leave_btn.clicked.connect(self._on_leave)
        root.addWidget(leave_btn)

    def _build_rolls_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._rolls_view = QTextEdit()
        self._rolls_view.setReadOnly(True)
        layout.addWidget(self._rolls_view, stretch=1)

        roll_row = QHBoxLayout()
        self._manual_roll_input = QLineEdit()
        self._manual_roll_input.setPlaceholderText("Ex: 1d8, 2d6+3, 4d6-2...")
        self._manual_roll_input.returnPressed.connect(self._roll_manual)
        roll_row.addWidget(self._manual_roll_input, stretch=1)

        roll_btn = QPushButton("🎲 Rolar")
        roll_btn.setFixedWidth(80)
        roll_btn.clicked.connect(self._roll_manual)
        roll_row.addWidget(roll_btn)
        layout.addLayout(roll_row)
        return w

    def _build_chat_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        self._chat_view = QTextEdit()
        self._chat_view.setReadOnly(True)
        layout.addWidget(self._chat_view, stretch=1)

        send_row = QHBoxLayout()
        self._chat_input = QLineEdit()
        self._chat_input.setPlaceholderText("Digite uma mensagem...")
        self._chat_input.returnPressed.connect(self._send_message)
        send_row.addWidget(self._chat_input, stretch=1)

        send_btn = QPushButton("Enviar")
        send_btn.setFixedWidth(80)
        send_btn.clicked.connect(self._send_message)
        send_row.addWidget(send_btn)
        layout.addLayout(send_row)
        return w

    def _build_players_tab(self) -> QWidget:
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setContentsMargins(8, 8, 8, 8)

        self._players_list = QListWidget()
        layout.addWidget(self._players_list)
        return w

    # ------------------------------------------------------------------
    # Conexão de sinais
    # ------------------------------------------------------------------

    def _connect_signals(self):
        self.service.roll_received.connect(self._on_roll_received)
        self.service.message_received.connect(self._on_message_received)
        self.service.player_joined.connect(self._on_player_joined)
        self.service.session_error.connect(self._on_error)

    # ------------------------------------------------------------------
    # Carregamento do histórico inicial
    # ------------------------------------------------------------------

    def _load_history(self):
        for roll in self.service.fetch_recent_rolls():
            self._append_roll(roll, initial=True)
        for msg in self.service.fetch_recent_messages():
            self._append_message(msg, initial=True)
        for player in self.service.fetch_players():
            self._add_player_item(player)

    # ------------------------------------------------------------------
    # Slots de eventos em tempo real
    # ------------------------------------------------------------------

    @pyqtSlot(object)
    def _on_roll_received(self, data):
        if not isinstance(data, dict):
            return
        # Ignorar rolagens do próprio jogador (já foram adicionadas localmente)
        if data.get("player_name") == self._my_name:
            return
        self._append_roll(data)

    @pyqtSlot(object)
    def _on_message_received(self, data):
        if not isinstance(data, dict):
            return
        if data.get("player_name") == self._my_name:
            return
        self._append_message(data)

    @pyqtSlot(object)
    def _on_player_joined(self, data):
        if not isinstance(data, dict):
            return
        self._add_player_item(data)

    @pyqtSlot(str)
    def _on_error(self, msg: str):
        QMessageBox.warning(self, "Erro na Sessão", msg)

    # ------------------------------------------------------------------
    # Helpers de renderização
    # ------------------------------------------------------------------

    def _append_roll(self, data: dict, initial: bool = False):
        roll_type  = data.get("roll_type", "ROLL")
        player     = data.get("player_name", "?")
        char_name  = data.get("character_name", "")
        expression = data.get("expression", "")
        result     = data.get("result", "?")
        breakdown  = data.get("breakdown", "")
        ts_raw     = data.get("created_at", "")
        # Mostrar só HH:MM:SS (sem a data)
        ts = ts_raw[11:19] if len(ts_raw) >= 19 else ts_raw

        color = ROLL_COLORS.get(roll_type, "#8B4513")
        who   = f"{char_name} ({player})" if char_name else player

        # Se há breakdown (vem de add_roll): expressão simples + → resultado
        # Se não há (vem de add_entry): expressão já contém o resultado completo
        if breakdown:
            content = f'{expression} → <b>{result}</b>'
        else:
            content = expression

        html = (
            f'<div style="margin-bottom:8px; padding:5px 8px; background:#FFFAF0;'
            f'border-left:4px solid {color}; border-radius:3px;">'
            # Linha 1: tipo + jogador + hora
            f'<span style="color:{color}; font-weight:bold; font-size:11px;">{roll_type}</span>'
            f'<span style="color:#666; font-size:11px;"> — {who}</span>'
            f'<span style="color:#bbb; font-size:9px;"> [{ts}]</span>'
            # Linha 2: conteúdo da rolagem
            f'<br><span style="color:#281E14; font-size:12px;">{content}</span>'
        )
        if breakdown:
            html += f'<br><span style="color:#888; font-size:10px;">{breakdown}</span>'
        html += '</div><br>'

        cursor = self._rolls_view.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._rolls_view.setTextCursor(cursor)
        self._rolls_view.insertHtml(html)
        if not initial:
            self._rolls_view.verticalScrollBar().setValue(
                self._rolls_view.verticalScrollBar().maximum()
            )

    def _append_message(self, data: dict, initial: bool = False):
        player  = data.get("player_name", "?")
        message = data.get("message", "")
        ts      = data.get("created_at", "")[:19].replace("T", " ") if data.get("created_at") else ""
        ts_str  = f" [{ts}]" if ts else ""

        is_me  = (player == self._my_name)
        color  = "#8B4513" if is_me else "#1a4a7a"
        prefix = "Voce" if is_me else player

        html = (
            f'<div style="margin-bottom:6px; padding:4px 8px; '
            f'border-left:3px solid {color}; background:#FFFAF0;">'
            f'<b style="color:{color};">{prefix}</b>'
            f'<span style="color:#999; font-size:10px;">{ts_str}</span>: '
            f'{message}'
            f'</div><br>'
        )

        cursor = self._chat_view.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self._chat_view.setTextCursor(cursor)
        self._chat_view.insertHtml(html)
        if not initial:
            self._chat_view.verticalScrollBar().setValue(
                self._chat_view.verticalScrollBar().maximum()
            )

    def _add_player_item(self, data: dict):
        player = data.get("player_name", "?")
        char   = data.get("character_name", "")
        label  = f"[{char}]  {player}" if char else player
        item   = QListWidgetItem(label)
        self._players_list.addItem(item)

    # ------------------------------------------------------------------
    # Enviar mensagem
    # ------------------------------------------------------------------

    def _send_message(self):
        text = self._chat_input.text().strip()
        if not text:
            return
        self.service.publish_message(text)
        # Adiciona localmente (o evento próprio é ignorado no slot)
        self._append_message({
            "player_name": self._my_name,
            "message":     text,
        })
        self._chat_input.clear()

    # ------------------------------------------------------------------
    # Rolagem manual diretamente no painel
    # ------------------------------------------------------------------

    def _roll_manual(self):
        expression = self._manual_roll_input.text().strip()
        if not expression:
            return

        pattern = r'(\d+)d(\d+)([\+\-]\d+)?'
        match = re.match(pattern, expression.lower().replace(' ', ''))
        if not match:
            QMessageBox.warning(
                self, "Formato Inválido",
                f"Formato inválido: '{expression}'\n\nUse: 1d8, 2d6+3, 4d6-2"
            )
            return

        num_dice = int(match.group(1))
        die_size = int(match.group(2))
        modifier = int(match.group(3)) if match.group(3) else 0

        if num_dice < 1 or num_dice > 100:
            QMessageBox.warning(self, "Erro", "Número de dados deve ser entre 1 e 100.")
            return
        if die_size not in [2, 4, 6, 8, 10, 12, 20, 100]:
            QMessageBox.warning(self, "Erro", f"Dado inválido: d{die_size}")
            return

        rolls = [random.randint(1, die_size) for _ in range(num_dice)]
        total = sum(rolls) + modifier
        rolls_str = " + ".join(str(r) for r in rolls)
        mod_str = f" + {modifier}" if modifier > 0 else (f" - {abs(modifier)}" if modifier < 0 else "")
        breakdown = f"🎲 ({rolls_str}){mod_str}"

        self.publish_roll("MANUAL", expression, total, breakdown)
        self._manual_roll_input.clear()
        self._manual_roll_input.setFocus()

    # ------------------------------------------------------------------
    # Sair da sessão
    # ------------------------------------------------------------------

    def _on_leave(self):
        reply = QMessageBox.question(
            self, "Sair da Sessão",
            "Deseja sair da sessão compartilhada?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.service.leave_session()
            self.close()

    # ------------------------------------------------------------------
    # Método público: recebe rolagem local e a publica
    # ------------------------------------------------------------------

    def publish_roll(self, roll_type: str, expression: str,
                     result: int, breakdown: str = ""):
        """Chamado pela DiceHistoryWindow quando há uma rolagem local."""
        self.service.publish_roll(roll_type, expression, result, breakdown)
        from datetime import datetime
        self._append_roll({
            "player_name":    self._my_name,
            "character_name": self.service.character_name,
            "roll_type":      roll_type,
            "expression":     expression,
            "result":         result,
            "breakdown":      breakdown,
            "created_at":     datetime.now().isoformat(),
        })
