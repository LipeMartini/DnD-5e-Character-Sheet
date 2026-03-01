from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QWidget, QLabel, QPushButton, QListWidget, QListWidgetItem,
                             QGroupBox, QFormLayout, QLineEdit, QSpinBox, QComboBox,
                             QMessageBox, QFrame, QScrollArea, QGridLayout)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor
from models import Weapon, Armor, Item, COMMON_WEAPONS, COMMON_ARMORS, COMMON_ITEMS, Inventory

class InventoryWindow(QDialog):
    """Janela de gerenciamento de inventário"""
    
    inventory_updated = pyqtSignal()
    
    def __init__(self, character, parent=None):
        super().__init__(parent)
        self.character = character
        self.setWindowTitle("Inventário")
        self.setMinimumSize(900, 700)
        self.init_ui()
        self.apply_theme()
        self.update_display()
    
    def apply_theme(self):
        """Aplica tema medieval/pergaminho"""
        self.setStyleSheet("""
            QDialog {
                background-color: #F5E6D3;
            }
            QTabWidget::pane {
                border: 2px solid #8B4513;
                background-color: #FFF8DC;
                border-radius: 5px;
            }
            QTabBar::tab {
                background-color: #D2B48C;
                color: #654321;
                border: 2px solid #8B4513;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                padding: 8px 15px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #FFF8DC;
                color: #654321;
            }
            QGroupBox {
                border: 2px solid #8B4513;
                border-radius: 5px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: #FFF8DC;
                font-weight: bold;
                color: #654321;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px;
            }
            QListWidget {
                border: 2px solid #8B4513;
                border-radius: 5px;
                background-color: #FFFAF0;
                padding: 5px;
            }
            QListWidget::item {
                padding: 5px;
                border-bottom: 1px solid #D2B48C;
            }
            QListWidget::item:selected {
                background-color: #DEB887;
                color: #654321;
            }
            QPushButton {
                background-color: #8B4513;
                color: #F5EBDC;
                border: 2px solid #654321;
                border-radius: 5px;
                padding: 8px 15px;
                font-weight: bold;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #A0522D;
            }
            QPushButton:pressed {
                background-color: #654321;
            }
            QLineEdit, QSpinBox, QComboBox {
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 5px;
                background-color: #FFFAF0;
            }
            QLabel {
                color: #654321;
            }
        """)
    
    def init_ui(self):
        """Inicializa a interface"""
        layout = QVBoxLayout(self)
        
        # Título
        title = QLabel("🎒 INVENTÁRIO DO PERSONAGEM")
        title.setFont(QFont("Georgia", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("color: #654321; padding: 10px;")
        layout.addWidget(title)
        
        # Tabs para diferentes categorias
        self.tabs = QTabWidget()
        
        # Aba de Armas
        weapons_tab = self.create_weapons_tab()
        self.tabs.addTab(weapons_tab, "⚔️ Armas")
        
        # Aba de Armaduras
        armors_tab = self.create_armors_tab()
        self.tabs.addTab(armors_tab, "🛡️ Armaduras")
        
        # Aba de Itens
        items_tab = self.create_items_tab()
        self.tabs.addTab(items_tab, "📦 Itens")
        
        # Aba de Dinheiro
        money_tab = self.create_money_tab()
        self.tabs.addTab(money_tab, "💰 Dinheiro")
        
        layout.addWidget(self.tabs)
        
        # Rodapé com informações
        footer = self.create_footer()
        layout.addWidget(footer)
        
        # Botão de fechar
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)
    
    def create_weapons_tab(self):
        """Cria aba de armas"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Lista de armas
        weapons_group = QGroupBox("Armas no Inventário")
        weapons_layout = QVBoxLayout()
        
        self.weapons_list = QListWidget()
        self.weapons_list.itemClicked.connect(self.on_weapon_selected)
        weapons_layout.addWidget(self.weapons_list)
        
        # Botões de ação
        weapons_buttons = QHBoxLayout()
        
        equip_weapon_btn = QPushButton("Equipar/Desequipar")
        equip_weapon_btn.clicked.connect(self.toggle_weapon_equipped)
        weapons_buttons.addWidget(equip_weapon_btn)
        
        remove_weapon_btn = QPushButton("Remover")
        remove_weapon_btn.clicked.connect(self.remove_weapon)
        weapons_buttons.addWidget(remove_weapon_btn)
        
        weapons_layout.addLayout(weapons_buttons)
        weapons_group.setLayout(weapons_layout)
        layout.addWidget(weapons_group, 2)
        
        # Painel de adicionar arma
        add_panel = QGroupBox("Adicionar Arma")
        add_layout = QVBoxLayout()
        
        # Armas pré-definidas
        predefined_layout = QHBoxLayout()
        predefined_layout.addWidget(QLabel("Arma Comum:"))
        
        self.weapon_combo = QComboBox()
        self.weapon_combo.addItems(COMMON_WEAPONS.keys())
        predefined_layout.addWidget(self.weapon_combo)
        
        add_predefined_btn = QPushButton("Adicionar")
        add_predefined_btn.clicked.connect(self.add_common_weapon)
        predefined_layout.addWidget(add_predefined_btn)
        
        add_layout.addLayout(predefined_layout)
        
        # Arma customizada
        add_layout.addWidget(QLabel("Ou criar arma customizada:"))
        
        custom_form = QFormLayout()
        
        self.weapon_name_input = QLineEdit()
        custom_form.addRow("Nome:", self.weapon_name_input)
        
        self.weapon_damage_input = QLineEdit("1d8")
        custom_form.addRow("Dano:", self.weapon_damage_input)
        
        self.weapon_type_combo = QComboBox()
        self.weapon_type_combo.addItems(["slashing", "piercing", "bludgeoning", "fire", "cold", "lightning"])
        custom_form.addRow("Tipo de Dano:", self.weapon_type_combo)
        
        self.weapon_range_combo = QComboBox()
        self.weapon_range_combo.addItems(["melee", "ranged"])
        custom_form.addRow("Alcance:", self.weapon_range_combo)
        
        self.weapon_ability_combo = QComboBox()
        self.weapon_ability_combo.addItems(["strength", "dexterity"])
        custom_form.addRow("Atributo:", self.weapon_ability_combo)
        
        self.weapon_bonus_spin = QSpinBox()
        self.weapon_bonus_spin.setRange(0, 3)
        custom_form.addRow("Bônus Mágico:", self.weapon_bonus_spin)
        
        add_layout.addLayout(custom_form)
        
        add_custom_btn = QPushButton("Criar Arma")
        add_custom_btn.clicked.connect(self.add_custom_weapon)
        add_layout.addWidget(add_custom_btn)
        
        add_layout.addStretch()
        add_panel.setLayout(add_layout)
        layout.addWidget(add_panel, 1)
        
        return tab
    
    def create_armors_tab(self):
        """Cria aba de armaduras"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Lista de armaduras
        armors_group = QGroupBox("Armaduras no Inventário")
        armors_layout = QVBoxLayout()
        
        self.armors_list = QListWidget()
        self.armors_list.itemClicked.connect(self.on_armor_selected)
        armors_layout.addWidget(self.armors_list)
        
        # Botões de ação
        armors_buttons = QHBoxLayout()
        
        equip_armor_btn = QPushButton("Equipar/Desequipar")
        equip_armor_btn.clicked.connect(self.toggle_armor_equipped)
        armors_buttons.addWidget(equip_armor_btn)
        
        remove_armor_btn = QPushButton("Remover")
        remove_armor_btn.clicked.connect(self.remove_armor)
        armors_buttons.addWidget(remove_armor_btn)
        
        armors_layout.addLayout(armors_buttons)
        armors_group.setLayout(armors_layout)
        layout.addWidget(armors_group, 2)
        
        # Painel de adicionar armadura
        add_panel = QGroupBox("Adicionar Armadura")
        add_layout = QVBoxLayout()
        
        # Armaduras pré-definidas
        predefined_layout = QHBoxLayout()
        predefined_layout.addWidget(QLabel("Armadura Comum:"))
        
        self.armor_combo = QComboBox()
        self.armor_combo.addItems(COMMON_ARMORS.keys())
        predefined_layout.addWidget(self.armor_combo)
        
        add_predefined_btn = QPushButton("Adicionar")
        add_predefined_btn.clicked.connect(self.add_common_armor)
        predefined_layout.addWidget(add_predefined_btn)
        
        add_layout.addLayout(predefined_layout)
        
        # Seletor de método de cálculo de CA
        add_layout.addWidget(QLabel("\n⚙️ Método de Cálculo de CA:"))
        
        self.ac_method_combo = QComboBox()
        self.ac_method_combo.addItems([
            "Armadura (padrão)",
            "Defesa sem Armadura (Bárbaro)",
            "Defesa sem Armadura (Monge)",
            "Mage Armor",
            "Armadura Natural",
            "CA Customizada"
        ])
        self.ac_method_combo.currentIndexChanged.connect(self.on_ac_method_changed)
        add_layout.addWidget(self.ac_method_combo)
        
        # Campos para métodos especiais
        self.natural_armor_spin = QSpinBox()
        self.natural_armor_spin.setRange(10, 20)
        self.natural_armor_spin.setValue(10)
        self.natural_armor_spin.setPrefix("CA Base: ")
        self.natural_armor_spin.hide()
        add_layout.addWidget(self.natural_armor_spin)
        
        self.custom_ac_spin = QSpinBox()
        self.custom_ac_spin.setRange(10, 30)
        self.custom_ac_spin.setValue(10)
        self.custom_ac_spin.setPrefix("CA: ")
        self.custom_ac_spin.hide()
        add_layout.addWidget(self.custom_ac_spin)
        
        apply_ac_btn = QPushButton("Aplicar Método de CA")
        apply_ac_btn.clicked.connect(self.apply_ac_method)
        add_layout.addWidget(apply_ac_btn)
        
        add_layout.addStretch()
        add_panel.setLayout(add_layout)
        layout.addWidget(add_panel, 1)
        
        return tab
    
    def create_items_tab(self):
        """Cria aba de itens"""
        tab = QWidget()
        layout = QHBoxLayout(tab)
        
        # Lista de itens
        items_group = QGroupBox("Itens no Inventário")
        items_layout = QVBoxLayout()
        
        self.items_list = QListWidget()
        items_layout.addWidget(self.items_list)
        
        # Botões de ação
        items_buttons = QHBoxLayout()
        
        remove_item_btn = QPushButton("Remover")
        remove_item_btn.clicked.connect(self.remove_item)
        items_buttons.addWidget(remove_item_btn)
        
        items_layout.addLayout(items_buttons)
        items_group.setLayout(items_layout)
        layout.addWidget(items_group, 2)
        
        # Painel de adicionar item
        add_panel = QGroupBox("Adicionar Item")
        add_layout = QVBoxLayout()
        
        # Itens pré-definidos
        predefined_layout = QHBoxLayout()
        predefined_layout.addWidget(QLabel("Item Comum:"))
        
        self.item_combo = QComboBox()
        self.item_combo.addItems(COMMON_ITEMS.keys())
        predefined_layout.addWidget(self.item_combo)
        
        add_predefined_btn = QPushButton("Adicionar")
        add_predefined_btn.clicked.connect(self.add_common_item)
        predefined_layout.addWidget(add_predefined_btn)
        
        add_layout.addLayout(predefined_layout)
        
        # Item customizado
        add_layout.addWidget(QLabel("Ou criar item customizado:"))
        
        custom_form = QFormLayout()
        
        self.item_name_input = QLineEdit()
        custom_form.addRow("Nome:", self.item_name_input)
        
        self.item_desc_input = QLineEdit()
        custom_form.addRow("Descrição:", self.item_desc_input)
        
        self.item_quantity_spin = QSpinBox()
        self.item_quantity_spin.setRange(1, 999)
        self.item_quantity_spin.setValue(1)
        custom_form.addRow("Quantidade:", self.item_quantity_spin)
        
        self.item_weight_spin = QSpinBox()
        self.item_weight_spin.setRange(0, 100)
        self.item_weight_spin.setSuffix(" lb")
        custom_form.addRow("Peso:", self.item_weight_spin)
        
        add_layout.addLayout(custom_form)
        
        add_custom_btn = QPushButton("Criar Item")
        add_custom_btn.clicked.connect(self.add_custom_item)
        add_layout.addWidget(add_custom_btn)
        
        add_layout.addStretch()
        add_panel.setLayout(add_layout)
        layout.addWidget(add_panel, 1)
        
        return tab
    
    def create_money_tab(self):
        """Cria aba de dinheiro"""
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        money_group = QGroupBox("💰 Moedas")
        money_layout = QGridLayout()
        
        # Labels e spinboxes para cada tipo de moeda
        coins = [
            ("Platina (PP)", "platinum", "#E5E4E2"),
            ("Ouro (GP)", "gold", "#FFD700"),
            ("Electrum (EP)", "electrum", "#C0C0C0"),
            ("Prata (SP)", "silver", "#C0C0C0"),
            ("Cobre (CP)", "copper", "#B87333")
        ]
        
        self.coin_spins = {}
        
        for i, (name, key, color) in enumerate(coins):
            label = QLabel(name)
            label.setFont(QFont("Georgia", 12, QFont.Weight.Bold))
            label.setStyleSheet(f"color: {color}; background-color: #654321; padding: 5px; border-radius: 3px;")
            money_layout.addWidget(label, i, 0)
            
            spin = QSpinBox()
            spin.setRange(0, 999999)
            spin.setValue(getattr(self.character.inventory, key))
            spin.valueChanged.connect(lambda v, k=key: self.update_money(k, v))
            self.coin_spins[key] = spin
            money_layout.addWidget(spin, i, 1)
        
        money_group.setLayout(money_layout)
        layout.addWidget(money_group)
        
        # Conversor de moedas
        converter_group = QGroupBox("Conversor de Moedas")
        converter_layout = QFormLayout()
        
        converter_info = QLabel(
            "Taxas de conversão:\n"
            "1 PP = 10 GP\n"
            "1 GP = 10 SP\n"
            "1 SP = 10 CP\n"
            "1 EP = 5 SP"
        )
        converter_info.setStyleSheet("color: #654321; font-style: italic;")
        converter_layout.addRow(converter_info)
        
        converter_group.setLayout(converter_layout)
        layout.addWidget(converter_group)
        
        layout.addStretch()
        
        return tab
    
    def create_footer(self):
        """Cria rodapé com informações de peso e capacidade"""
        footer = QFrame()
        footer.setStyleSheet("""
            QFrame {
                background-color: #D2B48C;
                border: 2px solid #8B4513;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(footer)
        
        self.weight_label = QLabel("Peso Total: 0 lb")
        self.weight_label.setFont(QFont("Georgia", 11, QFont.Weight.Bold))
        layout.addWidget(self.weight_label)
        
        layout.addStretch()
        
        self.capacity_label = QLabel("Capacidade: 0 lb")
        self.capacity_label.setFont(QFont("Georgia", 11, QFont.Weight.Bold))
        layout.addWidget(self.capacity_label)
        
        return footer
    
    # ========== MÉTODOS DE ARMAS ==========
    
    def add_common_weapon(self):
        """Adiciona arma pré-definida"""
        weapon_name = self.weapon_combo.currentText()
        weapon = COMMON_WEAPONS[weapon_name]
        
        # Cria cópia da arma
        new_weapon = Weapon(
            name=weapon.name,
            damage_dice=weapon.damage_dice,
            damage_type=weapon.damage_type,
            properties=weapon.properties.copy(),
            weapon_range=weapon.weapon_range,
            ability=weapon.ability
        )
        
        self.character.inventory.add_weapon(new_weapon)
        self.update_weapons_list()
        self.update_footer()
        self.inventory_updated.emit()
    
    def add_custom_weapon(self):
        """Adiciona arma customizada"""
        name = self.weapon_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Digite um nome para a arma.")
            return
        
        weapon = Weapon(
            name=name,
            damage_dice=self.weapon_damage_input.text(),
            damage_type=self.weapon_type_combo.currentText(),
            weapon_range=self.weapon_range_combo.currentText(),
            ability=self.weapon_ability_combo.currentText(),
            magical_bonus=self.weapon_bonus_spin.value()
        )
        
        self.character.inventory.add_weapon(weapon)
        self.update_weapons_list()
        self.update_footer()
        self.inventory_updated.emit()
        
        # Limpa campos
        self.weapon_name_input.clear()
    
    def toggle_weapon_equipped(self):
        """Equipa/desequipa arma selecionada"""
        current_item = self.weapons_list.currentItem()
        if not current_item:
            return
        
        index = self.weapons_list.currentRow()
        weapon = self.character.inventory.weapons[index]
        weapon.equipped = not weapon.equipped
        
        self.update_weapons_list()
        self.inventory_updated.emit()
    
    def remove_weapon(self):
        """Remove arma selecionada"""
        current_item = self.weapons_list.currentItem()
        if not current_item:
            return
        
        index = self.weapons_list.currentRow()
        weapon = self.character.inventory.weapons[index]
        
        reply = QMessageBox.question(
            self, "Confirmar",
            f"Remover {weapon.name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.character.inventory.remove_weapon(weapon)
            self.update_weapons_list()
            self.update_footer()
            self.inventory_updated.emit()
    
    def on_weapon_selected(self, item):
        """Callback quando arma é selecionada"""
        pass
    
    def update_weapons_list(self):
        """Atualiza lista de armas"""
        self.weapons_list.clear()
        
        for weapon in self.character.inventory.weapons:
            equipped_mark = "✓ " if weapon.equipped else "  "
            icon = "⚔️" if weapon.weapon_range == "melee" else "🏹"
            bonus_text = f" +{weapon.magical_bonus}" if weapon.magical_bonus > 0 else ""
            
            # Indicador de proficiência
            is_proficient = self.character.is_proficient_with_weapon(weapon)
            prof_mark = "[P] " if is_proficient else "[NP] "
            
            item_text = f"{equipped_mark}{prof_mark}{icon} {weapon.name}{bonus_text} ({weapon.damage_dice})"
            
            item = QListWidgetItem(item_text)
            if weapon.equipped:
                item.setBackground(QColor("#DEB887"))
            elif not is_proficient:
                item.setForeground(QColor("#999999"))
            self.weapons_list.addItem(item)
    
    # ========== MÉTODOS DE ARMADURAS ==========
    
    def add_common_armor(self):
        """Adiciona armadura pré-definida"""
        armor_name = self.armor_combo.currentText()
        armor = COMMON_ARMORS[armor_name]
        
        # Cria cópia da armadura
        new_armor = Armor(
            name=armor.name,
            base_ac=armor.base_ac,
            armor_type=armor.armor_type,
            max_dex_bonus=armor.max_dex_bonus,
            strength_requirement=armor.strength_requirement,
            stealth_disadvantage=armor.stealth_disadvantage
        )
        
        self.character.inventory.add_armor(new_armor)
        self.update_armors_list()
        self.update_footer()
        self.inventory_updated.emit()
    
    def toggle_armor_equipped(self):
        """Equipa/desequipa armadura selecionada"""
        current_item = self.armors_list.currentItem()
        if not current_item:
            return
        
        index = self.armors_list.currentRow()
        armor = self.character.inventory.armors[index]
        
        # Se for escudo, pode equipar junto com armadura
        # Se for armadura, desequipa outras armaduras (exceto escudo)
        if armor.armor_type != Armor.SHIELD and armor.equipped == False:
            # Desequipa outras armaduras
            for other_armor in self.character.inventory.armors:
                if other_armor.armor_type != Armor.SHIELD:
                    other_armor.equipped = False
        
        armor.equipped = not armor.equipped
        
        self.update_armors_list()
        self.inventory_updated.emit()
    
    def remove_armor(self):
        """Remove armadura selecionada"""
        current_item = self.armors_list.currentItem()
        if not current_item:
            return
        
        index = self.armors_list.currentRow()
        armor = self.character.inventory.armors[index]
        
        reply = QMessageBox.question(
            self, "Confirmar",
            f"Remover {armor.name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.character.inventory.remove_armor(armor)
            self.update_armors_list()
            self.update_footer()
            self.inventory_updated.emit()
    
    def on_armor_selected(self, item):
        """Callback quando armadura é selecionada"""
        pass
    
    def update_armors_list(self):
        """Atualiza lista de armaduras"""
        self.armors_list.clear()
        
        for armor in self.character.inventory.armors:
            equipped_mark = "✓ " if armor.equipped else "  "
            icon = "🛡️"
            bonus_text = f" +{armor.magical_bonus}" if armor.magical_bonus > 0 else ""
            
            item_text = f"{equipped_mark}{icon} {armor.name}{bonus_text} (CA {armor.base_ac})"
            
            item = QListWidgetItem(item_text)
            if armor.equipped:
                item.setBackground(QColor("#DEB887"))
            self.armors_list.addItem(item)
    
    def on_ac_method_changed(self, index):
        """Mostra/esconde campos baseado no método de CA"""
        self.natural_armor_spin.hide()
        self.custom_ac_spin.hide()
        
        if index == 4:  # Armadura Natural
            self.natural_armor_spin.show()
        elif index == 5:  # CA Customizada
            self.custom_ac_spin.show()
    
    def apply_ac_method(self):
        """Aplica método de cálculo de CA selecionado"""
        method_index = self.ac_method_combo.currentIndex()
        
        methods = [
            Inventory.AC_ARMOR,
            Inventory.AC_UNARMORED_BARBARIAN,
            Inventory.AC_UNARMORED_MONK,
            Inventory.AC_MAGE_ARMOR,
            Inventory.AC_NATURAL,
            Inventory.AC_CUSTOM
        ]
        
        self.character.inventory.ac_calculation_method = methods[method_index]
        
        if method_index == 4:  # Armadura Natural
            self.character.inventory.natural_armor_base = self.natural_armor_spin.value()
        elif method_index == 5:  # CA Customizada
            self.character.inventory.custom_ac = self.custom_ac_spin.value()
        
        # Recalcula CA
        self.character.update_derived_stats()
        self.inventory_updated.emit()
        
        QMessageBox.information(self, "Sucesso", f"Método de CA atualizado!\nNova CA: {self.character.armor_class}")
    
    # ========== MÉTODOS DE ITENS ==========
    
    def add_common_item(self):
        """Adiciona item pré-definido"""
        item_name = self.item_combo.currentText()
        item = COMMON_ITEMS[item_name]
        
        # Cria cópia do item
        new_item = Item(
            name=item.name,
            description=item.description,
            quantity=item.quantity,
            weight=item.weight,
            value_gp=item.value_gp,
            item_type=item.item_type
        )
        
        self.character.inventory.add_item(new_item)
        self.update_items_list()
        self.update_footer()
    
    def add_custom_item(self):
        """Adiciona item customizado"""
        name = self.item_name_input.text().strip()
        if not name:
            QMessageBox.warning(self, "Aviso", "Digite um nome para o item.")
            return
        
        item = Item(
            name=name,
            description=self.item_desc_input.text(),
            quantity=self.item_quantity_spin.value(),
            weight=self.item_weight_spin.value()
        )
        
        self.character.inventory.add_item(item)
        self.update_items_list()
        self.update_footer()
        
        # Limpa campos
        self.item_name_input.clear()
        self.item_desc_input.clear()
    
    def remove_item(self):
        """Remove item selecionado"""
        current_item = self.items_list.currentItem()
        if not current_item:
            return
        
        index = self.items_list.currentRow()
        item = self.character.inventory.items[index]
        
        reply = QMessageBox.question(
            self, "Confirmar",
            f"Remover {item.name}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.character.inventory.remove_item(item)
            self.update_items_list()
            self.update_footer()
    
    def update_items_list(self):
        """Atualiza lista de itens"""
        self.items_list.clear()
        
        for item in self.character.inventory.items:
            item_text = f"📦 {item.name} x{item.quantity}"
            if item.description:
                item_text += f" - {item.description}"
            
            self.items_list.addItem(item_text)
    
    # ========== MÉTODOS DE DINHEIRO ==========
    
    def update_money(self, coin_type, value):
        """Atualiza quantidade de moedas"""
        setattr(self.character.inventory, coin_type, value)
        self.update_footer()
    
    # ========== MÉTODOS GERAIS ==========
    
    def update_display(self):
        """Atualiza toda a exibição"""
        self.update_weapons_list()
        self.update_armors_list()
        self.update_items_list()
        self.update_footer()
        
        # Atualiza método de CA selecionado
        method_map = {
            Inventory.AC_ARMOR: 0,
            Inventory.AC_UNARMORED_BARBARIAN: 1,
            Inventory.AC_UNARMORED_MONK: 2,
            Inventory.AC_MAGE_ARMOR: 3,
            Inventory.AC_NATURAL: 4,
            Inventory.AC_CUSTOM: 5
        }
        
        current_method = self.character.inventory.ac_calculation_method
        self.ac_method_combo.setCurrentIndex(method_map.get(current_method, 0))
        
        self.natural_armor_spin.setValue(self.character.inventory.natural_armor_base)
        self.custom_ac_spin.setValue(self.character.inventory.custom_ac)
    
    def update_footer(self):
        """Atualiza informações de peso e capacidade"""
        total_weight = self.character.inventory.get_total_weight()
        capacity = self.character.inventory.get_carrying_capacity(self.character)
        
        self.weight_label.setText(f"Peso Total: {total_weight} lb")
        self.capacity_label.setText(f"Capacidade: {capacity} lb")
        
        # Muda cor se estiver sobrecarregado
        if total_weight > capacity:
            self.weight_label.setStyleSheet("color: #D32F2F; font-weight: bold;")
        else:
            self.weight_label.setStyleSheet("color: #654321; font-weight: bold;")
