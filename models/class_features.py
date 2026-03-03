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
        ClassFeature('Fighting Style', 'Você adota um estilo particular de luta como sua especialidade. Escolha: Archery, Defense, Dueling, Great Weapon Fighting, Protection, ou Two-Weapon Fighting.', 1),
        ClassFeature('Second Wind', 'Você pode usar uma ação bônus para recuperar 1d10 + seu nível de guerreiro em HP. Recarrega após descanso curto ou longo.', 1)
    ],
    2: [ClassFeature('Action Surge (um uso)', 'Você pode realizar uma ação adicional no seu turno. Recarrega após descanso curto ou longo.', 2)],
    3: [],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5)],
    6: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [ClassFeature('Indomitable (um uso)', 'Você pode repetir um teste de resistência que falhou. Recarrega após descanso longo.', 9)],
    10: [],
    11: [ClassFeature('Extra Attack (2)', 'Você pode atacar três vezes quando realizar a ação de Ataque.', 11)],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [ClassFeature('Indomitable (dois usos)', 'Você pode usar Indomitable duas vezes entre descansos longos.', 13)],
    14: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 14)],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [
        ClassFeature('Action Surge (dois usos)', 'Você pode usar Action Surge duas vezes antes de descansar, mas apenas uma vez no mesmo turno.', 17),
        ClassFeature('Indomitable (três usos)', 'Você pode usar Indomitable três vezes entre descansos longos.', 17)
    ],
    18: [],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Extra Attack (3)', 'Você pode atacar quatro vezes quando realizar a ação de Ataque.', 20)]
}


# ========== WIZARD FEATURES ==========
WIZARD_FEATURES = {
    1: [ClassFeature('Spellcasting', 'Como um estudante de magia arcana, você possui um livro de magias contendo feitiços que mostram os primeiros vislumbres do seu verdadeiro poder. Você conhece três truques à sua escolha da lista de magias de mago. Você aprende truques de mago adicionais à sua escolha em níveis mais altos.', 1),
        ClassFeature('Arcane Recovery', 'Você aprendeu a recuperar um pouco de sua energia mágica estudando seu livro de magias. Uma vez por dia, quando você terminar um descanso curto, você pode escolher espaços de magia gastos para recuperar. Os espaços de magia podem ter um nível combinado igual ou menor que metade do seu nível de mago (arredondado para cima), e nenhum dos espaços pode ser de 6º nível ou superior.', 1)],
    2: [],
    3: [],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.', 4)],
    5: [],
    6: [ClassFeature('Arcane Tradition Feature', 'Você ganha uma característica concedida pela sua Tradição Arcana.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.', 8)],
    9: [],
    10: [ClassFeature('Arcane Tradition Feature', 'Você ganha uma característica concedida pela sua Tradição Arcana.', 10)],
    11: [],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.', 12)],
    13: [],
    14: [ClassFeature('Arcane Tradition Feature', 'Você ganha uma característica concedida pela sua Tradição Arcana.', 14)],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.', 16)],
    17: [],
    18: [ClassFeature('Spell Mastery', 'Você alcançou tamanha maestria sobre certas magias que pode conjurá-las à vontade. Escolha uma magia de mago de 1º nível e uma magia de mago de 2º nível que estejam no seu livro de magias. Você pode conjurar essas magias no nível mínimo delas sem gastar um espaço de magia quando as tiver preparadas.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade à sua escolha em 2, ou você pode aumentar dois valores de habilidade à sua escolha em 1.', 19)],
    20: [ClassFeature('Signature Spells', 'Você ganha maestria sobre duas poderosas magias e pode conjurá-las com pouco esforço. Escolha duas magias de mago de 3º nível no seu livro de magias como suas magias assinatura. Você sempre tem essas magias preparadas e elas não contam contra o número de magias que você pode preparar. Você pode conjurar cada uma das suas magias assinatura uma vez no 3º nível sem gastar um espaço de magia. Quando o fizer, você não pode fazê-lo novamente até terminar um descanso curto ou longo.', 20)]
}


