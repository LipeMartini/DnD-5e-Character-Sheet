class Item:
    """Representa um item genérico no inventário"""
    
    def __init__(self, name: str = "", description: str = "", quantity: int = 1,
                 weight: float = 0.0, value_gp: float = 0.0, item_type: str = "misc"):
        self.name = name
        self.description = description
        self.quantity = quantity
        self.weight = weight  # em libras
        self.value_gp = value_gp  # valor em peças de ouro
        self.item_type = item_type  # misc, consumable, tool, etc.
    
    def total_weight(self) -> float:
        """Retorna o peso total (peso × quantidade)"""
        return self.weight * self.quantity
    
    def total_value(self) -> float:
        """Retorna o valor total (valor × quantidade)"""
        return self.value_gp * self.quantity
    
    def to_dict(self) -> dict:
        """Serializa para dicionário"""
        return {
            'name': self.name,
            'description': self.description,
            'quantity': self.quantity,
            'weight': self.weight,
            'value_gp': self.value_gp,
            'item_type': self.item_type
        }
    
    @staticmethod
    def from_dict(data: dict):
        """Desserializa de dicionário"""
        return Item(
            name=data.get('name', ''),
            description=data.get('description', ''),
            quantity=data.get('quantity', 1),
            weight=data.get('weight', 0.0),
            value_gp=data.get('value_gp', 0.0),
            item_type=data.get('item_type', 'misc')
        )

# Itens comuns pré-definidos
COMMON_ITEMS = {
    'Poção de Cura': Item('Poção de Cura', 'Recupera 2d4+2 HP', 1, 0.5, 50, 'consumable'),
    'Poção de Cura Maior': Item('Poção de Cura Maior', 'Recupera 4d4+4 HP', 1, 0.5, 150, 'consumable'),
    'Antídoto': Item('Antídoto', 'Cura envenenamento', 1, 0.1, 50, 'consumable'),
    'Tocha': Item('Tocha', 'Ilumina 20 pés por 1 hora', 1, 1.0, 0.01, 'tool'),
    'Corda (50 pés)': Item('Corda (50 pés)', 'Corda de cânhamo', 1, 10.0, 1, 'tool'),
    'Mochila': Item('Mochila', 'Capacidade de 30 libras', 1, 5.0, 2, 'tool'),
    'Kit de Ladrão': Item('Kit de Ladrão', 'Ferramentas para arrombar fechaduras', 1, 1.0, 25, 'tool'),
    'Ração (1 dia)': Item('Ração (1 dia)', 'Comida para um dia', 1, 2.0, 0.5, 'consumable'),
    'Cantil': Item('Cantil', 'Armazena água', 1, 5.0, 0.2, 'tool'),
}
