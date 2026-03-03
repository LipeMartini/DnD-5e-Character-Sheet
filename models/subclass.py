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

# ========== MONK SUBCLASSES ==========

WAY_OF_THE_OPEN_HAND = Subclass(
    name="Way of the Open Hand",
    class_name="Monk",
    description="Monks of the Way of the Open Hand are the ultimate masters of martial arts combat, whether armed or unarmed. They learn techniques to push and trip their opponents, manipulate ki to heal damage to their bodies, and practice advanced meditation that can protect them from harm.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Open Hand Technique",
            level=3,
            description="You can manipulate your enemy's ki when you harness your own. Whenever you hit a creature with one of the attacks granted by your Flurry of Blows, you can impose one of the following effects on that target:\n• It must succeed on a Dexterity saving throw or be knocked prone.\n• It must make a Strength saving throw. If it fails, you can push it up to 15 feet away from you.\n• It can't take reactions until the end of your next turn."
        ),
        SubclassFeature(
            name="Wholeness of Body",
            level=6,
            description="You gain the ability to heal yourself. As an action, you can regain hit points equal to three times your monk level. You must finish a long rest before you can use this feature again."
        ),
        SubclassFeature(
            name="Tranquility",
            level=11,
            description="You can enter a special meditation that surrounds you with an aura of peace. At the end of a long rest, you gain the effect of a Sanctuary spell that lasts until the start of your next long rest (the spell can end early as normal). The saving throw DC for the spell equals 8 + your Wisdom modifier + your proficiency bonus."
        ),
        SubclassFeature(
            name="Quivering Palm",
            level=17,
            description="You gain the ability to set up lethal vibrations in someone's body. When you hit a creature with an unarmed strike, you can spend 3 ki points to start these imperceptible vibrations, which last for a number of days equal to your monk level. The vibrations are harmless unless you use your action to end them. To do so, you and the target must be on the same plane of existence. When you use this action, the creature must make a Constitution saving throw. If it fails, it is reduced to 0 hit points. If it succeeds, it takes 10d10 necrotic damage. You can have only one creature under the effect of this feature at a time. You can choose to end the vibrations harmlessly without using an action."
        )
    ]
)

WAY_OF_SHADOW = Subclass(
    name="Way of Shadow",
    class_name="Monk",
    description="Monks of the Way of Shadow follow a tradition that values stealth and subterfuge. These monks might be called ninjas or shadowdancers, and they serve as spies and assassins. Sometimes the members of a ninja monastery are family members, forming a clan sworn to secrecy about their arts and missions.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Shadow Arts",
            level=3,
            description="You can use your ki to duplicate the effects of certain spells. As an action, you can spend 2 ki points to cast Darkness, Darkvision, Pass without Trace, or Silence, without providing material components. Additionally, you gain the Minor Illusion cantrip if you don't already know it."
        ),
        SubclassFeature(
            name="Shadow Step",
            level=6,
            description="You gain the ability to step from one shadow into another. When you are in dim light or darkness, as a bonus action you can teleport up to 60 feet to an unoccupied space you can see that is also in dim light or darkness. You then have advantage on the first melee attack you make before the end of the turn."
        ),
        SubclassFeature(
            name="Cloak of Shadows",
            level=11,
            description="You have learned to become one with the shadows. When you are in an area of dim light or darkness, you can use your action to become invisible. You remain invisible until you make an attack, cast a spell, or are in an area of bright light."
        ),
        SubclassFeature(
            name="Opportunist",
            level=17,
            description="You can exploit a creature's momentary distraction when it is hit by an attack. Whenever a creature within 5 feet of you is hit by an attack made by a creature other than you, you can use your reaction to make a melee attack against that creature."
        )
    ]
)

WAY_OF_THE_FOUR_ELEMENTS = Subclass(
    name="Way of the Four Elements",
    class_name="Monk",
    description="You follow a monastic tradition that teaches you to harness the elements. When you focus your ki, you can align yourself with the forces of creation and bend the four elements to your will, using them as an extension of your body.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Disciple of the Elements",
            level=3,
            description="You learn magical disciplines that harness the power of the four elements. You know the Elemental Attunement discipline and one other elemental discipline of your choice. You learn one additional elemental discipline of your choice at 6th, 11th, and 17th level.\n\nWhenever you learn a new elemental discipline, you can also replace one elemental discipline that you already know with a different discipline.\n\nSome elemental disciplines require you to spend ki points when you use them. You must spend the ki points when you use the discipline. The maximum number of ki points you can spend to cast a spell in this way (including its base ki point cost and any additional ki points you spend to increase its level) is determined by your monk level."
        ),
        SubclassFeature(
            name="Additional Elemental Discipline",
            level=6,
            description="You learn one additional elemental discipline of your choice. You can also replace one elemental discipline that you already know with a different discipline."
        ),
        SubclassFeature(
            name="Additional Elemental Discipline",
            level=11,
            description="You learn one additional elemental discipline of your choice. You can also replace one elemental discipline that you already know with a different discipline."
        ),
        SubclassFeature(
            name="Additional Elemental Discipline",
            level=17,
            description="You learn one additional elemental discipline of your choice. You can also replace one elemental discipline that you already know with a different discipline."
        )
    ]
)