# ========== CLERIC FEATURES ==========
CLERIC_FEATURES = {
    1: [ClassFeature('Spellcasting', 'Você pode conjurar magias de clérigo. Sabedoria é sua habilidade de conjuração.', 1)],
    2: [ClassFeature('Channel Divinity (1/rest)', 'Você ganha a habilidade de canalizar energia divina. Você pode usar Channel Divinity uma vez entre descansos.', 2)],
    3: [],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Destroy Undead (CR 1/2)', 'Quando um morto-vivo falha no teste de resistência contra seu Channel Divinity, ele é destruído se seu CR for 1/2 ou menor.', 5)],
    6: [ClassFeature('Channel Divinity (2/rest)', 'Você pode usar Channel Divinity duas vezes entre descansos.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8),
        ClassFeature('Destroy Undead (CR 1)', 'Mortos-vivos de CR 1 ou menor são destruídos.', 8)],
    9: [],
    10: [ClassFeature('Divine Intervention', 'Você pode implorar pela ajuda de sua divindade. Role d100; se rolar igual ou menor que seu nível de clérigo, sua divindade intervém.', 10)],
    11: [ClassFeature('Destroy Undead (CR 2)', 'Mortos-vivos de CR 2 ou menor são destruídos.', 11)],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [],
    14: [ClassFeature('Destroy Undead (CR 3)', 'Mortos-vivos de CR 3 ou menor são destruídos.', 14)],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [ClassFeature('Destroy Undead (CR 4)', 'Mortos-vivos de CR 4 ou menor são destruídos.', 17)],
    18: [ClassFeature('Channel Divinity (3/rest)', 'Você pode usar Channel Divinity três vezes entre descansos.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Divine Intervention Improvement', 'Sua Divine Intervention funciona automaticamente, sem necessidade de rolar.', 20)]
}

# ========== SORCERER FEATURES ==========
SORCERER_FEATURES = {
    1: [ClassFeature('Spellcasting', 'Você pode conjurar magias de feiticeiro. Carisma é sua habilidade de conjuração.', 1)],
    2: [ClassFeature('Font of Magic', 'Você ganha 2 pontos de feitiçaria e pode converter spell slots em pontos e vice-versa.', 2)],
    3: [ClassFeature('Metamagic', 'Você ganha a habilidade de modificar suas magias. Escolha 2 opções de Metamagic.', 3)],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [],
    6: [ClassFeature('Sorcerous Origin Feature', 'Você ganha uma característica da sua origem de feiticeiro.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [],
    10: [ClassFeature('Metamagic', 'Você aprende uma opção adicional de Metamagic.', 10)],
    11: [],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [],
    14: [ClassFeature('Sorcerous Origin Feature', 'Você ganha uma característica da sua origem de feiticeiro.', 14)],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [ClassFeature('Metamagic', 'Você aprende uma opção adicional de Metamagic.', 17)],
    18: [ClassFeature('Sorcerous Origin Feature', 'Você ganha uma característica da sua origem de feiticeiro.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Sorcerous Restoration', 'Você recupera 4 pontos de feitiçaria quando termina um descanso curto.', 20)]
}

# ========== BARD FEATURES ==========
BARD_FEATURES = {
    1: [ClassFeature('Spellcasting', 'Você pode conjurar magias de bardo. Carisma é sua habilidade de conjuração.', 1),
        ClassFeature('Bardic Inspiration (d6)', 'Você pode inspirar aliados com uma ação bônus. Eles ganham 1d6 para adicionar a um teste.', 1)],
    2: [ClassFeature('Jack of All Trades', 'Você adiciona metade do seu bônus de proficiência a testes de habilidade que não usa proficiência.', 2),
        ClassFeature('Song of Rest (d6)', 'Aliados que descansam com você recuperam 1d6 HP adicional.', 2)],
    3: [ClassFeature('Expertise', 'Escolha duas perícias. Seu bônus de proficiência é dobrado para elas.', 3)],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Bardic Inspiration (d8)', 'Seu dado de Inspiração Bárdica se torna 1d8.', 5),
        ClassFeature('Font of Inspiration', 'Você recupera usos de Inspiração Bárdica após descanso curto ou longo.', 5)],
    6: [ClassFeature('Countercharm', 'Você pode usar uma ação para dar vantagem contra efeitos de medo e charme.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [ClassFeature('Song of Rest (d8)', 'Aliados que descansam com você recuperam 1d8 HP adicional.', 9)],
    10: [ClassFeature('Bardic Inspiration (d10)', 'Seu dado de Inspiração Bárdica se torna 1d10.', 10),
        ClassFeature('Magical Secrets', 'Você aprende 2 magias de qualquer classe.', 10),
        ClassFeature('Expertise', 'Escolha mais duas perícias. Seu bônus de proficiência é dobrado para elas.', 10)],
    11: [],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [ClassFeature('Song of Rest (d10)', 'Aliados que descansam com você recuperam 1d10 HP adicional.', 13)],
    14: [ClassFeature('Magical Secrets', 'Você aprende 2 magias adicionais de qualquer classe.', 14)],
    15: [ClassFeature('Bardic Inspiration (d12)', 'Seu dado de Inspiração Bárdica se torna 1d12.', 15)],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [ClassFeature('Song of Rest (d12)', 'Aliados que descansam com você recuperam 1d12 HP adicional.', 17)],
    18: [ClassFeature('Magical Secrets', 'Você aprende 2 magias adicionais de qualquer classe.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Superior Inspiration', 'Quando rola iniciativa e não tem usos de Inspiração Bárdica, você recupera 1 uso.', 20)]
}

# ========== WARLOCK FEATURES ==========
WARLOCK_FEATURES = {
    1: [ClassFeature('Pact Magic', 'Você pode conjurar magias de bruxo. Carisma é sua habilidade de conjuração. Seus spell slots são sempre do nível máximo que você pode conjurar.', 1)],
    2: [ClassFeature('Eldritch Invocations', 'Você ganha invocações místicas. Escolha 2 invocações.', 2)],
    3: [ClassFeature('Pact Boon', 'Seu patrono concede uma dádiva. Escolha: Pact of the Chain, Blade, ou Tome.', 3)],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Eldritch Invocations', 'Você aprende uma invocação adicional.', 5)],
    6: [ClassFeature('Otherworldly Patron Feature', 'Você ganha uma característica do seu patrono.', 6)],
    7: [ClassFeature('Eldritch Invocations', 'Você aprende uma invocação adicional.', 7)],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [ClassFeature('Eldritch Invocations', 'Você aprende uma invocação adicional.', 9)],
    10: [ClassFeature('Otherworldly Patron Feature', 'Você ganha uma característica do seu patrono.', 10)],
    11: [ClassFeature('Mystic Arcanum (6th level)', 'Seu patrono concede um segredo místico. Escolha uma magia de 6º nível.', 11)],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12),
        ClassFeature('Eldritch Invocations', 'Você aprende uma invocação adicional.', 12)],
    13: [ClassFeature('Mystic Arcanum (7th level)', 'Escolha uma magia de 7º nível.', 13)],
    14: [ClassFeature('Otherworldly Patron Feature', 'Você ganha uma característica do seu patrono.', 14)],
    15: [ClassFeature('Mystic Arcanum (8th level)', 'Escolha uma magia de 8º nível.', 15),
        ClassFeature('Eldritch Invocations', 'Você aprende uma invocação adicional.', 15)],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [ClassFeature('Mystic Arcanum (9th level)', 'Escolha uma magia de 9º nível.', 17)],
    18: [ClassFeature('Eldritch Invocations', 'Você aprende uma invocação adicional.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Eldritch Master', 'Você pode recuperar todos os seus spell slots de Pact Magic com 1 minuto de súplica (1x por descanso longo).', 20)]
}

# ========== DRUID FEATURES ==========
DRUID_FEATURES = {
    1: [ClassFeature('Spellcasting', 'Você pode conjurar magias de druida. Sabedoria é sua habilidade de conjuração.', 1),
        ClassFeature('Druidic', 'Você conhece Druídico, a linguagem secreta dos druidas.', 1)],
    2: [ClassFeature('Wild Shape', 'Você pode usar uma ação para assumir a forma de uma besta que já viu. Você pode fazer isso 2 vezes por descanso curto/longo.', 2),
        ClassFeature('Druid Circle', 'Escolha um círculo druídico: Circle of the Land ou Circle of the Moon.', 2)],
    3: [],
    4: [ClassFeature('Wild Shape Improvement', 'Você pode se transformar em bestas com CR até 1/2 e pode nadar.', 4),
        ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [],
    6: [],
    7: [],
    8: [ClassFeature('Wild Shape Improvement', 'Você pode se transformar em bestas com CR até 1 e pode voar.', 8),
        ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [],
    10: [],
    11: [],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [],
    14: [],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [],
    18: [ClassFeature('Timeless Body', 'A magia primordial que você exerce faz você envelhecer mais lentamente. Para cada 10 anos que passam, seu corpo envelhece apenas 1 ano.', 18),
        ClassFeature('Beast Spells', 'Você pode conjurar muitas de suas magias de druida em qualquer forma que assumir usando Wild Shape.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Archdruid', 'Você pode usar Wild Shape um número ilimitado de vezes. Você ignora componentes verbais e somáticos de magias de druida.', 20)]
}

# ========== RANGER FEATURES ==========
RANGER_FEATURES = {
    1: [ClassFeature('Favored Enemy', 'Você tem vantagem em testes de Sabedoria (Sobrevivência) para rastrear seus inimigos favoritos e em testes de Inteligência para lembrar informações sobre eles.', 1),
        ClassFeature('Natural Explorer', 'Você é particularmente familiar com um tipo de ambiente natural e é adepto em viajar e sobreviver nessas regiões.', 1)],
    2: [ClassFeature('Fighting Style', 'Você adota um estilo de luta: Archery, Defense, Dueling, ou Two-Weapon Fighting.', 2),
        ClassFeature('Spellcasting', 'Você pode conjurar magias de patrulheiro. Sabedoria é sua habilidade de conjuração.', 2)],
    3: [],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5)],
    6: [ClassFeature('Favored Enemy and Natural Explorer Improvements', 'Você escolhe um inimigo favorito adicional e um terreno favorito adicional.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8),
        ClassFeature("Land's Stride", 'Mover-se através de terreno difícil não-mágico não custa movimento extra.', 8)],
    9: [],
    10: [ClassFeature('Natural Explorer Improvement', 'Você escolhe um terreno favorito adicional.', 10),
        ClassFeature('Hide in Plain Sight', 'Você pode gastar 1 minuto criando camuflagem para si mesmo, ganhando +10 em testes de Furtividade.', 10)],
    11: [],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [],
    14: [ClassFeature('Favored Enemy Improvement', 'Você escolhe um inimigo favorito adicional.', 14),
        ClassFeature('Vanish', 'Você pode usar a ação Esconder como ação bônus. Você não pode ser rastreado por meios não-mágicos.', 14)],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [],
    18: [ClassFeature('Feral Senses', 'Você ganha sentidos preternaturais. Você não tem desvantagem em ataques contra criaturas que não pode ver.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Foe Slayer', 'Você se torna um caçador implacável. Uma vez por turno, adicione seu modificador de Sabedoria a um ataque ou dano.', 20)]
}

# ========== PALADIN FEATURES ==========
PALADIN_FEATURES = {
    1: [ClassFeature('Divine Sense', 'Você pode detectar o bem e o mal. Como uma ação, você detecta celestiais, mortos-vivos e demônios a até 60 pés.', 1),
        ClassFeature('Lay on Hands', 'Você tem uma reserva de poder curativo que restaura HP igual a 5x seu nível de paladino. Como ação, você pode curar uma criatura.', 1)],
    2: [ClassFeature('Fighting Style', 'Você adota um estilo de luta: Defense, Dueling, Great Weapon Fighting, ou Protection.', 2),
        ClassFeature('Spellcasting', 'Você pode conjurar magias de paladino. Carisma é sua habilidade de conjuração.', 2),
        ClassFeature('Divine Smite', 'Quando acertar com arma corpo a corpo, você pode gastar um spell slot para causar 2d8 de dano radiante adicional (+1d8 por nível do slot).', 2)],
    3: [ClassFeature('Divine Health', 'Você é imune a doenças.', 3),],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5)],
    6: [ClassFeature('Aura of Protection', 'Você e aliados a até 10 pés ganham bônus em testes de resistência igual ao seu modificador de Carisma.', 6)],
    7: [],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [],
    10: [ClassFeature('Aura of Courage', 'Você e aliados a até 10 pés não podem ser amedrontados.', 10)],
    11: [ClassFeature('Improved Divine Smite', 'Você causa 1d8 de dano radiante adicional sempre que acertar com arma corpo a corpo.', 11)],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [],
    14: [ClassFeature('Cleansing Touch', 'Você pode usar uma ação para encerrar uma magia em si ou em uma criatura que tocar (Carisma vezes por descanso longo).', 14)],
    15: [],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [],
    18: [ClassFeature('Aura Improvements', 'O alcance das suas auras aumenta para 30 pés.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: []
}

# ========== BARBARIAN FEATURES ==========
BARBARIAN_FEATURES = {
    1: [ClassFeature('Rage', 'Você pode entrar em fúria como ação bônus. Enquanto furioso, você ganha vantagem em testes de Força, +2 de dano corpo a corpo com Força, e resistência a dano físico. Dura 1 minuto. 2 usos por descanso longo.', 1),
        ClassFeature('Unarmored Defense', 'Quando não estiver usando armadura, sua CA é 10 + modificador de Destreza + modificador de Constituição.', 1)],
    2: [ClassFeature('Reckless Attack', 'Quando fizer seu primeiro ataque no turno, você pode atacar imprudentemente, ganhando vantagem em ataques corpo a corpo com Força, mas dando vantagem aos inimigos contra você.', 2),
        ClassFeature('Danger Sense', 'Você tem vantagem em testes de resistência de Destreza contra efeitos que pode ver.', 2)],
    3: [],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5),
        ClassFeature('Fast Movement', 'Sua velocidade aumenta em 10 pés quando não estiver usando armadura pesada.', 5)],
    6: [],
    7: [ClassFeature('Feral Instinct', 'Você tem vantagem em rolagens de iniciativa. Se estiver surpreso, pode agir normalmente no primeiro turno se entrar em fúria.', 7)],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [ClassFeature('Brutal Critical (1 die)', 'Você pode rolar um dado de dano adicional ao determinar o dano extra de um acerto crítico com ataque corpo a corpo.', 9)],
    10: [],
    11: [ClassFeature('Relentless Rage', 'Sua fúria pode mantê-lo lutando. Se cair a 0 HP enquanto furioso, você pode fazer um teste de Constituição CD 10 para ficar com 1 HP. A CD aumenta em 5 a cada uso.', 11)],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [ClassFeature('Brutal Critical (2 dice)', 'Você pode rolar dois dados de dano adicionais ao determinar o dano extra de um acerto crítico.', 13)],
    14: [],
    15: [ClassFeature('Persistent Rage', 'Sua fúria só termina prematuramente se você cair inconsciente ou escolher terminá-la.', 15)],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [ClassFeature('Brutal Critical (3 dice)', 'Você pode rolar três dados de dano adicionais ao determinar o dano extra de um acerto crítico.', 17)],
    18: [ClassFeature('Indomitable Might', 'Se seu total de um teste de Força for menor que seu valor de Força, você pode usar seu valor de Força no lugar do total.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Primal Champion', 'Seus valores de Força e Constituição aumentam em 4. Seu máximo para esses valores agora é 24.', 20)]
}

# ========== ROGUE FEATURES ==========
ROGUE_FEATURES = {
    1: [ClassFeature('Expertise', 'Escolha duas perícias ou ferramentas. Seu bônus de proficiência é dobrado para elas.', 1),
        ClassFeature('Sneak Attack', 'Uma vez por turno, você causa 1d6 de dano extra ao acertar com ataque com vantagem ou se outro inimigo do alvo estiver a 5 pés dele.', 1),
        ClassFeature("Thieves' Cant", 'Você conhece a gíria secreta dos ladrões, permitindo comunicação escondida.', 1)],
    2: [ClassFeature('Cunning Action', 'Você pode usar ação bônus para Dash, Disengage ou Hide.', 2)],
    3: [],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4)],
    5: [ClassFeature('Uncanny Dodge', 'Quando um atacante que você pode ver acerta você, você pode usar sua reação para reduzir o dano pela metade.', 5)],
    6: [ClassFeature('Expertise', 'Escolha mais duas perícias ou ferramentas. Seu bônus de proficiência é dobrado para elas.', 6)],
    7: [ClassFeature('Evasion', 'Quando fizer um teste de resistência de Destreza para reduzir dano pela metade, você não sofre dano se passar, e apenas metade se falhar.', 7)],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [],
    10: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 10)],
    11: [ClassFeature('Reliable Talent', 'Sempre que fizer um teste de habilidade com proficiência, você trata rolagens de 9 ou menos como 10.', 11)],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [],
    14: [ClassFeature('Blindsense', 'Se você puder ouvir, você está ciente da localização de qualquer criatura escondida ou invisível a até 10 pés de você.', 14)],
    15: [ClassFeature('Slippery Mind', 'Você ganha proficiência em testes de resistência de Sabedoria.', 15)],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [],
    18: [ClassFeature('Elusive', 'Nenhum ataque tem vantagem contra você enquanto você não estiver incapacitado.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Stroke of Luck', 'Se errar um ataque, você pode transformá-lo em acerto. Ou se falhar em um teste de habilidade, pode tratá-lo como 20. 1 uso por descanso curto ou longo.', 20)]
}

