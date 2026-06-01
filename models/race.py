from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class Race:
    name: str
    ability_bonuses: Dict[str, int] = field(default_factory=dict)
    speed: int = 30
    size: str = "Medium"
    languages: List[str] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'ability_bonuses': self.ability_bonuses,
            'speed': self.speed,
            'size': self.size,
            'languages': self.languages,
            'traits': self.traits,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Race':
        return cls(**data)

class RaceDatabase:
    """Banco de dados de raças disponíveis"""
    
    @staticmethod
    def get_all_races() -> Dict[str, Race]:
        return {
            'Human': Race(
                name='Human',
                ability_bonuses={'strength': 1, 'dexterity': 1, 'constitution': 1, 
                               'intelligence': 1, 'wisdom': 1, 'charisma': 1},
                speed=30,
                size='Medium',
                languages=['Common', 'One extra language'],
                traits=['Versatile']
            ),
            'Elf': Race(
                name='Elf',
                ability_bonuses={'dexterity': 2},
                speed=30,
                size='Medium',
                languages=['Common', 'Elvish'],
                traits=['Darkvision', 'Keen Senses', 'Fey Ancestry', 'Trance']
            ),
            'Dwarf': Race(
                name='Dwarf',
                ability_bonuses={'constitution': 2},
                speed=25,
                size='Medium',
                languages=['Common', 'Dwarvish'],
                traits=['Darkvision', 'Dwarven Resilience', 'Dwarven Combat Training', 'Stonecunning']
            ),
            'Halfling': Race(
                name='Halfling',
                ability_bonuses={'dexterity': 2},
                speed=25,
                size='Small',
                languages=['Common', 'Halfling'],
                traits=['Lucky', 'Brave', 'Halfling Nimbleness']
            ),
            'Dragonborn': Race(
                name='Dragonborn',
                ability_bonuses={'strength': 2, 'charisma': 1},
                speed=30,
                size='Medium',
                languages=['Common', 'Draconic'],
                traits=['Draconic Ancestry', 'Breath Weapon', 'Damage Resistance']
            ),
            'Gnome': Race(
                name='Gnome',
                ability_bonuses={'intelligence': 2},
                speed=25,
                size='Small',
                languages=['Common', 'Gnomish'],
                traits=['Darkvision', 'Gnome Cunning']
            ),
            'Half-Elf': Race(
                name='Half-Elf',
                ability_bonuses={'charisma': 2},
                speed=30,
                size='Medium',
                languages=['Common', 'Elvish', 'One extra language'],
                traits=['Darkvision', 'Fey Ancestry']
            ),
            'Half-Orc': Race(
                name='Half-Orc',
                ability_bonuses={'strength': 2, 'constitution': 1},
                speed=30,
                size='Medium',
                languages=['Common', 'Orc'],
                traits=['Darkvision', 'Menacing', 'Relentless Endurance', 'Savage Attacks']
            ),
            'Tiefling': Race(
                name='Tiefling',
                ability_bonuses={'charisma': 2, 'intelligence': 1},
                speed=30,
                size='Medium',
                languages=['Common', 'Infernal'],
                traits=['Darkvision', 'Hellish Resistance', 'Infernal Legacy']
            ),
            'Variant Human': Race(
                name='Variant Human',
                ability_bonuses={},  # +1 em dois atributos à escolha (aplicado via racial_ability_choices)
                speed=30,
                size='Medium',
                languages=['Common', 'One extra language'],
                traits=['Variant Human Feat', 'Variant Human Skills']
            ),
            'Custom Lineage': Race(
                name='Custom Lineage',
                ability_bonuses={},  # +2 em um atributo à escolha (aplicado via racial_ability_choices)
                speed=30,
                size='Medium',
                languages=['Common'],
                traits=['Custom Lineage Feat', 'Custom Lineage Variable Trait']
            ),
        }
    
    @staticmethod
    def get_race(race_name: str) -> Race:
        races = RaceDatabase.get_all_races()
        return races.get(race_name, races['Human'])
