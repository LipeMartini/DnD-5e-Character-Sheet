from dataclasses import dataclass
from typing import Optional, Dict, List

ALL_STATS = [
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
]


@dataclass
class Feat:
    """Representa um Feat (Talento) em D&D 5e"""
    name: str
    description: str
    mechanical_effect: str
    prerequisites: Optional[Dict[str, int]] = None  # Ex: {"Strength": 13}
    is_asi: bool = False  # True se for o feat especial de ASI
    ability_increase_options: Optional[List[str]] = None  # Lista de atributos elegíveis para +1
    ability_increase_amount: int = 1
    
    def meets_prerequisites(self, character) -> bool:
        """
        Verifica se o personagem atende aos pré-requisitos do feat
        
        Args:
            character: Objeto Character
            
        Returns:
            True se atende aos pré-requisitos, False caso contrário
        """
        if not self.prerequisites:
            return True
        
        for prereq_key, min_value in self.prerequisites.items():
            # Pré-requisitos especiais (não diretamente atributos)
            if prereq_key == "proficiency":
                # TODO: verificar proficiências específicas (armadura/arma)
                continue
            
            if prereq_key == "spellcasting":
                if not getattr(character, "is_spellcaster", lambda: False)():
                    return False
                continue
            
            if prereq_key == "any_of":
                passed = False
                if isinstance(min_value, dict):
                    for stat_name, required in min_value.items():
                        try:
                            stat_value = getattr(character.stats, stat_name.lower(), 0)
                            if stat_value >= required:
                                passed = True
                                break
                        except AttributeError:
                            continue
                if not passed:
                    return False
                continue
            
            # Verificação direta de atributo
            try:
                stat_value = getattr(character.stats, prereq_key.lower(), 0)
                if isinstance(stat_value, (int, float)) and isinstance(min_value, (int, float)):
                    if stat_value < min_value:
                        return False
            except (AttributeError, TypeError):
                return False
        
        return True


# Feat especial de ASI (sempre aparece primeiro)
ABILITY_SCORE_IMPROVEMENT = Feat(
    name="Ability Score Improvement",
    description="Você pode aumentar um valor de atributo à sua escolha em 2, ou pode aumentar dois valores de atributo à sua escolha em 1. Como normal, você não pode aumentar um valor de atributo acima de 20 usando esta feature.",
    mechanical_effect="Escolha uma das opções:\n• +2 em um atributo (máx 20)\n• +1 em dois atributos (máx 20)",
    prerequisites=None,
    is_asi=True
)