# ========== MONK FEATURES ==========
MONK_FEATURES = {
    1: [ClassFeature('Unarmored Defense', 'Quando não estiver usando armadura ou escudo, sua CA é 10 + modificador de Destreza + modificador de Sabedoria.', 1),
        ClassFeature('Martial Arts', 'Você pode usar Destreza ao invés de Força para ataques desarmados e armas de monge. Dado de dano: 1d4. Você pode fazer um ataque desarmado como ação bônus após atacar.', 1)],
    2: [ClassFeature('Ki', 'Você ganha 2 pontos de ki. Você pode gastar ki para: Flurry of Blows (1 ki, 2 ataques desarmados como bônus), Patient Defense (1 ki, Dodge como bônus), Step of the Wind (1 ki, Disengage/Dash como bônus, dobra salto).', 2),
        ClassFeature('Unarmored Movement', 'Sua velocidade aumenta em 10 pés quando não estiver usando armadura ou escudo.', 2)],
    3: [ClassFeature('Deflect Missiles', 'Você pode usar sua reação para reduzir dano de projéteis em 1d10 + Destreza + nível de monge. Se reduzir a 0, você pode gastar 1 ki para arremessar de volta.', 3)],
    4: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 4),
        ClassFeature('Slow Fall', 'Você pode usar sua reação para reduzir dano de queda em 5x seu nível de monge.', 4)],
    5: [ClassFeature('Extra Attack', 'Você pode atacar duas vezes quando realizar a ação de Ataque.', 5),
        ClassFeature('Stunning Strike', 'Você pode gastar 1 ki quando acertar com ataque corpo a corpo para forçar o alvo a fazer teste de Constituição ou ficar atordoado até o fim do seu próximo turno.', 5)],
    6: [ClassFeature('Ki-Empowered Strikes', 'Seus ataques desarmados contam como mágicos para superar resistência e imunidade.', 6)],
    7: [ClassFeature('Evasion', 'Quando fizer um teste de resistência de Destreza para reduzir dano pela metade, você não sofre dano se passar, e apenas metade se falhar.', 7),
        ClassFeature('Stillness of Mind', 'Você pode usar sua ação para encerrar um efeito de charme ou medo em si mesmo.', 7)],
    8: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 8)],
    9: [ClassFeature('Unarmored Movement Improvement', 'Você pode se mover em superfícies verticais e sobre líquidos sem cair durante seu movimento.', 9)],
    10: [ClassFeature('Purity of Body', 'Você é imune a doenças e venenos.', 10)],
    11: [],
    12: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 12)],
    13: [ClassFeature('Tongue of the Sun and Moon', 'Você pode entender todos os idiomas falados e qualquer criatura que entenda um idioma pode entender o que você fala.', 13)],
    14: [ClassFeature('Diamond Soul', 'Você ganha proficiência em todos os testes de resistência. Você pode gastar 1 ki para repetir um teste de resistência falhado.', 14)],
    15: [ClassFeature('Timeless Body', 'Você não sofre desvantagens do envelhecimento e não pode ser envelhecido magicamente. Você não precisa mais de comida ou água.', 15)],
    16: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 16)],
    17: [],
    18: [ClassFeature('Empty Body', 'Você pode gastar 4 ki para ficar invisível por 1 minuto e ter resistência a todo dano exceto dano de força. Você pode gastar 8 ki para conjurar Astral Projection.', 18)],
    19: [ClassFeature('Ability Score Improvement', 'Você pode aumentar um valor de habilidade em 2, ou dois valores em 1.', 19)],
    20: [ClassFeature('Perfect Self', 'Quando rolar iniciativa e não tiver pontos de ki, você recupera 4 pontos de ki.', 20)]
}

# Dicionário mestre de todas as features de classe
CLASS_FEATURES: Dict[str, Dict[int, List[ClassFeature]]] = {
    'Fighter': FIGHTER_FEATURES,
    'Wizard': WIZARD_FEATURES,
    'Cleric': CLERIC_FEATURES,
    'Sorcerer': SORCERER_FEATURES,
    'Bard': BARD_FEATURES,
    'Warlock': WARLOCK_FEATURES,
    'Druid': DRUID_FEATURES,
    'Ranger': RANGER_FEATURES,
    'Paladin': PALADIN_FEATURES,
    'Barbarian': BARBARIAN_FEATURES,
    'Rogue': ROGUE_FEATURES,
    'Monk': MONK_FEATURES,
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
