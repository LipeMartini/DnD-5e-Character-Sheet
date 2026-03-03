"""
Subclasses (Arquétipos) para D&D 5e
Cada classe tem suas próprias subclasses que são escolhidas em níveis específicos
"""

from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SubclassFeature:
    """Representa uma feature específica de uma subclasse"""
    name: str
    level: int
    description: str
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'level': self.level,
            'description': self.description
        }
    
    @staticmethod
    def from_dict(data: dict):
        return SubclassFeature(
            name=data['name'],
            level=data['level'],
            description=data['description']
        )

@dataclass
class Subclass:
    """Representa uma subclasse/arquétipo de personagem"""
    name: str
    class_name: str  # Classe pai (Barbarian, Fighter, etc.)
    description: str
    features: List[SubclassFeature]
    selection_level: int = 3  # Nível em que a subclasse é escolhida
    
    def get_features_at_level(self, level: int) -> List[SubclassFeature]:
        """Retorna features disponíveis em um nível específico"""
        return [f for f in self.features if f.level == level]
    
    def get_all_features_up_to_level(self, level: int) -> List[SubclassFeature]:
        """Retorna todas as features até um nível específico"""
        return [f for f in self.features if f.level <= level]
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'class_name': self.class_name,
            'description': self.description,
            'features': [f.to_dict() for f in self.features],
            'selection_level': self.selection_level
        }
    
    @staticmethod
    def from_dict(data: dict):
        return Subclass(
            name=data['name'],
            class_name=data['class_name'],
            description=data['description'],
            features=[SubclassFeature.from_dict(f) for f in data['features']],
            selection_level=data.get('selection_level', 3)
        )


# ========== BARBARIAN SUBCLASSES ==========

BERSERKER = Subclass(
    name="Path of the Berserker",
    class_name="Barbarian",
    description="For some barbarians, rage is a means to an end — that end being violence. The Path of the Berserker is a path of untrammeled fury, slick with blood.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Frenzy",
            level=3,
            description="You can go into a frenzy when you rage. If you do so, for the duration of your rage you can make a single melee weapon attack as a bonus action on each of your turns after this one. When your rage ends, you suffer one level of exhaustion."
        ),
        SubclassFeature(
            name="Mindless Rage",
            level=6,
            description="You can't be charmed or frightened while raging. If you are charmed or frightened when you enter your rage, the effect is suspended for the duration of the rage."
        ),
        SubclassFeature(
            name="Intimidating Presence",
            level=10,
            description="You can use your action to frighten someone with your menacing presence. When you do so, choose one creature that you can see within 30 feet of you. If the creature can see or hear you, it must succeed on a Wisdom saving throw (DC equal to 8 + your proficiency bonus + your Charisma modifier) or be frightened of you until the end of your next turn. On subsequent turns, you can use your action to extend the duration of this effect on the frightened creature until the end of your next turn. This effect ends if the creature ends its turn out of line of sight or more than 60 feet away from you. If the creature succeeds on its saving throw, you can't use this feature on that creature again for 24 hours."
        ),
        SubclassFeature(
            name="Retaliation",
            level=14,
            description="When you take damage from a creature that is within 5 feet of you, you can use your reaction to make a melee weapon attack against that creature."
        )
    ]
)

