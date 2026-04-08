"""Diálogo para escolher Eldritch Invocations."""

from __future__ import annotations

from typing import List

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

from models.eldritch_invocations import EldritchInvocationDatabase


class EldritchInvocationDialog(QDialog):
    """Permite escolher novas Eldritch Invocations para o Bruxo."""

    def __init__(self, character, max_choices: int, parent=None):
        super().__init__(parent)
        self.character = character
        self.max_choices = max_choices
        self._selected_count = 0
        self._available_invocations = EldritchInvocationDatabase.get_invocations_for_level(
            character.level,
            exclude=character.eldritch_invocations,
            pact_boon=character.pact_boon,
            patron_name=getattr(character, "subclass_name", None)
        )

        self.setWindowTitle("Selecionar Eldritch Invocations")
        self.setModal(True)
        self.resize(620, 520)

        self._build_ui()
        self._refresh_selection_state()

    # --------------------------------------------------------------------- UI
    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        headline = QLabel("Escolha novas invocações místicas")
        headline.setAlignment(Qt.AlignmentFlag.AlignCenter)
        headline.setStyleSheet("font: bold 16px 'Georgia'; color: #3E2723;")
        layout.addWidget(headline)

        self.info_label = QLabel()
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info_label.setStyleSheet("color: #5D4037;")
        layout.addWidget(self.info_label)

        hint_label = QLabel(
            "💡 Você pode reconfigurar suas invocações depois na Edição Avançada."
        )
        hint_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint_label.setStyleSheet("color: #6D4C41; font-style: italic;")
        layout.addWidget(hint_label)

        # Conteúdo principal: lista + detalhes
        content_layout = QHBoxLayout()
        content_layout.setSpacing(10)

        self.invocation_list = QListWidget()
        self.invocation_list.itemChanged.connect(self._on_item_changed)
        self.invocation_list.currentItemChanged.connect(self._on_current_changed)
        self.invocation_list.setStyleSheet("font: 11px 'Georgia';")
        content_layout.addWidget(self.invocation_list, 2)

        for invocation in self._available_invocations:
            subtitle = f"(Nível {invocation.min_level}+)"
            if invocation.prerequisites:
                subtitle += f" | {invocation.prerequisites}"

            item = QListWidgetItem(f"{invocation.name} {subtitle}")
            item.setData(Qt.ItemDataRole.UserRole, invocation)
            item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.invocation_list.addItem(item)

        self.details_panel = QTextEdit()
        self.details_panel.setReadOnly(True)
        self.details_panel.setStyleSheet("background-color: #FFF8DC; font: 11px 'Georgia';")
        self.details_panel.setPlaceholderText("Selecione uma invocação para ver os detalhes...")
        content_layout.addWidget(self.details_panel, 3)

        layout.addLayout(content_layout)

        # Botões
        button_row = QHBoxLayout()
        button_row.addStretch()

        self.confirm_btn = QPushButton("Adicionar")
        self.confirm_btn.setEnabled(False)
        self.confirm_btn.clicked.connect(self.accept)
        self.confirm_btn.setStyleSheet("background-color: #2E7D32; color: white; font-weight: bold;")
        button_row.addWidget(self.confirm_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        button_row.addWidget(cancel_btn)

        layout.addLayout(button_row)

        if self.invocation_list.count() == 0:
            QMessageBox.information(
                self,
                "Nenhuma invocação disponível",
                "Não há invocações compatíveis com o nível atual ou você já aprendeu todas."
            )

    # ---------------------------------------------------------------- Selection helpers
    def _refresh_selection_state(self) -> None:
        remaining = max(self.max_choices - self._selected_count, 0)
        self.info_label.setText(
            f"Você pode escolher <b>{self.max_choices}</b> nova(s) invocação(ões). "
            f"Faltam <b>{remaining}</b>."
        )
        self.confirm_btn.setEnabled(self._selected_count == self.max_choices and self.max_choices > 0)

    def _on_item_changed(self, item: QListWidgetItem) -> None:
        if not item.flags() & Qt.ItemFlag.ItemIsEnabled:
            return

        invocation = item.data(Qt.ItemDataRole.UserRole)
        if item.checkState() == Qt.CheckState.Checked:
            if self._selected_count >= self.max_choices:
                item.setCheckState(Qt.CheckState.Unchecked)
                QMessageBox.warning(
                    self,
                    "Limite atingido",
                    f"Você só pode escolher {self.max_choices} invocação(ões) neste nível."
                )
                return
            self._selected_count += 1
        else:
            self._selected_count = max(self._selected_count - 1, 0)

        self._refresh_selection_state()
        if invocation:
            self._render_details(invocation)

    def _on_current_changed(self, current: QListWidgetItem, _previous: QListWidgetItem) -> None:
        if not current:
            return
        invocation = current.data(Qt.ItemDataRole.UserRole)
        if invocation:
            self._render_details(invocation)

    def _render_details(self, invocation) -> None:
        prerequisites = invocation.prerequisites or "Nenhum requisito adicional"
        notes = f"<br><br><i>{invocation.notes}</i>" if invocation.notes else ""
        html = (
            f"<h3>{invocation.name}</h3>"
            f"<p><b>Fonte:</b> {invocation.source}</p>"
            f"<p><b>Nível mínimo:</b> {invocation.min_level}</p>"
            f"<p><b>Pré-requisitos:</b> {prerequisites}</p>"
            f"<p>{invocation.description}</p>"
            f"{notes}"
        )
        self.details_panel.setHtml(html)

    # ------------------------------------------------------------------- Public API
    def get_selected_invocations(self) -> List[str]:
        selected = []
        for row in range(self.invocation_list.count()):
            item = self.invocation_list.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                invocation = item.data(Qt.ItemDataRole.UserRole)
                if invocation:
                    selected.append(invocation.name)
        return selected
