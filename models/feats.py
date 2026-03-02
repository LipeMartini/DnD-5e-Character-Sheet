from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class Feat:
    """Representa um Feat (Talento) em D&D 5e"""
    name: str
    description: str
    mechanical_effect: str
    prerequisites: Optional[Dict[str, int]] = None  # Ex: {"Strength": 13}
    is_asi: bool = False  # True se for o feat especial de ASI
    
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
            # Verifica se é um pré-requisito especial (não é um atributo)
            if prereq_key == "proficiency":
                # Pré-requisitos especiais (ex: proficiência com armadura média)
                # Por enquanto, retorna True (será implementado depois)
                continue
            
            # Verifica atributo
            try:
                stat_value = getattr(character.stats, prereq_key.lower(), 0)
                if isinstance(stat_value, (int, float)) and isinstance(min_value, (int, float)):
                    if stat_value < min_value:
                        return False
            except (AttributeError, TypeError):
                # Se não conseguir verificar, assume que não atende
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
        mechanical_effect="• +5 de bônus na iniciativa\n• Você não pode ser surpreendido enquanto estiver consciente\n• Outras criaturas não ganham vantagem em ataques contra você como resultado de estarem escondidas",
        prerequisites=None
    ),
    
    "Athlete": Feat(
        name="Athlete",
        description="Você passou por rigoroso treinamento físico para ganhar os seguintes benefícios:",
        mechanical_effect="• Aumente sua Força ou Destreza em 1 (máx 20)\n• Quando estiver caído, levantar usa apenas 5 pés de movimento\n• Escalar não custa movimento extra\n• Você pode fazer um salto em distância com corrida de apenas 5 pés",
        prerequisites=None
    ),
    
    "Tough": Feat(
        name="Tough",
        description="Seu máximo de pontos de vida aumenta em uma quantidade igual ao seu nível quando você ganha este feat. Sempre que você ganhar um nível depois disso, seu máximo de pontos de vida aumenta em 1 adicional.",
        mechanical_effect="• +2 HP por nível (aplicado retroativamente e em níveis futuros)",
        prerequisites=None
    ),
    
    "Lucky": Feat(
        name="Lucky",
        description="Você tem uma sorte inexplicável que parece entrar em ação no momento certo.",
        mechanical_effect="• Você tem 3 pontos de sorte\n• Pode gastar 1 ponto para rolar um d20 adicional em um teste, ataque ou resistência\n• Pode gastar 1 ponto quando uma criatura rolar um ataque contra você para forçá-la a rolar novamente\n• Você recupera todos os pontos gastos quando termina um descanso longo",
        prerequisites=None
    ),
    
    "War Caster": Feat(
        name="War Caster",
        description="Você aprendeu técnicas para conjurar magias em meio ao combate, ganhando os seguintes benefícios:",
        mechanical_effect="• Vantagem em testes de resistência de Constituição para manter concentração em magias\n• Você pode realizar componentes somáticos mesmo com armas ou escudo nas mãos\n• Quando uma criatura provoca ataque de oportunidade, você pode usar sua reação para conjurar uma magia ao invés de fazer um ataque",
        prerequisites=None
    ),
    
    "Great Weapon Master": Feat(
        name="Great Weapon Master",
        description="Você aprendeu a colocar o peso de uma arma em seu favor, deixando seu impulso capacitá-lo a atacar. Você ganha os seguintes benefícios:",
        mechanical_effect="• Em seu turno, quando você acertar um crítico ou reduzir uma criatura a 0 HP com arma corpo a corpo, pode fazer um ataque corpo a corpo como ação bônus\n• Antes de fazer um ataque corpo a corpo com arma pesada que você é proficiente, pode escolher receber -5 no ataque. Se acertar, adiciona +10 ao dano",
        prerequisites=None
    ),
    
    "Sharpshooter": Feat(
        name="Sharpshooter",
        description="Você dominou armas de longo alcance e pode fazer tiros que outros achariam impossíveis. Você ganha os seguintes benefícios:",
        mechanical_effect="• Atacar a longo alcance não impõe desvantagem em suas rolagens de ataque com armas de longo alcance\n• Seus ataques com armas de longo alcance ignoram meia cobertura e três quartos de cobertura\n• Antes de fazer um ataque com arma de longo alcance que você é proficiente, pode escolher receber -5 no ataque. Se acertar, adiciona +10 ao dano",
        prerequisites=None
    ),
    
    "Sentinel": Feat(
        name="Sentinel",
        description="Você dominou técnicas para aproveitar cada queda na defesa de um oponente, ganhando os seguintes benefícios:",
        mechanical_effect="• Quando você acerta uma criatura com ataque de oportunidade, a velocidade dela se torna 0 pelo resto do turno\n• Criaturas provocam ataques de oportunidade mesmo se usarem a ação Disengage\n• Quando uma criatura a 5 pés de você faz um ataque contra um alvo diferente de você, você pode usar sua reação para fazer um ataque corpo a corpo contra a criatura atacante",
        prerequisites=None
    ),
    
    "Mobile": Feat(
        name="Mobile",
        description="Você é excepcionalmente veloz e ágil. Você ganha os seguintes benefícios:",
        mechanical_effect="• Sua velocidade aumenta em 10 pés\n• Quando você usa a ação Dash, terreno difícil não custa movimento extra naquele turno\n• Quando você faz um ataque corpo a corpo contra uma criatura, você não provoca ataques de oportunidade dela pelo resto do turno, independente de acertar ou não",
        prerequisites=None
    ),
    
    "Resilient": Feat(
        name="Resilient",
        description="Escolha um atributo. Você ganha os seguintes benefícios:",
        mechanical_effect="• Aumente o atributo escolhido em 1 (máx 20)\n• Você ganha proficiência em testes de resistência usando o atributo escolhido",
        prerequisites=None
    ),
    
    "Dual Wielder": Feat(
        name="Dual Wielder",
        description="Você dominou a luta com duas armas, ganhando os seguintes benefícios:",
        mechanical_effect="• +1 de bônus na CA enquanto estiver empunhando uma arma corpo a corpo separada em cada mão\n• Você pode usar duas armas mesmo se as armas de uma mão que você está empunhando não forem leves\n• Você pode sacar ou guardar duas armas de uma mão quando normalmente poderia sacar ou guardar apenas uma",
        prerequisites=None
    ),
    
    "Defensive Duelist": Feat(
        name="Defensive Duelist",
        description="Quando você está empunhando uma arma finesse com a qual você é proficiente e outra criatura te acerta com um ataque corpo a corpo, você pode usar sua reação para adicionar seu bônus de proficiência à sua CA para aquele ataque, potencialmente fazendo o ataque errar você.",
        mechanical_effect="• Reação: +bônus de proficiência na CA contra um ataque corpo a corpo (requer arma finesse equipada)",
        prerequisites={"Dexterity": 13}
    ),
    
    "Heavily Armored": Feat(
        name="Heavily Armored",
        description="Você treinou para dominar o uso de armaduras pesadas, ganhando os seguintes benefícios:",
        mechanical_effect="• Aumente sua Força em 1 (máx 20)\n• Você ganha proficiência com armaduras pesadas",
        prerequisites={"proficiency": "medium_armor"}  # Nota: requer verificação especial
    ),
    
    "Mage Slayer": Feat(
        name="Mage Slayer",
        description="Você treinou técnicas úteis para lutar contra conjuradores, ganhando os seguintes benefícios:",
        mechanical_effect="• Quando uma criatura a 5 pés de você conjura uma magia, você pode usar sua reação para fazer um ataque corpo a corpo contra ela\n• Quando você danifica uma criatura concentrando em uma magia, ela tem desvantagem no teste de resistência para manter concentração\n• Você tem vantagem em testes de resistência contra magias conjuradas por criaturas a 5 pés de você",
        prerequisites=None
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