TOTEM_WARRIOR = Subclass(
    name="Path of the Totem Warrior",
    class_name="Barbarian",
    description="The Path of the Totem Warrior is a spiritual journey, as the barbarian accepts a spirit animal as guide, protector, and inspiration.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Spirit Seeker",
            level=3,
            description="Yours is a path that seeks attunement with the natural world, giving you a kinship with beasts. You gain the ability to cast the Beast Sense and Speak with Animals spells, but only as rituals."
        ),
        SubclassFeature(
            name="Totem Spirit",
            level=3,
            description="You choose a totem spirit and gain its feature. You must make or acquire a physical totem object—an amulet or similar adornment—that incorporates fur or feathers, claws, teeth, or bones of the totem animal.\n\nBear: While raging, you have resistance to all damage except psychic damage.\nEagle: While raging, other creatures have disadvantage on opportunity attack rolls against you.\nWolf: While raging, your friends have advantage on melee attack rolls against any creature within 5 feet of you that is hostile to you."
        ),
        SubclassFeature(
            name="Aspect of the Beast",
            level=6,
            description="You gain a magical benefit based on the totem animal of your choice.\n\nBear: You gain the might of a bear. Your carrying capacity (including maximum load and maximum lift) is doubled, and you have advantage on Strength checks made to push, pull, lift, or break objects.\nEagle: You gain the eyesight of an eagle. You can see up to 1 mile away with no difficulty, able to discern even fine details as though looking at something no more than 100 feet away from you. Additionally, dim light doesn't impose disadvantage on your Wisdom (Perception) checks.\nWolf: You gain the hunting sensibilities of a wolf. You can track other creatures while traveling at a fast pace, and you can move stealthily while traveling at a normal pace."
        ),
        SubclassFeature(
            name="Spirit Walker",
            level=10,
            description="You can cast the Commune with Nature spell, but only as a ritual. When you do so, a spiritual version of one of the animals you chose for Totem Spirit or Aspect of the Beast appears to you to convey the information you seek."
        ),
        SubclassFeature(
            name="Totemic Attunement",
            level=14,
            description="You gain a magical benefit based on a totem animal of your choice.\n\nBear: While you're raging, any creature within 5 feet of you that's hostile to you has disadvantage on attack rolls against targets other than you or another character with this feature.\nEagle: While raging, you have a flying speed equal to your current walking speed. This benefit works only in short bursts; you fall if you end your turn in the air and nothing else is holding you aloft.\nWolf: While you're raging, you can use a bonus action on your turn to knock a Large or smaller creature prone when you hit it with melee weapon attack."
        )
    ]
)

# ========== BARD SUBCLASSES ==========

COLLEGE_OF_LORE = Subclass(
    name="College of Lore",
    class_name="Bard",
    description="Bards of the College of Lore know something about most things, collecting bits of knowledge from sources as diverse as scholarly tomes and peasant tales.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with three skills of your choice."
        ),
        SubclassFeature(
            name="Cutting Words",
            level=3,
            description="You learn how to use your wit to distract, confuse, and otherwise sap the confidence and competence of others. When a creature that you can see within 60 feet of you makes an attack roll, an ability check, or a damage roll, you can use your reaction to expend one of your uses of Bardic Inspiration, rolling a Bardic Inspiration die and subtracting the number rolled from the creature's roll. You can choose to use this feature after the creature makes its roll, but before the DM determines whether the attack roll or ability check succeeds or fails, or before the creature deals its damage. The creature is immune if it can't hear you or if it's immune to being charmed."
        ),
        SubclassFeature(
            name="Additional Magical Secrets",
            level=6,
            description="You learn two spells of your choice from any class. A spell you choose must be of a level you can cast, as shown on the Bard table, or a cantrip. The chosen spells count as bard spells for you but don't count against the number of bard spells you know."
        ),
        SubclassFeature(
            name="Peerless Skill",
            level=14,
            description="When you make an ability check, you can expend one use of Bardic Inspiration. Roll a Bardic Inspiration die and add the number rolled to your ability check. You can choose to do so after you roll the die for the ability check, but before the DM tells you whether you succeed or fail."
        )
    ]
)

