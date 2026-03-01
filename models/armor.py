class Armor:
    """Representa uma armadura em D&D 5e"""
    
    # Tipos de armadura
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"
    SHIELD = "shield"
    
    def __init__(self, name: str = "", base_ac: int = 10, armor_type: str = "light",
                 max_dex_bonus: int = None, strength_requirement: int = 0,
                 stealth_disadvantage: bool = False, magical_bonus: int = 0):
        self.name = name
        self.base_ac = base_ac
        self.armor_type = armor_type
        self.max_dex_bonus = max_dex_bonus  # None = sem limite
        self.strength_requirement = strength_requirement
        self.stealth_disadvantage = stealth_disadvantage
        self.magical_bonus = magical_bonus
        self.equipped = False
    
    def calculate_ac(self, dex_modifier: int) -> int:
        """Calcula a CA fornecida por esta armadura"""
        ac = self.base_ac + self.magical_bonus
        
        # Adiciona modificador de DEX se aplicável
        if self.armor_type in [self.LIGHT, self.MEDIUM]:
            if self.max_dex_bonus is not None:
                ac += min(dex_modifier, self.max_dex_bonus)
            else:
                ac += dex_modifier
        
        return ac
    
    def to_dict(self) -> dict:
        """Serializa para dicionário"""
        return {
            'name': self.name,
            'base_ac': self.base_ac,
            'armor_type': self.armor_type,
            'max_dex_bonus': self.max_dex_bonus,
            'strength_requirement': self.strength_requirement,
            'stealth_disadvantage': self.stealth_disadvantage,
            'magical_bonus': self.magical_bonus,
            'equipped': self.equipped
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Desserializa de dicionário"""
        armor = Armor(
            name=data.get('name', ''),
            base_ac=data.get('base_ac', 10),
            armor_type=data.get('armor_type', 'light'),
            max_dex_bonus=data.get('max_dex_bonus'),
            strength_requirement=data.get('strength_requirement', 0),
            stealth_disadvantage=data.get('stealth_disadvantage', False),
            magical_bonus=data.get('magical_bonus', 0)
        )
        armor.equipped = data.get('equipped', False)
        return armor

# Armaduras pré-definidas comuns
COMMON_ARMORS = {
    # Light Armor
    'Armadura Acolchoada': Armor('Armadura Acolchoada', 11, Armor.LIGHT, stealth_disadvantage=True),
    'Armadura de Couro': Armor('Armadura de Couro', 11, Armor.LIGHT),
    'Armadura de Couro Batido': Armor('Armadura de Couro Batido', 12, Armor.LIGHT),
    
    # Medium Armor
    'Gibão de Peles': Armor('Gibão de Peles', 12, Armor.MEDIUM, max_dex_bonus=2),
    'Camisão de Malha': Armor('Camisão de Malha', 13, Armor.MEDIUM, max_dex_bonus=2),
    'Brunea': Armor('Brunea', 14, Armor.MEDIUM, max_dex_bonus=2, stealth_disadvantage=True),
    'Peitoral': Armor('Peitoral', 14, Armor.MEDIUM, max_dex_bonus=2),
    'Meia-Armadura': Armor('Meia-Armadura', 15, Armor.MEDIUM, max_dex_bonus=2, stealth_disadvantage=True),
    
    # Heavy Armor
    'Cota de Anéis': Armor('Cota de Anéis', 14, Armor.HEAVY, max_dex_bonus=0, stealth_disadvantage=True),
    'Cota de Malha': Armor('Cota de Malha', 16, Armor.HEAVY, max_dex_bonus=0, strength_requirement=13, stealth_disadvantage=True),
    'Cota de Talas': Armor('Cota de Talas', 17, Armor.HEAVY, max_dex_bonus=0, strength_requirement=15, stealth_disadvantage=True),
    'Armadura Completa': Armor('Armadura Completa', 18, Armor.HEAVY, max_dex_bonus=0, strength_requirement=15, stealth_disadvantage=True),
    
    # Shield
    'Escudo': Armor('Escudo', 2, Armor.SHIELD),
}
