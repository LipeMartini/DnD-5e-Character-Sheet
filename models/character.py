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
from .spellcasting import SpellcastingInfo, SpellSlotTable

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
    # Perícias com Expertise (bônus de proficiência dobrado)
    skill_expertise: List[str] = field(default_factory=list)
    saving_throw_proficiencies: List[str] = field(default_factory=list)
    weapon_proficiencies: List[str] = field(default_factory=list)
    armor_proficiencies: List[str] = field(default_factory=list)
    
    languages: List[str] = field(default_factory=list)
    traits: List[str] = field(default_factory=list)
    class_features: List[str] = field(default_factory=list)
    
    equipment: List[str] = field(default_factory=list)  # Mantido para compatibilidade
    inventory: Inventory = field(default_factory=Inventory)
    
    # Sistema de magias
    spellcasting: Optional[SpellcastingInfo] = None
    
    # Fighting Styles (pode ter múltiplos via feats ou multiclasse)
    fighting_styles: List[str] = field(default_factory=list)
    
    # Feats (Talentos)
    feats: List[str] = field(default_factory=list)
    
    # Subclass (Arquétipo de classe)
    subclass_name: Optional[str] = None
    
    # Notas do personagem (organizadas por categoria)
    notes: Dict[str, str] = field(default_factory=dict)
    
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
    
    def apply_racial_proficiencies(self):
        """Aplica proficiências de armas e armaduras baseadas em traits raciais"""
        # Elf Weapon Training (High Elf, Wood Elf)
        if self.has_trait('Elf Weapon Training'):
            racial_weapons = ['Longsword', 'Shortsword', 'Shortbow', 'Longbow']
            for weapon in racial_weapons:
                if weapon not in self.weapon_proficiencies:
                    self.weapon_proficiencies.append(weapon)
        
        # Drow Weapon Training (Dark Elf)
        if self.has_trait('Drow Weapon Training'):
            drow_weapons = ['Rapier', 'Shortsword', 'Hand Crossbow']
            for weapon in drow_weapons:
                if weapon not in self.weapon_proficiencies:
                    self.weapon_proficiencies.append(weapon)
        
        # Dwarven Combat Training (Dwarf)
        if self.has_trait('Dwarven Combat Training'):
            dwarf_weapons = ['Battleaxe', 'Handaxe', 'Light Hammer', 'Warhammer']
            for weapon in dwarf_weapons:
                if weapon not in self.weapon_proficiencies:
                    self.weapon_proficiencies.append(weapon)
        
        # Dwarven Armor Training (Mountain Dwarf)
        if self.has_trait('Dwarven Armor Training'):
            dwarf_armors = ['Light armor', 'Medium armor']
            for armor in dwarf_armors:
                if armor not in self.armor_proficiencies:
                    self.armor_proficiencies.append(armor)
    
    def update_derived_stats(self):
        """Atualiza estatísticas derivadas"""
        self.proficiency_bonus = self.calculate_proficiency_bonus()
        
        if self.race:
            self.speed = self.race.speed
            self.languages = self.race.languages.copy()
            self.traits = self.race.traits.copy()
        
        if self.subrace:
            self.traits.extend(self.subrace.traits)
            # Aplica velocidade da subraça se especificada (Wood Elf)
            if self.subrace.speed:
                self.speed = self.subrace.speed
        
        if self.character_class:
            self.saving_throw_proficiencies = self.character_class.saving_throw_proficiencies.copy()
        
        # Aplica proficiências raciais de armas/armaduras
        self.apply_racial_proficiencies()
        
        # Calcula CA usando o sistema de inventário
        self.armor_class = self.inventory.calculate_armor_class(self)
        
        dex_modifier = self.stats.get_modifier('dexterity')
        self.initiative = dex_modifier
        
        # Aplica bônus de Alert (+5 iniciativa)
        if self.has_feat("Alert"):
            self.initiative += 5
        
        # Aplica bônus de Mobile (+10 velocidade)
        if self.has_feat("Mobile"):
            self.speed += 10
    
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
        
        # Aplica proficiências raciais (depois das de classe para evitar duplicatas)
        self.apply_racial_proficiencies()
        
        # Inicializa spellcasting se for classe conjuradora
        self.initialize_spellcasting()
        
        self.update_derived_stats()
        self.recalculate_max_hp()

    def set_background(self, background_name: str):
        """Define o background do personagem"""
        self.background = BackgroundDatabase.get_all_backgrounds().get(background_name)
        self.update_derived_stats()
    
    def is_proficient_with_weapon(self, weapon) -> bool:
        """Verifica se o personagem é proficiente com uma arma"""
        # Mapeamento de nomes em português para inglês
        weapon_name_map = {
            'Adaga': 'Dagger',
            'Espada Curta': 'Shortsword',
            'Espada Longa': 'Longsword',
            'Machado de Batalha': 'Battleaxe',
            'Martelo de Guerra': 'Warhammer',
            'Espada Grande': 'Greatsword',
            'Machado Grande': 'Greataxe',
            'Arco Curto': 'Shortbow',
            'Arco Longo': 'Longbow',
            'Besta Leve': 'Light Crossbow',
            'Cajado': 'Quarterstaff',
            'Lança': 'Spear',
            'Clava': 'Club',
            'Maça': 'Mace',
            'Rapieira': 'Rapier',
            'Cimitarra': 'Scimitar',
            'Tridente': 'Trident',
            'Alabarda': 'Halberd',
            'Glaive': 'Glaive',
            'Lança de Cavalaria': 'Lance',
            'Mangual': 'Flail',
            'Estrela da Manhã': 'Morningstar',
            'Pique': 'Pike',
            'Malho': 'Maul',
            'Chicote': 'Whip',
            'Besta de Mão': 'Hand Crossbow',
            'Besta Pesada': 'Heavy Crossbow',
            'Rede': 'Net',
            'Zarabatana': 'Blowgun',
        }
        
        # Obtém o nome em inglês se existir mapeamento
        weapon_name_en = weapon_name_map.get(weapon.name, weapon.name)
        
        # Verifica proficiência por nome específico (português ou inglês)
        if weapon.name in self.weapon_proficiencies or weapon_name_en in self.weapon_proficiencies:
            return True
        
        # Verifica proficiência por categoria
        for prof in self.weapon_proficiencies:
            # Simple weapons
            if prof.lower() == "simple weapons":
                simple_weapons = ["Club", "Dagger", "Greatclub", "Handaxe", "Javelin", 
                                "Light Hammer", "Mace", "Quarterstaff", "Sickle", "Spear",
                                "Light Crossbow", "Dart", "Shortbow", "Sling"]
                if weapon_name_en in simple_weapons:
                    return True
            
            # Martial weapons
            elif prof.lower() == "martial weapons":
                martial_weapons = ["Battleaxe", "Flail", "Glaive", "Greataxe", "Greatsword",
                                  "Halberd", "Lance", "Longsword", "Maul", "Morningstar",
                                  "Pike", "Rapier", "Scimitar", "Shortsword", "Trident",
                                  "War Pick", "Warhammer", "Whip", "Blowgun", "Hand Crossbow",
                                  "Heavy Crossbow", "Longbow", "Net"]
                if weapon_name_en in martial_weapons:
                    return True
            
            # Proficiência específica (ex: "Longswords", "Rapiers")
            elif weapon.name.lower() in prof.lower() or prof.lower() in weapon.name.lower():
                return True
            elif weapon_name_en.lower() in prof.lower() or prof.lower() in weapon_name_en.lower():
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
        # Expertise tem precedência e dobra o bônus de proficiência
        if skill in self.skill_expertise:
            modifier += (2 * self.proficiency_bonus)
        elif skill in self.skill_proficiencies:
            modifier += self.proficiency_bonus
        return DiceRoller.roll_d20(modifier)
    
    def roll_attack(self, ability: str, weapon_proficient: bool = True) -> tuple[int, int]:
        """Rola ataque"""
        modifier = self.stats.get_modifier(ability)
        if weapon_proficient:
            modifier += self.proficiency_bonus
        return DiceRoller.roll_d20(modifier)
    
    def has_trait(self, trait_name: str) -> bool:
        """Verifica se o personagem possui um trait específico"""
        return trait_name in self.traits
    
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
        
        # Dwarven Toughness: +1 HP por nível (Hill Dwarf)
        if self.has_trait('Dwarven Toughness'):
            self.max_hit_points += self.level
    
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
        """Descanso longo - recupera HP e HD"""
        self.current_hit_points = self.max_hit_points
        self.temporary_hit_points = 0
        
        # Restaura spell slots
        if self.spellcasting:
            self.spellcasting.restore_spell_slots()
    
    def initialize_spellcasting(self):
        """Inicializa o sistema de magias para classes conjuradoras"""
        if not self.character_class:
            return
        
        class_name = self.character_class.name
        
        # Verifica se a classe é conjuradora
        caster_classes = ['Wizard', 'Sorcerer', 'Cleric', 'Druid', 'Bard', 'Warlock', 'Paladin', 'Ranger']
        
        # Subclasses que conjuram magias (não remover spellcasting delas!)
        spellcasting_subclasses = ['Eldritch Knight', 'Arcane Trickster']
        
        # Se não é uma classe conjuradora E não tem uma subclasse conjuradora, remove spellcasting
        if class_name not in caster_classes:
            if not (self.subclass_name and self.subclass_name in spellcasting_subclasses):
                self.spellcasting = None
                return
            # Se tem subclasse conjuradora, não inicializa automaticamente (já foi configurado)
            # Apenas atualiza os spell slots se já existe spellcasting
            if self.spellcasting:
                from models.spellcasting import SpellSlotTable
                slots = SpellSlotTable.get_third_caster_slots(self.level)
                self.spellcasting.max_spell_slots = slots
                self.spellcasting.current_spell_slots = slots.copy()
                # Recalcula DC e bônus
                ability_mod = self.stats.get_modifier(self.spellcasting.spellcasting_ability)
                self.spellcasting.spell_save_dc = 8 + self.proficiency_bonus + ability_mod
                self.spellcasting.spell_attack_bonus = self.proficiency_bonus + ability_mod
            return
        
        # Cria SpellcastingInfo se não existir
        if not self.spellcasting:
            self.spellcasting = SpellcastingInfo()
        
        # Define habilidade de conjuração
        self.spellcasting.spellcasting_ability = SpellSlotTable.get_spellcasting_ability(class_name)
        
        # Atualiza spell slots baseado no nível
        self.spellcasting.max_spell_slots = SpellSlotTable.get_spell_slots(class_name, self.level)
        self.spellcasting.current_spell_slots = self.spellcasting.max_spell_slots.copy()
        
        # Calcula DC e bônus de ataque de magia
        ability_mod = self.stats.get_modifier(self.spellcasting.spellcasting_ability)
        self.spellcasting.spell_save_dc = 8 + self.proficiency_bonus + ability_mod
        self.spellcasting.spell_attack_bonus = self.proficiency_bonus + ability_mod
    
    def is_spellcaster(self) -> bool:
        """Verifica se o personagem é um conjurador"""
        return self.spellcasting is not None
    
    def can_prepare_spells(self) -> bool:
        """Verifica se a classe prepara magias (vs conhece magias)"""
        if not self.character_class:
            return False
        return SpellSlotTable.uses_prepared_spells(self)
    
    def get_max_prepared_spells(self) -> int:
        """Retorna o número máximo de magias que podem ser preparadas"""
        if not self.can_prepare_spells() or not self.spellcasting:
            return 0
        
        ability_mod = self.stats.get_modifier(self.spellcasting.spellcasting_ability)
        return max(1, ability_mod + self.level)
    
    def get_spellcasting_type(self) -> str:
        """
        Retorna o tipo de sistema de magias da classe:
        - 'wizard': Tem spellbook (conhece muitas) e prepara algumas
        - 'prepared': Prepara magias diretamente da lista completa (Cleric, Druid, Paladin)
        - 'known': Conhece número limitado de magias (Sorcerer, Bard, Warlock, Ranger)
        """
        if not self.character_class:
            return 'known'
        
        class_name = self.character_class.name
        
        if class_name == 'Wizard':
            return 'wizard'
        elif class_name in ['Cleric', 'Druid', 'Paladin']:
            return 'prepared'
        else:  # Sorcerer, Bard, Warlock, Ranger
            return 'known'
    
    def level_up(self, use_average: bool = True) -> int:
        """Sobe de nível e retorna HP ganho"""
        self.level += 1
        self.proficiency_bonus = self.calculate_proficiency_bonus()
        self.update_derived_stats()
        
        # Atualiza spell slots se for conjurador
        if self.is_spellcaster():
            self.initialize_spellcasting()
        
        if self.character_class:
            con_modifier = self.stats.get_modifier('constitution')
            
            if use_average:
                hp_gain = (self.character_class.hit_die // 2) + 1
            else:
                hp_gain, _ = DiceRoller.roll(f"1d{self.character_class.hit_die}")
            
            hp_gain += con_modifier
            
            # Dwarven Toughness: +1 HP por nível (Hill Dwarf)
            if self.has_trait('Dwarven Toughness'):
                hp_gain += 1
            
            # Tough Feat: +2 HP por nível
            if self.has_feat('Tough'):
                hp_gain += 2
            
            hp_gain = max(1, hp_gain)
            self.max_hit_points += hp_gain
            self.current_hit_points = self.max_hit_points
            return hp_gain
        return 0
    
    def add_class_features(self, class_name: str, level: int) -> List[str]:
        """
        Adiciona features de classe para um nível específico
        
        Args:
            class_name: Nome da classe (preparado para multiclasse)
            level: Nível da classe para obter features
            
        Returns:
            Lista com nomes das features adicionadas
        """
        from .class_features import get_class_features
        
        features = get_class_features(class_name, level)
        new_features = []
        
        for feature in features:
            feature_name = feature.name
            if feature_name not in self.class_features:
                self.class_features.append(feature_name)
                new_features.append(feature_name)
        
        return new_features
    
    def apply_subclass_proficiencies(self, subclass_name: str):
        """
        Aplica proficiências de uma subclasse ao personagem
        
        Args:
            subclass_name: Nome da subclasse
        """
        if not self.character_class:
            return
        
        class_name = self.character_class.name
        
        # Mapeamento de proficiências por subclasse
        subclass_proficiencies = {
            # Bard
            "College of Valor": {
                "armor": ["Medium Armor", "Shields"],
                "weapon": ["Martial Weapons"]
            },
            # Cleric
            "Life Domain": {
                "armor": ["Heavy Armor"],
                "weapon": []
            },
            "War Domain": {
                "armor": ["Heavy Armor"],
                "weapon": ["Martial Weapons"]
            }
        }
        
        if subclass_name in subclass_proficiencies:
            profs = subclass_proficiencies[subclass_name]
            
            # Adiciona proficiências de armadura
            for armor_prof in profs.get("armor", []):
                if armor_prof not in self.armor_proficiencies:
                    self.armor_proficiencies.append(armor_prof)
            
            # Adiciona proficiências de arma
            for weapon_prof in profs.get("weapon", []):
                if weapon_prof not in self.weapon_proficiencies:
                    self.weapon_proficiencies.append(weapon_prof)
    
    def get_critical_range(self) -> int:
        """
        Retorna o valor mínimo para crítico (normalmente 20, mas Champion tem 19 ou 18)
        
        Returns:
            Valor mínimo do d20 para crítico (18, 19, ou 20)
        """
        # Champion Fighter tem crítico expandido
        if self.subclass_name == "Champion":
            if self.level >= 15:
                return 18  # Superior Critical (18-20)
            elif self.level >= 3:
                return 19  # Improved Critical (19-20)
        
        # Padrão para todas as outras classes/subclasses
        return 20
    
    def get_class_feature_description(self, feature_name: str) -> str:
        """
        Retorna a descrição de uma feature de classe
        
        Args:
            feature_name: Nome da feature
            
        Returns:
            Descrição da feature ou mensagem padrão
        """
        from .class_features import get_all_features_up_to_level
        
        if not self.character_class:
            return "Nenhuma classe selecionada."
        
        all_features = get_all_features_up_to_level(self.character_class.name, self.level)
        
        for feature in all_features:
            if feature.name == feature_name:
                return feature.description
        
        return "Descrição não disponível."
    
    def has_fighting_style(self, style_name: str) -> bool:
        """
        Verifica se o personagem tem um Fighting Style específico
        
        Args:
            style_name: Nome do Fighting Style
            
        Returns:
            True se o personagem tem o estilo, False caso contrário
        """
        return style_name in self.fighting_styles
    
    def has_feat(self, feat_name: str) -> bool:
        """
        Verifica se o personagem tem um Feat específico
        
        Args:
            feat_name: Nome do Feat
            
        Returns:
            True se o personagem tem o feat, False caso contrário
        """
        return feat_name in self.feats
    
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
            'skill_expertise': self.skill_expertise,
            'saving_throw_proficiencies': self.saving_throw_proficiencies,
            'weapon_proficiencies': self.weapon_proficiencies,
            'armor_proficiencies': self.armor_proficiencies,
            'languages': self.languages,
            'traits': self.traits,
            'class_features': self.class_features,
            'equipment': self.equipment,
            'inventory': self.inventory.to_dict(),
            'spellcasting': self.spellcasting.to_dict() if self.spellcasting else None,
            'fighting_styles': self.fighting_styles,
            'feats': self.feats,
            'subclass_name': self.subclass_name,
            'notes': self.notes,
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
        char.skill_expertise = data.get('skill_expertise', [])
        char.saving_throw_proficiencies = data.get('saving_throw_proficiencies', [])
        char.weapon_proficiencies = data.get('weapon_proficiencies', [])
        char.armor_proficiencies = data.get('armor_proficiencies', [])
        char.languages = data.get('languages', [])
        char.traits = data.get('traits', [])
        char.class_features = data.get('class_features', [])
        char.equipment = data.get('equipment', [])
        
        if data.get('inventory'):
            char.inventory = Inventory.from_dict(data['inventory'])
        
        if data.get('spellcasting'):
            char.spellcasting = SpellcastingInfo.from_dict(data['spellcasting'])
        
        char.fighting_styles = data.get('fighting_styles', [])
        char.feats = data.get('feats', [])
        char.subclass_name = data.get('subclass_name')
        char.notes = data.get('notes', {})
        
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