COLLEGE_OF_VALOR = Subclass(
    name="College of Valor",
    class_name="Bard",
    description="Bards of the College of Valor are daring skalds whose tales keep alive the memory of the great heroes of the past, and thereby inspire a new generation of heroes.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with medium armor, shields, and martial weapons."
        ),
        SubclassFeature(
            name="Combat Inspiration",
            level=3,
            description="You learn to inspire others in battle. A creature that has a Bardic Inspiration die from you can roll that die and add the number rolled to a weapon damage roll it just made. Alternatively, when an attack roll is made against the creature, it can use its reaction to roll the Bardic Inspiration die and add the number rolled to its AC against that attack, after seeing the roll but before knowing whether it hits or misses."
        ),
        SubclassFeature(
            name="Extra Attack",
            level=6,
            description="You can attack twice, instead of once, whenever you take the Attack action on your turn."
        ),
        SubclassFeature(
            name="Battle Magic",
            level=14,
            description="You have mastered the art of weaving spellcasting and weapon use into a single harmonious act. When you use your action to cast a bard spell, you can make one weapon attack as a bonus action."
        )
    ]
)

# Dicionário de subclasses por classe
BARBARIAN_SUBCLASSES = {
    "Path of the Berserker": BERSERKER,
    "Path of the Totem Warrior": TOTEM_WARRIOR
}

BARD_SUBCLASSES = {
    "College of Lore": COLLEGE_OF_LORE,
    "College of Valor": COLLEGE_OF_VALOR
}

# ========== CLERIC SUBCLASSES ==========

LIFE_DOMAIN = Subclass(
    name="Life Domain",
    class_name="Cleric",
    description="The Life domain focuses on the vibrant positive energy—one of the fundamental forces of the universe—that sustains all life. The gods of life promote vitality and health through healing the sick and wounded, caring for those in need, and driving away the forces of death and undeath.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Bonus Proficiency",
            level=1,
            description="You gain proficiency with heavy armor."
        ),
        SubclassFeature(
            name="Disciple of Life",
            level=1,
            description="Your healing spells are more effective. Whenever you use a spell of 1st level or higher to restore hit points to a creature, the creature regains additional hit points equal to 2 + the spell's level."
        ),
        SubclassFeature(
            name="Channel Divinity: Preserve Life",
            level=2,
            description="You can use your Channel Divinity to heal the badly injured. As an action, you present your holy symbol and evoke healing energy that can restore a number of hit points equal to five times your cleric level. Choose any creatures within 30 feet of you, and divide those hit points among them. This feature can restore a creature to no more than half of its hit point maximum. You can't use this feature on an undead or a construct."
        ),
        SubclassFeature(
            name="Blessed Healer",
            level=6,
            description="The healing spells you cast on others heal you as well. When you cast a spell of 1st level or higher that restores hit points to a creature other than you, you regain hit points equal to 2 + the spell's level."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="You gain the ability to infuse your weapon strikes with divine energy. Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 radiant damage to the target. When you reach 14th level, the extra damage increases to 2d8."
        ),
        SubclassFeature(
            name="Supreme Healing",
            level=17,
            description="When you would normally roll one or more dice to restore hit points with a spell, you instead use the highest number possible for each die. For example, instead of restoring 2d6 hit points to a creature, you restore 12."
        )
    ]
)

WAR_DOMAIN = Subclass(
    name="War Domain",
    class_name="Cleric",
    description="War has many manifestations. It can make heroes of ordinary people. It can be desperate and horrific, with acts of cruelty and cowardice eclipsing instances of excellence and courage. In either case, the gods of war watch over warriors and reward them for their great deeds.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=1,
            description="You gain proficiency with martial weapons and heavy armor."
        ),
        SubclassFeature(
            name="War Priest",
            level=1,
            description="Your god delivers bolts of inspiration to you while you are engaged in battle. When you use the Attack action, you can make one weapon attack as a bonus action. You can use this feature a number of times equal to your Wisdom modifier (a minimum of once). You regain all expended uses when you finish a long rest."
        ),
        SubclassFeature(
            name="Channel Divinity: Guided Strike",
            level=2,
            description="You can use your Channel Divinity to strike with supernatural accuracy. When you make an attack roll, you can use your Channel Divinity to gain a +10 bonus to the roll. You make this choice after you see the roll, but before the DM says whether the attack hits or misses."
        ),
        SubclassFeature(
            name="Channel Divinity: War God's Blessing",
            level=6,
            description="When a creature within 30 feet of you makes an attack roll, you can use your reaction to grant that creature a +10 bonus to the roll, using your Channel Divinity. You make this choice after you see the roll, but before the DM says whether the attack hits or misses."
        ),
        SubclassFeature(
            name="Divine Strike",
            level=8,
            description="You gain the ability to infuse your weapon strikes with divine energy. Once on each of your turns when you hit a creature with a weapon attack, you can cause the attack to deal an extra 1d8 damage of the same type dealt by the weapon to the target. When you reach 14th level, the extra damage increases to 2d8."
        ),
        SubclassFeature(
            name="Avatar of Battle",
            level=17,
            description="You gain resistance to bludgeoning, piercing, and slashing damage from nonmagical weapons."
        )
    ]
)

