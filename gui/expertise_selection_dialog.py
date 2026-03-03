from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class ExpertiseSelectionDialog(QDialog):
    """Dialog para escolher perícias que receberão Expertise."""

    def __init__(self, character, num_skills: int, eligible_skills: list[str], parent=None, title: str = "Escolher Expertise"):
        super().__init__(parent)
        self.character = character
        self.eligible_skills = sorted(eligible_skills)
        self.requested = num_skills
        self.selected_skills: list[str] = []
        self.setWindowTitle(title)
        self.setModal(True)
        self.resize(420, 520)

        if not self.eligible_skills:
            self.requested = 0

        # Se não houver skills suficientes, limita para evitar bloqueio
        if len(self.eligible_skills) < self.requested:
            self.requested = len(self.eligible_skills)
            self.insufficient_skills = True
        else:
            self.insufficient_skills = False

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Escolha perícias para ganhar Expertise")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setFont(QFont("Georgia", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        desc_text = (
            "Selecione exatamente"
            f" {self.requested} perícias nas quais você já é proficiente."
            if self.requested
            else "Não há perícias disponíveis para receber Expertise no momento."
        )
        desc = QLabel(desc_text)
        desc.setWordWrap(True)
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)

        if self.insufficient_skills:
            warn = QLabel(
                "⚠️ Nem todas as escolhas previstas pelo nível são possíveis,"
                " pois você não possui perícias suficientes com proficiência."
            )
            warn.setWordWrap(True)
            warn.setStyleSheet("color: #D35400; font-style: italic; padding: 6px;")
            layout.addWidget(warn)

        self.counter_label = QLabel(f"Selecionadas: 0/{self.requested}")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter_label.setStyleSheet("color: #8B4513; font-weight: bold; padding: 5px;")
        layout.addWidget(self.counter_label)

        self.skills_list = QListWidget()
        self.skills_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.skills_list.itemSelectionChanged.connect(self.on_selection_changed)

        for skill in self.eligible_skills:
            item = QListWidgetItem(skill)
            self.skills_list.addItem(item)

        layout.addWidget(self.skills_list)

        buttons_layout = QHBoxLayout()
        confirm_btn = QPushButton("Confirmar")
        confirm_btn.clicked.connect(self.confirm_selection)
        confirm_btn.setStyleSheet(
            "QPushButton {background-color: #8B4513; color: white; border: 2px solid #654321;"
            "border-radius: 5px; padding: 8px 20px; font-weight: bold;}"
            "QPushButton:hover {background-color: #A0522D;}"
        )
        buttons_layout.addWidget(confirm_btn)

        cancel_btn = QPushButton("Cancelar")
        cancel_btn.clicked.connect(self.reject)
        cancel_btn.setStyleSheet(
            "QPushButton {background-color: #696969; color: white; border: 2px solid #444;"
            "border-radius: 5px; padding: 8px 20px;}"
            "QPushButton:hover {background-color: #7F8C8D;}"
        )
        buttons_layout.addWidget(cancel_btn)

        layout.addLayout(buttons_layout)

        if self.requested == 0:
            self.skills_list.setEnabled(False)
            confirm_btn.setEnabled(False)

    def on_selection_changed(self):
        selected = len(self.skills_list.selectedItems())
        self.counter_label.setText(f"Selecionadas: {selected}/{self.requested}")
        if selected == self.requested:
            self.counter_label.setStyleSheet("color: green; font-weight: bold; padding: 5px;")
        elif selected > self.requested:
            self.counter_label.setStyleSheet("color: red; font-weight: bold; padding: 5px;")
        else:
            self.counter_label.setStyleSheet("color: #8B4513; font-weight: bold; padding: 5px;")

    def confirm_selection(self):
        if self.requested == 0:
            self.accept()
            return

        selected_items = self.skills_list.selectedItems()
        count = len(selected_items)
        if count != self.requested:
            QMessageBox.warning(
                self,
                "Seleção incompleta",
                f"Você deve selecionar exatamente {self.requested} perícias.",
            )
            return

        self.selected_skills = [item.text() for item in selected_items]
        self.accept()

    def get_selected_skills(self) -> list[str]:
        return self.selected_skills
