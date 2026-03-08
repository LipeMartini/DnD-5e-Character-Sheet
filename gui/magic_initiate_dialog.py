from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QTextEdit,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from models import SpellDatabase
from models.spellcasting import SpellSlotTable


class MagicInitiateDialog(QDialog):
    """Dialog para escolher as magias concedidas por Magic Initiate."""

    ALLOWED_CLASSES = ["Bard", "Cleric", "Druid", "Sorcerer", "Warlock", "Wizard"]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Magic Initiate - Escolha de Magias")
        self.setMinimumSize(700, 500)

        self.selected_class = None
        self.available_cantrips = {}
        self.available_level1 = {}

        self._setup_ui()
        self._load_spell_lists()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Escolha uma lista de magias e selecione 2 truques e 1 magia de 1º nível")
        title.setFont(QFont("Georgia", 12, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #8B4513; padding: 8px;")
        layout.addWidget(title)

        # Classe
        class_layout = QHBoxLayout()
        class_label = QLabel("Lista de Magias:")
        class_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        class_layout.addWidget(class_label)

        self.class_combo = QComboBox()
        self.class_combo.setFont(QFont("Georgia", 10))
        for spell_class in self.ALLOWED_CLASSES:
            self.class_combo.addItem(spell_class, spell_class)
        self.class_combo.currentIndexChanged.connect(self._load_spell_lists)
        class_layout.addWidget(self.class_combo)

        class_layout.addStretch()
        layout.addLayout(class_layout)

        content_layout = QHBoxLayout()

        # Cantrips
        cantrip_layout = QVBoxLayout()
        cantrip_label = QLabel("Truques (escolha 2):")
        cantrip_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        cantrip_layout.addWidget(cantrip_label)

        self.cantrip_list = QListWidget()
        self.cantrip_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.cantrip_list.itemSelectionChanged.connect(lambda: self._show_details_from_list(self.cantrip_list))
        cantrip_layout.addWidget(self.cantrip_list)

        content_layout.addLayout(cantrip_layout, 1)

        # Magias de nível 1
        spell_layout = QVBoxLayout()
        spell_label = QLabel("Magia de 1º nível (escolha 1):")
        spell_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        spell_layout.addWidget(spell_label)

        self.spell_list = QListWidget()
        self.spell_list.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.spell_list.itemSelectionChanged.connect(lambda: self._show_details_from_list(self.spell_list))
        spell_layout.addWidget(self.spell_list)

        content_layout.addLayout(spell_layout, 1)

        # Detalhes
        details_layout = QVBoxLayout()
        details_label = QLabel("Detalhes da Magia:")
        details_label.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        details_layout.addWidget(details_label)

        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setFont(QFont("Georgia", 9))
        self.details_text.setStyleSheet(
            "QTextEdit { background-color: #FFF8DC; border: 2px solid #8B4513; border-radius: 6px; padding: 10px; }"
        )
        details_layout.addWidget(self.details_text)

        content_layout.addLayout(details_layout, 1)

        layout.addLayout(content_layout)

        # Botões
        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()

        confirm_btn = QPushButton("Confirmar")
        confirm_btn.setFont(QFont("Georgia", 10, QFont.Weight.Bold))
        confirm_btn.setStyleSheet(
            "QPushButton { background-color: #8B4513; color: #F5EBDC; border: 2px solid #654321; border-radius: 5px; padding: 8px 20px; }"
            "QPushButton:hover { background-color: #A0522D; }"
        )
        confirm_btn.clicked.connect(self._on_confirm)
        buttons_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.setFont(QFont("Georgia", 10))
        cancel_btn.setStyleSheet(
            "QPushButton { background-color: #777777; color: white; border: 2px solid #555555; border-radius: 5px; padding: 8px 20px; }"
            "QPushButton:hover { background-color: #999999; }"
        )
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

    def _load_spell_lists(self):
        self.selected_class = self.class_combo.currentData()
        if not self.selected_class:
            return

        self.available_cantrips = SpellDatabase.get_spells_by_level(0, self.selected_class)
        self.available_level1 = SpellDatabase.get_spells_by_level(1, self.selected_class)

        self._populate_list(self.cantrip_list, self.available_cantrips)
        self._populate_list(self.spell_list, self.available_level1)
        self.details_text.clear()

    def _populate_list(self, widget: QListWidget, spells: dict):
        widget.clear()
        for spell_name in sorted(spells.keys()):
            spell = spells[spell_name]
            item = QListWidgetItem(spell_name)
            item.setData(Qt.ItemDataRole.UserRole, spell)
            widget.addItem(item)

    def _show_details_from_list(self, widget: QListWidget):
        selected_items = widget.selectedItems()
        if not selected_items:
            return
        spell = selected_items[-1].data(Qt.ItemDataRole.UserRole)
        if not spell:
            return

        details = f"""<h3 style='color:#8B4513;'>{spell.name}</h3>
<p><b>Nível:</b> {spell.get_level_text()}<br>
<b>Escola:</b> {spell.school}<br>
<b>Tempo de Conjuração:</b> {spell.casting_time}<br>
<b>Alcance:</b> {spell.range}<br>
<b>Componentes:</b> {spell.components}<br>
<b>Duração:</b> {spell.duration}</p>
<p>{spell.description.replace(chr(10), '<br>')}</p>
"""
        if spell.ritual:
            details += "<p><i>✨ Pode ser conjurada como ritual.</i></p>"
        if spell.concentration:
            details += "<p><i>🧠 Requer concentração.</i></p>"
        self.details_text.setHtml(details)

    def _on_confirm(self):
        if not self.selected_class:
            QMessageBox.warning(self, "Classe obrigatória", "Escolha uma lista de magias válida.")
            return

        selected_cantrips = [item.text() for item in self.cantrip_list.selectedItems()]
        if len(selected_cantrips) != 2:
            QMessageBox.warning(self, "Seleção inválida", "Você deve escolher exatamente 2 truques.")
            return

        selected_spell_items = self.spell_list.selectedItems()
        if not selected_spell_items:
            QMessageBox.warning(self, "Seleção inválida", "Escolha uma magia de 1º nível.")
            return

        self._selection = {
            "spell_class": self.selected_class,
            "cantrips": selected_cantrips,
            "level1_spell": selected_spell_items[0].text(),
            "spellcasting_ability": SpellSlotTable.get_spellcasting_ability(self.selected_class),
        }
        self.accept()

    def get_selection(self) -> dict:
        return getattr(self, "_selection", None)