# Dicionário de subclasses por classe
BARBARIAN_SUBCLASSES = {
    "Path of the Berserker": BERSERKER,
    "Path of the Totem Warrior": TOTEM_WARRIOR
}

BARD_SUBCLASSES = {
    "College of Lore": COLLEGE_OF_LORE,
    "College of Valor": COLLEGE_OF_VALOR
}

CLERIC_SUBCLASSES = {
    "Life Domain": LIFE_DOMAIN,
    "War Domain": WAR_DOMAIN
}

# ========== DRUID SUBCLASSES ==========

CIRCLE_OF_THE_LAND = Subclass(
    name="Circle of the Land",
    class_name="Druid",
    description="The Circle of the Land is made up of mystics and sages who safeguard ancient knowledge and rites through a vast oral tradition. These druids meet within sacred circles of trees or standing stones to whisper primal secrets in Druidic.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Bonus Cantrip",
            level=2,
            description="You learn one additional druid cantrip of your choice."
        ),
        SubclassFeature(
            name="Natural Recovery",
            level=2,
            description="You can regain some of your magical energy by sitting in meditation and communing with nature. During a short rest, you choose expended spell slots to recover. The spell slots can have a combined level that is equal to or less than half your druid level (rounded up), and none of the slots can be 6th level or higher. You can't use this feature again until you finish a long rest."
        ),
        SubclassFeature(
            name="Circle Spells",
            level=3,
            description="Your mystical connection to the land infuses you with the ability to cast certain spells. You gain access to circle spells connected to the land where you became a druid. Choose that land—arctic, coast, desert, forest, grassland, mountain, swamp, or Underdark—and consult the associated list of spells. Once you gain access to a circle spell, you always have it prepared, and it doesn't count against the number of spells you can prepare each day."
        ),
        SubclassFeature(
            name="Land's Stride",
            level=6,
            description="Moving through nonmagical difficult terrain costs you no extra movement. You can also pass through nonmagical plants without being slowed by them and without taking damage from them if they have thorns, spines, or a similar hazard. In addition, you have advantage on saving throws against plants that are magically created or manipulated to impede movement."
        ),
        SubclassFeature(
            name="Nature's Ward",
            level=10,
            description="You can't be charmed or frightened by elementals or fey, and you are immune to poison and disease."
        ),
        SubclassFeature(
            name="Nature's Sanctuary",
            level=14,
            description="Creatures of the natural world sense your connection to nature and become hesitant to attack you. When a beast or plant creature attacks you, that creature must make a Wisdom saving throw against your druid spell save DC. On a failed save, the creature must choose a different target, or the attack automatically misses. On a successful save, the creature is immune to this effect for 24 hours."
        )
    ]
)