MONK_SUBCLASSES = {
    "Way of the Open Hand": WAY_OF_THE_OPEN_HAND,
    "Way of Shadow": WAY_OF_SHADOW,
    "Way of the Four Elements": WAY_OF_THE_FOUR_ELEMENTS
}

# ========== PALADIN SUBCLASSES ==========

OATH_OF_DEVOTION = Subclass(
    name="Oath of Devotion",
    class_name="Paladin",
    description="The Oath of Devotion binds a paladin to the loftiest ideals of justice, virtue, and order. Sometimes called cavaliers, white knights, or holy warriors, these paladins meet the ideal of the knight in shining armor, acting with honor in pursuit of justice and the greater good.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Protection from Evil and Good, Sanctuary\n5th: Lesser Restoration, Zone of Truth\n9th: Beacon of Hope, Dispel Magic\n13th: Freedom of Movement, Guardian of Faith\n17th: Commune, Flame Strike"
        ),
        SubclassFeature(
            name="Channel Divinity: Sacred Weapon",
            level=3,
            description="As an action, you can imbue one weapon that you are holding with positive energy, using your Channel Divinity. For 1 minute, you add your Charisma modifier to attack rolls made with that weapon (with a minimum bonus of +1). The weapon also emits bright light in a 20-foot radius and dim light 20 feet beyond that. If the weapon is not already magical, it becomes magical for the duration. You can end this effect on your turn as part of any other action. If you are no longer holding or carrying this weapon, or if you fall unconscious, this effect ends."
        ),
        SubclassFeature(
            name="Channel Divinity: Turn the Unholy",
            level=3,
            description="As an action, you present your holy symbol and speak a prayer censuring fiends and undead, using your Channel Divinity. Each fiend or undead that can see or hear you within 30 feet of you must make a Wisdom saving throw. If the creature fails its saving throw, it is turned for 1 minute or until it takes damage. A turned creature must spend its turns trying to move as far away from you as it can, and it can't willingly move to a space within 30 feet of you. It also can't take reactions. For its action, it can use only the Dash action or try to escape from an effect that prevents it from moving. If there's nowhere to move, the creature can use the Dodge action."
        ),
        SubclassFeature(
            name="Aura of Devotion",
            level=7,
            description="You and friendly creatures within 10 feet of you can't be charmed while you are conscious. At 18th level, the range of this aura increases to 30 feet."
        ),
        SubclassFeature(
            name="Purity of Spirit",
            level=15,
            description="You are always under the effects of a Protection from Evil and Good spell."
        ),
        SubclassFeature(
            name="Holy Nimbus",
            level=20,
            description="As an action, you can emanate an aura of sunlight. For 1 minute, bright light shines from you in a 30-foot radius, and dim light shines 30 feet beyond that. Whenever an enemy creature starts its turn in the bright light, the creature takes 10 radiant damage. In addition, for the duration, you have advantage on saving throws against spells cast by fiends or undead. Once you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

OATH_OF_THE_ANCIENTS = Subclass(
    name="Oath of the Ancients",
    class_name="Paladin",
    description="The Oath of the Ancients is as old as the race of elves and the rituals of the druids. Sometimes called fey knights, green knights, or horned knights, paladins who swear this oath cast their lot with the side of the light in the cosmic struggle against darkness because they love the beautiful and life-giving things of the world.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Ensnaring Strike, Speak with Animals\n5th: Moonbeam, Misty Step\n9th: Plant Growth, Protection from Energy\n13th: Ice Storm, Stoneskin\n17th: Commune with Nature, Tree Stride"
        ),
        SubclassFeature(
            name="Channel Divinity: Nature's Wrath",
            level=3,
            description="You can use your Channel Divinity to invoke primeval forces to ensnare a foe. As an action, you can cause spectral vines to spring up and reach for a creature within 10 feet of you that you can see. The creature must succeed on a Strength or Dexterity saving throw (its choice) or be restrained. While restrained by the vines, the creature repeats the saving throw at the end of each of its turns. On a success, it frees itself and the vines vanish."
        ),
        SubclassFeature(
            name="Channel Divinity: Turn the Faithless",
            level=3,
            description="You can use your Channel Divinity to utter ancient words that are painful for fey and fiends to hear. As an action, you present your holy symbol, and each fey or fiend within 30 feet of you that can hear you must make a Wisdom saving throw. On a failed save, the creature is turned for 1 minute or until it takes damage."
        ),
        SubclassFeature(
            name="Aura of Warding",
            level=7,
            description="Ancient magic lies so heavily upon you that it forms an eldritch ward. You and friendly creatures within 10 feet of you have resistance to damage from spells. At 18th level, the range of this aura increases to 30 feet."
        ),
        SubclassFeature(
            name="Undying Sentinel",
            level=15,
            description="When you are reduced to 0 hit points and are not killed outright, you can choose to drop to 1 hit point instead. Once you use this ability, you can't use it again until you finish a long rest. Additionally, you suffer none of the drawbacks of old age, and you can't be aged magically."
        ),
        SubclassFeature(
            name="Elder Champion",
            level=20,
            description="You can assume the form of an ancient force of nature, taking on an appearance you choose. For example, your skin might turn green or take on a bark-like texture, your hair might become leafy or moss-like, or you might sprout antlers or a lion-like mane. Using your action, you undergo a transformation. For 1 minute, you gain the following benefits:\n• At the start of each of your turns, you regain 10 hit points.\n• Whenever you cast a paladin spell that has a casting time of 1 action, you can cast it using a bonus action instead.\n• Enemy creatures within 10 feet of you have disadvantage on saving throws against your paladin spells and Channel Divinity options.\nOnce you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

OATH_OF_VENGEANCE = Subclass(
    name="Oath of Vengeance",
    class_name="Paladin",
    description="The Oath of Vengeance is a solemn commitment to punish those who have committed a grievous sin. When evil forces slaughter helpless villagers, when an entire people turns against the will of the gods, when a thieves' guild grows too violent and powerful, when a dragon rampages through the countryside—at times like these, paladins arise and swear an Oath of Vengeance to set right that which has gone wrong.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Oath Spells",
            level=3,
            description="You gain oath spells at the paladin levels listed.\n3rd: Bane, Hunter's Mark\n5th: Hold Person, Misty Step\n9th: Haste, Protection from Energy\n13th: Banishment, Dimension Door\n17th: Hold Monster, Scrying"
        ),
        SubclassFeature(
            name="Channel Divinity: Abjure Enemy",
            level=3,
            description="As an action, you present your holy symbol and speak a prayer of denunciation, using your Channel Divinity. Choose one creature within 60 feet of you that you can see. That creature must make a Wisdom saving throw, unless it is immune to being frightened. Fiends and undead have disadvantage on this saving throw. On a failed save, the creature is frightened for 1 minute or until it takes any damage. While frightened, the creature's speed is 0, and it can't benefit from any bonus to its speed. On a successful save, the creature's speed is halved for 1 minute or until the creature takes any damage."
        ),
        SubclassFeature(
            name="Channel Divinity: Vow of Enmity",
            level=3,
            description="As a bonus action, you can utter a vow of enmity against a creature you can see within 10 feet of you, using your Channel Divinity. You gain advantage on attack rolls against the creature for 1 minute or until it drops to 0 hit points or falls unconscious."
        ),
        SubclassFeature(
            name="Relentless Avenger",
            level=7,
            description="Your supernatural focus helps you close off a foe's retreat. When you hit a creature with an opportunity attack, you can move up to half your speed immediately after the attack and as part of the same reaction. This movement doesn't provoke opportunity attacks."
        ),
        SubclassFeature(
            name="Soul of Vengeance",
            level=15,
            description="The authority with which you speak your Vow of Enmity gives you greater power over your foe. When a creature under the effect of your Vow of Enmity makes an attack, you can use your reaction to make a melee weapon attack against that creature if it is within range."
        ),
        SubclassFeature(
            name="Avenging Angel",
            level=20,
            description="You can assume the form of an angelic avenger. Using your action, you undergo a transformation. For 1 minute, you gain the following benefits:\n• Wings sprout from your back and grant you a flying speed of 60 feet.\n• You emanate an aura of menace in a 30-foot radius. The first time any enemy creature enters the aura or starts its turn there during a battle, the creature must succeed on a Wisdom saving throw or become frightened of you for 1 minute or until it takes any damage. Attack rolls against the frightened creature have advantage.\nOnce you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

PALADIN_SUBCLASSES = {
    "Oath of Devotion": OATH_OF_DEVOTION,
    "Oath of the Ancients": OATH_OF_THE_ANCIENTS,
    "Oath of Vengeance": OATH_OF_VENGEANCE
}

# ========== RANGER SUBCLASSES ==========

HUNTER = Subclass(
    name="Hunter",
    class_name="Ranger",
    description="Emulating the Hunter archetype means accepting your place as a bulwark between civilization and the terrors of the wilderness. As you walk the Hunter's path, you learn specialized techniques for fighting the threats you face.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Hunter's Prey",
            level=3,
            description="You gain one of the following features of your choice.\nColossus Slayer: Your tenacity can wear down the most potent foes. When you hit a creature with a weapon attack, the creature takes an extra 1d8 damage if it's below its hit point maximum. You can deal this extra damage only once per turn.\nGiant Killer: When a Large or larger creature within 5 feet of you hits or misses you with an attack, you can use your reaction to attack that creature immediately after its attack, provided that you can see the creature.\nHorde Breaker: Once on each of your turns when you make a weapon attack, you can make another attack with the same weapon against a different creature that is within 5 feet of the original target and within range of your weapon."
        ),
        SubclassFeature(
            name="Defensive Tactics",
            level=7,
            description="You gain one of the following features of your choice.\nEscape the Horde: Opportunity attacks against you are made with disadvantage.\nMultiattack Defense: When a creature hits you with an attack, you gain a +4 bonus to AC against all subsequent attacks made by that creature for the rest of the turn.\nSteel Will: You have advantage on saving throws against being frightened."
        ),
        SubclassFeature(
            name="Multiattack",
            level=11,
            description="You gain one of the following features of your choice.\nVolley: You can use your action to make a ranged attack against any number of creatures within 10 feet of a point you can see within your weapon's range. You must have ammunition for each target, as normal, and you make a separate attack roll for each target.\nWhirlwind Attack: You can use your action to make a melee attack against any number of creatures within 5 feet of you, with a separate attack roll for each target."
        ),
        SubclassFeature(
            name="Superior Hunter's Defense",
            level=15,
            description="You gain one of the following features of your choice.\nEvasion: When you are subjected to an effect, such as a red dragon's fiery breath or a Lightning Bolt spell, that allows you to make a Dexterity saving throw to take only half damage, you instead take no damage if you succeed on the saving throw, and only half damage if you fail.\nStand Against the Tide: When a hostile creature misses you with a melee attack, you can use your reaction to force that creature to repeat the same attack against another creature (other than itself) of your choice.\nUncanny Dodge: When an attacker that you can see hits you with an attack, you can use your reaction to halve the attack's damage against you."
        )
    ]
)

BEAST_MASTER = Subclass(
    name="Beast Master",
    class_name="Ranger",
    description="The Beast Master archetype embodies a friendship between the civilized races and the beasts of the world. United in focus, beast and ranger work as one to fight the monstrous foes that threaten civilization and the wilderness alike.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Ranger's Companion",
            level=3,
            description="You gain a beast companion that accompanies you on your adventures and is trained to fight alongside you. Choose a beast that is no larger than Medium and that has a challenge rating of 1/4 or lower. Add your proficiency bonus to the beast's AC, attack rolls, and damage rolls, as well as to any saving throws and skills it is proficient in. Its hit point maximum equals its normal maximum or four times your ranger level, whichever is higher. Like any creature, the beast can spend Hit Dice during a short rest. The beast obeys your commands as best as it can. It takes its turn on your initiative. On your turn, you can verbally command the beast where to move (no action required by you). You can use your action to verbally command it to take the Attack, Dash, Disengage, or Help action. If you don't issue a command, the beast takes the Dodge action."
        ),
        SubclassFeature(
            name="Exceptional Training",
            level=7,
            description="On any of your turns when your beast companion doesn't attack, you can use a bonus action to command the beast to take the Dash, Disengage, or Help action on its turn. In addition, the beast's attacks now count as magical for the purpose of overcoming resistance and immunity to nonmagical attacks and damage."
        ),
        SubclassFeature(
            name="Bestial Fury",
            level=11,
            description="When you command your beast companion to take the Attack action, the beast can make two attacks, or it can take the Multiattack action if it has that action."
        ),
        SubclassFeature(
            name="Share Spells",
            level=15,
            description="When you cast a spell targeting yourself, you can also affect your beast companion with the spell if the beast is within 30 feet of you."
        )
    ]
)

