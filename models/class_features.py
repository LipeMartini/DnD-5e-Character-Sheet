"""
Sistema de features de classe por nível para D&D 5e
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ClassFeature:
    """Representa uma feature de classe"""
    name: str
    description: str
    level: int
    
    def __str__(self):
        return self.name


# ========== FIGHTER FEATURES ==========
FIGHTER_FEATURES = {
    1: [
        ClassFeature(
            'Fighting Style',
            'Você adota um estilo particular de luta como sua especialidade. Escolha uma das seguintes opções: Archery, Defense, Dueling, Great Weapon Fighting, Protection, ou Two-Weapon Fighting.',
            1
        ),
        ClassFeature(
            'Second Wind',
            'Você possui uma reserva limitada de vigor que pode usar para se proteger. No seu turno, você pode usar uma ação bônus para recuperar pontos de vida igual a 1d10 + seu nível de guerreiro. Uma vez que você use essa característica, você precisa terminar um descanso curto ou longo para usá-la novamente.',
            1
        )
    ],
    2: [
        ClassFeature(
            'Action Surge',
            'Você pode forçar-se além dos seus limites normais por um momento. No seu turno, você pode realizar uma ação adicional. Uma vez que você use essa característica, você precisa terminar um descanso curto ou longo para usá-la novamente. A partir do 17º nível, você pode usá-la duas vezes antes de descansar, mas apenas uma vez no mesmo turno.',
            2
        )
    ],
    3: [
        ClassFeature(
            'Martial Archetype',
            'Você escolhe um arquétipo que você se esforça para imitar nos seus estilos e técnicas de combate. Escolha Champion, Battle Master, ou Eldritch Knight. O arquétipo que você escolher concede características no 3º nível e novamente no 7º, 10º, 15º e 18º níveis.',
            3
        )
    ],
    4: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1. Como padrão, você não pode elevar um valor de habilidade acima de 20 com essa característica.',
            4
        )
    ],
    5: [
        ClassFeature(
            'Extra Attack',
            'Você pode atacar duas vezes, ao invés de uma, sempre que você realizar a ação de Ataque no seu turno. O número de ataques aumenta para três quando você alcança o 11º nível nesta classe e para quatro quando você alcança o 20º nível nesta classe.',
            5
        )
    ],
    6: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            6
        )
    ],
    7: [
        ClassFeature(
            'Martial Archetype Feature',
            'Você ganha uma característica concedida pelo seu Arquétipo Marcial.',
            7
        )
    ],
    8: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            8
        )
    ],
    9: [
        ClassFeature(
            'Indomitable',
            'Você pode repetir um teste de resistência que falhou. Se você fizer isso, você deve usar o novo resultado, e você não pode usar essa característica novamente até terminar um descanso longo. Você pode usar essa característica duas vezes entre descansos longos a partir do 13º nível e três vezes entre descansos longos a partir do 17º nível.',
            9
        )
    ],
    10: [
        ClassFeature(
            'Martial Archetype Feature',
            'Você ganha uma característica concedida pelo seu Arquétipo Marcial.',
            10
        )
    ],
    11: [
        ClassFeature(
            'Extra Attack (2)',
            'Você pode atacar três vezes sempre que você realizar a ação de Ataque no seu turno.',
            11
        )
    ],
    12: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            12
        )
    ],
    13: [
        ClassFeature(
            'Indomitable (two uses)',
            'Você pode usar Indomitable duas vezes entre descansos longos.',
            13
        )
    ],
    14: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            14
        )
    ],
    15: [
        ClassFeature(
            'Martial Archetype Feature',
            'Você ganha uma característica concedida pelo seu Arquétipo Marcial.',
            15
        )
    ],
    16: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            16
        )
    ],
    17: [
        ClassFeature(
            'Action Surge (two uses)',
            'Você pode usar Action Surge duas vezes antes de descansar, mas apenas uma vez no mesmo turno.',
            17
        ),
        ClassFeature(
            'Indomitable (three uses)',
            'Você pode usar Indomitable três vezes entre descansos longos.',
            17
        )
    ],
    18: [
        ClassFeature(
            'Martial Archetype Feature',
            'Você ganha uma característica concedida pelo seu Arquétipo Marcial.',
            18
        )
    ],
    19: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            19
        )
    ],
    20: [
        ClassFeature(
            'Extra Attack (3)',
            'Você pode atacar quatro vezes sempre que você realizar a ação de Ataque no seu turno.',
            20
        )
    ]
}


# ========== WIZARD FEATURES ==========
WIZARD_FEATURES = {
    1: [
        ClassFeature(
            'Spellcasting',
            'Como um estudante de magia arcana, você possui um livro de magias contendo feitiços que mostram os primeiros vislumbres do seu verdadeiro poder. Você conhece três truques à sua escolha da lista de magias de mago. Você aprende truques de mago adicionais à sua escolha em níveis mais altos.',
            1
        ),
        ClassFeature(
            'Arcane Recovery',
            'Você aprendeu a recuperar um pouco de sua energia mágica estudando seu livro de magias. Uma vez por dia, quando você terminar um descanso curto, você pode escolher espaços de magia gastos para recuperar. Os espaços de magia podem ter um nível combinado igual ou menor que metade do seu nível de mago (arredondado para cima), e nenhum dos espaços pode ser de 6º nível ou superior.',
            1
        )
    ],
    2: [
        ClassFeature(
            'Arcane Tradition',
            'Você escolhe uma tradição arcana, moldando sua prática de magia através de uma das oito escolas: Abjuration, Conjuration, Divination, Enchantment, Evocation, Illusion, Necromancy, ou Transmutation. Sua escolha concede características no 2º nível e novamente no 6º, 10º e 14º níveis.',
            2
        )
    ],
    3: [],
    4: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            4
        )
    ],
    5: [],
    6: [
        ClassFeature(
            'Arcane Tradition Feature',
            'Você ganha uma característica concedida pela sua Tradição Arcana.',
            6
        )
    ],
    7: [],
    8: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            8
        )
    ],
    9: [],
    10: [
        ClassFeature(
            'Arcane Tradition Feature',
            'Você ganha uma característica concedida pela sua Tradição Arcana.',
            10
        )
    ],
    11: [],
    12: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            12
        )
    ],
    13: [],
    14: [
        ClassFeature(
            'Arcane Tradition Feature',
            'Você ganha uma característica concedida pela sua Tradição Arcana.',
            14
        )
    ],
    15: [],
    16: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            16
        )
    ],
    17: [],
    18: [
        ClassFeature(
            'Spell Mastery',
            'Você alcançou tamanha maestria sobre certas magias que pode conjurá-las à vontade. Escolha uma magia de mago de 1º nível e uma magia de mago de 2º nível que estejam no seu livro de magias. Você pode conjurar essas magias no nível mínimo delas sem gastar um espaço de magia quando as tiver preparadas.',
            18
        )
    ],
    19: [
        ClassFeature(
            'Ability Score Improvement',
            'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.',
            19
        )
    ],
    20: [
        ClassFeature(
            'Signature Spells',
            'Você ganha maestria sobre duas poderosas magias e pode conjurá-las com pouco esforço. Escolha duas magias de mago de 3º nível no seu livro de magias como suas magias assinatura. Você sempre tem essas magias preparadas e elas não contam contra o número de magias que você pode preparar. Você pode conjurar cada uma das suas magias assinatura uma vez no 3º nível sem gastar um espaço de magia. Quando o fizer, você não pode fazê-lo novamente até terminar um descanso curto ou longo.',
            20
        )
    ]
}


# ========== SORCERER FEATURES ==========
SORCERER_FEATURES = {
    1: [
        ClassFeature('Spellcasting', 'Você pode conjurar magias de feiticeiro. Carisma é sua habilidade de conjuração.', 1),
        ClassFeature('Sorcerous Origin', 'Escolha uma origem de seus poderes inatos: Draconic Bloodline ou Wild Magic.', 1)
    ],
    2: [ClassFeature('Font of Magic', 'Você ganha 2 pontos de feitiçaria e pode converter spell slots em pontos e vice-versa.', 2)],
    3: [ClassFeature('Metamagic', 'Você ganha a habilidade de modificar suas magias. Escolha 2 opções de Metamagic.', 3)],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [],
    6: [ClassFeature('Sorcerous Origin Feature', 'Você ganha uma característica da sua origem de feiticeiro.', 6)],
    10: [ClassFeature('Metamagic', 'Você aprende uma opção adicional de Metamagic.', 10)],
    14: [ClassFeature('Sorcerous Origin Feature', 'Você ganha uma característica da sua origem de feiticeiro.', 14)],
    17: [ClassFeature('Metamagic', 'Você aprende uma opção adicional de Metamagic.', 17)],
    18: [ClassFeature('Sorcerous Origin Feature', 'Você ganha uma característica da sua origem de feiticeiro.', 18)],
    20: [ClassFeature('Sorcerous Restoration', 'Você recupera 4 pontos de feitiçaria quando termina um descanso curto.', 20)]
}

# ========== BARD FEATURES ==========
BARD_FEATURES = {
    1: [
        ClassFeature('Spellcasting', 'Você pode conjurar magias de bardo. Carisma é sua habilidade de conjuração.', 1),
        ClassFeature('Bardic Inspiration (d6)', 'Você pode inspirar aliados com uma ação bônus. Eles ganham 1d6 para adicionar a um teste.', 1)
    ],
    2: [
        ClassFeature('Jack of All Trades', 'Você adiciona metade do seu bônus de proficiência a testes de habilidade que não usa proficiência.', 2),
        ClassFeature('Song of Rest (d6)', 'Aliados que descansam com você recuperam 1d6 HP adicional.', 2)
    ],
    3: [
        ClassFeature('Bard College', 'Escolha um colégio de bardos: College of Lore ou College of Valor.', 3),
        ClassFeature('Expertise', 'Escolha duas perícias. Seu bônus de proficiência é dobrado para elas.', 3)
    ],
    5: [ClassFeature('Bardic Inspiration (d8)', 'Seu dado de Inspiração Bárdica se torna 1d8.', 5)],
    6: [ClassFeature('Countercharm', 'Você pode usar uma ação para dar vantagem contra efeitos de medo e charme.', 6)],
    10: [
        ClassFeature('Bardic Inspiration (d10)', 'Seu dado de Inspiração Bárdica se torna 1d10.', 10),
        ClassFeature('Magical Secrets', 'Você aprende 2 magias de qualquer classe.', 10)
    ],
    14: [ClassFeature('Magical Secrets', 'Você aprende 2 magias adicionais de qualquer classe.', 14)],
    15: [ClassFeature('Bardic Inspiration (d12)', 'Seu dado de Inspiração Bárdica se torna 1d12.', 15)],
    18: [ClassFeature('Magical Secrets', 'Você aprende 2 magias adicionais de qualquer classe.', 18)],
    20: [ClassFeature('Superior Inspiration', 'Quando rola iniciativa e não tem usos de Inspiração Bárdica, você recupera 1 uso.', 20)]
}

# ========== WARLOCK FEATURES ==========
WARLOCK_FEATURES = {
    1: [
        ClassFeature('Otherworldly Patron', 'Você fez um pacto com um ser de outro mundo: Archfey, Fiend, ou Great Old One.', 1),
        ClassFeature('Pact Magic', 'Você pode conjurar magias de bruxo. Carisma é sua habilidade de conjuração. Seus spell slots são sempre do nível máximo que você pode conjurar.', 1)
    ],
    2: [ClassFeature('Eldritch Invocations', 'Você ganha invocações místicas. Escolha 2 invocações.', 2)],
    3: [ClassFeature('Pact Boon', 'Seu patrono concede uma dádiva. Escolha: Pact of the Chain, Blade, ou Tome.', 3)],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    11: [ClassFeature('Mystic Arcanum (6th level)', 'Seu patrono concede um segredo místico. Escolha uma magia de 6º nível.', 11)],
    13: [ClassFeature('Mystic Arcanum (7th level)', 'Escolha uma magia de 7º nível.', 13)],
    15: [ClassFeature('Mystic Arcanum (8th level)', 'Escolha uma magia de 8º nível.', 15)],
    17: [ClassFeature('Mystic Arcanum (9th level)', 'Escolha uma magia de 9º nível.', 17)],
    20: [ClassFeature('Eldritch Master', 'Você pode recuperar todos os seus spell slots de Pact Magic com 1 minuto de súplica (1x por descanso longo).', 20)]
}

# ========== DRUID FEATURES ==========
DRUID_FEATURES = {
    1: [
        ClassFeature('Spellcasting', 'Você pode conjurar magias de druida. Sabedoria é sua habilidade de conjuração.', 1),
        ClassFeature('Druidic', 'Você conhece Druídico, a linguagem secreta dos druidas.', 1)
    ],
    2: [
        ClassFeature('Wild Shape', 'Você pode usar uma ação para assumir a forma de uma besta que já viu. Você pode fazer isso 2 vezes por descanso curto/longo.', 2),
        ClassFeature('Druid Circle', 'Escolha um círculo druídico: Circle of the Land ou Circle of the Moon.', 2)
    ],
    4: [ClassFeature('Wild Shape Improvement', 'Você pode se transformar em bestas com CR até 1/2 e pode nadar.', 4)],
    8: [ClassFeature('Wild Shape Improvement', 'Você pode se transformar em bestas com CR até 1 e pode voar.', 8)],
    18: [ClassFeature('Timeless Body', 'A magia primordial que você exerce faz você envelhecer mais lentamente. Para cada 10 anos que passam, seu corpo envelhece apenas 1 ano.', 18)],
    20: [ClassFeature('Archdruid', 'Você pode usar Wild Shape um número ilimitado de vezes. Você ignora componentes verbais e somáticos de magias de druida.', 20)]
}

# ========== RANGER FEATURES ==========
RANGER_FEATURES = {
    1: [
        ClassFeature('Favored Enemy', 'Você tem vantagem em testes de Sabedoria (Sobrevivência) para rastrear seus inimigos favoritos e em testes de Inteligência para lembrar informações sobre eles.', 1),
        ClassFeature('Natural Explorer', 'Você é particularmente familiar com um tipo de ambiente natural e é adepto em viajar e sobreviver nessas regiões.', 1)
    ],
    2: [
        ClassFeature('Fighting Style', 'Você adota um estilo de luta: Archery, Defense, Dueling, ou Two-Weapon Fighting.', 2),
        ClassFeature('Spellcasting', 'Você pode conjurar magias de patrulheiro. Sabedoria é sua habilidade de conjuração.', 2)
    ],
    3: [ClassFeature('Ranger Archetype', 'Escolha um arquétipo: Hunter ou Beast Master.', 3)],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5)],
    8: [ClassFeature("Land's Stride", 'Mover-se através de terreno difícil não-mágico não custa movimento extra.', 8)],
    10: [ClassFeature('Hide in Plain Sight', 'Você pode gastar 1 minuto criando camuflagem para si mesmo, ganhando +10 em testes de Furtividade.', 10)],
    14: [ClassFeature('Vanish', 'Você pode usar a ação Esconder como ação bônus. Você não pode ser rastreado por meios não-mágicos.', 14)],
    18: [ClassFeature('Feral Senses', 'Você ganha sentidos preternaturais. Você não tem desvantagem em ataques contra criaturas que não pode ver.', 18)],
    20: [ClassFeature('Foe Slayer', 'Você se torna um caçador implacável. Uma vez por turno, adicione seu modificador de Sabedoria a um ataque ou dano contra um inimigo favorito.', 20)]
}

# ========== PALADIN FEATURES ==========
PALADIN_FEATURES = {
    1: [
        ClassFeature('Divine Sense', 'Você pode detectar o bem e o mal. Como uma ação, você detecta celestiais, mortos-vivos e demônios a até 60 pés.', 1),
        ClassFeature('Lay on Hands', 'Você tem uma reserva de poder curativo que restaura HP igual a 5x seu nível de paladino. Como ação, você pode curar uma criatura.', 1)
    ],
    2: [
        ClassFeature('Fighting Style', 'Você adota um estilo de luta: Defense, Dueling, Great Weapon Fighting, ou Protection.', 2),
        ClassFeature('Spellcasting', 'Você pode conjurar magias de paladino. Carisma é sua habilidade de conjuração.', 2),
        ClassFeature('Divine Smite', 'Quando acertar com arma corpo a corpo, você pode gastar um spell slot para causar 2d8 de dano radiante adicional (+1d8 por nível do slot).', 2)
    ],
    3: [
        ClassFeature('Divine Health', 'Você é imune a doenças.', 3),
        ClassFeature('Sacred Oath', 'Você faz um juramento sagrado. Escolha: Oath of Devotion, Ancients, ou Vengeance.', 3)
    ],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5)],
    6: [ClassFeature('Aura of Protection', 'Você e aliados a até 10 pés ganham bônus em testes de resistência igual ao seu modificador de Carisma.', 6)],
    10: [ClassFeature('Aura of Courage', 'Você e aliados a até 10 pés não podem ser amedrontados.', 10)],
    11: [ClassFeature('Improved Divine Smite', 'Você causa 1d8 de dano radiante adicional sempre que acertar com arma corpo a corpo.', 11)],
    14: [ClassFeature('Cleansing Touch', 'Você pode usar uma ação para encerrar uma magia em si ou em uma criatura que tocar (Carisma vezes por descanso longo).', 14)],
    18: [ClassFeature('Aura Improvements', 'O alcance das suas auras aumenta para 30 pés.', 18)]
}

# Dicionário mestre de todas as features de classe
CLASS_FEATURES: Dict[str, Dict[int, List[ClassFeature]]] = {
    'Fighter': FIGHTER_FEATURES,
    'Wizard': WIZARD_FEATURES,
    'Sorcerer': SORCERER_FEATURES,
    'Bard': BARD_FEATURES,
    'Warlock': WARLOCK_FEATURES,
    'Druid': DRUID_FEATURES,
    'Ranger': RANGER_FEATURES,
    'Paladin': PALADIN_FEATURES,
}


def get_class_features(class_name: str, level: int) -> List[ClassFeature]:
    """
    Retorna as features de uma classe em um nível específico
    
    Args:
        class_name: Nome da classe
        level: Nível da classe
        
    Returns:
        Lista de ClassFeature para aquele nível, ou lista vazia se não houver
    """
    if class_name not in CLASS_FEATURES:
        return []
    
    class_features = CLASS_FEATURES[class_name]
    return class_features.get(level, [])


def get_all_features_up_to_level(class_name: str, level: int) -> List[ClassFeature]:
    """
    Retorna todas as features de uma classe até um nível específico
    
    Args:
        class_name: Nome da classe
        level: Nível máximo da classe
        
    Returns:
        Lista de todas as ClassFeature até aquele nível
    """
    if class_name not in CLASS_FEATURES:
        return []
    
    all_features = []
    class_features = CLASS_FEATURES[class_name]
    
    for lvl in range(1, level + 1):
        all_features.extend(class_features.get(lvl, []))
    
    return all_features