CIRCLE_OF_THE_MOON = Subclass(
    name="Circle of the Moon",
    class_name="Druid",
    description="Druids of the Circle of the Moon are fierce guardians of the wilds. Their order gathers under the full moon to share news and trade warnings. They haunt the deepest parts of the wilderness, where they might go for weeks on end before crossing paths with another humanoid creature, let alone another druid.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Combat Wild Shape",
            level=2,
            description="You gain the ability to use Wild Shape on your turn as a bonus action, rather than as an action. Additionally, while you are transformed by Wild Shape, you can use a bonus action to expend one spell slot to regain 1d8 hit points per level of the spell slot expended."
        ),
        SubclassFeature(
            name="Circle Forms",
            level=2,
            description="The rites of your circle grant you the ability to transform into more dangerous animal forms. You can transform into a beast with a challenge rating as high as 1 (you ignore the Max. CR column of the Beast Shapes table, but must abide by the other limitations there). Starting at 6th level, you can transform into a beast with a challenge rating as high as your druid level divided by 3, rounded down."
        ),
        SubclassFeature(
            name="Primal Strike",
            level=6,
            description="Your attacks in beast form count as magical for the purpose of overcoming resistance and immunity to nonmagical attacks and damage."
        ),
        SubclassFeature(
            name="Elemental Wild Shape",
            level=10,
            description="You can expend two uses of Wild Shape at the same time to transform into an air elemental, an earth elemental, a fire elemental, or a water elemental."
        ),
        SubclassFeature(
            name="Thousand Forms",
            level=14,
            description="You have learned to use magic to alter your physical form in more subtle ways. You can cast the Alter Self spell at will."
        )
    ]
)

DRUID_SUBCLASSES = {
    "Circle of the Land": CIRCLE_OF_THE_LAND,
    "Circle of the Moon": CIRCLE_OF_THE_MOON
}

# ========== FIGHTER SUBCLASSES ==========

CHAMPION = Subclass(
    name="Champion",
    class_name="Fighter",
    description="The archetypal Champion focuses on the development of raw physical power honed to deadly perfection. Those who model themselves on this archetype combine rigorous training with physical excellence to deal devastating blows.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Improved Critical",
            level=3,
            description="Your weapon attacks score a critical hit on a roll of 19 or 20."
        ),
        SubclassFeature(
            name="Remarkable Athlete",
            level=7,
            description="You can add half your proficiency bonus (rounded up) to any Strength, Dexterity, or Constitution check you make that doesn't already use your proficiency bonus. In addition, when you make a running long jump, the distance you can cover increases by a number of feet equal to your Strength modifier."
        ),
        SubclassFeature(
            name="Additional Fighting Style",
            level=10,
            description="You can choose a second option from the Fighting Style class feature."
        ),
        SubclassFeature(
            name="Superior Critical",
            level=15,
            description="Your weapon attacks score a critical hit on a roll of 18-20."
        ),
        SubclassFeature(
            name="Survivor",
            level=18,
            description="You attain the pinnacle of resilience in battle. At the start of each of your turns, you regain hit points equal to 5 + your Constitution modifier if you have no more than half of your hit points left. You don't gain this benefit if you have 0 hit points."
        )
    ]
)

BATTLE_MASTER = Subclass(
    name="Battle Master",
    class_name="Fighter",
    description="Those who emulate the archetypal Battle Master employ martial techniques passed down through generations. To a Battle Master, combat is an academic field, sometimes including subjects beyond battle such as weaponsmithing and calligraphy.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Combat Superiority",
            level=3,
            description="You learn maneuvers that are fueled by special dice called superiority dice. You learn three maneuvers of your choice. You have four superiority dice, which are d8s. A superiority die is expended when you use it. You regain all of your expended superiority dice when you finish a short or long rest. You gain another superiority die at 7th level and one more at 15th level."
        ),
        SubclassFeature(
            name="Student of War",
            level=3,
            description="You gain proficiency with one type of artisan's tools of your choice."
        ),
        SubclassFeature(
            name="Know Your Enemy",
            level=7,
            description="If you spend at least 1 minute observing or interacting with another creature outside combat, you can learn certain information about its capabilities compared to your own. The DM tells you if the creature is your equal, superior, or inferior in regard to two of the following characteristics of your choice: Strength score, Dexterity score, Constitution score, Armor Class, Current hit points, Total class levels (if any), Fighter class levels (if any)."
        ),
        SubclassFeature(
            name="Improved Combat Superiority",
            level=10,
            description="Your superiority dice turn into d10s. At 18th level, they turn into d12s."
        ),
        SubclassFeature(
            name="Relentless",
            level=15,
            description="When you roll initiative and have no superiority dice remaining, you regain 1 superiority die."
        )
    ]
)