RANGER_SUBCLASSES = {
    "Hunter": HUNTER,
    "Beast Master": BEAST_MASTER
}

# ========== ROGUE SUBCLASSES ==========

THIEF = Subclass(
    name="Thief",
    class_name="Rogue",
    description="You hone your skills in the larcenous arts. Burglars, bandits, cutpurses, and other criminals typically follow this archetype, but so do rogues who prefer to think of themselves as professional treasure seekers, explorers, delvers, and investigators.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Fast Hands",
            level=3,
            description="You can use the bonus action granted by your Cunning Action to make a Dexterity (Sleight of Hand) check, use your thieves' tools to disarm a trap or open a lock, or take the Use an Object action."
        ),
        SubclassFeature(
            name="Second-Story Work",
            level=3,
            description="You gain the ability to climb faster than normal; climbing no longer costs you extra movement. In addition, when you make a running jump, the distance you cover increases by a number of feet equal to your Dexterity modifier."
        ),
        SubclassFeature(
            name="Supreme Sneak",
            level=9,
            description="You have advantage on a Dexterity (Stealth) check if you move no more than half your speed on the same turn."
        ),
        SubclassFeature(
            name="Use Magic Device",
            level=13,
            description="You have learned enough about the workings of magic that you can improvise the use of items even when they are not intended for you. You ignore all class, race, and level requirements on the use of magic items."
        ),
        SubclassFeature(
            name="Thief's Reflexes",
            level=17,
            description="You have become adept at laying ambushes and quickly escaping danger. You can take two turns during the first round of any combat. You take your first turn at your normal initiative and your second turn at your initiative minus 10. You can't use this feature when you are surprised."
        )
    ]
)

