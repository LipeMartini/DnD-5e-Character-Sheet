from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
                              QComboBox, QGroupBox, QRadioButton, QButtonGroup, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from .feat_dialog import FeatDialog

ALL_SKILLS = [
    'Acrobatics', 'Animal Handling', 'Arcana', 'Athletics', 'Deception',
    'History', 'Insight', 'Intimidation', 'Investigation', 'Medicine',
    'Nature', 'Perception', 'Performance', 'Persuasion', 'Religion',
    'Sleight of Hand', 'Stealth', 'Survival'
]

STAT_DISPLAY = [
    ('strength',     'Força (Strength)'),
    ('dexterity',    'Destreza (Dexterity)'),
    ('constitution', 'Constituição (Constitution)'),
    ('intelligence', 'Inteligência (Intelligence)'),
    ('wisdom',       'Sabedoria (Wisdom)'),
    ('charisma',     'Carisma (Charisma)'),
]


class VariantRaceDialog(QDialog):
    """Dialog para as escolhas de Variant Human e Custom Lineage."""

    def __init__(self, race_name: str, character, parent=None):
        super().__init__(parent)
        self.race_name = race_name
        self.character = character

        self.chosen_ability_bonuses = {}
        self.chosen_skill = None
        self.chosen_darkvision = False
        self.chosen_feat = None
        self.chosen_feat_asi = None
        self.chosen_feat_half_ability = None
        self.chosen_feat_magic_initiate = None

        is_vh = race_name == 'Variant Human'
        title = 'Variant Human — Escolhas Raciais' if is_vh else 'Custom Lineage — Escolhas Raciais'
        self.setWindowTitle(title)
        self.setModal(True)
        self.setMinimumSize(520, 420)
        self._setup_ui(is_vh)

    # ──────────────────────────────────────────────────────────────────
    def _setup_ui(self, is_vh: bool):
        layout = QVBoxLayout(self)

        subtitle = (
            'Variant Human: +1 em dois atributos diferentes, uma perícia e um Feat de nível 1.'
            if is_vh else
            'Custom Lineage: +2 em um atributo, uma perícia ou Visão no Escuro (9m) e um Feat de nível 1.'
        )
        lbl = QLabel(subtitle)
        lbl.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        lbl.setStyleSheet('color: #8B4513; padding: 6px;')
        lbl.setWordWrap(True)
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl)

        if is_vh:
            self._build_vh_stats(layout)
            self._build_skill_section(layout)
        else:
            self._build_cl_stats(layout)
            self._build_cl_variable(layout)

        self._build_feat_section(layout)
        self._build_buttons(layout)

    # ── Stat panels ────────────────────────────────────────────────────
    def _build_vh_stats(self, layout):
        grp = QGroupBox('+1 em dois atributos diferentes')
        grp.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        row = QHBoxLayout()

        row.addWidget(QLabel('+1 em:'))
        self.stat1_combo = self._stat_combo(default_index=0)
        row.addWidget(self.stat1_combo)

        row.addWidget(QLabel('  e  +1 em:'))
        self.stat2_combo = self._stat_combo(default_index=1)
        row.addWidget(self.stat2_combo)

        grp.setLayout(row)
        layout.addWidget(grp)

    def _build_cl_stats(self, layout):
        grp = QGroupBox('+2 em um atributo')
        grp.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        row = QHBoxLayout()
        row.addWidget(QLabel('+2 em:'))
        self.stat1_combo = self._stat_combo(default_index=0)
        row.addWidget(self.stat1_combo)
        grp.setLayout(row)
        layout.addWidget(grp)

    def _stat_combo(self, default_index=0) -> QComboBox:
        combo = QComboBox()
        combo.setFont(QFont('Georgia', 9))
        for key, label in STAT_DISPLAY:
            combo.addItem(label, key)
        combo.setCurrentIndex(default_index)
        return combo

    # ── Skill / variable trait panels ──────────────────────────────────
    def _build_skill_section(self, layout):
        grp = QGroupBox('Proficiência em Perícia')
        grp.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        row = QHBoxLayout()
        row.addWidget(QLabel('Perícia:'))
        self.skill_combo = QComboBox()
        self.skill_combo.setFont(QFont('Georgia', 9))
        self.skill_combo.addItems(ALL_SKILLS)
        row.addWidget(self.skill_combo)
        grp.setLayout(row)
        layout.addWidget(grp)

    def _build_cl_variable(self, layout):
        grp = QGroupBox('Traço Variável: Perícia ou Visão no Escuro (9m)')
        grp.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        col = QVBoxLayout()

        self._variable_group = QButtonGroup()

        self.skill_radio = QRadioButton('Proficiência em Perícia:')
        self.skill_radio.setFont(QFont('Georgia', 9))
        self.skill_radio.setChecked(True)
        self._variable_group.addButton(self.skill_radio)

        skill_row = QHBoxLayout()
        skill_row.addWidget(self.skill_radio)
        self.skill_combo = QComboBox()
        self.skill_combo.setFont(QFont('Georgia', 9))
        self.skill_combo.addItems(ALL_SKILLS)
        skill_row.addWidget(self.skill_combo)
        col.addLayout(skill_row)

        self.darkvision_radio = QRadioButton('Visão no Escuro (alcance 9m / 30ft)')
        self.darkvision_radio.setFont(QFont('Georgia', 9))
        self._variable_group.addButton(self.darkvision_radio)
        col.addWidget(self.darkvision_radio)

        self.skill_radio.toggled.connect(lambda checked: self.skill_combo.setEnabled(checked))

        grp.setLayout(col)
        layout.addWidget(grp)

    # ── Feat section ───────────────────────────────────────────────────
    def _build_feat_section(self, layout):
        grp = QGroupBox('Feat de Nível 1')
        grp.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        row = QHBoxLayout()

        self.feat_label = QLabel('Nenhum feat escolhido')
        self.feat_label.setFont(QFont('Georgia', 9))
        self.feat_label.setStyleSheet('color: #888;')
        row.addWidget(self.feat_label, stretch=1)

        btn = QPushButton('Escolher Feat...')
        btn.setFont(QFont('Georgia', 9))
        btn.setStyleSheet(
            'QPushButton { background-color: #8B4513; color: #F5EBDC; border: 2px solid #654321;'
            ' border-radius: 4px; padding: 5px 14px; }'
            'QPushButton:hover { background-color: #A0522D; }'
        )
        btn.clicked.connect(self._open_feat_dialog)
        row.addWidget(btn)

        grp.setLayout(row)
        layout.addWidget(grp)

    def _open_feat_dialog(self):
        dlg = FeatDialog(self.character, self)
        if dlg.exec():
            feat = dlg.get_selected_feat()
            if feat:
                self.chosen_feat = feat
                self.chosen_feat_asi = dlg.get_asi_choice()
                self.chosen_feat_half_ability = dlg.get_half_feat_ability()
                self.chosen_feat_magic_initiate = dlg.get_magic_initiate_choice()
                self.feat_label.setText(f'✔  {feat.name}')
                self.feat_label.setStyleSheet('color: #2E7D32; font-weight: bold;')

    # ── Buttons ────────────────────────────────────────────────────────
    def _build_buttons(self, layout):
        row = QHBoxLayout()
        row.addStretch()

        ok_btn = QPushButton('Confirmar')
        ok_btn.setFont(QFont('Georgia', 10, QFont.Weight.Bold))
        ok_btn.setStyleSheet(
            'QPushButton { background-color: #8B4513; color: #F5EBDC; border: 2px solid #654321;'
            ' border-radius: 5px; padding: 8px 20px; }'
            'QPushButton:hover { background-color: #A0522D; }'
        )
        ok_btn.clicked.connect(self._accept)
        row.addWidget(ok_btn)

        cancel_btn = QPushButton('Cancelar')
        cancel_btn.setFont(QFont('Georgia', 10))
        cancel_btn.setStyleSheet(
            'QPushButton { background-color: #666; color: #fff; border: 2px solid #444;'
            ' border-radius: 5px; padding: 8px 20px; }'
            'QPushButton:hover { background-color: #888; }'
        )
        cancel_btn.clicked.connect(self.reject)
        row.addWidget(cancel_btn)

        layout.addLayout(row)

    # ── Validation & accept ────────────────────────────────────────────
    def _accept(self):
        is_vh = self.race_name == 'Variant Human'

        if is_vh:
            s1 = self.stat1_combo.currentData()
            s2 = self.stat2_combo.currentData()
            if s1 == s2:
                QMessageBox.warning(self, 'Atributos Iguais',
                                    'Os dois atributos devem ser diferentes.')
                return
            self.chosen_ability_bonuses = {s1: 1, s2: 1}
        else:
            s1 = self.stat1_combo.currentData()
            self.chosen_ability_bonuses = {s1: 2}

        if is_vh or (hasattr(self, 'skill_radio') and self.skill_radio.isChecked()):
            self.chosen_skill = self.skill_combo.currentText()
            self.chosen_darkvision = False
        else:
            self.chosen_skill = None
            self.chosen_darkvision = True

        if not self.chosen_feat:
            reply = QMessageBox.question(
                self, 'Feat não escolhido',
                'Você não escolheu um Feat. Continuar sem escolher agora?\n'
                '(Pode ser adicionado manualmente depois.)',
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        self.accept()

    # ── Result accessor ────────────────────────────────────────────────
    def get_results(self) -> dict:
        return {
            'ability_bonuses':       self.chosen_ability_bonuses,
            'skill':                 self.chosen_skill,
            'darkvision':            self.chosen_darkvision,
            'feat':                  self.chosen_feat,
            'feat_asi':              self.chosen_feat_asi,
            'feat_half_ability':     self.chosen_feat_half_ability,
            'feat_magic_initiate':   self.chosen_feat_magic_initiate,
        }