ELDRITCH_KNIGHT = Subclass(
    name="Eldritch Knight",
    class_name="Fighter",
    description="The archetypal Eldritch Knight combines the martial mastery common to all fighters with a careful study of magic. Eldritch Knights use magical techniques similar to those practiced by wizards.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Spellcasting",
            level=3,
            description="You augment your martial prowess with the ability to cast spells. You learn two cantrips of your choice from the wizard spell list. You learn an additional wizard cantrip of your choice at 10th level. The Eldritch Knight Spellcasting table shows how many spell slots you have to cast your spells of 1st level and higher."
        ),
        SubclassFeature(
            name="Weapon Bond",
            level=3,
            description="You learn a ritual that creates a magical bond between yourself and one weapon. You perform the ritual over the course of 1 hour, which can be done during a short rest. The weapon must be within your reach throughout the ritual. Once you have bonded a weapon to yourself, you can't be disarmed of that weapon unless you are incapacitated. If it is on the same plane of existence, you can summon that weapon as a bonus action, causing it to teleport instantly to your hand."
        ),
        SubclassFeature(
            name="War Magic",
            level=7,
            description="When you use your action to cast a cantrip, you can make one weapon attack as a bonus action."
        ),
        SubclassFeature(
            name="Eldritch Strike",
            level=10,
            description="You learn how to make your weapon strikes undercut a creature's resistance to your spells. When you hit a creature with a weapon attack, that creature has disadvantage on the next saving throw it makes against a spell you cast before the end of your next turn."
        ),
        SubclassFeature(
            name="Arcane Charge",
            level=15,
            description="You gain the ability to teleport up to 30 feet to an unoccupied space you can see when you use your Action Surge. You can teleport before or after the additional action."
        ),
        SubclassFeature(
            name="Improved War Magic",
            level=18,
            description="When you use your action to cast a spell, you can make one weapon attack as a bonus action."
        )
    ]
)

FIGHTER_SUBCLASSES = {
    "Champion": CHAMPION,
    "Battle Master": BATTLE_MASTER,
    "Eldritch Knight": ELDRITCH_KNIGHT
}

# Dicionário mestre de todas as subclasses
ALL_SUBCLASSES = {
    "Barbarian": BARBARIAN_SUBCLASSES,
    "Bard": BARD_SUBCLASSES,
    "Cleric": CLERIC_SUBCLASSES,
    "Druid": DRUID_SUBCLASSES,
    "Fighter": FIGHTER_SUBCLASSES
}


class SubclassDatabase:
    """Database de subclasses"""
    
    @staticmethod
    def get_subclasses_for_class(class_name: str) -> Dict[str, Subclass]:
        """Retorna todas as subclasses disponíveis para uma classe"""
        return ALL_SUBCLASSES.get(class_name, {})
    
    @staticmethod
    def get_subclass(class_name: str, subclass_name: str) -> Subclass:
        """Retorna uma subclasse específica"""
        subclasses = ALL_SUBCLASSES.get(class_name, {})
        return subclasses.get(subclass_name)
    
    @staticmethod
    def get_selection_level(class_name: str) -> int:
        """Retorna o nível em que a classe escolhe sua subclasse"""
        # A maioria das classes escolhe no nível 3
        # Cleric e Warlock escolhem no nível 1
        # Sorcerer e Wizard escolhem no nível 1 (origem/escola)
        special_levels = {
            "Cleric": 1,
            "Warlock": 1,
            "Sorcerer": 1,
            "Wizard": 2
        }
        return special_levels.get(class_name, 3)