ASSASSIN = Subclass(
    name="Assassin",
    class_name="Rogue",
    description="You focus your training on the grim art of death. Those who adhere to this archetype are diverse: hired killers, spies, bounty hunters, and even specially anointed priests trained to exterminate the enemies of their deity.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Bonus Proficiencies",
            level=3,
            description="You gain proficiency with the disguise kit and the poisoner's kit."
        ),
        SubclassFeature(
            name="Assassinate",
            level=3,
            description="You are at your deadliest when you get the drop on your enemies. You have advantage on attack rolls against any creature that hasn't taken a turn in the combat yet. In addition, any hit you score against a creature that is surprised is a critical hit."
        ),
        SubclassFeature(
            name="Infiltration Expertise",
            level=9,
            description="You can unfailingly create false identities for yourself. You must spend seven days and 25 gp to establish the history, profession, and affiliations for an identity. You can't establish an identity that belongs to someone else. Thereafter, if you adopt the new identity as a disguise, other creatures believe you to be that person until given an obvious reason not to."
        ),
        SubclassFeature(
            name="Impostor",
            level=13,
            description="You gain the ability to unerringly mimic another person's speech, writing, and behavior. You must spend at least three hours studying these three components of the person's behavior, listening to speech, examining handwriting, and observing mannerisms. Your ruse is indiscernible to the casual observer. If a wary creature suspects something is amiss, you have advantage on any Charisma (Deception) check you make to avoid detection."
        ),
        SubclassFeature(
            name="Death Strike",
            level=17,
            description="You become a master of instant death. When you attack and hit a creature that is surprised, it must make a Constitution saving throw (DC 8 + your Dexterity modifier + your proficiency bonus). On a failed save, double the damage of your attack against the creature."
        )
    ]
)

