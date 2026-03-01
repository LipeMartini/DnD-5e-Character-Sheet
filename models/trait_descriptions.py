"""
Descrições detalhadas de traços raciais, de classe e de background para tooltips
"""

TRAIT_DESCRIPTIONS = {
    # Traços Raciais - Humano
    'Versatile': 'Humanos são adaptáveis e versáteis, ganhando +1 em todos os atributos.',
    
    # Traços Raciais - Elfo
    'Darkvision': 'Você pode enxergar na penumbra a até 18 metros como se fosse luz plena, e no escuro como se fosse penumbra. Você não pode discernir cores no escuro, apenas tons de cinza.',
    'Keen Senses': 'Você tem proficiência na perícia Percepção.',
    'Fey Ancestry': 'Você tem vantagem em testes de resistência contra ser enfeitiçado e magias não podem colocá-lo para dormir.',
    'Trance': 'Elfos não precisam dormir. Em vez disso, meditam profundamente por 4 horas por dia, permanecendo semiconscientes.',
    
    # Traços Raciais - Elfo (Subraças)
    'Cantrip': 'Você conhece um truque à sua escolha da lista de magias de mago. Inteligência é seu atributo para conjuração.',
    'Elf Weapon Training': 'Você tem proficiência com espadas longas, espadas curtas, arcos longos e arcos curtos.',
    'Extra Language': 'Você pode falar, ler e escrever um idioma adicional à sua escolha.',
    'Superior Darkvision': 'Sua visão no escuro tem alcance de 36 metros.',
    'Sunlight Sensitivity': 'Você tem desvantagem em testes de ataque e Percepção (Sabedoria) que dependam da visão quando você, o alvo do seu ataque, ou o que quer que você esteja tentando perceber esteja sob luz solar direta.',
    'Drow Magic': 'Você conhece o truque Luzes Dançantes. Quando alcança o 3º nível, pode conjurar Fogo das Fadas uma vez. Quando alcança o 5º nível, pode conjurar Escuridão uma vez. Carisma é seu atributo para conjuração.',
    'Drow Weapon Training': 'Você tem proficiência com rapieiras, espadas curtas e bestas de mão.',
    'Fleet of Foot': 'Seu deslocamento base de caminhada aumenta para 10,5 metros (35 pés).',
    'Mask of the Wild': 'Você pode tentar se esconder mesmo quando está apenas levemente obscurecido por folhagem, chuva forte, neve caindo, névoa e outros fenômenos naturais.',
    
    # Traços Raciais - Anão
    'Dwarven Resilience': 'Você tem vantagem em testes de resistência contra veneno e resistência a dano de veneno.',
    'Dwarven Combat Training': 'Você tem proficiência com machados de batalha, machadinhas, martelos leves e martelos de guerra.',
    'Stonecunning': 'Sempre que fizer um teste de Inteligência (História) relacionado à origem de um trabalho em pedra, você é considerado proficiente e adiciona o dobro do seu bônus de proficiência ao teste.',
    'Dwarven Toughness': 'Seu máximo de pontos de vida aumenta em 1, e aumenta em 1 novamente sempre que você ganha um nível.',
    'Dwarven Armor Training': 'Você tem proficiência com armaduras leves e médias.',
    
    # Traços Raciais - Halfling
    'Lucky': 'Quando você obtiver um 1 natural em um teste de ataque, teste de atributo ou teste de resistência, você pode rolar o dado novamente e deve usar o novo resultado.',
    'Brave': 'Você tem vantagem em testes de resistência contra ser amedrontado.',
    'Halfling Nimbleness': 'Você pode se mover através do espaço de qualquer criatura que seja de um tamanho maior que o seu.',
    'Naturally Stealthy': 'Você pode tentar se esconder mesmo quando estiver obscurecido apenas por uma criatura que seja pelo menos um tamanho maior que você.',
    'Stout Resilience': 'Você tem vantagem em testes de resistência contra veneno e resistência a dano de veneno.',
    
    # Traços Raciais - Draconato
    'Draconic Ancestry': 'Você tem ancestralidade dracônica. Escolha um tipo de dragão da tabela de Ancestralidade Dracônica. Seu sopro e resistência a dano são determinados pelo tipo de dragão.',
    'Breath Weapon': 'Você pode usar sua ação para exalar energia destrutiva. Quando você usa seu sopro, cada criatura na área deve fazer um teste de resistência. A CD é 8 + seu modificador de Constituição + seu bônus de proficiência. Uma criatura sofre 2d6 de dano em um fracasso, e metade do dano em um sucesso. O dano aumenta para 3d6 no 6º nível, 4d6 no 11º nível e 5d6 no 16º nível. Você pode usar essa característica uma vez, recuperando o uso após um descanso curto ou longo.',
    'Damage Resistance': 'Você tem resistência ao tipo de dano associado à sua ancestralidade dracônica.',
    
    # Traços Raciais - Gnomo
    'Gnome Cunning': 'Você tem vantagem em todos os testes de resistência de Inteligência, Sabedoria e Carisma contra magia.',
    'Natural Illusionist': 'Você conhece o truque Ilusão Menor. Inteligência é seu atributo para conjuração.',
    'Speak with Small Beasts': 'Através de sons e gestos, você pode comunicar ideias simples com bestas Pequenas ou menores.',
    'Artificer\'s Lore': 'Sempre que fizer um teste de Inteligência (História) relacionado a itens mágicos, objetos alquímicos ou dispositivos tecnológicos, você adiciona o dobro do seu bônus de proficiência ao teste.',
    'Tinker': 'Você tem proficiência com ferramentas de artesão (ferramentas de engenhoqueiro). Usando essas ferramentas, você pode gastar 1 hora e 10 po em materiais para construir um dispositivo mecânico Miúdo (CA 5, 1 pv).',
    
    # Traços Raciais - Meio-Elfo
    'Skill Versatility': 'Você ganha proficiência em duas perícias à sua escolha.',
    
    # Traços Raciais - Meio-Orc
    'Menacing': 'Você ganha proficiência na perícia Intimidação.',
    'Relentless Endurance': 'Quando você é reduzido a 0 pontos de vida mas não é completamente morto, você pode cair para 1 ponto de vida. Você não pode usar essa característica novamente até terminar um descanso longo.',
    'Savage Attacks': 'Quando você acerta um ataque crítico com uma arma corpo a corpo, você pode rolar um dos dados de dano da arma mais uma vez e adicioná-lo ao dano extra do acerto crítico.',
    
    # Traços Raciais - Tiefling
    'Hellish Resistance': 'Você tem resistência a dano de fogo.',
    'Infernal Legacy': 'Você conhece o truque Taumaturgia. Quando alcança o 3º nível, pode conjurar Repreensão Infernal como uma magia de 2º nível uma vez. Quando alcança o 5º nível, pode conjurar Escuridão uma vez. Carisma é seu atributo para conjuração.',
    
    # Traços de Background
    'Feature: By Popular Demand': 'Você sempre pode encontrar um lugar para se apresentar, geralmente em uma taverna ou estalagem, mas possivelmente em um circo, teatro ou até mesmo em uma corte nobre. Você recebe alojamento e comida modestos gratuitamente.',
    'Feature: Shelter of the Faithful': 'Você e seus companheiros de aventura podem esperar receber cura gratuita e cuidados em um templo, santuário ou outra presença estabelecida de sua fé.',
    'Feature: Discovery': 'A quietude e reclusão de sua estadia estendida deu a você acesso a uma descoberta única e poderosa.',
    'Feature: Researcher': 'Quando você tenta aprender ou recordar uma informação, se você não souber essa informação, você frequentemente sabe onde e de quem pode obtê-la.',
    'Feature: Position of Privilege': 'Graças à sua nobre nascença, as pessoas tendem a pensar o melhor de você. Você é bem-vindo na alta sociedade.',
    'Feature: Wanderer': 'Você tem uma memória excelente para mapas e geografia, e sempre pode recordar o layout geral de terrenos, assentamentos e outras características ao seu redor.',
    'Feature: Rustic Hospitality': 'Como você vem das fileiras do povo comum, você se encaixa entre eles com facilidade. Você pode encontrar um lugar para se esconder, descansar ou se recuperar entre os plebeus.',
    'Feature: Ship\'s Passage': 'Quando você precisar, pode garantir passagem gratuita em um navio de vela para você e seus companheiros de aventura.',
    'Feature: Criminal Contact': 'Você tem um contato confiável e de confiança que atua como seu elo de ligação com uma rede de outros criminosos.',
    'Feature: False Identity': 'Você tem criado uma segunda identidade que inclui documentação, conhecidos estabelecidos e disfarces que lhe permitem assumir essa persona.',
    
    # Traços de Classe - Bárbaro
    'Rage': 'Em batalha, você luta com ferocidade primitiva. No seu turno, você pode entrar em fúria como uma ação bônus. Enquanto estiver em fúria, você ganha vantagem em testes de Força e testes de resistência de Força, bônus de dano corpo a corpo com armas que usam Força, e resistência a dano de concussão, perfuração e cortante.',
    'Unarmored Defense': 'Enquanto não estiver vestindo armadura, sua Classe de Armadura é 10 + seu modificador de Destreza + seu modificador de Constituição. Você pode usar um escudo e ainda ganhar esse benefício.',
    'Reckless Attack': 'Você pode desistir de toda preocupação com defesa para atacar com desespero feroz. Quando fizer seu primeiro ataque no turno, você pode decidir atacar imprudentemente. Fazer isso lhe dá vantagem em testes de ataque corpo a corpo usando Força durante este turno, mas testes de ataque contra você têm vantagem até seu próximo turno.',
    'Danger Sense': 'Você ganha vantagem em testes de resistência de Destreza contra efeitos que você possa ver, como armadilhas e magias. Para ganhar esse benefício, você não pode estar cego, surdo ou incapacitado.',
    
    # Traços de Classe - Bardo
    'Bardic Inspiration': 'Você pode inspirar outros através de palavras animadoras ou música. Para fazer isso, você usa uma ação bônus no seu turno para escolher uma criatura diferente de você a até 18 metros de você que possa ouvi-lo. Essa criatura ganha um dado de Inspiração Bárdica (d6).',
    'Jack of All Trades': 'Você pode adicionar metade do seu bônus de proficiência, arredondado para baixo, a qualquer teste de atributo que você fizer que ainda não inclua seu bônus de proficiência.',
    'Song of Rest': 'Você pode usar música ou oração calmantes para ajudar a revitalizar seus aliados feridos durante um descanso curto.',
    'Expertise': 'Escolha duas de suas proficiências de perícia. Seu bônus de proficiência é dobrado para qualquer teste de atributo que você fizer que use qualquer uma das proficiências escolhidas.',
    
    # Traços de Classe - Clérigo
    'Divine Domain': 'Escolha um domínio relacionado à sua divindade. Sua escolha concede magias de domínio e outras características quando você a escolhe no 1º nível.',
    'Channel Divinity': 'Você ganha a habilidade de canalizar energia divina diretamente de sua divindade, usando essa energia para alimentar efeitos mágicos.',
    
    # Traços de Classe - Druida
    'Druidic': 'Você conhece Druídico, a linguagem secreta dos druidas. Você pode falar o idioma e usá-lo para deixar mensagens ocultas.',
    'Wild Shape': 'Você pode usar sua ação para assumir magicamente a forma de uma besta que você já viu antes.',
    
    # Traços de Classe - Guerreiro
    'Fighting Style': 'Você adota um estilo particular de luta como sua especialidade.',
    'Second Wind': 'Você tem um poço limitado de resistência que pode recorrer para se proteger de danos. No seu turno, você pode usar uma ação bônus para recuperar pontos de vida iguais a 1d10 + seu nível de guerreiro.',
    'Action Surge': 'Você pode se forçar além de seus limites normais por um momento. No seu turno, você pode realizar uma ação adicional além de sua ação regular e possível ação bônus.',
    
    # Traços de Classe - Monge
    'Unarmored Defense (Monk)': 'Enquanto não estiver vestindo armadura ou empunhando um escudo, sua CA é 10 + seu modificador de Destreza + seu modificador de Sabedoria.',
    'Martial Arts': 'Você ganha os seguintes benefícios enquanto estiver desarmado ou empunhando apenas armas de monge e não estiver vestindo armadura ou empunhando um escudo: Você pode usar Destreza em vez de Força para os testes de ataque e dano de seus golpes desarmados e armas de monge.',
    'Ki': 'Seu treinamento permite que você aproveite a energia mística do ki. Você tem um número de pontos de ki igual ao seu nível de monge.',
    'Unarmored Movement': 'Seu deslocamento aumenta em 3 metros enquanto você não estiver vestindo armadura ou empunhando um escudo.',
    
    # Traços de Classe - Paladino
    'Divine Sense': 'Você pode detectar o bem e o mal como uma ação. Até o final do seu próximo turno, você conhece a localização de qualquer celestial, corruptor ou morto-vivo a até 18 metros de você que não esteja com cobertura total.',
    'Lay on Hands': 'Você tem uma reserva de poder curativo que se reabastece quando você faz um descanso longo. Com essa reserva, você pode restaurar um número total de pontos de vida igual ao seu nível de paladino × 5.',
    'Divine Smite': 'Quando você acerta uma criatura com um ataque corpo a corpo com arma, você pode gastar um espaço de magia para causar dano radiante ao alvo, além do dano da arma.',
    
    # Traços de Classe - Patrulheiro
    'Favored Enemy': 'Você tem experiência significativa estudando, rastreando, caçando e até mesmo falando com um certo tipo de inimigo.',
    'Natural Explorer': 'Você é particularmente familiar com um tipo de ambiente natural e é hábil em viajar e sobreviver em tais regiões.',
    
    # Traços de Classe - Ladino
    'Sneak Attack': 'Você sabe como atacar sutilmente e explorar a distração de um inimigo. Uma vez por turno, você pode causar 1d6 de dano extra a uma criatura que você acertar com um ataque se você tiver vantagem no teste de ataque.',
    'Thieves\' Cant': 'Você aprendeu o calão dos ladrões, uma mistura secreta de dialeto, jargão e código que permite que você esconda mensagens em conversas aparentemente normais.',
    'Cunning Action': 'Você pode usar uma ação bônus em cada um de seus turnos em combate para Disparada, Desengajar ou Esconder.',
    'Evasion': 'Quando você é submetido a um efeito que permite fazer um teste de resistência de Destreza para sofrer apenas metade do dano, você não sofre dano algum se for bem-sucedido no teste de resistência, e apenas metade do dano se falhar.',
    
    # Traços de Classe - Feiticeiro
    'Sorcerous Origin': 'Escolha uma origem de feiticeiro, que descreve a fonte do seu poder mágico inato.',
    'Font of Magic': 'Você pode explorar a fonte profunda de magia dentro de você. Essa fonte é representada por pontos de feitiçaria.',
    'Metamagic': 'Você ganha a habilidade de torcer suas magias para se adequarem às suas necessidades. Você ganha duas opções de Metamagia à sua escolha.',
    
    # Traços de Classe - Bruxo
    'Otherworldly Patron': 'Você fez um pacto com um ser de outro mundo à sua escolha.',
    'Pact Magic': 'Sua pesquisa arcana e a magia concedida a você por seu patrono lhe deram facilidade com magias.',
    'Eldritch Invocations': 'Em seus estudos de conhecimento oculto, você desenterrou invocações místicas, fragmentos de conhecimento proibido que lhe conferem uma habilidade mágica permanente.',
    
    # Traços de Classe - Mago
    'Arcane Recovery': 'Você aprendeu a recuperar parte de sua energia mágica estudando seu grimório. Uma vez por dia quando você termina um descanso curto, você pode escolher espaços de magia gastos para recuperar.',
    'Arcane Tradition': 'Você escolhe uma tradição arcana, moldando sua prática de magia através de uma das oito escolas.',
    'Spell Mastery': 'Você alcançou tal maestria sobre certas magias que pode conjurá-las à vontade.',
}

def get_trait_description(trait_name: str) -> str:
    """Retorna a descrição de um traço, ou uma mensagem padrão se não encontrado"""
    return TRAIT_DESCRIPTIONS.get(trait_name, f"Característica especial: {trait_name}")
