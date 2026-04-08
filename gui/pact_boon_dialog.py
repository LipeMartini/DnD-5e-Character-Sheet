"""Diálogo para seleção de Pact Boon do Warlock."""

from __future__ import annotations

from typing import Optional

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QHBoxLayout,
    QPushButton,
    QMessageBox,
)

from models.pact_boons import PactBoonDatabase


class PactBoonDialog(QDialog):
    """Permite que o personagem escolha um Pact Boon disponível."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Escolher Pact Boon")
        self.setModal(True)
        self.resize(520, 420)

        self._selected_boon: Optional[str] = None
        self._available_boons = PactBoonDatabase.get_all_boons()

        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        headline = QLabel("Seu patrono oferece uma dádiva especial")
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headline.setStyleSheet("font: bold 16px 'Georgia'; color: #3E2723;")
        layout.addWidget(headline)

        subtitle = QLabel(
            "Escolha uma das opções abaixo. Essa decisão define quais invocações futuras você desbloqueia."
        )
        subtitle.setWordWrap(True)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)

        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        self.boon_list = QListWidget()
        self.boon_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.boon_list.currentItemChanged.connect(self._on_selection_changed)
        self.boon_list.itemDoubleClicked.connect(lambda _: self.accept())
        content_layout.addWidget(self.boon_list, 2)

        for boon in self._available_boons:
            item = QListWidgetItem(boon.name)
            item.setData(Qt.ItemDataRole.UserRole, boon)
            self.boon_list.addItem(item)

        self.details_panel = QTextEdit()
        self.details_panel.setReadOnly(True)
        self.details_panel.setStyleSheet("background-color: #FFF8DC; font: 11px 'Georgia';")
        self.details_panel.setPlaceholderText("Selecione um Pact Boon para ver os detalhes")
        content_layout.addWidget(self.details_panel, 3)

        layout.addLayout(content_layout)

        buttons = QHBoxLayout()
        buttons.addStretch()

        self.confirm_btn = QPushButton("Confirmar")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.clicked.connect(self._confirm_selection)
        self.confirm_btn.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold;")
        buttons.addWidget(self.confirm_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        buttons.addWidget(cancel_btn)

        layout.addLayout(buttons)

        if not self._available_boons:
            QMessageBox.warning(
                self,
                "Nenhuma opção disponível",
                "Não há Pact Boons cadastrados. Adicione novos no arquivo de dados para prosseguir."
            )

    def _on_selection_changed(self, current: QListWidgetItem, _previous: QListWidgetItem) -> None:
        if not current:
            self._selected_boon = None
            self.confirm_btn.setEnabled(False)
            return

        boon = current.data(Qt.ItemDataRole.UserRole)
        if boon:
            self._selected_boon = boon.name
            self.confirm_btn.setEnabled(True)
            self._render_details(boon)

    def _render_details(self, boon) -> None:
        html = (
            f"<h3>{boon.name}</h3>"
            f"<p><b>Fonte:</b> {boon.source}</p>"
            f"<p>{boon.description}</p>"
            f"<p><b>Efeito mecânico:</b> {boon.mechanical_effect}</p>"
        )
        self.details_panel.setHtml(html)

    def _confirm_selection(self) -> None:
        if not self._selected_boon:
            QMessageBox.warning(self, "Selecione uma opção", "Escolha um Pact Boon antes de confirmar.")
            return
        self.accept()

    def get_selected_boon(self) -> Optional[str]:
        return self._selected_boon
