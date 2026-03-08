from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class SpellcastingInfo:
    """Informações de conjuração de magias do personagem"""
    spellcasting_ability: str = 'intelligence'  # intelligence, wisdom, charisma
    spell_save_dc: int = 8
    spell_attack_bonus: int = 0
    
    # Spell slots máximos por nível (índice 0 = cantrips, 1-9 = níveis de magia)
    max_spell_slots: List[int] = field(default_factory=lambda: [0] * 10)
    
    # Spell slots atuais (gastados durante o dia)
    current_spell_slots: List[int] = field(default_factory=lambda: [0] * 10)
    
    # Magias conhecidas (para Sorcerer, Bard, Warlock, Ranger)
    known_spells: List[str] = field(default_factory=list)
    
    # Magias preparadas (para Wizard, Cleric, Druid, Paladin)
    prepared_spells: List[str] = field(default_factory=list)
    
    # Cantrips conhecidos
    known_cantrips: List[str] = field(default_factory=list)
    
    # Tracking de usos diários de Magic Initiate (spell_name -> uses_remaining)
    magic_initiate_daily_uses: Dict[str, int] = field(default_factory=dict)
    
    def to_dict(self) -> dict:
        return {
            'spellcasting_ability': self.spellcasting_ability,
            'spell_save_dc': self.spell_save_dc,
            'spell_attack_bonus': self.spell_attack_bonus,
            'max_spell_slots': self.max_spell_slots,
            'current_spell_slots': self.current_spell_slots,
            'known_spells': self.known_spells,
            'prepared_spells': self.prepared_spells,
            'known_cantrips': self.known_cantrips,
            'magic_initiate_daily_uses': self.magic_initiate_daily_uses,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'SpellcastingInfo':
        return cls(**data)
    
    def has_spell_slot(self, level: int) -> bool:
        """Verifica se tem spell slot disponível para um nível"""
        if level < 1 or level > 9:
            return False
        return self.current_spell_slots[level] > 0
    
    def use_spell_slot(self, level: int) -> bool:
        """Usa um spell slot de um nível específico"""
        if not self.has_spell_slot(level):
            return False
        self.current_spell_slots[level] -= 1
        return True
    
    def restore_spell_slots(self):
        """Restaura todos os spell slots (descanso longo)"""
        self.current_spell_slots = self.max_spell_slots.copy()
        # Restaura usos de Magic Initiate
        for spell_name in self.magic_initiate_daily_uses:
            self.magic_initiate_daily_uses[spell_name] = 1
    
    def get_available_slots(self, level: int) -> int:
        """Retorna quantos slots estão disponíveis para um nível"""
        if level < 1 or level > 9:
            return 0
        return self.current_spell_slots[level]
    
    def get_max_slots(self, level: int) -> int:
        """Retorna quantos slots máximos existem para um nível"""
        if level < 1 or level > 9:
            return 0
        return self.max_spell_slots[level]


class SpellSlotTable:
    """Tabelas de spell slots por nível de classe"""
    
    # Full casters: Wizard, Sorcerer, Cleric, Druid, Bard
    FULL_CASTER_SLOTS = {
        1:  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        2:  [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
        4:  [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
        6:  [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
        7:  [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],
        8:  [0, 4, 3, 3, 2, 0, 0, 0, 0, 0],
        9:  [0, 4, 3, 3, 3, 1, 0, 0, 0, 0],
        10: [0, 4, 3, 3, 3, 2, 0, 0, 0, 0],
        11: [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],
        12: [0, 4, 3, 3, 3, 2, 1, 0, 0, 0],
        13: [0, 4, 3, 3, 3, 2, 1, 1, 0, 0],
        14: [0, 4, 3, 3, 3, 2, 1, 1, 0, 0],
        15: [0, 4, 3, 3, 3, 2, 1, 1, 1, 0],
        16: [0, 4, 3, 3, 3, 2, 1, 1, 1, 0],
        17: [0, 4, 3, 3, 3, 2, 1, 1, 1, 1],
        18: [0, 4, 3, 3, 3, 3, 1, 1, 1, 1],
        19: [0, 4, 3, 3, 3, 3, 2, 1, 1, 1],
        20: [0, 4, 3, 3, 3, 3, 2, 2, 1, 1],
    }
    
    # Half casters: Paladin, Ranger
    HALF_CASTER_SLOTS = {
        1:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        2:  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        4:  [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
        6:  [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
        8:  [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
        9:  [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
        10: [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
        11: [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
        12: [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
        13: [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],
        14: [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],
        15: [0, 4, 3, 3, 2, 0, 0, 0, 0, 0],
        16: [0, 4, 3, 3, 2, 0, 0, 0, 0, 0],
        17: [0, 4, 3, 3, 3, 1, 0, 0, 0, 0],
        18: [0, 4, 3, 3, 3, 1, 0, 0, 0, 0],
        19: [0, 4, 3, 3, 3, 2, 0, 0, 0, 0],
        20: [0, 4, 3, 3, 3, 2, 0, 0, 0, 0],
    }
    
    # Third casters: Eldritch Knight, Arcane Trickster
    THIRD_CASTER_SLOTS = {
        1:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        2:  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        4:  [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        6:  [0, 3, 0, 0, 0, 0, 0, 0, 0, 0],
        7:  [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
        8:  [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
        9:  [0, 4, 2, 0, 0, 0, 0, 0, 0, 0],
        10: [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
        11: [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
        12: [0, 4, 3, 0, 0, 0, 0, 0, 0, 0],
        13: [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
        14: [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
        15: [0, 4, 3, 2, 0, 0, 0, 0, 0, 0],
        16: [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
        17: [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
        18: [0, 4, 3, 3, 0, 0, 0, 0, 0, 0],
        19: [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],
        20: [0, 4, 3, 3, 1, 0, 0, 0, 0, 0],
    }
    
    # Warlock (Pact Magic - funciona diferente)
    WARLOCK_SLOTS = {
        1:  [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        2:  [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
        3:  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        4:  [0, 0, 2, 0, 0, 0, 0, 0, 0, 0],
        5:  [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
        6:  [0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
        7:  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        8:  [0, 0, 0, 0, 2, 0, 0, 0, 0, 0],
        9:  [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        10: [0, 0, 0, 0, 0, 2, 0, 0, 0, 0],
        11: [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        12: [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        13: [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        14: [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        15: [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        16: [0, 0, 0, 0, 0, 3, 0, 0, 0, 0],
        17: [0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
        18: [0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
        19: [0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
        20: [0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    }
    
    @staticmethod
    def get_third_caster_slots(level: int) -> List[int]:
        """Retorna os spell slots para 1/3 casters (Eldritch Knight, Arcane Trickster)"""
        if level < 1 or level > 20:
            return [0] * 10
        return SpellSlotTable.THIRD_CASTER_SLOTS.get(level, [0] * 10)
    
    @staticmethod
    def get_spell_slots(class_name: str, level: int) -> List[int]:
        """Retorna os spell slots para uma classe e nível específicos"""
        if level < 1 or level > 20:
            return [0] * 10
        
        # Full casters
        if class_name in ['Wizard', 'Sorcerer', 'Cleric', 'Druid', 'Bard']:
            return SpellSlotTable.FULL_CASTER_SLOTS.get(level, [0] * 10)
        
        # Half casters
        elif class_name in ['Paladin', 'Ranger']:
            return SpellSlotTable.HALF_CASTER_SLOTS.get(level, [0] * 10)
        
        # Warlock (Pact Magic)
        elif class_name == 'Warlock':
            return SpellSlotTable.WARLOCK_SLOTS.get(level, [0] * 10)
        
        # Non-casters
        else:
            return [0] * 10
    
    @staticmethod
    def get_spellcasting_ability(class_name: str) -> str:
        """Retorna a habilidade de conjuração para uma classe"""
        ability_map = {
            'Wizard': 'intelligence',
            'Sorcerer': 'charisma',
            'Warlock': 'charisma',
            'Bard': 'charisma',
            'Cleric': 'wisdom',
            'Druid': 'wisdom',
            'Paladin': 'charisma',
            'Ranger': 'wisdom',
        }
        return ability_map.get(class_name, 'intelligence')
    
    @staticmethod
    def uses_prepared_spells(class_name: str) -> bool:
        """Verifica se a classe prepara magias (vs conhece magias)"""
        prepared_casters = ['Wizard', 'Cleric', 'Druid', 'Paladin']
        return class_name in prepared_casters
    
    @staticmethod
    def get_cantrips_known(class_name: str, level: int) -> int:
        """Retorna quantos cantrips a classe conhece em um nível"""
        cantrip_tables = {
            'Wizard': {1: 3, 4: 4, 10: 5},
            'Sorcerer': {1: 4, 4: 5, 10: 6},
            'Cleric': {1: 3, 4: 4, 10: 5},
            'Druid': {1: 2, 4: 3, 10: 4},
            'Bard': {1: 2, 4: 3, 10: 4},
            'Warlock': {1: 2, 4: 3, 10: 4},
        }
        
        if class_name not in cantrip_tables:
            return 0
        
        table = cantrip_tables[class_name]
        cantrips = 0
        for lvl in sorted(table.keys()):
            if level >= lvl:
                cantrips = table[lvl]
        
        return cantrips
    
    @staticmethod
    def get_spells_known(character, level: int) -> int:
        """Retorna quantas magias o personagem conhece (para classes que não preparam)"""
        # Determinar qual "classe" usar para a tabela
        # Prioriza subclasse se for spellcaster (Eldritch Knight, Arcane Trickster)
        lookup_name = None
        
        if hasattr(character, 'subclass_name') and character.subclass_name:
            if character.subclass_name in ['Eldritch Knight', 'Arcane Trickster']:
                lookup_name = character.subclass_name
        
        # Se não é subclasse spellcaster, usa a classe principal
        if not lookup_name and character.character_class:
            lookup_name = character.character_class.name
        
        if not lookup_name:
            return 0
        
        # Wizard e Cleric preparam, não têm limite de "conhecidas" (têm spellbook/domínio)
        if lookup_name in ['Wizard', 'Cleric', 'Druid', 'Paladin']:
            return 999  # Sem limite (preparam do total disponível)
        
        spells_known_tables = {
            'Sorcerer': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 11, 11: 12, 12: 12, 13: 13, 14: 13, 15: 14, 16: 14, 17: 15, 18: 15, 19: 15, 20: 15},
            'Bard': {1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9, 7: 10, 8: 11, 9: 12, 10: 14, 11: 15, 12: 15, 13: 16, 14: 18, 15: 19, 16: 19, 17: 20, 18: 22, 19: 22, 20: 22},
            'Ranger': {1: 0, 2: 2, 3: 3, 4: 3, 5: 4, 6: 4, 7: 5, 8: 5, 9: 6, 10: 6, 11: 7, 12: 7, 13: 8, 14: 8, 15: 9, 16: 9, 17: 10, 18: 10, 19: 11, 20: 11},
            'Warlock': {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 8, 8: 9, 9: 10, 10: 10, 11: 11, 12: 11, 13: 12, 14: 12, 15: 13, 16: 13, 17: 14, 18: 14, 19: 15, 20: 15},
            'Arcane Trickster': {1: 0, 2: 0, 3: 3, 4: 4, 5: 4, 6: 4, 7: 5, 8: 6, 9: 6, 10: 7, 11: 8, 12: 8, 13: 9, 14: 10, 15: 10, 16: 11, 17: 11, 18: 11, 19: 12, 20: 13},
            'Eldritch Knight': {1: 0, 2: 0, 3: 3, 4: 4, 5: 4, 6: 4, 7: 5, 8: 6, 9: 6, 10: 7, 11: 8, 12: 8, 13: 9, 14: 10, 15: 10, 16: 11, 17: 11, 18: 11, 19: 12, 20: 13}
        }
        
        if lookup_name not in spells_known_tables:
            return 0
        
        return spells_known_tables[lookup_name].get(level, 0)