# Feats disponíveis em D&D 5e
FEATS = {
    "Alert": Feat(
        name="Alert",
        description="Sempre alerta ao perigo, você ganha os seguintes benefícios:",
        mechanical_effect="• +5 na iniciativa\n• Você não pode ser surpreendido enquanto estiver consciente\n• Inimigos escondidos não ganham vantagem contra você",
        prerequisites=None
    ),
    "Actor": Feat(
        name="Actor",
        description="Você domina truques de atuação e enganação.",
        mechanical_effect="• +1 em Carisma (máx 20)\n• Vantagem em testes de Enganação e Atuação ao tentar passar por outra pessoa\n• Pode imitar vozes ou sons que ouviu por pelo menos 1 minuto (teste de Insight vs. Enganação)",
        prerequisites={"Charisma": 13},
        ability_increase_options=["charisma"]
    ),
    "Athlete": Feat(
        name="Athlete",
        description="Treinamento físico intenso aprimorou sua mobilidade.",
        mechanical_effect="• +1 em Força ou Destreza (máx 20)\n• Levantar do chão custa apenas 5 pés de movimento\n• Escalar não custa movimento extra\n• Começar um salto em distância exige apenas 5 pés de corrida",
        prerequisites=None,
        ability_increase_options=["strength", "dexterity"]
    ),
    "Charger": Feat(
        name="Charger",
        description="Você transforma deslocamento em impacto.",
        mechanical_effect="• Após usar Dash, pode fazer ataque corpo a corpo ou empurrão como ação bônus\n•  +5 dano no ataque de carga OU empurrar alvo até 10 pés",
        prerequisites=None
    ),
    "Crossbow Expert": Feat(
        name="Crossbow Expert",
        description="Você treinou para atirar bestas em curto alcance.",
        mechanical_effect="• Ignora carregamento de bestas com que tem proficiência\n• Ataques à 5 pés não impõem desvantagem em ataques à distância\n• Ao atacar com arma de uma mão, pode usar ação bônus para disparar uma besta leve",
        prerequisites=None
    ),
    "Defensive Duelist": Feat(
        name="Defensive Duelist",
        description="Você redireciona golpes com uma arma com acuidade.",
        mechanical_effect="• Reação: adiciona bônus de proficiência à CA contra um ataque corpo a corpo enquanto empunha arma com acuidade",
        prerequisites={"Dexterity": 13}
    ),
    "Dual Wielder": Feat(
        name="Dual Wielder",
        description="Você domina o combate com duas armas.",
        mechanical_effect="• +1 CA quando empunha armas corpo a corpo em ambas as mãos\n• Pode usar duas armas de uma mão mesmo que não sejam leves\n• Pode sacar/guardar duas armas quando normalmente poderia apenas uma",
        prerequisites=None
    ),
    "Dungeon Delver": Feat(
        name="Dungeon Delver",
        description="Você se move com confiança por túneis e armadilhas.",
        mechanical_effect="• Vantagem em testes de Percepção/Investigação para detectar portas secretas\n• Vantagem em testes de resistência contra armadilhas\n• Resistência ao dano de armadilhas\n• Movimenta-se normalmente mesmo em passagens estreitas ou escuras",
        prerequisites=None
    ),
    "Durable": Feat(
        name="Durable",
        description="Seu corpo é resistente a ferimentos.",
        mechanical_effect="• +1 em Constituição (máx 20)\n• Ao gastar dado de vida, o mínimo recuperado é 2 × seu modificador de Constituição",
        prerequisites=None,
        ability_increase_options=["constitution"]
    ),
    "Elemental Adept": Feat(
        name="Elemental Adept",
        description="Escolha um tipo de dano elemental.",
        mechanical_effect="• Magias que você conjura ignoram resistência do tipo escolhido\n• Rolagens de dano 1 são tratadas como 2 nesse tipo",
        prerequisites={"spellcasting": True}
    ),
    "Grappler": Feat(
        name="Grappler",
        description="Você domina agarrões e imobilizações.",
        mechanical_effect="• Vantagem em testes de ataque contra criaturas que você agarra\n• Pode usar ação para tentar imobilizar a criatura agarrada (teste vs. Des/For)\n• Criaturas maiores que você não podem ser agarradas (regra padrão)",
        prerequisites={"Strength": 13}
    ),
    "Great Weapon Master": Feat(
        name="Great Weapon Master",
        description="Você canaliza o impulso de armas pesadas.",
        mechanical_effect="• Ao acertar crítico ou reduzir inimigo a 0 HP, faz ataque corpo a corpo como ação bônus\n• Pode aceitar -5 no ataque com arma pesada proficiente para +10 dano",
        prerequisites=None
    ),
    "Healer": Feat(
        name="Healer",
        description="Você sabe estabilizar e curar aliados rapidamente.",
        mechanical_effect="• Quando usa kit de curandeiro para estabilizar, alvo recupera 1 HP\n• Como ação, gaste uso do kit para curar 1d6 +4 + modificador de Constituição do alvo (não funciona se alvo já recebeu nesse descanso)",
        prerequisites=None
    ),
    "Heavily Armored": Feat(
        name="Heavily Armored",
        description="Você treinou com armaduras pesadas.",
        mechanical_effect="• +1 em Força (máx 20)\n• Ganha proficiência em armadura pesada",
        prerequisites={"proficiency": "medium_armor"},
        ability_increase_options=["strength"]
    ),
    "Heavy Armor Master": Feat(
        name="Heavy Armor Master",
        description="Seu treinamento em armadura pesada absorve impacto.",
        mechanical_effect="• +1 em Força (máx 20)\n• Enquanto usar armadura pesada, reduz em 3 o dano de ataques corpo a corpo não mágicos",
        prerequisites={"Strength": 13, "proficiency": "heavy_armor"},
        ability_increase_options=["strength"]
    ),
    "Inspiring Leader": Feat(
        name="Inspiring Leader",
        description="Sua voz galvaniza aliados.",
        mechanical_effect="• Após 10 minutos de discurso, escolha até seis criaturas (incluindo você) que possam te ouvir/compreender\n• Cada alvo recebe PV temporários iguais ao seu nível + modificador de Carisma (1 vez por descanso curto/longo)",
        prerequisites={"Charisma": 13}
    ),
    "Keen Mind": Feat(
        name="Keen Mind",
        description="Sua mente registra cada detalhe.",
        mechanical_effect="• +1 em Inteligência (máx 20)\n• Sempre sabe a direção do norte, a hora exata e quantos dias se passaram\n• Pode recordar qualquer informação vista ou ouvida no último mês",
        prerequisites=None,
        ability_increase_options=["intelligence"]
    ),
    "Lightly Armored": Feat(
        name="Lightly Armored",
        description="Você treinou com armaduras leves.",
        mechanical_effect="• +1 em Força ou Destreza (máx 20)\n• Ganha proficiência com armaduras leves",
        prerequisites=None,
        ability_increase_options=["strength", "dexterity"]
    ),
    "Linguist": Feat(
        name="Linguist",
        description="Você domina códigos e línguas.",
        mechanical_effect="• +1 em Inteligência (máx 20)\n• Aprende três idiomas à sua escolha\n• Pode criar/decifrar códigos escritos (teste de Investigação)",
        prerequisites={"Intelligence": 13},
        ability_increase_options=["intelligence"]
    ),
    "Lucky": Feat(
        name="Lucky",
        description="Sua sorte interfere no destino.",
        mechanical_effect="• 3 pontos de sorte por descanso longo\n• Gaste 1 ponto para rolar d20 adicional em ataque/teste/resistência\n• Pode gastar para forçar inimigo a rolar novamente ataque contra você",
        prerequisites=None
    ),
    "Mage Slayer": Feat(
        name="Mage Slayer",
        description="Você caça conjuradores.",
        mechanical_effect="• Reação: atacar corpo a corpo quando inimigo a 5 pés conjura magia\n• Criaturas que você acerta têm desvantagem nos testes de concentração\n• Vantagem em testes de resistência contra magias conjuradas a 5 pés",
        prerequisites=None
    ),
    "Magic Initiate": Feat(
        name="Magic Initiate",
        description="Você estudou fundamentos arcanos ou divinos.",
        mechanical_effect="• Escolha classe: Bard, Cleric, Druid, Sorcerer, Warlock ou Wizard\n• Aprende dois truques e uma magia de 1º nível dessa lista\n• A magia de 1º nível pode ser conjurada 1x/dia sem slot",
        prerequisites=None
    ),
    "Martial Adept": Feat(
        name="Martial Adept",
        description="Você estudou manobras de mestres de batalha.",
        mechanical_effect="• Aprende duas manobras do Battle Master\n• Recebe um dado de superioridade d6 (recupera em descanso curto/longo)",
        prerequisites=None
    ),
    "Medium Armor Master": Feat(
        name="Medium Armor Master",
        description="Você se move confortavelmente em armadura média.",
        mechanical_effect="• Usando armadura média, você adiciona até +3 do modificador de Destreza à CA\n• Armadura média não impõe desvantagem em furtividade",
        prerequisites={"proficiency": "medium_armor"}
    ),
    "Mobile": Feat(
        name="Mobile",
        description="Sua velocidade é inigualável.",
        mechanical_effect="• +10 pés de deslocamento\n• Dash ignora terreno difícil naquele turno\n• Após atacar corpo a corpo uma criatura, você não provoca OA dela nesse turno",
        prerequisites=None
    ),
    "Moderately Armored": Feat(
        name="Moderately Armored",
        description="Você reforça sua defesa com armaduras médias.",
        mechanical_effect="• +1 em Força ou Destreza (máx 20)\n• Ganha proficiência com armaduras médias e escudos",
        prerequisites={"proficiency": "light_armor"},
        ability_increase_options=["strength", "dexterity"]
    ),
    "Mounted Combatant": Feat(
        name="Mounted Combatant",
        description="Você protege sua montaria e controla o campo.",
        mechanical_effect="• Vantagem em ataques corpo a corpo contra criaturas menores que sua montaria\n• Pode direcionar ataques que visariam sua montaria para você\n• Montaria tem resistência a dano de efeitos que permitem teste de Destreza",
        prerequisites=None
    ),
    "Observant": Feat(
        name="Observant",
        description="Você nota detalhes que outros ignoram.",
        mechanical_effect="• +1 em Inteligência ou Sabedoria (máx 20)\n• +5 em Percepção passiva e Investigação passiva\n• Pode ler lábios se puder ver a criatura e compreender o idioma",
        prerequisites={"any_of": {"Intelligence": 13, "Wisdom": 13}},
        ability_increase_options=["intelligence", "wisdom"]
    ),
    "Polearm Master": Feat(
        name="Polearm Master",
        description="Você tira proveito do alcance de lanças e alabardas.",
        mechanical_effect="• Quando usa a ação Ataque com arma de haste, pode usar ação bônus para atacar com o outro lado (1d4 dano)\n• Criaturas que entram no seu alcance provocam ataque de oportunidade",
        prerequisites=None
    ),
    "Resilient": Feat(
        name="Resilient",
        description="Sua resiliência mental ou física aumenta.",
        mechanical_effect="• +1 em um atributo à escolha (máx 20)\n• Ganha proficiência em testes de resistência do atributo escolhido",
        prerequisites=None,
        ability_increase_options=ALL_STATS
    ),
    "Ritual Caster": Feat(
        name="Ritual Caster",
        description="Você estudou rituais mágicos.",
        mechanical_effect="• Escolha classe baseada em conjuração ritual\n• Ganha livro de rituais com duas magias (nível 1) dessa classe\n• Pode adicionar novos rituais encontrados (processo similar ao Wizard)",
        prerequisites={"any_of": {"Intelligence": 13, "Wisdom": 13}}
    ),
    "Savage Attacker": Feat(
        name="Savage Attacker",
        description="Seus golpes encontram os pontos fracos.",
        mechanical_effect="• Uma vez por turno, ao rolar dano de ataque corpo a corpo, você pode rolar novamente e escolher qual resultado usar",
        prerequisites=None
    ),
    "Sentinel": Feat(
        name="Sentinel",
        description="Você pune inimigos que descuidam da defesa.",
        mechanical_effect="• Ataques de oportunidade reduzem velocidade do alvo para 0\n• Inimigos provocam OA mesmo usando Disengage\n• Reação para atacar inimigo a 5 pés que atacar aliado",
        prerequisites=None
    ),
    "Sharpshooter": Feat(
        name="Sharpshooter",
        description="Seus disparos perfuram qualquer cobertura.",
        mechanical_effect="• Ataques a longo alcance não têm desvantagem\n• Ignora meia e três-quartos de cobertura\n• Pode aceitar -5 no ataque com arma à distância proficiente para +10 dano",
        prerequisites=None
    ),
    "Shield Master": Feat(
        name="Shield Master",
        description="Você transforma o escudo em arma e defesa.",
        mechanical_effect="• Se fizer Dash/Desengage e tiver escudo, pode empurrar como ação bônus\n• Pode adicionar bônus de escudo a testes de resistência de Destreza contra efeitos apenas em você\n• Em resistência de Destreza que permitir metade do dano, pode usar reação para tomar 0 em sucesso",
        prerequisites=None
    ),
    "Skilled": Feat(
        name="Skilled",
        description="Você desenvolveu talentos variados.",
        mechanical_effect="• Escolha três perícias ou ferramentas para ganhar proficiência",
        prerequisites=None
    ),
    "Skulker": Feat(
        name="Skulker",
        description="Você é mestre em se esconder nas sombras.",
        mechanical_effect="• Pode tentar se esconder quando estiver levemente obscurecido\n• Falha em ataque à distância não revela sua posição\n• Vê normalmente em escuridão leve",
        prerequisites={"Dexterity": 13}
    ),
    "Spell Sniper": Feat(
        name="Spell Sniper",
        description="Seus ataques mágicos viajam mais longe.",
        mechanical_effect="• Requer capacidade de conjurar pelo menos uma magia de ataque\n• Dobra o alcance de magias de ataque à distância\n• Ignora meia e três-quartos de cobertura ao usar magia de ataque\n• Aprende um truque adicional de ataque à distância",
        prerequisites={"spellcasting": True}
    ),
    "Tavern Brawler": Feat(
        name="Tavern Brawler",
        description="Você transforma objetos comuns em armas.",
        mechanical_effect="• +1 em Força ou Constituição (máx 20)\n• Proficiência com armas improvisadas\n• Dano desarmado torna-se 1d4\n• Após acertar ataque desarmado ou com arma improvisada, pode tentar agarrar como ação bônus",
        prerequisites=None,
        ability_increase_options=["strength", "constitution"]
    ),
    "Tough": Feat(
        name="Tough",
        description="Sua vitalidade é impressionante.",
        mechanical_effect="• Seu HP máximo aumenta em 2 × seu nível ao receber o feat\n• Ganha +2 HP toda vez que subir de nível",
        prerequisites=None
    ),
    "War Caster": Feat(
        name="War Caster",
        description="Você conjura com precisão em combate.",
        mechanical_effect="• Vantagem em testes de concentração\n• Pode realizar componentes somáticos mesmo com armas/escudo em mãos\n• Pode conjurar magia no lugar de ataque de oportunidade",
        prerequisites=None
    ),
    "Weapon Master": Feat(
        name="Weapon Master",
        description="Você treina com uma variedade de armas.",
        mechanical_effect="• +1 em Força ou Destreza (máx 20)\n• Escolha quatro armas; você ganha proficiência nelas",
        prerequisites=None,
        ability_increase_options=["strength", "dexterity"]
    ),
}


