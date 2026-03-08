"""
Magias adicionais de Warlock (Níveis 3-9) do PHB
Este arquivo complementa o spell.py com magias de níveis superiores
"""

WARLOCK_SPELLS_3_TO_9 = {
    # ========== NÍVEL 3 ==========
    'Counterspell': {
        'name': 'Counterspell',
        'level': 3,
        'school': 'Abjuration',
        'casting_time': '1 reação',
        'range': '60 pés',
        'components': 'S',
        'duration': 'Instantânea',
        'description': 'Você tenta interromper uma criatura no processo de conjurar uma magia. Se a criatura estiver conjurando uma magia de 3º nível ou inferior, sua magia falha e não tem efeito. Se estiver conjurando uma magia de 4º nível ou superior, faça um teste de habilidade usando sua habilidade de conjuração. A CD é igual a 10 + o nível da magia. Em um sucesso, a magia da criatura falha e não tem efeito.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 4º nível ou superior, a magia interrompida não tem efeito se seu nível for menor ou igual ao nível do espaço de magia que você usou.',
        'classes': ['Wizard', 'Sorcerer', 'Warlock'],
        'ritual': False,
        'concentration': False
    },
    'Dispel Magic': {
        'name': 'Dispel Magic',
        'level': 3,
        'school': 'Abjuration',
        'casting_time': '1 ação',
        'range': '120 pés',
        'components': 'V, S',
        'duration': 'Instantânea',
        'description': 'Escolha uma criatura, objeto ou efeito mágico dentro do alcance. Qualquer magia de 3º nível ou inferior no alvo termina. Para cada magia de 4º nível ou superior no alvo, faça um teste de habilidade usando sua habilidade de conjuração. A CD é igual a 10 + o nível da magia. Em um sucesso, a magia termina.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 4º nível ou superior, você automaticamente termina os efeitos de uma magia no alvo se o nível da magia for igual ou menor que o nível do espaço de magia que você usou.',
        'classes': ['Wizard', 'Sorcerer', 'Cleric', 'Druid', 'Paladin', 'Bard', 'Warlock'],
        'ritual': False,
        'concentration': False
    },
    'Fear': {
        'name': 'Fear',
        'level': 3,
        'school': 'Illusion',
        'casting_time': '1 ação',
        'range': 'Pessoal (cone de 30 pés)',
        'components': 'V, S, M (uma pena branca ou coração de galinha)',
        'duration': 'Concentração, até 1 minuto',
        'description': 'Você projeta uma imagem fantasmagórica dos piores medos de uma criatura. Cada criatura em um cone de 30 pés deve ter sucesso em um teste de resistência de Sabedoria ou largar o que estiver segurando e ficar amedrontada pela duração.\n\nEnquanto amedrontada por esta magia, uma criatura deve fazer a ação Disparada e se afastar de você pelo caminho mais seguro disponível em cada um de seus turnos, a menos que não haja lugar para se mover. Se a criatura terminar seu turno em um local onde não tem linha de visão para você, a criatura pode fazer um teste de resistência de Sabedoria. Em um sucesso, a magia acaba para essa criatura.',
        'classes': ['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
        'ritual': False,
        'concentration': True
    },
    'Fly': {
        'name': 'Fly',
        'level': 3,
        'school': 'Transmutation',
        'casting_time': '1 ação',
        'range': 'Toque',
        'components': 'V, S, M (uma pena de asa de qualquer pássaro)',
        'duration': 'Concentração, até 10 minutos',
        'description': 'Você toca uma criatura voluntária. O alvo ganha uma velocidade de voo de 60 pés pela duração. Quando a magia acabar, o alvo cai se ainda estiver no ar, a menos que possa parar a queda.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 4º nível ou superior, você pode mirar em uma criatura adicional para cada nível do espaço acima do 3º.',
        'classes': ['Wizard', 'Sorcerer', 'Warlock'],
        'ritual': False,
        'concentration': True
    },
    'Gaseous Form': {
        'name': 'Gaseous Form',
        'level': 3,
        'school': 'Transmutation',
        'casting_time': '1 ação',
        'range': 'Toque',
        'components': 'V, S, M (um pouco de gaze e uma mecha de fumaça)',
        'duration': 'Concentração, até 1 hora',
        'description': 'Você transforma uma criatura voluntária que você tocar, junto com tudo o que ela estiver vestindo e carregando, em uma nuvem enevoada pela duração. A magia acaba se a criatura cair a 0 pontos de vida. Uma criatura incorpórea não é afetada.\n\nEnquanto nesta forma, o único método de movimento do alvo é uma velocidade de voo de 10 pés. O alvo pode entrar e ocupar o espaço de outra criatura. O alvo tem resistência a dano não-mágico, e tem vantagem em testes de resistência de Força, Destreza e Constituição. O alvo pode passar por pequenos buracos, aberturas estreitas e até meras rachaduras, embora trate líquidos como superfícies sólidas. O alvo não pode cair e permanece pairando no ar mesmo quando atordoado ou incapacitado.\n\nEnquanto na forma de uma nuvem enevoada, o alvo não pode falar ou manipular objetos, e qualquer objeto que estava carregando ou segurando não pode ser largado, usado ou de outra forma interagido. O alvo não pode atacar ou conjurar magias.',
        'classes': ['Wizard', 'Sorcerer', 'Warlock'],
        'ritual': False,
        'concentration': True
    },
    'Hunger of Hadar': {
        'name': 'Hunger of Hadar',
        'level': 3,
        'school': 'Conjuration',
        'casting_time': '1 ação',
        'range': '150 pés',
        'components': 'V, S, M (um tentáculo em conserva de um polvo gigante ou lula gigante)',
        'duration': 'Concentração, até 1 minuto',
        'description': 'Você abre um portal para o vazio escuro entre as estrelas, uma região infestada de horrores desconhecidos. Uma esfera de escuridão de 20 pés de raio aparece, centrada em um ponto dentro do alcance e durando pela duração. Este vazio é preenchido com um cacofonia de sussurros suaves e sons de mastigação que podem ser ouvidos até 30 pés de distância. Nenhuma luz, mágica ou não, pode iluminar a área, e criaturas totalmente dentro da área são cegas.\n\nO vazio cria uma distorção no tecido do espaço, e a área é terreno difícil. Qualquer criatura que comece seu turno na área sofre 2d6 de dano de frio. Qualquer criatura que termine seu turno na área deve ter sucesso em um teste de resistência de Destreza ou sofre 2d6 de dano ácido enquanto tentáculos leitosos a esfregam com força.',
        'classes': ['Warlock'],
        'ritual': False,
        'concentration': True
    },
    'Hypnotic Pattern': {
        'name': 'Hypnotic Pattern',
        'level': 3,
        'school': 'Illusion',
        'casting_time': '1 ação',
        'range': '120 pés',
        'components': 'S, M (um bastão de incenso brilhante ou um frasco de cristal cheio de material fosforescente)',
        'duration': 'Concentração, até 1 minuto',
        'description': 'Você cria um padrão torcido de cores que tece através do ar dentro de um cubo de 30 pés dentro do alcance. O padrão aparece por um momento e desaparece. Cada criatura na área que vê o padrão deve fazer um teste de resistência de Sabedoria. Em uma falha, a criatura fica encantada pela duração. Enquanto encantada por esta magia, a criatura está incapacitada e tem velocidade de 0.\n\nA magia acaba para uma criatura afetada se ela sofrer qualquer dano ou se alguém mais usar uma ação para sacudir a criatura para fora de seu estupor.',
        'classes': ['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
        'ritual': False,
        'concentration': True
    },
    'Magic Circle': {
        'name': 'Magic Circle',
        'level': 3,
        'school': 'Abjuration',
        'casting_time': '1 minuto',
        'range': '10 pés',
        'components': 'V, S, M (água benta ou pó de prata e ferro no valor de pelo menos 100 po, que a magia consome)',
        'duration': '1 hora',
        'description': 'Você cria um cilindro de energia mágica de 10 pés de raio e 20 pés de altura centrado em um ponto no chão que você possa ver dentro do alcance. Runas brilhantes aparecem onde quer que o cilindro intercepte o chão ou outra superfície.\n\nEscolha um ou mais dos seguintes tipos de criaturas: celestiais, elementais, fadas, demoníacos ou mortos-vivos. O círculo afeta uma criatura do tipo escolhido das seguintes maneiras:\n\n• A criatura não pode entrar voluntariamente no cilindro por meios não-mágicos. Se a criatura tentar usar teletransporte ou viagem interplanar para fazê-lo, ela deve primeiro ter sucesso em um teste de resistência de Carisma.\n• A criatura tem desvantagem em jogadas de ataque contra alvos dentro do cilindro.\n• Alvos dentro do cilindro não podem ser encantados, amedrontados ou possuídos pela criatura.\n\nQuando você conjura essa magia, você pode optar por fazer sua magia operar na direção reversa, impedindo uma criatura do tipo especificado de deixar o cilindro e protegendo alvos fora dele.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 4º nível ou superior, a duração aumenta em 1 hora para cada nível do espaço acima do 3º.',
        'classes': ['Wizard', 'Cleric', 'Paladin', 'Warlock'],
        'ritual': False,
        'concentration': False
    },
    'Major Image': {
        'name': 'Major Image',
        'level': 3,
        'school': 'Illusion',
        'casting_time': '1 ação',
        'range': '120 pés',
        'components': 'V, S, M (um pouco de lã de carneiro)',
        'duration': 'Concentração, até 10 minutos',
        'description': 'Você cria a imagem de um objeto, uma criatura ou algum outro fenômeno visível que não seja maior que um cubo de 20 pés. A imagem aparece em um local que você possa ver dentro do alcance e dura pela duração. Parece completamente real, incluindo sons, cheiros e temperatura apropriados à coisa retratada. Você não pode criar calor ou frio suficiente para causar dano, um som alto o suficiente para causar dano trovejante ou ensurdecer uma criatura, ou um cheiro que possa adoecer uma criatura (como um fedor de troglodita).\n\nEnquanto você estiver dentro do alcance da ilusão, você pode usar sua ação para fazer a imagem se mover para qualquer outro local dentro do alcance. Como a imagem muda de local, você pode alterar sua aparência para que seus movimentos pareçam naturais para a imagem. Por exemplo, se você criar uma imagem de uma criatura e movê-la, você pode alterar a imagem para que pareça estar andando. Da mesma forma, você pode fazer a ilusão fazer sons diferentes em momentos diferentes, até mesmo fazê-la participar de uma conversa, por exemplo.\n\nInteração física com a imagem revela que é uma ilusão, porque as coisas podem passar através dela. Uma criatura que usar sua ação para examinar a imagem pode determinar que é uma ilusão com um teste bem-sucedido de Inteligência (Investigação) contra sua CD de magia. Se uma criatura discernir a ilusão pelo que ela é, a criatura pode ver através da imagem, e seus outros aspectos sensoriais se tornam fracos para a criatura.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 6º nível ou superior, a magia dura até ser dissipada, sem exigir sua concentração.',
        'classes': ['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
        'ritual': False,
        'concentration': True
    },
    'Remove Curse': {
        'name': 'Remove Curse',
        'level': 3,
        'school': 'Abjuration',
        'casting_time': '1 ação',
        'range': 'Toque',
        'components': 'V, S',
        'duration': 'Instantânea',
        'description': 'Ao seu toque, todas as maldições afetando uma criatura ou objeto terminam. Se o objeto for um item mágico amaldiçoado, sua maldição permanece, mas a magia quebra a sintonia do dono com o objeto para que possa ser removido ou descartado.',
        'classes': ['Wizard', 'Cleric', 'Paladin', 'Warlock'],
        'ritual': False,
        'concentration': False
    },
    'Tongues': {
        'name': 'Tongues',
        'level': 3,
        'school': 'Divination',
        'casting_time': '1 ação',
        'range': 'Toque',
        'components': 'V, M (um pequeno modelo de argila de um zigurate)',
        'duration': '1 hora',
        'description': 'Esta magia concede à criatura que você tocar a habilidade de compreender qualquer idioma falado que ouvir. Além disso, quando o alvo fala, qualquer criatura que conheça pelo menos um idioma e possa ouvir o alvo entende o que ele diz.',
        'classes': ['Wizard', 'Sorcerer', 'Bard', 'Cleric', 'Warlock'],
        'ritual': False,
        'concentration': False
    },
    'Vampiric Touch': {
        'name': 'Vampiric Touch',
        'level': 3,
        'school': 'Necromancy',
        'casting_time': '1 ação',
        'range': 'Pessoal',
        'components': 'V, S',
        'duration': 'Concentração, até 1 minuto',
        'description': 'O toque de sua mão envolta em sombras pode sugar a força vital de outros para curar seus próprios ferimentos. Faça um ataque de magia corpo a corpo contra uma criatura dentro do seu alcance. Em um acerto, o alvo sofre 3d6 de dano necrótico, e você recupera pontos de vida iguais a metade da quantidade de dano necrótico causado. Até a magia acabar, você pode fazer o ataque novamente em cada um de seus turnos como uma ação.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 4º nível ou superior, o dano aumenta em 1d6 para cada nível do espaço acima do 3º.',
        'classes': ['Wizard', 'Warlock'],
        'ritual': False,
        'concentration': True
    },
}