ARCANE_TRICKSTER = Subclass(
    name="Arcane Trickster",
    class_name="Rogue",
    description="Some rogues enhance their fine-honed skills of stealth and agility with magic, learning tricks of enchantment and illusion. These rogues include pickpockets and burglars, but also pranksters, mischief-makers, and a significant number of adventurers.",
    selection_level=3,
    features=[
        SubclassFeature(
            name="Spellcasting",
            level=3,
            description="You augment your martial prowess with the ability to cast spells. You learn three cantrips: Mage Hand and two other cantrips of your choice from the wizard spell list. You learn another wizard cantrip of your choice at 10th level. When you cast Mage Hand, you can make the spectral hand invisible, and you can perform additional tasks with it (stow/retrieve objects, pick locks, disarm traps, use objects)."
        ),
        SubclassFeature(
            name="Mage Hand Legerdemain",
            level=3,
            description="When you cast Mage Hand, you can make the spectral hand invisible, and you can perform the following additional tasks with it:\n• You can stow one object the hand is holding in a container worn or carried by another creature.\n• You can retrieve an object in a container worn or carried by another creature.\n• You can use thieves' tools to pick locks and disarm traps at range.\nYou can perform one of these tasks without being noticed by a creature if you succeed on a Dexterity (Sleight of Hand) check contested by the creature's Wisdom (Perception) check. In addition, you can use the bonus action granted by your Cunning Action to control the hand."
        ),
        SubclassFeature(
            name="Magical Ambush",
            level=9,
            description="If you are hidden from a creature when you cast a spell on it, the creature has disadvantage on any saving throw it makes against the spell this turn."
        ),
        SubclassFeature(
            name="Versatile Trickster",
            level=13,
            description="You gain the ability to distract targets with your Mage Hand. As a bonus action on your turn, you can designate a creature within 5 feet of the spectral hand created by the spell. Doing so gives you advantage on attack rolls against that creature until the end of the turn."
        ),
        SubclassFeature(
            name="Spell Thief",
            level=17,
            description="You gain the ability to magically steal the knowledge of how to cast a spell from another spellcaster. Immediately after a creature casts a spell that targets you or includes you in its area of effect, you can use your reaction to force the creature to make a saving throw with its spellcasting ability modifier. The DC equals your spell save DC. On a failed save, you negate the spell's effect against you, and you steal the knowledge of the spell if it is at least 1st level and of a level you can cast (it doesn't need to be a wizard spell). For the next 8 hours, you know the spell and can cast it using your spell slots. The creature can't cast that spell until the 8 hours have passed. Once you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

ROGUE_SUBCLASSES = {
    "Thief": THIEF,
    "Assassin": ASSASSIN,
    "Arcane Trickster": ARCANE_TRICKSTER
}

# ========== SORCERER SUBCLASSES ==========

DRACONIC_BLOODLINE = Subclass(
    name="Draconic Bloodline",
    class_name="Sorcerer",
    description="Your innate magic comes from draconic magic that was mingled with your blood or that of your ancestors. Most often, sorcerers with this origin trace their descent back to a mighty sorcerer of ancient times who made a bargain with a dragon or who might even have claimed a dragon parent.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Dragon Ancestor",
            level=1,
            description="You choose one type of dragon as your ancestor. The damage type associated with each dragon is used by features you gain later. You can speak, read, and write Draconic. Additionally, whenever you make a Charisma check when interacting with dragons, your proficiency bonus is doubled if it applies to the check."
        ),
        SubclassFeature(
            name="Draconic Resilience",
            level=1,
            description="As magic flows through your body, it causes physical traits of your dragon ancestors to emerge. At 1st level, your hit point maximum increases by 1 and increases by 1 again whenever you gain a level in this class. Additionally, parts of your skin are covered by a thin sheen of dragon-like scales. When you aren't wearing armor, your AC equals 13 + your Dexterity modifier."
        ),
        SubclassFeature(
            name="Elemental Affinity",
            level=6,
            description="When you cast a spell that deals damage of the type associated with your draconic ancestry, you can add your Charisma modifier to one damage roll of that spell. At the same time, you can spend 1 sorcery point to gain resistance to that damage type for 1 hour."
        ),
        SubclassFeature(
            name="Dragon Wings",
            level=14,
            description="You gain the ability to sprout a pair of dragon wings from your back, gaining a flying speed equal to your current speed. You can create these wings as a bonus action on your turn. They last until you dismiss them as a bonus action on your turn. You can't manifest your wings while wearing armor unless the armor is made to accommodate them, and clothing not made to accommodate your wings might be destroyed when you manifest them."
        ),
        SubclassFeature(
            name="Draconic Presence",
            level=18,
            description="You can channel the dread presence of your dragon ancestor, causing those around you to become awestruck or frightened. As an action, you can spend 5 sorcery points to draw on this power and exude an aura of awe or fear (your choice) to a distance of 60 feet. For 1 minute or until you lose your concentration, each hostile creature that starts its turn in this aura must succeed on a Wisdom saving throw or be charmed (if you chose awe) or frightened (if you chose fear) until the aura ends. A creature that succeeds on this saving throw is immune to your aura for 24 hours."
        )
    ]
)

WILD_MAGIC = Subclass(
    name="Wild Magic",
    class_name="Sorcerer",
    description="Your innate magic comes from the wild forces of chaos that underlie the order of creation. You might have endured exposure to some form of raw magic, perhaps through a planar portal leading to Limbo, the Elemental Planes, or the Far Realm.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Wild Magic Surge",
            level=1,
            description="Your spellcasting can unleash surges of untamed magic. Immediately after you cast a sorcerer spell of 1st level or higher, the DM can have you roll a d20. If you roll a 1, roll on the Wild Magic Surge table to create a random magical effect."
        ),
        SubclassFeature(
            name="Tides of Chaos",
            level=1,
            description="You can manipulate the forces of chance and chaos to gain advantage on one attack roll, ability check, or saving throw. Once you do so, you must finish a long rest before you can use this feature again. Any time before you regain the use of this feature, the DM can have you roll on the Wild Magic Surge table immediately after you cast a sorcerer spell of 1st level or higher. You then regain the use of this feature."
        ),
        SubclassFeature(
            name="Bend Luck",
            level=6,
            description="You have the ability to twist fate using your wild magic. When another creature you can see makes an attack roll, an ability check, or a saving throw, you can use your reaction and spend 2 sorcery points to roll 1d4 and apply the number rolled as a bonus or penalty (your choice) to the creature's roll. You can do so after the creature rolls but before any effects of the roll occur."
        ),
        SubclassFeature(
            name="Controlled Chaos",
            level=14,
            description="You gain a modicum of control over the surges of your wild magic. Whenever you roll on the Wild Magic Surge table, you can roll twice and use either number."
        ),
        SubclassFeature(
            name="Spell Bombardment",
            level=18,
            description="The harmful energy of your spells intensifies. When you roll damage for a spell and roll the highest number possible on any of the dice, choose one of those dice, roll it again and add that roll to the damage. You can use the feature only once per turn."
        )
    ]
)

