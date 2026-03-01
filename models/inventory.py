from .weapon import Weapon
from .armor import Armor
from .item import Item

class Inventory:
    """Gerencia o inventário do personagem"""
    
    # Métodos de cálculo de CA
    AC_ARMOR = "armor"  # 10 + Armor Base + DEX mod (limitado pelo tipo de armadura)
    AC_UNARMORED_BARBARIAN = "unarmored_barbarian"  # 10 + DEX mod + CON mod
    AC_UNARMORED_MONK = "unarmored_monk"  # 10 + DEX mod + WIS mod
    AC_MAGE_ARMOR = "mage_armor"  # 13 + DEX mod
    AC_NATURAL = "natural"  # Base natural + DEX mod
    AC_CUSTOM = "custom"  # Valor manual
    
    def __init__(self):
        self.weapons = []
        self.armors = []
        self.items = []
        
        # Dinheiro
        self.copper = 0
        self.silver = 0
        self.electrum = 0
        self.gold = 0
        self.platinum = 0
        
        # Configuração de CA
        self.ac_calculation_method = self.AC_ARMOR
        self.natural_armor_base = 10
        self.custom_ac = 10
    
    def add_weapon(self, weapon: Weapon):
        """Adiciona uma arma ao inventário"""
        self.weapons.append(weapon)
    
    def remove_weapon(self, weapon: Weapon):
        """Remove uma arma do inventário"""
        if weapon in self.weapons:
            self.weapons.remove(weapon)
    
    def add_armor(self, armor: Armor):
        """Adiciona uma armadura ao inventário"""
        self.armors.append(armor)
    
    def remove_armor(self, armor: Armor):
        """Remove uma armadura do inventário"""
        if armor in self.armors:
            self.armors.remove(armor)
    
    def add_item(self, item: Item):
        """Adiciona um item ao inventário"""
        # Verifica se já existe item com mesmo nome
        for existing_item in self.items:
            if existing_item.name == item.name:
                existing_item.quantity += item.quantity
                return
        self.items.append(item)
    
    def remove_item(self, item: Item):
        """Remove um item do inventário"""
        if item in self.items:
            self.items.remove(item)
    
    def get_equipped_armor(self) -> Armor:
        """Retorna a armadura equipada (não escudo)"""
        for armor in self.armors:
            if armor.equipped and armor.armor_type != Armor.SHIELD:
                return armor
        return None
    
    def get_equipped_shield(self) -> Armor:
        """Retorna o escudo equipado"""
        for armor in self.armors:
            if armor.equipped and armor.armor_type == Armor.SHIELD:
                return armor
        return None
    
    def get_equipped_weapons(self) -> list:
        """Retorna lista de armas equipadas"""
        return [w for w in self.weapons if w.equipped]
    
    def calculate_armor_class(self, character) -> int:
        """Calcula a CA baseado no método selecionado"""
        dex_mod = character.stats.get_modifier('dexterity')
        
        if self.ac_calculation_method == self.AC_ARMOR:
            # CA baseada em armadura
            armor = self.get_equipped_armor()
            if armor:
                ac = armor.calculate_ac(dex_mod)
            else:
                # Sem armadura = 10 + DEX
                ac = 10 + dex_mod
            
            # Adiciona escudo
            shield = self.get_equipped_shield()
            if shield:
                ac += shield.base_ac + shield.magical_bonus
            
            return ac
        
        elif self.ac_calculation_method == self.AC_UNARMORED_BARBARIAN:
            # Defesa sem armadura do Bárbaro
            con_mod = character.stats.get_modifier('constitution')
            ac = 10 + dex_mod + con_mod
            
            # Escudo ainda pode ser usado
            shield = self.get_equipped_shield()
            if shield:
                ac += shield.base_ac + shield.magical_bonus
            
            return ac
        
        elif self.ac_calculation_method == self.AC_UNARMORED_MONK:
            # Defesa sem armadura do Monge
            wis_mod = character.stats.get_modifier('wisdom')
            return 10 + dex_mod + wis_mod
        
        elif self.ac_calculation_method == self.AC_MAGE_ARMOR:
            # Mage Armor spell
            return 13 + dex_mod
        
        elif self.ac_calculation_method == self.AC_NATURAL:
            # Armadura natural (ex: raças específicas)
            return self.natural_armor_base + dex_mod
        
        elif self.ac_calculation_method == self.AC_CUSTOM:
            # CA customizada
            return self.custom_ac
        
        return 10
    
    def get_total_weight(self) -> float:
        """Calcula o peso total do inventário"""
        total = 0.0
        
        # Armas
        for weapon in self.weapons:
            total += 3.0  # Peso médio de arma (simplificado)
        
        # Armaduras
        for armor in self.armors:
            if armor.armor_type == Armor.LIGHT:
                total += 10.0
            elif armor.armor_type == Armor.MEDIUM:
                total += 20.0
            elif armor.armor_type == Armor.HEAVY:
                total += 40.0
            elif armor.armor_type == Armor.SHIELD:
                total += 6.0
        
        # Itens
        for item in self.items:
            total += item.total_weight()
        
        # Moedas (50 moedas = 1 libra)
        total_coins = self.copper + self.silver + self.electrum + self.gold + self.platinum
        total += total_coins / 50.0
        
        return round(total, 2)
    
    def get_carrying_capacity(self, character) -> int:
        """Calcula a capacidade de carga (FOR × 15)"""
        return character.stats.strength * 15
    
    def to_dict(self) -> dict:
        """Serializa para dicionário"""
        return {
            'weapons': [w.to_dict() for w in self.weapons],
            'armors': [a.to_dict() for a in self.armors],
            'items': [i.to_dict() for i in self.items],
            'copper': self.copper,
            'silver': self.silver,
            'electrum': self.electrum,
            'gold': self.gold,
            'platinum': self.platinum,
            'ac_calculation_method': self.ac_calculation_method,
            'natural_armor_base': self.natural_armor_base,
            'custom_ac': self.custom_ac
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Desserializa de dicionário"""
        inventory = Inventory()
        
        # Armas
        for weapon_data in data.get('weapons', []):
            inventory.weapons.append(Weapon.from_dict(weapon_data))
        
        # Armaduras
        for armor_data in data.get('armors', []):
            inventory.armors.append(Armor.from_dict(armor_data))
        
        # Itens
        for item_data in data.get('items', []):
            inventory.items.append(Item.from_dict(item_data))
        
        # Dinheiro
        inventory.copper = data.get('copper', 0)
        inventory.silver = data.get('silver', 0)
        inventory.electrum = data.get('electrum', 0)
        inventory.gold = data.get('gold', 0)
        inventory.platinum = data.get('platinum', 0)
        
        # Configuração de CA
        inventory.ac_calculation_method = data.get('ac_calculation_method', Inventory.AC_ARMOR)
        inventory.natural_armor_base = data.get('natural_armor_base', 10)
        inventory.custom_ac = data.get('custom_ac', 10)
        
        return inventory