def get_all_feats(include_asi: bool = True) -> List[Feat]:
    """
    Retorna lista de todos os feats disponíveis
    
    Args:
        include_asi: Se True, inclui ASI no início da lista
        
    Returns:
        Lista de Feats
    """
    feats = []
    
    if include_asi:
        feats.append(ABILITY_SCORE_IMPROVEMENT)
    
    feats.extend(FEATS.values())
    
    return feats


def get_available_feats(character, include_asi: bool = True) -> List[Feat]:
    """
    Retorna lista de feats disponíveis para o personagem (que atendem pré-requisitos)
    
    Args:
        character: Objeto Character
        include_asi: Se True, inclui ASI no início da lista
        
    Returns:
        Lista de Feats disponíveis
    """
    all_feats = get_all_feats(include_asi)
    
    available = []
    for feat in all_feats:
        # ASI sempre está disponível
        if feat.is_asi:
            available.append(feat)
            continue
        
        # Verifica se já tem o feat (não pode pegar duplicado, exceto ASI)
        if feat.name in character.feats:
            continue
        
        # Verifica pré-requisitos
        if feat.meets_prerequisites(character):
            available.append(feat)
    
    return available


def get_feat(feat_name: str) -> Optional[Feat]:
    """
    Retorna um feat pelo nome
    
    Args:
        feat_name: Nome do feat
        
    Returns:
        Feat ou None se não encontrado
    """
    if feat_name == "Ability Score Improvement":
        return ABILITY_SCORE_IMPROVEMENT
    
    return FEATS.get(feat_name)