SORCERER_SUBCLASSES = {
    "Draconic Bloodline": DRACONIC_BLOODLINE,
    "Wild Magic": WILD_MAGIC
}

# ========== WARLOCK SUBCLASSES ==========

THE_ARCHFEY = Subclass(
    name="The Archfey",
    class_name="Warlock",
    description="Your patron is a lord or lady of the fey, a creature of legend who holds secrets that were forgotten before the mortal races were born. This being's motivations are often inscrutable, and sometimes whimsical, and might involve a striving for greater magical power or the settling of age-old grudges.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="The Archfey lets you choose from an expanded list of spells when you learn a warlock spell. The following spells are added to the warlock spell list for you.\n1st: Faerie Fire, Sleep\n2nd: Calm Emotions, Phantasmal Force\n3rd: Blink, Plant Growth\n4th: Dominate Beast, Greater Invisibility\n5th: Dominate Person, Seeming"
        ),
        SubclassFeature(
            name="Fey Presence",
            level=1,
            description="Your patron bestows upon you the ability to project the beguiling and fearsome presence of the fey. As an action, you can cause each creature in a 10-foot cube originating from you to make a Wisdom saving throw against your warlock spell save DC. The creatures that fail their saving throws are all charmed or frightened by you (your choice) until the end of your next turn. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Misty Escape",
            level=6,
            description="You can vanish in a puff of mist in response to harm. When you take damage, you can use your reaction to turn invisible and teleport up to 60 feet to an unoccupied space you can see. You remain invisible until the start of your next turn or until you attack or cast a spell. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Beguiling Defenses",
            level=10,
            description="Your patron teaches you how to turn the mind-affecting magic of your enemies against them. You are immune to being charmed, and when another creature attempts to charm you, you can use your reaction to attempt to turn the charm back on that creature. The creature must succeed on a Wisdom saving throw against your warlock spell save DC or be charmed by you for 1 minute or until the creature takes any damage."
        ),
        SubclassFeature(
            name="Dark Delirium",
            level=14,
            description="You can plunge a creature into an illusory realm. As an action, choose a creature that you can see within 60 feet of you. It must make a Wisdom saving throw against your warlock spell save DC. On a failed save, it is charmed or frightened by you (your choice) for 1 minute or until your concentration is broken. This effect ends early if the creature takes any damage. Until this illusion ends, the creature thinks it is lost in a misty realm, the appearance of which you choose. The creature can see and hear only itself, you, and the illusion. You must finish a short or long rest before you can use this feature again."
        )
    ]
)

