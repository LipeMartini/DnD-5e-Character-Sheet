from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json
from .stats import Stats
from .race import Race, RaceDatabase
from .subrace import Subrace, SubraceDatabase
from .character_class import CharacterClass, ClassDatabase
from .background import Background, BackgroundDatabase
from .dice import DiceRoller
from .inventory import Inventory

@dataclass
class Character:
    name: str = ""
    race: Optional[Race] = None
    subrace: Optional[Subrace] = None
    character_class: Optional[CharacterClass] = None
    level: int = 1
    background: Optional[Background] = None
    alignment: str = "Neutral"
    experience_points: int = 0
    
    stats: Stats = field(default_factory=Stats)
    base_stats: Stats = field(default_factory=Stats)
    
    max_hit_points: int = 0
    current_hit_points: int = 0
    temporary_hit_points: int = 0
    
    armor_class: int = 10
    initiative: int = 0
    speed: int = 30
    
    proficiency_bonus: int = 2
    
    skill_proficiencies: List[str] = field(default_factory=list)
    saving_throw_proficiencies: List[str] = field(default_factory=list)
    weapon_proficiencies: List[str] = field(default_factory=list)
    armor_proficiencies: List[str] = field(default_factory=list)
    
    languages: List[str] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    
    equipment: List[str] = field(default_factory=list)  # Mantido para compatibilidade
    inventory: Inventory = field(default_factory=Inventory)
    
    def __post_init__(self):
        self.update_derived_stats()
    
    def calculate_proficiency_bonus(self) -> int:
        """Calcula o bônus de proficiência baseado no nível"""
        return 2 + ((self.level - 1) // 4)
    
    def recalculate_stats(self):
        """Recalcula os atributos aplicando bônus raciais e subraciais aos valores base"""
        # Começa com os valores base
        self.stats = Stats(
            strength=self.base_stats.strength,
            dexterity=self.base_stats.dexterity,
            constitution=self.base_stats.constitution,
            intelligence=self.base_stats.intelligence,
            wisdom=self.base_stats.wisdom,
            charisma=self.base_stats.charisma
        )
        
        # Aplica bônus raciais
        if self.race:
            self.stats.apply_racial_bonuses(self.race.ability_bonuses)
        
        # Aplica bônus subraciais
        if self.subrace:
            self.stats.apply_racial_bonuses(self.subrace.ability_bonuses)
    
    def update_derived_stats(self):
        """Atualiza estatísticas derivadas"""
        self.proficiency_bonus = self.calculate_proficiency_bonus()
        
        if self.race:
            self.speed = self.race.speed
            self.languages = self.race.languages.copy()
            self.traits = self.race.traits.copy()
        
        if self.subrace:
            self.traits.extend(self.subrace.traits)
        
        if self.character_class:
            self.saving_throw_proficiencies = self.character_class.saving_throw_proficiencies.copy()
        
        # Calcula CA usando o sistema de inventário
        self.armor_class = self.inventory.calculate_armor_class(self)
        
        dex_modifier = self.stats.get_modifier('dexterity')
        self.initiative = dex_modifier
    
    def set_race(self, race_name: str):
        """Define a raça do personagem e aplica bônus raciais"""
        self.race = RaceDatabase.get_race(race_name)
        self.recalculate_stats()
        self.update_derived_stats()
    
    def set_subrace(self, subrace_name: str):
        """Define a subraça do personagem e aplica bônus subraciais"""
        self.subrace = SubraceDatabase.get_all_subraces().get(subrace_name)
        self.recalculate_stats()
        self.update_derived_stats()
    
    def set_class(self, class_name: str):
        """Define a classe do personagem"""
        self.character_class = ClassDatabase.get_class(class_name)
        
        # Aplica proficiências de armas e armaduras da classe
        if self.character_class:
            self.weapon_proficiencies = self.character_class.weapon_proficiencies.copy()
            self.armor_proficiencies = self.character_class.armor_proficiencies.copy()
        
        self.update_derived_stats()
        self.recalculate_max_hp()

    def set_background(self, background_name: str):
        """Define o background do personagem"""
        self.background = BackgroundDatabase.get_all_backgrounds().get(background_name)
        self.update_derived_stats()
    
    def is_proficient_with_weapon(self, weapon) -> bool:
        """Verifica se o personagem é proficiente com uma arma"""
        # Verifica proficiência por nome específico
        if weapon.name in self.weapon_proficiencies:
            return True
        
        # Verifica proficiência por categoria
        for prof in self.weapon_proficiencies:
            # Simple weapons
            if prof.lower() == "simple weapons":
                simple_weapons = ["Club", "Dagger", "Greatclub", "Handaxe", "Javelin", 
                                "Light Hammer", "Mace", "Quarterstaff", "Sickle", "Spear",
                                "Light Crossbow", "Dart", "Shortbow", "Sling"]
                if weapon.name in simple_weapons:
                    return True
            
            # Martial weapons
            elif prof.lower() == "martial weapons":
                martial_weapons = ["Battleaxe", "Flail", "Glaive", "Greataxe", "Greatsword",
                                  "Halberd", "Lance", "Longsword", "Maul", "Morningstar",
                                  "Pike", "Rapier", "Scimitar", "Shortsword", "Trident",
                                  "War Pick", "Warhammer", "Whip", "Blowgun", "Hand Crossbow",
                                  "Heavy Crossbow", "Longbow", "Net"]
                if weapon.name in martial_weapons:
                    return True
            
            # Proficiência específica (ex: "Longswords", "Rapiers")
            elif weapon.name.lower() in prof.lower() or prof.lower() in weapon.name.lower():
                return True
        
        return False
    
    def roll_initiative(self) -> tuple[int, int]:
        """Rola iniciativa"""
        return DiceRoller.roll_d20(self.initiative)
    
    def roll_saving_throw(self, ability: str) -> tuple[int, int]:
        """Rola teste de resistência"""
        modifier = self.stats.get_modifier(ability)
        if ability.lower() in self.saving_throw_proficiencies:
            modifier += self.proficiency_bonus
        return DiceRoller.roll_d20(modifier)
    
    def roll_skill_check(self, skill: str, ability: str) -> tuple[int, int]:
        """Rola teste de perícia"""
        modifier = self.stats.get_modifier(ability)
        if skill in self.skill_proficiencies:
            modifier += self.proficiency_bonus
        return DiceRoller.roll_d20(modifier)
    
    def roll_attack(self, ability: str, weapon_proficient: bool = True) -> tuple[int, int]:
        """Rola ataque"""
        modifier = self.stats.get_modifier(ability)
        if weapon_proficient:
            modifier += self.proficiency_bonus
        return DiceRoller.roll_d20(modifier)
    
    def recalculate_max_hp(self):
        """Recalcula HP máximo baseado no nível e constituição"""
        if not self.character_class:
            return
        
        con_modifier = self.stats.get_modifier('constitution')
        
        # Nível 1: HP máximo do dado + CON
        if self.level == 1:
            self.max_hit_points = self.character_class.hit_die + con_modifier
            self.current_hit_points = self.max_hit_points
        else:
            # Níveis 2+: Mantém HP atual se já foi calculado
            # (não recalcula automaticamente para não sobrescrever rolagens)
            if self.max_hit_points == 0:
                # Se ainda não tem HP, calcula usando média
                avg_per_level = (self.character_class.hit_die // 2) + 1
                self.max_hit_points = self.character_class.hit_die + con_modifier
                self.max_hit_points += (self.level - 1) * (avg_per_level + con_modifier)
                self.current_hit_points = self.max_hit_points
    
    def take_damage(self, damage: int):
        """Aplica dano ao personagem"""
        if damage < 0:
            return
        
        # Primeiro, remove HP temporário
        if self.temporary_hit_points > 0:
            if damage <= self.temporary_hit_points:
                self.temporary_hit_points -= damage
                return
            else:
                damage -= self.temporary_hit_points
                self.temporary_hit_points = 0
        
        # Depois, remove HP atual
        self.current_hit_points -= damage
        self.current_hit_points = max(0, self.current_hit_points)
    
    def heal(self, healing: int):
        """Cura o personagem"""
        if healing < 0:
            return
        
        self.current_hit_points += healing
        self.current_hit_points = min(self.current_hit_points, self.max_hit_points)
    
    def add_temp_hp(self, temp_hp: int):
        """Adiciona HP temporário (não acumula, pega o maior)"""
        if temp_hp > self.temporary_hit_points:
            self.temporary_hit_points = temp_hp
    
    def short_rest(self):
        """Descanso curto - pode usar dados de vida para curar"""
        # Implementação básica - apenas retorna informação
        return f"Você tem {self.level} dados de vida (d{self.character_class.hit_die if self.character_class else 6})"
    
    def long_rest(self):
        """Descanso longo - recupera HP e metade dos dados de vida"""
        self.current_hit_points = self.max_hit_points
        self.temporary_hit_points = 0
        return "HP completamente restaurado!"
    
    def level_up(self, use_average: bool = False):
        """Sobe de nível
        
        Args:
            use_average: Se True, usa média do dado de vida. Se False, rola o dado.
        """
        self.level += 1
        self.update_derived_stats()
        
        if self.character_class:
            con_modifier = self.stats.get_modifier('constitution')
            
            if use_average:
                # Média arredondada para cima: (dado / 2) + 1
                hp_gain = (self.character_class.hit_die // 2) + 1
            else:
                # Rola o dado de vida
                hp_gain, _ = DiceRoller.roll(f"1d{self.character_class.hit_die}")
            
            hp_gain += con_modifier
            hp_gain = max(1, hp_gain)  # Mínimo de 1 HP por nível
            self.max_hit_points += hp_gain
            self.current_hit_points = self.max_hit_points
            return hp_gain
        return 0
    
    def to_dict(self) -> dict:
        """Converte personagem para dicionário (para salvar)"""
        return {
            'name': self.name,
            'race': self.race.to_dict() if self.race else None,
            'subrace': self.subrace.to_dict() if self.subrace else None,
            'character_class': self.character_class.to_dict() if self.character_class else None,
            'level': self.level,
            'background': self.background.to_dict() if self.background else None,
            'alignment': self.alignment,
            'experience_points': self.experience_points,
            'stats': self.stats.to_dict(),
            'base_stats': self.base_stats.to_dict(),
            'max_hit_points': self.max_hit_points,
            'current_hit_points': self.current_hit_points,
            'temporary_hit_points': self.temporary_hit_points,
            'armor_class': self.armor_class,
            'initiative': self.initiative,
            'speed': self.speed,
            'proficiency_bonus': self.proficiency_bonus,
            'skill_proficiencies': self.skill_proficiencies,
            'saving_throw_proficiencies': self.saving_throw_proficiencies,
            'weapon_proficiencies': self.weapon_proficiencies,
            'armor_proficiencies': self.armor_proficiencies,
            'languages': self.languages,
            'traits': self.traits,
            'equipment': self.equipment,
            'inventory': self.inventory.to_dict(),
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        """Cria personagem a partir de dicionário (para carregar)"""
        char = cls()
        char.name = data.get('name', '')
        char.level = data.get('level', 1)
        char.alignment = data.get('alignment', 'Neutral')
        char.experience_points = data.get('experience_points', 0)
        
        if data.get('stats'):
            char.stats = Stats.from_dict(data['stats'])
        
        if data.get('base_stats'):
            char.base_stats = Stats.from_dict(data['base_stats'])
        
        if data.get('race'):
            char.race = Race.from_dict(data['race'])

        if data.get('subrace'):
            char.subrace = Subrace.from_dict(data['subrace'])
        
        if data.get('background'):
            char.background = Background.from_dict(data['background'])
        
        if data.get('character_class'):
            char.character_class = CharacterClass.from_dict(data['character_class'])
        
        char.max_hit_points = data.get('max_hit_points', 0)
        char.current_hit_points = data.get('current_hit_points', 0)
        char.temporary_hit_points = data.get('temporary_hit_points', 0)
        char.armor_class = data.get('armor_class', 10)
        char.initiative = data.get('initiative', 0)
        char.speed = data.get('speed', 30)
        char.proficiency_bonus = data.get('proficiency_bonus', 2)
        char.skill_proficiencies = data.get('skill_proficiencies', [])
        char.saving_throw_proficiencies = data.get('saving_throw_proficiencies', [])
        char.weapon_proficiencies = data.get('weapon_proficiencies', [])
        char.armor_proficiencies = data.get('armor_proficiencies', [])
        char.languages = data.get('languages', [])
        char.traits = data.get('traits', [])
        char.equipment = data.get('equipment', [])
        
        if data.get('inventory'):
            char.inventory = Inventory.from_dict(data['inventory'])
        
        return char
    
    def save_to_file(self, filepath: str):
        """Salva personagem em arquivo JSON"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2, ensure_ascii=False)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'Character':
        """Carrega personagem de arquivo JSON"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
