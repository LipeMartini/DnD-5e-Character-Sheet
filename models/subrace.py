from dataclasses import dataclass, field
from typing import Dict, List, Optional

@dataclass
class Subrace:
    name: str
    parent_race: str  # ← Importante! Liga a subrace à race
    ability_bonuses: Dict[str, int]
    traits: List[str]
    skill_proficiencies_count: int
    speed: Optional[int] = None
    languages: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'parent_race': self.parent_race,
            'ability_bonuses': self.ability_bonuses,
            'traits': self.traits,
            'skill_proficiencies_count': self.skill_proficiencies_count,
            'speed': self.speed,
            'languages': self.languages,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Subrace':
        return cls(**data)
    
class SubraceDatabase:
    @staticmethod
    def get_subraces_for_race(race_name: str) -> Dict[str, Subrace]:
        """Retorna apenas as subraças disponíveis para uma raça"""
        all_subraces = SubraceDatabase.get_all_subraces()
        return {sr.name: sr for sr in all_subraces.values() 
                if sr.parent_race == race_name}
    
    @staticmethod
    def get_all_subraces() -> Dict[str, Subrace]:
        return {
            'None': Subrace(
                name='None',
                parent_race='None',
                ability_bonuses={},
                traits=[],
                skill_proficiencies_count=0
            ),
            'Dark Elf': Subrace(
                name='Dark Elf',
                parent_race='Elf',
                ability_bonuses={'charisma': 1},
                traits=['Superior Darkvision', 'Sunlight Sensitivity', 'Drow Magic', 'Drow Weapon Training'],
                skill_proficiencies_count=0
            ),
            'High Elf': Subrace(
                name='High Elf',
                parent_race='Elf',
                ability_bonuses={'intelligence': 1},
                traits=['Cantrips', 'Elf Weapon Training', 'Extra Language'],
                skill_proficiencies_count=0
            ),
            'Wood Elf': Subrace(
                name='Wood Elf',
                parent_race='Elf',
                ability_bonuses={'wisdom': 1},
                traits=['Elf Weapon Training', 'Fleet of Foot', 'Mask of the Wild'],
                skill_proficiencies_count=0,
                speed=35
            ),
            'Hill Dwarf': Subrace(
                name= 'Hill Dwarf',
                parent_race='Dwarf',
                ability_bonuses={'wisdom': 1},
                traits=['Dwarven Toughness'],
                skill_proficiencies_count=0,
            ),
            'Mountain Dwarf': Subrace(
                name= 'Mountain Dwarf',
                parent_race='Dwarf',
                ability_bonuses={'strength': 2},
                traits=['Dwarven Armor Training'],
                skill_proficiencies_count=0,
            ),
            'Lightfoot Halfling': Subrace(
                name='Lightfoot Halfling',
                parent_race='Halfling',
                ability_bonuses={'charisma': 1},
                traits=['Naturally Stealthy'],
                skill_proficiencies_count=0,
            ),
            'Stout Halfling': Subrace(
                name='Stout Halfling',
                parent_race='Halfling',
                ability_bonuses={'constitution': 1},
                traits=['Stout Resilience'],
                skill_proficiencies_count=0,
            ),
            'Black Dragonborn': Subrace(
                name='Black Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Acid Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Blue Dragonborn': Subrace(
                name='Blue Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Lightning Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Brass Dragonborn': Subrace(
                name='Brass Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Fire Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Bronze Dragonborn': Subrace(
                name='Bronze Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Lightning Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Copper Dragonborn': Subrace(
                name='Copper Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Acid Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Gold Dragonborn': Subrace(
                name='Gold Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Fire Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Green Dragonborn': Subrace(
                name='Green Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Poison Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Red Dragonborn': Subrace(
                name='Red Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Fire Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Silver Dragonborn': Subrace(
                name='Silver Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Cold Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'White Dragonborn': Subrace(
                name='White Dragonborn',
                parent_race='Dragonborn',
                ability_bonuses={},
                traits=['Cold Damage Resistance'],
                skill_proficiencies_count=0,
            ),
            'Forest Gnome': Subrace(
                name='Forest Gnome',
                parent_race='Gnome',
                ability_bonuses={'dexterity': 1},
                traits=['Natural Illusionist', 'Speak With Small Beasts'],
                skill_proficiencies_count=0,
            ),
            'Rock Gnome': Subrace(
                name='Rock Gnome',
                parent_race='Gnome',
                ability_bonuses={'constitution': 1},
                traits=['Artificer\'s Lore', 'Tinker'],
                skill_proficiencies_count=0,
            ),
            'Half Elf (General)': Subrace(
                name='Half Elf (General)',
                parent_race='Half-Elf',
                ability_bonuses={},
                traits=['Skill Versatility'],
                skill_proficiencies_count=2,
            )
        }