THE_FIEND = Subclass(
    name="The Fiend",
    class_name="Warlock",
    description="You have made a pact with a fiend from the lower planes of existence, a being whose aims are evil, even if you strive against those aims. Such beings desire the corruption or destruction of all things, ultimately including you.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="The Fiend lets you choose from an expanded list of spells when you learn a warlock spell. The following spells are added to the warlock spell list for you.\n1st: Burning Hands, Command\n2nd: Blindness/Deafness, Scorching Ray\n3rd: Fireball, Stinking Cloud\n4th: Fire Shield, Wall of Fire\n5th: Flame Strike, Hallow"
        ),
        SubclassFeature(
            name="Dark One's Blessing",
            level=1,
            description="When you reduce a hostile creature to 0 hit points, you gain temporary hit points equal to your Charisma modifier + your warlock level (minimum of 1)."
        ),
        SubclassFeature(
            name="Dark One's Own Luck",
            level=6,
            description="You can call on your patron to alter fate in your favor. When you make an ability check or a saving throw, you can use this feature to add a d10 to your roll. You can do so after seeing the initial roll but before any of the roll's effects occur. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Fiendish Resilience",
            level=10,
            description="You can choose one damage type when you finish a short or long rest. You gain resistance to that damage type until you choose a different one with this feature. Damage from magical weapons or silver weapons ignores this resistance."
        ),
        SubclassFeature(
            name="Hurl Through Hell",
            level=14,
            description="When you hit a creature with an attack, you can use this feature to instantly transport the target through the lower planes. The creature disappears and hurtles through a nightmare landscape. At the end of your next turn, the target returns to the space it previously occupied, or the nearest unoccupied space. If the target is not a fiend, it takes 10d10 psychic damage as it reels from its horrific experience. Once you use this feature, you can't use it again until you finish a long rest."
        )
    ]
)

THE_GREAT_OLD_ONE = Subclass(
    name="The Great Old One",
    class_name="Warlock",
    description="Your patron is a mysterious entity whose nature is utterly foreign to the fabric of reality. It might come from the Far Realm, the space beyond reality, or it could be one of the elder gods known only in legends.",
    selection_level=1,
    features=[
        SubclassFeature(
            name="Expanded Spell List",
            level=1,
            description="The Great Old One lets you choose from an expanded list of spells when you learn a warlock spell. The following spells are added to the warlock spell list for you.\n1st: Dissonant Whispers, Tasha's Hideous Laughter\n2nd: Detect Thoughts, Phantasmal Force\n3rd: Clairvoyance, Sending\n4th: Dominate Beast, Evard's Black Tentacles\n5th: Dominate Person, Telekinesis"
        ),
        SubclassFeature(
            name="Awakened Mind",
            level=1,
            description="Your alien knowledge gives you the ability to touch the minds of other creatures. You can communicate telepathically with any creature you can see within 30 feet of you. You don't need to share a language with the creature for it to understand your telepathic utterances, but the creature must be able to understand at least one language."
        ),
        SubclassFeature(
            name="Entropic Ward",
            level=6,
            description="You learn to magically ward yourself against attack and to turn an enemy's failed strike into good luck for yourself. When a creature makes an attack roll against you, you can use your reaction to impose disadvantage on that roll. If the attack misses you, your next attack roll against the creature has advantage if you make it before the end of your next turn. Once you use this feature, you can't use it again until you finish a short or long rest."
        ),
        SubclassFeature(
            name="Thought Shield",
            level=10,
            description="Your thoughts can't be read by telepathy or other means unless you allow it. You also have resistance to psychic damage, and whenever a creature deals psychic damage to you, that creature takes the same amount of damage that you do."
        ),
        SubclassFeature(
            name="Create Thrall",
            level=14,
            description="You gain the ability to infect a humanoid's mind with the alien magic of your patron. You can use your action to touch an incapacitated humanoid. That creature is then charmed by you until a Remove Curse spell is cast on it, the charmed condition is removed from it, or you use this feature again. You can communicate telepathically with the charmed creature as long as the two of you are on the same plane of existence."
        )
    ]
)

