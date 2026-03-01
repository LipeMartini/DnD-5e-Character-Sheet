class Weapon:
    """Representa uma arma em D&D 5e"""
    
    def __init__(self, name: str = "", damage_dice: str = "1d4", damage_type: str = "slashing",
                 properties: list = None, weapon_range: str = "melee", ability: str = "strength",
                 proficient: bool = False, magical_bonus: int = 0):
        self.name = name
        self.damage_dice = damage_dice  # Ex: "1d8", "2d6"
        self.damage_type = damage_type  # slashing, piercing, bludgeoning, etc.
        self.properties = properties or []  # finesse, versatile, two-handed, etc.
        self.weapon_range = weapon_range  # melee, ranged
        self.ability = ability  # strength ou dexterity
        self.proficient = proficient
        self.magical_bonus = magical_bonus  # +1, +2, +3 weapons
        self.equipped = False
    
    def get_attack_bonus(self, character) -> int:
        """Calcula o bônus de ataque"""
        bonus = 0
        
        # Modificador de atributo
        if self.ability == "strength":
            bonus += character.stats.get_modifier('strength')
        elif self.ability == "dexterity":
            bonus += character.stats.get_modifier('dexterity')
        
        # Proficiência (verifica automaticamente se o personagem é proficiente)
        if self.proficient or character.is_proficient_with_weapon(self):
            bonus += character.proficiency_bonus
        
        # Bônus mágico
        bonus += self.magical_bonus
        
        return bonus
    
    def get_damage_bonus(self, character) -> int:
        """Calcula o bônus de dano"""
        bonus = 0
        
        # Modificador de atributo
        if self.ability == "strength":
            bonus += character.stats.get_modifier('strength')
        elif self.ability == "dexterity":
            bonus += character.stats.get_modifier('dexterity')
        
        # Bônus mágico
        bonus += self.magical_bonus
        
        return bonus
    
    def has_property(self, prop: str) -> bool:
        """Verifica se a arma tem uma propriedade específica"""
        return prop.lower() in [p.lower() for p in self.properties]
    
    def to_dict(self) -> dict:
        """Serializa para dicionário"""
        return {
            'name': self.name,
            'damage_dice': self.damage_dice,
            'damage_type': self.damage_type,
            'properties': self.properties,
            'weapon_range': self.weapon_range,
            'ability': self.ability,
            'proficient': self.proficient,
            'magical_bonus': self.magical_bonus,
            'equipped': self.equipped
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Desserializa de dicionário"""
        weapon = Weapon(
            name=data.get('name', ''),
            damage_dice=data.get('damage_dice', '1d4'),
            damage_type=data.get('damage_type', 'slashing'),
            properties=data.get('properties', []),
            weapon_range=data.get('weapon_range', 'melee'),
            ability=data.get('ability', 'strength'),
            proficient=data.get('proficient', False),
            magical_bonus=data.get('magical_bonus', 0)
        )
        weapon.equipped = data.get('equipped', False)
        return weapon

# Armas pré-definidas comuns
COMMON_WEAPONS = {
    'Adaga': Weapon('Adaga', '1d4', 'piercing', ['finesse', 'light', 'thrown'], 'melee', 'dexterity'),
    'Espada Curta': Weapon('Espada Curta', '1d6', 'piercing', ['finesse', 'light'], 'melee', 'dexterity'),
    'Espada Longa': Weapon('Espada Longa', '1d8', 'slashing', ['versatile'], 'melee', 'strength'),
    'Machado de Batalha': Weapon('Machado de Batalha', '1d8', 'slashing', ['versatile'], 'melee', 'strength'),
    'Martelo de Guerra': Weapon('Martelo de Guerra', '1d8', 'bludgeoning', ['versatile'], 'melee', 'strength'),
    'Espada Grande': Weapon('Espada Grande', '2d6', 'slashing', ['heavy', 'two-handed'], 'melee', 'strength'),
    'Machado Grande': Weapon('Machado Grande', '1d12', 'slashing', ['heavy', 'two-handed'], 'melee', 'strength'),
    'Arco Curto': Weapon('Arco Curto', '1d6', 'piercing', ['ammunition', 'two-handed'], 'ranged', 'dexterity'),
    'Arco Longo': Weapon('Arco Longo', '1d8', 'piercing', ['ammunition', 'heavy', 'two-handed'], 'ranged', 'dexterity'),
    'Besta Leve': Weapon('Besta Leve', '1d8', 'piercing', ['ammunition', 'loading', 'two-handed'], 'ranged', 'dexterity'),
    'Cajado': Weapon('Cajado', '1d6', 'bludgeoning', ['versatile'], 'melee', 'strength'),
    'Lança': Weapon('Lança', '1d6', 'piercing', ['thrown', 'versatile'], 'melee', 'strength'),
}