WARLOCK_SUBCLASSES = {
    "The Archfey": THE_ARCHFEY,
    "The Fiend": THE_FIEND,
    "The Great Old One": THE_GREAT_OLD_ONE
}

# ========== WIZARD SUBCLASSES ==========

SCHOOL_OF_ABJURATION = Subclass(
    name="School of Abjuration",
    class_name="Wizard",
    description="The School of Abjuration emphasizes magic that blocks, banishes, or protects. Detractors of this school say that its tradition is about denial, negation rather than positive assertion. You understand, however, that ending harmful effects, protecting the weak, and banishing evil influences is anything but a philosophical void.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Abjuration Savant",
            level=2,
            description="The gold and time you must spend to copy an abjuration spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Arcane Ward",
            level=2,
            description="You can weave magic around yourself for protection. When you cast an abjuration spell of 1st level or higher, you can simultaneously use a strand of the spell's magic to create a magical ward on yourself that lasts until you finish a long rest. The ward has hit points equal to twice your wizard level + your Intelligence modifier. Whenever you take damage, the ward takes the damage instead. If this damage reduces the ward to 0 hit points, you take any remaining damage. While the ward has 0 hit points, it can't absorb damage, but its magic remains. Whenever you cast an abjuration spell of 1st level or higher, the ward regains a number of hit points equal to twice the level of the spell."
        ),
        SubclassFeature(
            name="Projected Ward",
            level=6,
            description="When a creature that you can see within 30 feet of you takes damage, you can use your reaction to cause your Arcane Ward to absorb that damage. If this damage reduces the ward to 0 hit points, the warded creature takes any remaining damage."
        ),
        SubclassFeature(
            name="Improved Abjuration",
            level=10,
            description="When you cast an abjuration spell that requires you to make an ability check as a part of casting that spell (as in Counterspell and Dispel Magic), you add your proficiency bonus to that ability check."
        ),
        SubclassFeature(
            name="Spell Resistance",
            level=14,
            description="You have advantage on saving throws against spells. Furthermore, you have resistance against the damage of spells."
        )
    ]
)

SCHOOL_OF_EVOCATION = Subclass(
    name="School of Evocation",
    class_name="Wizard",
    description="You focus your study on magic that creates powerful elemental effects such as bitter cold, searing flame, rolling thunder, crackling lightning, and burning acid. Some evokers find employment in military forces, serving as artillery to blast enemy armies from afar.",
    selection_level=2,
    features=[
        SubclassFeature(
            name="Evocation Savant",
            level=2,
            description="The gold and time you must spend to copy an evocation spell into your spellbook is halved."
        ),
        SubclassFeature(
            name="Sculpt Spells",
            level=2,
            description="You can create pockets of relative safety within the effects of your evocation spells. When you cast an evocation spell that affects other creatures that you can see, you can choose a number of them equal to 1 + the spell's level. The chosen creatures automatically succeed on their saving throws against the spell, and they take no damage if they would normally take half damage on a successful save."
        ),
        SubclassFeature(
            name="Potent Cantrip",
            level=6,
            description="Your damaging cantrips affect even creatures that avoid the brunt of the effect. When a creature succeeds on a saving throw against your cantrip, the creature takes half the cantrip's damage (if any) but suffers no additional effect from the cantrip."
        ),
        SubclassFeature(
            name="Empowered Evocation",
            level=10,
            description="You can add your Intelligence modifier to one damage roll of any wizard evocation spell you cast."
        ),
        SubclassFeature(
            name="Overchannel",
            level=14,
            description="You can increase the power of your simpler spells. When you cast a wizard spell of 1st through 5th level that deals damage, you can deal maximum damage with that spell. The first time you do so, you suffer no adverse effect. If you use this feature again before you finish a long rest, you take 2d12 necrotic damage for each level of the spell, immediately after you cast it. Each time you use this feature again before finishing a long rest, the necrotic damage per spell level increases by 1d12. This damage ignores resistance and immunity."
        )
    ]
)

WIZARD_SUBCLASSES = {
    "School of Abjuration": SCHOOL_OF_ABJURATION,
    "School of Evocation": SCHOOL_OF_EVOCATION
}

# Dicionário mestre de todas as subclasses
ALL_SUBCLASSES = {
    "Barbarian": BARBARIAN_SUBCLASSES,
    "Bard": BARD_SUBCLASSES,
    "Cleric": CLERIC_SUBCLASSES,
    "Druid": DRUID_SUBCLASSES,
    "Fighter": FIGHTER_SUBCLASSES,
    "Monk": MONK_SUBCLASSES,
    "Paladin": PALADIN_SUBCLASSES,
    "Ranger": RANGER_SUBCLASSES,
    "Rogue": ROGUE_SUBCLASSES,
    "Sorcerer": SORCERER_SUBCLASSES,
    "Warlock": WARLOCK_SUBCLASSES,
    "Wizard": WIZARD_SUBCLASSES
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
