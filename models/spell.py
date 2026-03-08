from dataclasses import dataclass, field
from typing import List, Dict, Optional
import json
import os
from pathlib import Path

@dataclass
class Spell:
    """Representa uma magia de D&D 5e"""
    name: str
    level: int  # 0 = cantrip, 1-9 = spell levels
    school: str  # Abjuration, Conjuration, Divination, Enchantment, Evocation, Illusion, Necromancy, Transmutation
    casting_time: str  # "1 action", "1 bonus action", "1 minute", etc.
    range: str  # "Self", "Touch", "30 feet", etc.
    components: str  # "V", "S", "M (material)", "V, S", etc.
    duration: str  # "Instantaneous", "Concentration, up to 1 minute", etc.
    description: str
    classes: List[str] = field(default_factory=list)  # Classes que podem aprender esta magia
    ritual: bool = False
    concentration: bool = False
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'level': self.level,
            'school': self.school,
            'casting_time': self.casting_time,
            'range': self.range,
            'components': self.components,
            'duration': self.duration,
            'description': self.description,
            'classes': self.classes,
            'ritual': self.ritual,
            'concentration': self.concentration,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Spell':
        return cls(**data)
    
    def get_level_text(self) -> str:
        """Retorna texto formatado do nível da magia"""
        if self.level == 0:
            return "Cantrip"
        elif self.level == 1:
            return "1º Nível"
        elif self.level == 2:
            return "2º Nível"
        elif self.level == 3:
            return "3º Nível"
        else:
            return f"{self.level}º Nível"


class SpellDatabase:
    """Banco de dados de magias disponíveis"""
    
    _cache = None  # Cache em memória
    
    @staticmethod
    def _load_from_cache() -> Dict[str, Spell]:
        """Carrega magias do arquivo JSON de cache"""
        try:
            # Tenta encontrar o arquivo de cache
            current_dir = Path(__file__).parent.parent
            cache_file = current_dir / "data" / "spells_cache.json"
            
            if not cache_file.exists():
                return None
            
            with open(cache_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Converte dicionário JSON para objetos Spell
            spells = {}
            for name, spell_data in data.items():
                spells[name] = Spell(**spell_data)
            
            return spells
            
        except Exception as e:
            print(f"⚠️ Erro ao carregar cache de magias: {e}")
            return None
    
    @staticmethod
    def _get_manual_spells() -> Dict[str, Spell]:
        """Retorna magias definidas manualmente (fallback)"""
        return {
            # ========== CANTRIPS ==========
            'Fire Bolt': Spell(
                name='Fire Bolt',
                level=0,
                school='Evocation',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='Instantânea',
                description='Você arremessa um projétil de fogo em uma criatura ou objeto dentro do alcance. Faça um ataque de magia à distância contra o alvo. Em um acerto, o alvo sofre 1d10 de dano de fogo. Um objeto inflamável atingido por essa magia se incendeia se não estiver sendo vestido ou carregado.\n\nO dano da magia aumenta em 1d10 quando você alcança o 5º nível (2d10), 11º nível (3d10) e 17º nível (4d10).',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Cordon of Arrows': Spell(
                name='Cordon of Arrows',
                level=2,
                school='Transmutation',
                casting_time='1 ação',
                range='5 pés',
                components='V, S, M (quatro flechas ou virotes)',
                duration='8 horas',
                description='Você planta flechas ou virotes no solo e os imbui com magia. Quando uma criatura que você escolher entra no raio de 30 pés, uma flecha voa para atingi-la, realizando um ataque de arma à distância com +5 ao ataque e causando 1d6 de dano perfurante. Cada flecha pode atingir apenas uma vez. Em níveis superiores: você pode preparar duas flechas adicionais para cada nível acima do 2º.',
                classes=['Ranger'],
                ritual=False,
                concentration=False
            ),
            'Mage Hand': Spell(
                name='Mage Hand',
                level=0,
                school='Conjuration',
                casting_time='1 ação',
                range='30 pés',
                components='V, S',
                duration='1 minuto',
                description='Uma mão espectral flutuante aparece em um ponto que você escolher dentro do alcance. A mão dura pela duração ou até você a dispensar com uma ação. A mão desaparece se estiver a mais de 30 pés de você ou se você conjurar essa magia novamente.\n\nVocê pode usar sua ação para controlar a mão. Você pode usar a mão para manipular um objeto, abrir uma porta ou recipiente destrancado, guardar ou recuperar um item de um recipiente aberto, ou despejar o conteúdo de um frasco. Você pode mover a mão até 30 pés cada vez que a usar.\n\nA mão não pode atacar, ativar itens mágicos, ou carregar mais de 10 libras.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Prestidigitation': Spell(
                name='Prestidigitation',
                level=0,
                school='Transmutation',
                casting_time='1 ação',
                range='10 pés',
                components='V, S',
                duration='Até 1 hora',
                description='Este truque é um truque mágico menor que conjuradores novatos usam para praticar. Você cria um dos seguintes efeitos mágicos dentro do alcance:\n\n• Você cria um efeito sensorial inofensivo e instantâneo, como uma chuva de faíscas, uma lufada de vento, notas musicais suaves ou um odor estranho.\n• Você instantaneamente acende ou apaga uma vela, tocha ou pequena fogueira.\n• Você instantaneamente limpa ou suja um objeto não maior que 1 pé cúbico.\n• Você esfria, esquenta ou aromatiza até 1 pé cúbico de material inerte por 1 hora.\n• Você faz uma cor, uma pequena marca ou um símbolo aparecer em um objeto ou superfície por 1 hora.\n• Você cria uma bugiganga não-mágica ou uma imagem ilusória que cabe em sua mão e dura até o final do seu próximo turno.\n\nSe você conjurar essa magia múltiplas vezes, você pode ter até três de seus efeitos não-instantâneos ativos ao mesmo tempo.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Sacred Flame': Spell(
                name='Sacred Flame',
                level=0,
                school='Evocation',
                casting_time='1 ação',
                range='60 pés',
                components='V, S',
                duration='Instantânea',
                description='Chamas divinas descem sobre uma criatura que você possa ver dentro do alcance. O alvo deve ter sucesso em um teste de resistência de Destreza ou sofre 1d8 de dano radiante. O alvo não ganha benefício de cobertura para este teste de resistência.\n\nO dano da magia aumenta em 1d8 quando você alcança o 5º nível (2d8), 11º nível (3d8) e 17º nível (4d8).',
                classes=['Cleric'],
                ritual=False,
                concentration=False
            ),
            'Guidance': Spell(
                name='Guidance',
                level=0,
                school='Divination',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='Você toca uma criatura voluntária. Uma vez antes da magia acabar, o alvo pode rolar um d4 e adicionar o número rolado a um teste de habilidade de sua escolha. Ele pode rolar o dado antes ou depois de fazer o teste de habilidade. A magia então acaba.',
                classes=['Cleric', 'Druid'],
                ritual=False,
                concentration=True
            ),
            'Light': Spell(
                name='Light',
                level=0,
                school='Evocation',
                casting_time='1 ação',
                range='Toque',
                components='V, M (um vaga-lume ou musgo fosforescente)',
                duration='1 hora',
                description='Você toca um objeto que não seja maior que 10 pés em qualquer dimensão. Até a magia acabar, o objeto emite luz brilhante em um raio de 20 pés e penumbra por mais 20 pés. A luz pode ser de qualquer cor que você escolher. Cobrir completamente o objeto com algo opaco bloqueia a luz. A magia acaba se você a conjurar novamente ou a dispensar com uma ação.\n\nSe você mirar em um objeto sendo segurado ou vestido por uma criatura hostil, essa criatura deve ter sucesso em um teste de resistência de Destreza para evitar a magia.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Cleric'],
                ritual=False,
                concentration=False
            ),
            'Eldritch Blast': Spell(
                name='Eldritch Blast',
                level=0,
                school='Evocation',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='Instantânea',
                description='Um raio de energia crepitante dispara em direção a uma criatura dentro do alcance. Faça um ataque de magia à distância contra o alvo. Em um acerto, o alvo sofre 1d10 de dano de força.\n\nA magia cria mais de um raio quando você atinge níveis superiores: dois raios no 5º nível, três raios no 11º nível e quatro raios no 17º nível. Você pode direcionar os raios para o mesmo alvo ou para alvos diferentes. Faça uma jogada de ataque separada para cada raio.',
                classes=['Warlock'],
                ritual=False,
                concentration=False
            ),
            'Compelled Duel': Spell(
                name='Compelled Duel',
                level=1,
                school='Enchantment',
                casting_time='1 ação bônus',
                range='30 pés',
                components='V',
                duration='Concentração, até 1 minuto',
                description='Você tenta compelir uma criatura a lutar apenas com você. Em uma falha no teste de resistência de Sabedoria, o alvo sofre desvantagem em ataques contra criaturas que não sejam você e deve fazer testes quando tentar se mover para longe. O efeito termina se você atacar outra criatura ou se um aliado o atacar.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Searing Smite': Spell(
                name='Searing Smite',
                level=1,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='Na próxima vez que você acertar com um ataque corpo a corpo com arma, o ataque causa 1d6 de dano de fogo extra e incendeia o alvo. No início de cada turno, o alvo deve fazer um teste de resistência de Constituição ou sofrer 1d6 de dano e continuar em chamas. Um sucesso ou uma ação para apagar as chamas encerra a magia. Em níveis superiores: o dano inicial aumenta em 1d6 por nível acima do 1º.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Thunderous Smite': Spell(
                name='Thunderous Smite',
                level=1,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar com um ataque corpo a corpo com arma, ele causa 2d6 de dano trovejante extra e o alvo deve passar em um teste de resistência de Força ou ser empurrado 10 pés e derrubado. Em níveis superiores: o dano aumenta em 1d6 por nível acima do 1º.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Wrathful Smite': Spell(
                name='Wrathful Smite',
                level=1,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar com um ataque corpo a corpo com arma, ele causa 1d6 de dano psíquico extra e o alvo deve fazer um teste de resistência de Sabedoria ou ficar amedrontado. Enquanto estiver amedrontado, o alvo pode usar uma ação para repetir o teste com desvantagem, encerrando o efeito em um sucesso. Em níveis superiores: o dano aumenta em 1d6 por nível acima do 1º.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Ensnaring Strike': Spell(
                name='Ensnaring Strike',
                level=1,
                school='Conjuration',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar uma criatura com um ataque com arma, vinhas espinhosas a envolvem. O alvo sofre 1d6 de dano perfurante e deve fazer um teste de resistência de Força ou ficar contido, sofrendo 1d6 de dano adicional no início de cada turno enquanto contido. Ele ou outra criatura pode usar uma ação para fazer um teste de Força e se libertar. Em níveis superiores: o dano aumenta em 1d6 por nível acima do 1º.',
                classes=['Ranger'],
                ritual=False,
                concentration=True
            ),
            'Hail of Thorns': Spell(
                name='Hail of Thorns',
                level=1,
                school='Conjuration',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar uma criatura com um ataque de arma à distância, uma chuva de espinhos explode. O alvo e criaturas a 5 pés devem fazer um teste de resistência de Destreza, sofrendo 1d10 de dano perfurante em uma falha ou metade no sucesso. Em níveis superiores: o dano aumenta em 1d10 por nível acima do 1º.',
                classes=['Ranger'],
                ritual=False,
                concentration=True
            ),
            'Chill Touch': Spell(
                name='Chill Touch',
                level=0,
                school='Necromancy',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='1 rodada',
                description='Você cria uma mão fantasmagórica dentro do alcance. Faça um ataque de magia à distância contra uma criatura. Em um acerto, o alvo sofre 1d8 de dano necrótico e não pode recuperar pontos de vida até o início do seu próximo turno. Até lá, a mão se agarra ao alvo. Se você atingir um morto-vivo, ele também tem desvantagem em jogadas de ataque contra você até o final do seu próximo turno.\n\nO dano da magia aumenta em 1d8 quando você alcança o 5º nível (2d8), 11º nível (3d8) e 17º nível (4d8).',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Poison Spray': Spell(
                name='Poison Spray',
                level=0,
                school='Conjuration',
                casting_time='1 ação',
                range='10 pés',
                components='V, S',
                duration='Instantânea',
                description='Você estende sua mão em direção a uma criatura que você possa ver dentro do alcance e projeta uma lufada de gás tóxico de sua palma. A criatura deve ter sucesso em um teste de resistência de Constituição ou sofre 1d12 de dano de veneno.\n\nO dano da magia aumenta em 1d12 quando você alcança o 5º nível (2d12), 11º nível (3d12) e 17º nível (4d12).',
                classes=['Wizard', 'Sorcerer', 'Druid', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'True Strike': Spell(
                name='True Strike',
                level=0,
                school='Divination',
                casting_time='1 ação',
                range='30 pés',
                components='S',
                duration='Concentração, até 1 rodada',
                description='Você estende sua mão e aponta o dedo para um alvo dentro do alcance. Sua magia concede a você uma breve visão da defesa do alvo. No seu próximo turno, você tem vantagem na sua primeira jogada de ataque contra o alvo, desde que essa magia não tenha acabado.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Blade Ward': Spell(
                name='Blade Ward',
                level=0,
                school='Abjuration',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='1 rodada',
                description='Você traça um símbolo de proteção no ar. Até o fim do seu próximo turno, você tem resistência contra dano cortante, perfurante e contundente causado por ataques com armas.',
                classes=['Bard', 'Sorcerer', 'Warlock', 'Wizard'],
                ritual=False,
                concentration=False
            ),
            'Friends': Spell(
                name='Friends',
                level=0,
                school='Enchantment',
                casting_time='1 ação',
                range='Pessoal',
                components='S, M (um pouco de maquiagem aplicado ao rosto enquanto a magia é conjurada)',
                duration='Concentração, até 1 minuto',
                description='Pela duração, você tem vantagem em todos os testes de Carisma direcionados a uma criatura de sua escolha que não seja hostil a você. Ao término da magia, a criatura percebe que você influenciou suas emoções, tornando-se hostil a você.',
                classes=['Bard', 'Sorcerer', 'Warlock', 'Wizard'],
                ritual=False,
                concentration=True
            ),
            'Produce Flame': Spell(
                name='Produce Flame',
                level=0,
                school='Conjuration',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='10 minutos',
                description='Uma chama tremeluzente aparece em sua mão. A chama emite luz brilhante em um raio de 10 pés e penumbra por mais 10 pés, não causa dano a você ou ao que estiver carregando e dura até você a dispensar. Você pode lançar a chama contra uma criatura a até 30 pés com um ataque de magia à distância, causando 1d8 de dano de fogo (aumentando em 1d8 nos níveis 5, 11 e 17).',
                classes=['Druid'],
                ritual=False,
                concentration=False
            ),
            
            # ========== NÍVEL 1 ==========
            'Magic Missile': Spell(
                name='Magic Missile',
                level=1,
                school='Evocation',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='Instantânea',
                description='Você cria três dardos brilhantes de força mágica. Cada dardo atinge uma criatura de sua escolha que você possa ver dentro do alcance. Um dardo causa 1d4 + 1 de dano de força ao seu alvo. Os dardos atingem simultaneamente e você pode direcioná-los para atingir uma criatura ou várias.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, a magia cria mais um dardo para cada nível do espaço acima do 1º.',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Chromatic Orb': Spell(
                name='Chromatic Orb',
                level=1,
                school='Evocation',
                casting_time='1 ação',
                range='90 pés',
                components='V, S, M (um diamante valendo pelo menos 50 po)',
                duration='Instantânea',
                description='Você lança uma esfera de energia em uma criatura dentro do alcance, escolhendo ácido, frio, fogo, elétrico, trovejante ou veneno. Faça um ataque de magia à distância. Em um acerto, o alvo sofre 3d8 de dano do tipo escolhido.\n\nEm níveis superiores: o dano aumenta em 1d8 para cada nível do espaço acima do 1º.',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Shield': Spell(
                name='Shield',
                level=1,
                school='Abjuration',
                casting_time='1 reação',
                range='Pessoal',
                components='V, S',
                duration='1 rodada',
                description='Uma barreira invisível de força mágica aparece e o protege. Até o início do seu próximo turno, você tem um bônus de +5 na CA, incluindo contra o ataque desencadeador, e você não sofre dano de mísseis mágicos.',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Mage Armor': Spell(
                name='Mage Armor',
                level=1,
                school='Abjuration',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (um pedaço de couro curtido)',
                duration='8 horas',
                description='Você toca uma criatura voluntária que não esteja vestindo armadura, e uma força mágica protetora a envolve até a magia acabar. A CA base do alvo se torna 13 + seu modificador de Destreza. A magia acaba se o alvo colocar uma armadura ou se você a dispensar com uma ação.',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Detect Magic': Spell(
                name='Detect Magic',
                level=1,
                school='Divination',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='Concentração, até 10 minutos',
                description='Pela duração, você sente a presença de magia a até 30 pés de você. Se você sentir magia dessa forma, você pode usar sua ação para ver uma aura fraca ao redor de qualquer criatura ou objeto visível na área que carregue magia, e você aprende sua escola de magia, se houver.\n\nA magia pode penetrar a maioria das barreiras, mas é bloqueada por 1 pé de pedra, 1 polegada de metal comum, uma fina camada de chumbo, ou 3 pés de madeira ou terra.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Cleric', 'Druid', 'Paladin', 'Ranger'],
                ritual=True,
                concentration=True
            ),
            'Cure Wounds': Spell(
                name='Cure Wounds',
                level=1,
                school='Evocation',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='Instantânea',
                description='Uma criatura que você tocar recupera um número de pontos de vida igual a 1d8 + seu modificador de habilidade de conjuração. Esta magia não tem efeito em mortos-vivos ou constructos.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, a cura aumenta em 1d8 para cada nível do espaço acima do 1º.',
                classes=['Cleric', 'Bard', 'Druid', 'Paladin', 'Ranger'],
                ritual=False,
                concentration=False
            ),
            'Dissonant Whispers': Spell(
                name='Dissonant Whispers',
                level=1,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V',
                duration='Instantânea',
                description='Você sussurra uma melodia discordante que apenas uma criatura pode ouvir. O alvo deve fazer um teste de resistência de Sabedoria. Em uma falha, sofre 3d6 de dano psíquico e deve usar sua reação para se mover imediatamente o mais longe possível de você. Em um sucesso, sofre metade do dano e não precisa se mover.\n\nEm níveis superiores: o dano aumenta em 1d6 para cada nível do espaço acima do 1º.',
                classes=['Bard'],
                ritual=False,
                concentration=False
            ),
            'Ray of Sickness': Spell(
                name='Ray of Sickness',
                level=1,
                school='Necromancy',
                casting_time='1 ação',
                range='60 pés',
                components='V, S',
                duration='Instantânea',
                description='Um raio esverdeado nauseante dispara em direção a uma criatura dentro do alcance. Faça um ataque de magia à distância. Em um acerto, o alvo sofre 2d8 de dano de veneno e deve fazer um teste de resistência de Constituição. Em uma falha, fica envenenado até o final do seu próximo turno.\n\nEm níveis superiores: o dano aumenta em 1d8 para cada nível do espaço acima do 1º.',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Bless': Spell(
                name='Bless',
                level=1,
                school='Enchantment',
                casting_time='1 ação',
                range='30 pés',
                components='V, S, M (um borrifo de água benta)',
                duration='Concentração, até 1 minuto',
                description='Você abençoa até três criaturas de sua escolha dentro do alcance. Sempre que um alvo fizer um ataque ou teste de resistência antes da magia acabar, o alvo pode rolar um d4 e adicionar o número rolado ao ataque ou teste de resistência.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, você pode mirar em uma criatura adicional para cada nível do espaço acima do 1º.',
                classes=['Cleric', 'Paladin'],
                ritual=False,
                concentration=True
            ),
            'Healing Word': Spell(
                name='Healing Word',
                level=1,
                school='Evocation',
                casting_time='1 ação bônus',
                range='60 pés',
                components='V',
                duration='Instantânea',
                description='Uma criatura de sua escolha que você possa ver dentro do alcance recupera pontos de vida iguais a 1d4 + seu modificador de habilidade de conjuração. Esta magia não tem efeito em mortos-vivos ou constructos.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, a cura aumenta em 1d4 para cada nível do espaço acima do 1º.',
                classes=['Cleric', 'Bard', 'Druid'],
                ritual=False,
                concentration=False
            ),
            'Hex': Spell(
                name='Hex',
                level=1,
                school='Enchantment',
                casting_time='1 ação bônus',
                range='90 pés',
                components='V, S, M (o olho petrificado de um tritão)',
                duration='Concentração, até 1 hora',
                description='Você coloca uma maldição em uma criatura que você possa ver dentro do alcance. Até a magia acabar, você causa 1d6 de dano necrótico extra ao alvo sempre que você o atingir com um ataque. Além disso, escolha uma habilidade quando você conjurar a magia. O alvo tem desvantagem em testes de habilidade feitos com a habilidade escolhida.\n\nSe o alvo cair a 0 pontos de vida antes desta magia acabar, você pode usar uma ação bônus em um turno subsequente seu para amaldiçoar uma nova criatura.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º ou 4º nível, você pode manter sua concentração na magia por até 8 horas. Quando você usa um espaço de magia de 5º nível ou superior, você pode manter sua concentração na magia por até 24 horas.',
                classes=['Warlock'],
                ritual=False,
                concentration=True
            ),
            'Armor of Agathys': Spell(
                name='Armor of Agathys',
                level=1,
                school='Abjuration',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S, M (água)',
                duration='1 hora',
                description='Uma força mágica protetora envolve você, manifestando-se como um gelo espectral que cobre você e seu equipamento. Você ganha 5 pontos de vida temporários pela duração. Se uma criatura o atingir com um ataque corpo a corpo enquanto você tiver esses pontos de vida, a criatura sofre 5 de dano de frio.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, tanto os pontos de vida temporários quanto o dano de frio aumentam em 5 para cada nível do espaço acima do 1º.',
                classes=['Warlock'],
                ritual=False,
                concentration=False
            ),
            'Arms of Hadar': Spell(
                name='Arms of Hadar',
                level=1,
                school='Conjuration',
                casting_time='1 ação',
                range='Pessoal (raio de 10 pés)',
                components='V, S',
                duration='Instantânea',
                description='Você invoca o poder de Hadar, o Faminto das Trevas. Tentáculos de energia escura irrompem de você e açoitam todas as criaturas a 10 pés de você. Cada criatura nessa área deve fazer um teste de resistência de Força. Em uma falha, um alvo sofre 2d6 de dano necrótico e não pode fazer reações até o próximo turno dele. Em um sucesso, a criatura sofre metade do dano e não sofre outros efeitos.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, o dano aumenta em 1d6 para cada nível do espaço acima do 1º.',
                classes=['Warlock'],
                ritual=False,
                concentration=False
            ),
            'Charm Person': Spell(
                name='Charm Person',
                level=1,
                school='Enchantment',
                casting_time='1 ação',
                range='30 pés',
                components='V, S',
                duration='1 hora',
                description='Você tenta encantar um humanoide que você possa ver dentro do alcance. Ele deve fazer um teste de resistência de Sabedoria, e o faz com vantagem se você ou seus companheiros estiverem lutando com ele. Se ele falhar no teste de resistência, ele é encantado por você até a magia acabar ou até você ou seus companheiros fazerem algo prejudicial a ele. A criatura encantada o considera um conhecido amigável. Quando a magia acabar, a criatura sabe que foi encantada por você.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, você pode mirar em uma criatura adicional para cada nível do espaço acima do 1º.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Druid', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            "Tasha's Hideous Laughter": Spell(
                name="Tasha's Hideous Laughter",
                level=1,
                school='Enchantment',
                casting_time='1 ação',
                range='30 pés',
                components='V, S, M (pequenas tortas e uma pena dourada)',
                duration='Concentração, até 1 minuto',
                description='Uma criatura que você possa ver percebe tudo como hilário e precisa ter sucesso em um teste de resistência de Sabedoria ou cair no chão, ficando incapacitada e incapaz de ficar em pé durante a duração. A criatura tem vantagem no teste se tiver Inteligência 4 ou menor. No final de cada turno e sempre que sofrer dano, o alvo pode fazer novos testes de resistência para encerrar o efeito.',
                classes=['Bard', 'Wizard'],
                ritual=False,
                concentration=True
            ),
            'Comprehend Languages': Spell(
                name='Comprehend Languages',
                level=1,
                school='Divination',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S, M (fuligem e sal)',
                duration='1 hora',
                description='Pela duração, você compreende o significado literal de qualquer idioma falado que você ouvir. Você também compreende qualquer idioma escrito que você veja, mas você deve estar tocando a superfície na qual as palavras estão escritas. Leva cerca de 1 minuto para ler uma página de texto.\n\nEsta magia não decodifica mensagens secretas em um texto ou um glifo, como um símbolo arcano, que não faz parte de um idioma escrito.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=True,
                concentration=False
            ),
            'Expeditious Retreat': Spell(
                name='Expeditious Retreat',
                level=1,
                school='Transmutation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V, S',
                duration='Concentração, até 10 minutos',
                description='Esta magia permite que você se mova a uma velocidade incrível. Quando você conjura essa magia, e então como uma ação bônus em cada um de seus turnos até a magia acabar, você pode fazer a ação Disparada.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Hellish Rebuke': Spell(
                name='Hellish Rebuke',
                level=1,
                school='Evocation',
                casting_time='1 reação',
                range='60 pés',
                components='V, S',
                duration='Instantânea',
                description='Você aponta seu dedo, e a criatura que o danificou é momentaneamente envolvida em chamas infernais. A criatura deve fazer um teste de resistência de Destreza. Ela sofre 2d10 de dano de fogo em uma falha, ou metade do dano em um sucesso.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, o dano aumenta em 1d10 para cada nível do espaço acima do 1º.',
                classes=['Warlock'],
                ritual=False,
                concentration=False
            ),
            'Illusory Script': Spell(
                name='Illusory Script',
                level=1,
                school='Illusion',
                casting_time='1 minuto',
                range='Toque',
                components='S, M (tinta à base de chumbo no valor de pelo menos 10 po, que a magia consome)',
                duration='10 dias',
                description='Você escreve em pergaminho, papel ou algum outro material de escrita adequado e o imbui com uma poderosa ilusão que dura pela duração. Para você e qualquer criatura que você designar quando conjurar a magia, a escrita parece normal, escrita em sua mão, e transmite qualquer significado que você pretendia quando escreveu o texto. Para todos os outros, a escrita parece estar em um idioma desconhecido ou mágico que é ininteligível. Alternativamente, você pode fazer a escrita parecer ser uma mensagem totalmente diferente, escrita em uma caligrafia diferente e idioma diferente, embora o idioma deva ser um que você conheça.\n\nSe a magia for dissipada, tanto a escrita original quanto a ilusão desaparecem. Uma criatura com visão verdadeira pode ler a mensagem oculta.',
                classes=['Wizard', 'Bard', 'Warlock'],
                ritual=True,
                concentration=False
            ),
            'Protection from Evil and Good': Spell(
                name='Protection from Evil and Good',
                level=1,
                school='Abjuration',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (água benta ou pó de prata e ferro)',
                duration='Concentração, até 10 minutos',
                description='Até a magia acabar, uma criatura voluntária que você tocar está protegida contra certos tipos de criaturas: aberrações, celestiais, elementais, fadas, demoníacos e mortos-vivos. A proteção concede vários benefícios. Criaturas desses tipos têm desvantagem em jogadas de ataque contra o alvo. O alvo também não pode ser encantado, amedrontado ou possuído por eles. Se o alvo já estiver encantado, amedrontado ou possuído por tal criatura, o alvo tem vantagem em qualquer novo teste de resistência contra o efeito relevante.',
                classes=['Wizard', 'Cleric', 'Paladin', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Unseen Servant': Spell(
                name='Unseen Servant',
                level=1,
                school='Conjuration',
                casting_time='1 ação',
                range='60 pés',
                components='V, S, M (um pedaço de barbante e um pouco de madeira)',
                duration='1 hora',
                description='Esta magia cria uma força invisível, sem mente e sem forma que realiza tarefas simples ao seu comando até a magia acabar. O servo surge em um espaço desocupado no chão dentro do alcance. Ele tem CA 10, 1 ponto de vida e Força 2, e não pode atacar. Se cair a 0 pontos de vida, a magia acaba.\n\nUma vez em cada um de seus turnos como uma ação bônus, você pode comandar mentalmente o servo para se mover até 15 pés e interagir com um objeto. O servo pode realizar tarefas simples que um servo humano poderia fazer, como buscar coisas, limpar, consertar, dobrar roupas, acender fogos, servir comida e derramar vinho. Uma vez que você dá o comando, o servo realiza a tarefa da melhor de sua capacidade até completar a tarefa, então espera por seu próximo comando.\n\nSe você comandar o servo para realizar uma tarefa que o moveria mais de 60 pés de você, a magia acaba.',
                classes=['Wizard', 'Bard', 'Warlock'],
                ritual=True,
                concentration=False
            ),
            'Witch Bolt': Spell(
                name='Witch Bolt',
                level=1,
                school='Evocation',
                casting_time='1 ação',
                range='30 pés',
                components='V, S, M (um galho de uma árvore que foi atingida por um raio)',
                duration='Concentração, até 1 minuto',
                description='Um raio de energia elétrica azul-crepitante salta em direção a uma criatura dentro do alcance, formando um arco sustentado de relâmpago entre você e o alvo. Faça um ataque de magia à distância contra essa criatura. Em um acerto, o alvo sofre 1d12 de dano elétrico, e em cada um de seus turnos pela duração, você pode usar sua ação para causar 1d12 de dano elétrico ao alvo automaticamente. A magia acaba se você usar sua ação para fazer qualquer outra coisa. A magia também acaba se o alvo estiver sempre fora do alcance da magia ou se tiver cobertura total de você.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 2º nível ou superior, o dano inicial aumenta em 1d12 para cada nível do espaço acima do 1º.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            
            # ========== NÍVEL 2 ==========
            'Scorching Ray': Spell(
                name='Scorching Ray',
                level=2,
                school='Evocation',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='Instantânea',
                description='Você cria três raios de fogo e os arremessa em alvos dentro do alcance. Você pode arremessá-los em um alvo ou em vários. Faça um ataque de magia à distância para cada raio. Em um acerto, o alvo sofre 2d6 de dano de fogo.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º nível ou superior, você cria um raio adicional para cada nível do espaço acima do 2º.',
                classes=['Wizard', 'Sorcerer'],
                ritual=False,
                concentration=False
            ),
            'Phantasmal Force': Spell(
                name='Phantasmal Force',
                level=2,
                school='Illusion',
                casting_time='1 ação',
                range='60 pés',
                components='V, S, M (um pouco de lã)',
                duration='Concentração, até 1 minuto',
                description='Você cria uma ilusão que ocupa um cubo de 10 pés que apenas o alvo pode ver. O alvo deve fazer um teste de resistência de Inteligência. Em uma falha, ele acredita que a ilusão é real. Enquanto durar, a ilusão pode causar 1d6 de dano psíquico por rodada se representar algo perigoso. O alvo pode usar uma ação para examinar a ilusão e fazer um teste de Inteligência (Investigação) contra sua CD de magia para discernir a verdade.',
                classes=['Bard', 'Sorcerer', 'Wizard'],
                ritual=False,
                concentration=True
            ),
            'Misty Step': Spell(
                name='Misty Step',
                level=2,
                school='Conjuration',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Instantânea',
                description='Brevemente envolto em névoa prateada, você se teletransporta até 30 pés para um espaço desocupado que você possa ver.',
                classes=['Wizard', 'Sorcerer', 'Warlock', 'Bard'],
                ritual=False,
                concentration=False
            ),
            'Beast Sense': Spell(
                name='Beast Sense',
                level=2,
                school='Divination',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='Concentração, até 1 hora',
                description='Você toca uma fera voluntária que não seja hostil e percebe através de seus sentidos até a magia acabar. Enquanto estiver na forma da fera, você está cego e surdo em relação aos seus próprios sentidos.',
                classes=['Druid', 'Ranger'],
                ritual=True,
                concentration=True
            ),
            'Mirror Image': Spell(
                name='Mirror Image',
                level=2,
                school='Illusion',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='1 minuto',
                description='Três duplicatas ilusórias de você mesmo aparecem em seu espaço. Até a magia acabar, as duplicatas se movem com você e imitam suas ações, mudando de posição de modo que seja impossível rastrear qual imagem é real. Você pode usar sua ação para dispensar as duplicatas ilusórias.\n\nCada vez que uma criatura o mirar com um ataque durante a duração da magia, role um d20 para determinar se o ataque não mira em uma das suas duplicatas. Se você tem três duplicatas, você deve rolar 6 ou maior para mudar o alvo do ataque para uma duplicata. Com duas duplicatas, você deve rolar 8 ou maior. Com uma duplicata, você deve rolar 11 ou maior.\n\nA CA de uma duplicata é igual a 10 + seu modificador de Destreza. Se um ataque acertar uma duplicata, a duplicata é destruída. Uma duplicata pode ser destruída apenas por um ataque que a acerte. Ela ignora todos os outros danos e efeitos. A magia acaba quando todas as três duplicatas forem destruídas.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Branding Smite': Spell(
                name='Branding Smite',
                level=2,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar uma criatura com um ataque corpo a corpo com arma, o ataque causa 2d6 de dano radiante extra e o alvo brilha intensamente, emitindo luz brilhante em um raio de 5 pés. Ele não pode se tornar invisível até o término da magia. Em níveis superiores: o dano aumenta em 1d6 para cada nível do espaço acima do 2º.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Hold Person': Spell(
                name='Hold Person',
                level=2,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V, S, M (um pequeno pedaço de ferro reto)',
                duration='Concentração, até 1 minuto',
                description='Escolha um humanoide que você possa ver dentro do alcance. O alvo deve ter sucesso em um teste de resistência de Sabedoria ou ficará paralisado pela duração. No final de cada um de seus turnos, o alvo pode fazer outro teste de resistência de Sabedoria. Em um sucesso, a magia acaba no alvo.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º nível ou superior, você pode mirar em um humanoide adicional para cada nível do espaço acima do 2º. Os humanoides devem estar a 30 pés uns dos outros quando você os mirar.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Cleric', 'Druid', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Spiritual Weapon': Spell(
                name='Spiritual Weapon',
                level=2,
                school='Evocation',
                casting_time='1 ação bônus',
                range='60 pés',
                components='V, S',
                duration='1 minuto',
                description='Você cria uma arma espectral flutuante dentro do alcance que dura pela duração ou até você conjurar essa magia novamente. Quando você conjura a magia, você pode fazer um ataque de magia corpo a corpo contra uma criatura a 5 pés da arma. Em um acerto, o alvo sofre dano de força igual a 1d8 + seu modificador de habilidade de conjuração.\n\nComo uma ação bônus no seu turno, você pode mover a arma até 20 pés e repetir o ataque contra uma criatura a 5 pés dela.\n\nA arma pode tomar qualquer forma que você escolher. Clérigos de divindades associadas com uma arma particular (como São Cuthbert é conhecido por sua maça e Thor por seu martelo) fazem o efeito dessa magia se assemelhar àquela arma.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º nível ou superior, o dano aumenta em 1d8 para cada dois níveis do espaço acima do 2º.',
                classes=['Cleric'],
                ritual=False,
                concentration=False
            ),
            'Lesser Restoration': Spell(
                name='Lesser Restoration',
                level=2,
                school='Abjuration',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='Instantânea',
                description='Você toca uma criatura e pode acabar com uma doença ou uma condição que a esteja afligindo. A condição pode ser cegueira, surdez, paralisia ou envenenamento.',
                classes=['Cleric', 'Bard', 'Druid', 'Paladin', 'Ranger'],
                ritual=False,
                concentration=False
            ),
            'Cloud of Daggers': Spell(
                name='Cloud of Daggers',
                level=2,
                school='Conjuration',
                casting_time='1 ação',
                range='60 pés',
                components='V, S, M (um fragmento de vidro)',
                duration='Concentração, até 1 minuto',
                description='Você enche o ar com adagas giratórias em um cubo de 5 pés em um ponto que você escolher dentro do alcance. Uma criatura sofre 4d4 de dano cortante quando entra na área da magia pela primeira vez em um turno ou começa seu turno lá.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º nível ou superior, o dano aumenta em 2d4 para cada nível do espaço acima do 2º.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Crown of Madness': Spell(
                name='Crown of Madness',
                level=2,
                school='Enchantment',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='Um humanoide de sua escolha que você possa ver dentro do alcance deve ter sucesso em um teste de resistência de Sabedoria ou se tornar encantado por você pela duração. Enquanto o alvo está encantado dessa forma, uma coroa retorcida de ferro dentado aparece em sua cabeça, e uma loucura brilha em seus olhos.\n\nO alvo encantado deve usar sua ação antes de se mover em cada um de seus turnos para fazer um ataque corpo a corpo contra uma criatura diferente de si mesmo que você escolher mentalmente. O alvo pode agir normalmente em seu turno se você não escolher uma criatura ou se nenhuma estiver dentro de seu alcance.\n\nEm turnos subsequentes, você deve usar sua ação para manter o controle sobre o alvo, ou a magia acaba. Além disso, o alvo pode fazer um teste de resistência de Sabedoria no final de cada um de seus turnos. Em um sucesso, a magia acaba.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Darkness': Spell(
                name='Darkness',
                level=2,
                school='Evocation',
                casting_time='1 ação',
                range='60 pés',
                components='V, M (pelo de morcego e uma gota de piche ou um pedaço de carvão)',
                duration='Concentração, até 10 minutos',
                description='Escuridão mágica se espalha de um ponto que você escolher dentro do alcance para preencher uma esfera de 15 pés de raio pela duração. A escuridão se espalha em torno de cantos. Uma criatura com visão no escuro não pode ver através dessa escuridão, e luz não-mágica não pode iluminá-la.\n\nSe o ponto que você escolher estiver em um objeto que você está segurando ou um que não esteja sendo vestido ou carregado, a escuridão emana do objeto e se move com ele. Cobrir completamente a fonte da escuridão com um objeto opaco, como uma tigela ou um elmo, bloqueia a escuridão.\n\nSe qualquer área dessa magia se sobrepor a uma área de luz criada por uma magia de 2º nível ou inferior, a magia que criou a luz é dissipada.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Enthrall': Spell(
                name='Enthrall',
                level=2,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V, S',
                duration='1 minuto',
                description='Você tece uma teia distorcida de palavras, fazendo com que criaturas de sua escolha que você possa ver dentro do alcance e que possam ouvi-lo façam um teste de resistência de Sabedoria. Qualquer criatura que não possa ser encantada tem sucesso neste teste de resistência automaticamente, e se você ou seus companheiros estiverem lutando com uma criatura, ela tem vantagem no teste de resistência. Em uma falha no teste de resistência, o alvo tem desvantagem em testes de Sabedoria (Percepção) feitos para perceber qualquer criatura diferente de você até a magia acabar ou até o alvo não poder mais ouvi-lo. A magia acaba se você for incapacitado ou não puder mais falar.',
                classes=['Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Invisibility': Spell(
                name='Invisibility',
                level=2,
                school='Illusion',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (um cílio encapsulado em goma arábica)',
                duration='Concentração, até 1 hora',
                description='Uma criatura que você tocar se torna invisível até a magia acabar. Qualquer coisa que o alvo estiver vestindo ou carregando é invisível enquanto estiver na pessoa do alvo. A magia acaba para um alvo que ataca ou conjura uma magia.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º nível ou superior, você pode mirar em uma criatura adicional para cada nível do espaço acima do 2º.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Ray of Enfeeblement': Spell(
                name='Ray of Enfeeblement',
                level=2,
                school='Necromancy',
                casting_time='1 ação',
                range='60 pés',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='Um raio negro de energia enfraquecedora salta de seu dedo em direção a uma criatura dentro do alcance. Faça um ataque de magia à distância contra o alvo. Em um acerto, o alvo causa apenas metade do dano com ataques de arma que usam Força até a magia acabar.\n\nNo final de cada um dos turnos do alvo, ele pode fazer um teste de resistência de Constituição contra a magia. Em um sucesso, a magia acaba.',
                classes=['Wizard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Shatter': Spell(
                name='Shatter',
                level=2,
                school='Evocation',
                casting_time='1 ação',
                range='60 pés',
                components='V, S, M (um chip de mica)',
                duration='Instantânea',
                description='Um ruído dolorosamente intenso irrompe de um ponto de sua escolha dentro do alcance. Cada criatura em uma esfera de 10 pés de raio centrada nesse ponto deve fazer um teste de resistência de Constituição. Uma criatura sofre 3d8 de dano trovejante em uma falha no teste de resistência, ou metade do dano em um sucesso. Uma criatura feita de material inorgânico, como pedra, cristal ou metal, tem desvantagem neste teste de resistência.\n\nUm objeto não-mágico que não esteja sendo vestido ou carregado também sofre o dano se estiver na área da magia.\n\nEm Níveis Superiores: Quando você conjura essa magia usando um espaço de magia de 3º nível ou superior, o dano aumenta em 1d8 para cada nível do espaço acima do 2º.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Spider Climb': Spell(
                name='Spider Climb',
                level=2,
                school='Transmutation',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (uma gota de betume e uma aranha)',
                duration='Concentração, até 1 hora',
                description='Até a magia acabar, uma criatura voluntária que você tocar ganha a habilidade de se mover para cima, para baixo e ao longo de superfícies verticais e de cabeça para baixo ao longo de tetos, enquanto deixa suas mãos livres. O alvo também ganha uma velocidade de escalada igual à sua velocidade de caminhada.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Suggestion': Spell(
                name='Suggestion',
                level=2,
                school='Enchantment',
                casting_time='1 ação',
                range='30 pés',
                components='V, M (uma língua de cobra e um pedaço de favo de mel ou uma gota de óleo doce)',
                duration='Concentração, até 8 horas',
                description='Você sugere um curso de atividade (limitado a uma ou duas sentenças) e magicamente influencia uma criatura que você possa ver dentro do alcance e que possa ouvi-lo e entendê-lo. Criaturas que não podem ser encantadas são imunes a este efeito. A sugestão deve ser formulada de tal maneira que o curso de ação pareça razoável. Pedir à criatura para se esfaquear, se jogar em uma lança, se imolar ou fazer algum outro ato obviamente prejudicial acaba com a magia.\n\nO alvo deve fazer um teste de resistência de Sabedoria. Em uma falha, ele persegue o curso de ação que você descreveu da melhor forma que puder. O curso de ação sugerido pode continuar por toda a duração. Se a atividade sugerida puder ser completada em um tempo mais curto, a magia acaba quando o sujeito termina o que foi pedido para fazer.\n\nVocê também pode especificar condições que desencadearão uma atividade especial durante a duração. Por exemplo, você pode sugerir que um cavaleiro dê seu cavalo de guerra ao primeiro mendigo que encontrar. Se a condição não for atendida antes da magia expirar, a atividade não é realizada.\n\nSe você ou qualquer um de seus companheiros danificar o alvo, a magia acaba.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            
            # ========== NÍVEL 3 ==========
            'Counterspell': Spell(
                name='Counterspell',
                level=3,
                school='Abjuration',
                casting_time='1 reação',
                range='60 pés',
                components='S',
                duration='Instantânea',
                description='Você tenta interromper uma criatura no processo de conjurar uma magia. Se a criatura estiver conjurando uma magia de 3º nível ou inferior, sua magia falha e não tem efeito. Se estiver conjurando uma magia de 4º nível ou superior, faça um teste de habilidade usando sua habilidade de conjuração. A CD é igual a 10 + o nível da magia. Em um sucesso, a magia da criatura falha e não tem efeito.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Dispel Magic': Spell(
                name='Dispel Magic',
                level=3,
                school='Abjuration',
                casting_time='1 ação',
                range='120 pés',
                components='V, S',
                duration='Instantânea',
                description='Escolha uma criatura, objeto ou efeito mágico dentro do alcance. Qualquer magia de 3º nível ou inferior no alvo termina.',
                classes=['Wizard', 'Sorcerer', 'Cleric', 'Druid', 'Paladin', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Fear': Spell(
                name='Fear',
                level=3,
                school='Illusion',
                casting_time='1 ação',
                range='Pessoal (cone de 30 pés)',
                components='V, S, M (uma pena branca ou coração de galinha)',
                duration='Concentração, até 1 minuto',
                description='Você projeta uma imagem fantasmagórica dos piores medos de uma criatura. Cada criatura em um cone de 30 pés deve ter sucesso em um teste de resistência de Sabedoria ou largar o que estiver segurando e ficar amedrontada pela duração.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Fly': Spell(
                name='Fly',
                level=3,
                school='Transmutation',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (uma pena de asa de qualquer pássaro)',
                duration='Concentração, até 10 minutos',
                description='Você toca uma criatura voluntária. O alvo ganha uma velocidade de voo de 60 pés pela duração.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Gaseous Form': Spell(
                name='Gaseous Form',
                level=3,
                school='Transmutation',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (um pouco de gaze e uma mecha de fumaça)',
                duration='Concentração, até 1 hora',
                description='Você transforma uma criatura voluntária que você tocar, junto com tudo o que ela estiver vestindo e carregando, em uma nuvem enevoada pela duração.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Hunger of Hadar': Spell(
                name='Hunger of Hadar',
                level=3,
                school='Conjuration',
                casting_time='1 ação',
                range='150 pés',
                components='V, S, M (um tentáculo em conserva de um polvo gigante ou lula gigante)',
                duration='Concentração, até 1 minuto',
                description='Você abre um portal para o vazio escuro entre as estrelas. Uma esfera de escuridão de 20 pés de raio aparece, centrada em um ponto dentro do alcance. Qualquer criatura que comece seu turno na área sofre 2d6 de dano de frio. Qualquer criatura que termine seu turno na área deve ter sucesso em um teste de resistência de Destreza ou sofre 2d6 de dano ácido.',
                classes=['Warlock'],
                ritual=False,
                concentration=True
            ),
            'Hypnotic Pattern': Spell(
                name='Hypnotic Pattern',
                level=3,
                school='Illusion',
                casting_time='1 ação',
                range='120 pés',
                components='S, M (um bastão de incenso brilhante ou um frasco de cristal cheio de material fosforescente)',
                duration='Concentração, até 1 minuto',
                description='Você cria um padrão torcido de cores que tece através do ar. Cada criatura na área que vê o padrão deve fazer um teste de resistência de Sabedoria. Em uma falha, a criatura fica encantada pela duração e está incapacitada.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Magic Circle': Spell(
                name='Magic Circle',
                level=3,
                school='Abjuration',
                casting_time='1 minuto',
                range='10 pés',
                components='V, S, M (água benta ou pó de prata e ferro no valor de pelo menos 100 po)',
                duration='1 hora',
                description='Você cria um cilindro de energia mágica de 10 pés de raio e 20 pés de altura. Escolha celestiais, elementais, fadas, demoníacos ou mortos-vivos. O círculo impede que criaturas do tipo escolhido entrem.',
                classes=['Wizard', 'Cleric', 'Paladin', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Major Image': Spell(
                name='Major Image',
                level=3,
                school='Illusion',
                casting_time='1 ação',
                range='120 pés',
                components='V, S, M (um pouco de lã de carneiro)',
                duration='Concentração, até 10 minutos',
                description='Você cria a imagem de um objeto, uma criatura ou algum outro fenômeno visível que não seja maior que um cubo de 20 pés. A imagem parece completamente real, incluindo sons, cheiros e temperatura.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Remove Curse': Spell(
                name='Remove Curse',
                level=3,
                school='Abjuration',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='Instantânea',
                description='Ao seu toque, todas as maldições afetando uma criatura ou objeto terminam.',
                classes=['Wizard', 'Cleric', 'Paladin', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Tongues': Spell(
                name='Tongues',
                level=3,
                school='Divination',
                casting_time='1 ação',
                range='Toque',
                components='V, M (um pequeno modelo de argila de um zigurate)',
                duration='1 hora',
                description='Esta magia concede à criatura que você tocar a habilidade de compreender qualquer idioma falado que ouvir.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Cleric', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Vampiric Touch': Spell(
                name='Vampiric Touch',
                level=3,
                school='Necromancy',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='O toque de sua mão envolta em sombras pode sugar a força vital de outros. Faça um ataque de magia corpo a corpo. Em um acerto, o alvo sofre 3d6 de dano necrótico, e você recupera pontos de vida iguais a metade do dano causado.',
                classes=['Wizard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Aura of Vitality': Spell(
                name='Aura of Vitality',
                level=3,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal (raio de 30 pés)',
                components='V',
                duration='Concentração, até 1 minuto',
                description='Uma aura de energia curativa irradia de você em um raio de 30 pés. Enquanto a magia durar, você pode usar uma ação bônus em cada um dos seus turnos para fazer uma criatura (incluindo você) na aura recuperar 2d6 pontos de vida.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Blinding Smite': Spell(
                name='Blinding Smite',
                level=3,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar uma criatura com um ataque corpo a corpo com arma durante a duração, o ataque causa 3d8 de dano radiante extra e o alvo deve ter sucesso em um teste de resistência de Constituição ou ficará cego até a magia acabar. Em níveis superiores: o dano aumenta em 1d8 para cada nível do espaço acima do 3º.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Conjure Barrage': Spell(
                name='Conjure Barrage',
                level=3,
                school='Conjuration',
                casting_time='1 ação',
                range='Pessoal (cone de 60 pés)',
                components='V, S, M (uma arma de ataque à distância ou munição)',
                duration='Instantânea',
                description='Você arremessa no ar uma peça de munição ou uma arma que usa munição e cria uma chuva de duplicatas mágicas. Cada criatura em um cone de 60 pés deve fazer um teste de resistência de Destreza. Uma criatura sofre 3d8 de dano do mesmo tipo da munição ou arma usada em uma falha, ou metade desse dano em um sucesso.',
                classes=['Ranger'],
                ritual=False,
                concentration=False
            ),
            'Crusader\'s Mantle': Spell(
                name='Crusader\'s Mantle',
                level=3,
                school='Evocation',
                casting_time='1 ação',
                range='Pessoal (raio de 30 pés)',
                components='V',
                duration='Concentração, até 1 minuto',
                description='Luz santificada emana de você em um raio de 30 pés. Até a magia acabar, criaturas amigáveis (incluindo você) na aura que causem dano com ataques com arma causam 1d4 de dano radiante extra.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Elemental Weapon': Spell(
                name='Elemental Weapon',
                level=3,
                school='Transmutation',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='Concentração, até 1 hora',
                description='Você toca uma arma e a imbui com poder elementar. Escolha ácido, frio, fogo, relâmpago ou trovejante. Até a magia acabar, a arma recebe +1 em jogadas de ataque e causa 1d4 de dano adicional do tipo escolhido. Em níveis superiores: o bônus de ataque aumenta para +2 e o dano adicional para 2d4 quando você usa um espaço de 5º nível, e para +3 e 3d4 quando usa um espaço de 7º nível ou superior.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Feign Death': Spell(
                name='Feign Death',
                level=3,
                school='Necromancy',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (uma pitada de terra de cemitério e uma gota de sangue)',
                duration='1 hora',
                description='Você toca uma criatura voluntária e coloca-a em estado catatônico que imita a morte. Enquanto a magia durar, o alvo tem resistência a todo dano exceto psíquico, é imune a venenos e doenças e aparece morto para inspeções mágicas ou mundanas. Pode ser conjurada como ritual.',
                classes=['Bard', 'Cleric', 'Druid', 'Wizard'],
                ritual=True,
                concentration=False
            ),
            'Lightning Arrow': Spell(
                name='Lightning Arrow',
                level=3,
                school='Transmutation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você fizer um ataque com arma à distância durante a duração, a munição se transforma em relâmpago. O alvo sofre 4d8 de dano elétrico em um acerto, ou metade em um erro. Criaturas a até 10 pés do alvo devem fazer um teste de resistência de Destreza, sofrendo 2d8 de dano elétrico em falha ou metade em sucesso. Em níveis superiores: ambos os danos aumentam em 1d8 para cada nível do espaço acima do 3º.',
                classes=['Ranger'],
                ritual=False,
                concentration=True
            ),
            'Meld Into Stone': Spell(
                name='Meld Into Stone',
                level=3,
                school='Transmutation',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (um pouco de pedra)',
                duration='8 horas',
                description='Você entra em uma superfície de pedra sólida grande o suficiente para conter seu corpo, mesclando-se com ela. Enquanto estiver mesclado, você permanece consciente, mas não pode ver fora da pedra. Quando a magia termina, você reaparece no espaço que ocupava ou no mais próximo. Se a pedra for destruída, você é expulso sofrendo 6d6 de dano de concussão. Pode ser conjurada como ritual.',
                classes=['Cleric', 'Druid'],
                ritual=True,
                concentration=False
            ),
            
            # ========== NÍVEL 4 ==========
            'Banishment': Spell(
                name='Banishment',
                level=4,
                school='Abjuration',
                casting_time='1 ação',
                range='60 pés',
                components='V, S, M (um item desagradável ao alvo)',
                duration='Concentração, até 1 minuto',
                description='Você tenta enviar uma criatura que você possa ver dentro do alcance para outro plano de existência. O alvo deve ter sucesso em um teste de resistência de Carisma ou ser banido.',
                classes=['Wizard', 'Sorcerer', 'Cleric', 'Paladin', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Dimension Door': Spell(
                name='Dimension Door',
                level=4,
                school='Conjuration',
                casting_time='1 ação',
                range='500 pés',
                components='V',
                duration='Instantânea',
                description='Você se teletransporta de sua localização atual para qualquer outro local dentro do alcance.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Hallucinatory Terrain': Spell(
                name='Hallucinatory Terrain',
                level=4,
                school='Illusion',
                casting_time='10 minutos',
                range='300 pés',
                components='V, S, M (uma pedra, um galho e um pouco de planta verde)',
                duration='24 horas',
                description='Você faz o terreno natural em um cubo de 150 pés parecer, soar e cheirar como algum outro tipo de terreno natural.',
                classes=['Wizard', 'Bard', 'Druid', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Aura of Life': Spell(
                name='Aura of Life',
                level=4,
                school='Abjuration',
                casting_time='1 ação',
                range='Pessoal (raio de 30 pés)',
                components='V',
                duration='Concentração, até 10 minutos',
                description='Energia positiva irradia de você em um raio de 30 pés. Criaturas amigáveis na aura ganham resistência a dano necrótico e sua quantidade máxima de pontos de vida não pode ser reduzida. Além disso, criaturas na aura que estejam com 0 pontos de vida recuperam 1 ponto de vida no início do turno.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Aura of Purity': Spell(
                name='Aura of Purity',
                level=4,
                school='Abjuration',
                casting_time='1 ação',
                range='Pessoal (raio de 30 pés)',
                components='V',
                duration='Concentração, até 10 minutos',
                description='Uma aura purificadora surge em um raio de 30 pés a partir de você. Criaturas amigáveis na aura têm vantagem em testes de resistência contra cansaço, envenenamento, doenças, encantamento, medo, paralisia e petrificação, e também ganham resistência a dano de veneno.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Divination': Spell(
                name='Divination',
                level=4,
                school='Divination',
                casting_time='10 minutos',
                range='Pessoal',
                components='V, S, M (incenso e oferendas no valor de 25 po)',
                duration='Instantânea',
                description='Seu contato com seu deus ou um emissário divino concede uma resposta verdadeira a uma pergunta sobre um objetivo, evento ou atividade que ocorrerá dentro de 7 dias. Pode ser conjurada como ritual.',
                classes=['Cleric'],
                ritual=True,
                concentration=False
            ),
            'Grasping Vine': Spell(
                name='Grasping Vine',
                level=4,
                school='Conjuration',
                casting_time='1 ação bônus',
                range='30 pés',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='Você conjura uma videira que brota de uma superfície sólida dentro do alcance. Em cada um dos seus turnos, você pode usar uma ação bônus para fazer a videira puxar uma criatura que você possa ver a até 30 pés, movendo-a até 20 pés em direção à videira em um teste de resistência de Destreza mal sucedido.',
                classes=['Druid', 'Ranger'],
                ritual=False,
                concentration=True
            ),
            'Staggering Smite': Spell(
                name='Staggering Smite',
                level=4,
                school='Evocation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Concentração, até 1 minuto',
                description='A próxima vez que você acertar uma criatura com um ataque corpo a corpo com arma durante a duração, o ataque causa 4d6 de dano psíquico extra e o alvo deve ter sucesso em um teste de resistência de Sabedoria ou terá desvantagem em jogadas de ataque e testes de habilidade, e não poderá se mover mais de 10 pés até o fim do próximo turno.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            
            # ========== NÍVEL 5 ==========
            'Contact Other Plane': Spell(
                name='Contact Other Plane',
                level=5,
                school='Divination',
                casting_time='1 minuto',
                range='Pessoal',
                components='V',
                duration='1 minuto',
                description='Você mentalmente contata um semideus, o espírito de um sábio há muito morto, ou alguma outra entidade misteriosa de outro plano.',
                classes=['Wizard', 'Warlock'],
                ritual=True,
                concentration=False
            ),
            'Dream': Spell(
                name='Dream',
                level=5,
                school='Illusion',
                casting_time='1 minuto',
                range='Especial',
                components='V, S, M (um punhado de areia, uma gota de tinta e uma pena de pena arrancada de um pássaro adormecido)',
                duration='8 horas',
                description='Esta magia molda os sonhos de uma criatura. Você pode fazer a criatura ter um sonho agradável ou um pesadelo.',
                classes=['Wizard', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Hold Monster': Spell(
                name='Hold Monster',
                level=5,
                school='Enchantment',
                casting_time='1 ação',
                range='90 pés',
                components='V, S, M (um pequeno pedaço de ferro reto)',
                duration='Concentração, até 1 minuto',
                description='Escolha uma criatura que você possa ver dentro do alcance. O alvo deve ter sucesso em um teste de resistência de Sabedoria ou ficará paralisado pela duração.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Scrying': Spell(
                name='Scrying',
                level=5,
                school='Divination',
                casting_time='10 minutos',
                range='Pessoal',
                components='V, S, M (um foco no valor de pelo menos 1.000 po)',
                duration='Concentração, até 10 minutos',
                description='Você pode ver e ouvir uma criatura particular que você escolher que esteja no mesmo plano de existência que você.',
                classes=['Wizard', 'Cleric', 'Druid', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Circle of Power': Spell(
                name='Circle of Power',
                level=5,
                school='Abjuration',
                casting_time='1 ação',
                range='Pessoal (raio de 30 pés)',
                components='V',
                duration='Concentração, até 10 minutos',
                description='Uma aura de proteção se estende de você em um raio de 30 pés. Criaturas amigáveis na aura têm vantagem em testes de resistência contra magias e outros efeitos mágicos. Além disso, quando uma criatura afetada passa em um teste de resistência contra um efeito que normalmente causaria metade do dano em um sucesso, ela não sofre dano algum.',
                classes=['Paladin'],
                ritual=False,
                concentration=True
            ),
            'Conjure Volley': Spell(
                name='Conjure Volley',
                level=5,
                school='Conjuration',
                casting_time='1 ação',
                range='150 pés (cilindro de 40 pés de raio por 20 pés de altura)',
                components='V, S, M (uma peça de munição ou arma de arremesso)',
                duration='Instantânea',
                description='Você arremessa uma peça de munição ou arma no ar e cria uma chuva de cópias mágicas. Cada criatura em um cilindro de 40 pés de raio por 20 pés de altura deve fazer um teste de resistência de Destreza. Uma criatura sofre 8d8 de dano do mesmo tipo da munição usada em uma falha, ou metade em um sucesso.',
                classes=['Ranger'],
                ritual=False,
                concentration=False
            ),
            'Destructive Wave': Spell(
                name='Destructive Wave',
                level=5,
                school='Evocation',
                casting_time='1 ação',
                range='Pessoal (raio de 30 pés)',
                components='V',
                duration='Instantânea',
                description='Você bate o chão e libera uma onda de energia divina. Cada criatura que você escolher em um raio de 30 pés deve fazer um teste de resistência de Constituição. Em uma falha, a criatura sofre 5d6 de dano trovejante e 5d6 de dano radiante ou necrótico (à sua escolha) e fica derrubada. Em um sucesso, sofre metade do dano e não cai.',
                classes=['Paladin'],
                ritual=False,
                concentration=False
            ),
            'Swift Quiver': Spell(
                name='Swift Quiver',
                level=5,
                school='Transmutation',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V, S, M (uma aljava contendo pelo menos uma flecha)',
                duration='Concentração, até 1 minuto',
                description='Você transforma uma aljava, concedendo velocidade sobrenatural aos seus disparos. Até a magia acabar, você pode usar uma ação bônus em cada turno para realizar dois ataques adicionais com arma à distância usando a munição que parece surgir na aljava. A munição conjurada desaparece após atingir ou errar.',
                classes=['Ranger'],
                ritual=False,
                concentration=True
            ),

            # ========== NÍVEL 6 ==========
            'Arcane Gate': Spell(
                name='Arcane Gate',
                level=6,
                school='Conjuration',
                casting_time='1 ação',
                range='500 pés',
                components='V, S',
                duration='Concentração, até 10 minutos',
                description='Você cria portais de teletransporte ligados que permanecem abertos pela duração.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Circle of Death': Spell(
                name='Circle of Death',
                level=6,
                school='Necromancy',
                casting_time='1 ação',
                range='150 pés',
                components='V, S, M (o pó de uma pérola negra esmagada no valor de pelo menos 500 po)',
                duration='Instantânea',
                description='Uma esfera de energia negativa ondula em uma esfera de 60 pés de raio. Cada criatura nessa área deve fazer um teste de resistência de Constituição. Um alvo sofre 8d6 de dano necrótico em uma falha, ou metade do dano em um sucesso.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Conjure Fey': Spell(
                name='Conjure Fey',
                level=6,
                school='Conjuration',
                casting_time='1 minuto',
                range='90 pés',
                components='V, S',
                duration='Concentração, até 1 hora',
                description='Você invoca uma criatura feérica de nível de desafio 6 ou inferior.',
                classes=['Druid', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Create Undead': Spell(
                name='Create Undead',
                level=6,
                school='Necromancy',
                casting_time='1 minuto',
                range='10 pés',
                components='V, S, M (um pote de argila cheio de terra de cemitério, um pote de argila cheio de água salobra e uma ônix negra no valor de 150 po por cadáver)',
                duration='Instantânea',
                description='Você pode conjurar essa magia apenas à noite. Escolha até três cadáveres de humanoides Médios ou Pequenos dentro do alcance. Cada cadáver se torna um carniçal sob seu controle.',
                classes=['Wizard', 'Cleric', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Eyebite': Spell(
                name='Eyebite',
                level=6,
                school='Necromancy',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='Concentração, até 1 minuto',
                description='Pela duração da magia, seus olhos se tornam poços vazios imbuídos de poder terrível. Uma criatura de sua escolha a 60 pés de você que você possa ver deve ter sucesso em um teste de resistência de Sabedoria ou ser afetada por um dos seguintes efeitos de sua escolha pela duração.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Mass Suggestion': Spell(
                name='Mass Suggestion',
                level=6,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V, M (uma língua de cobra e um favo de mel ou uma gota de óleo doce)',
                duration='24 horas',
                description='Você sugere um curso de atividade e magicamente influencia até doze criaturas de sua escolha que você possa ver dentro do alcance.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'True Seeing': Spell(
                name='True Seeing',
                level=6,
                school='Divination',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (um unguento para os olhos que custa 25 po)',
                duration='1 hora',
                description='Esta magia dá à criatura voluntária que você tocar a habilidade de ver as coisas como elas realmente são.',
                classes=['Wizard', 'Sorcerer', 'Cleric', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            
            # ========== NÍVEL 7 ==========
            'Etherealness': Spell(
                name='Etherealness',
                level=7,
                school='Transmutation',
                casting_time='1 ação',
                range='Pessoal',
                components='V, S',
                duration='Até 8 horas',
                description='Você entra na região fronteiriça do Plano Etéreo.',
                classes=['Wizard', 'Cleric', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Finger of Death': Spell(
                name='Finger of Death',
                level=7,
                school='Necromancy',
                casting_time='1 ação',
                range='60 pés',
                components='V, S',
                duration='Instantânea',
                description='Você envia energia negativa através de uma criatura que você possa ver dentro do alcance, causando dor lancinante. O alvo deve fazer um teste de resistência de Constituição. Ele sofre 7d8 + 30 de dano necrótico em uma falha, ou metade do dano em um sucesso.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Forcecage': Spell(
                name='Forcecage',
                level=7,
                school='Evocation',
                casting_time='1 ação',
                range='100 pés',
                components='V, S, M (pó de rubi no valor de 1.500 po)',
                duration='1 hora',
                description='Uma prisão imóvel e invisível de força mágica surge ao redor de uma área que você escolher dentro do alcance.',
                classes=['Wizard', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Plane Shift': Spell(
                name='Plane Shift',
                level=7,
                school='Conjuration',
                casting_time='1 ação',
                range='Toque',
                components='V, S, M (um garfo de metal sintonizado com o plano de destino)',
                duration='Instantânea',
                description='Você e até oito criaturas voluntárias que se ligam às mãos em um círculo são transportados para um plano diferente de existência.',
                classes=['Wizard', 'Sorcerer', 'Cleric', 'Druid', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            
            # ========== NÍVEL 8 ==========
            'Demiplane': Spell(
                name='Demiplane',
                level=8,
                school='Conjuration',
                casting_time='1 ação',
                range='60 pés',
                components='S',
                duration='1 hora',
                description='Você cria uma porta sombreada em uma superfície plana sólida que você possa ver dentro do alcance. A porta é grande o suficiente para permitir que criaturas Médias passem através dela sem apertar.',
                classes=['Wizard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Dominate Monster': Spell(
                name='Dominate Monster',
                level=8,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V, S',
                duration='Concentração, até 1 hora',
                description='Você tenta seduzir uma criatura que você possa ver dentro do alcance. Ela deve ter sucesso em um teste de resistência de Sabedoria ou ser encantada por você pela duração.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
            'Feeblemind': Spell(
                name='Feeblemind',
                level=8,
                school='Enchantment',
                casting_time='1 ação',
                range='150 pés',
                components='V, S, M (um punhado de esferas de argila, cristal, vidro ou mineral)',
                duration='Instantânea',
                description='Você destrói o intelecto e a personalidade de uma criatura, deixando-a como um vegetal sem mente.',
                classes=['Wizard', 'Druid', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Glibness': Spell(
                name='Glibness',
                level=8,
                school='Transmutation',
                casting_time='1 ação',
                range='Pessoal',
                components='V',
                duration='1 hora',
                description='Até a magia acabar, quando você fizer um teste de Carisma, você pode substituir o número que você rolou por um 15.',
                classes=['Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Power Word Stun': Spell(
                name='Power Word Stun',
                level=8,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V',
                duration='Instantânea',
                description='Você fala uma palavra de poder que pode dominar a mente de uma criatura que você possa ver dentro do alcance, deixando-a atordoada.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Animal Shapes': Spell(
                name='Animal Shapes',
                level=8,
                school='Transmutation',
                casting_time='1 ação',
                range='30 pés',
                components='V, S',
                duration='Concentração, até 24 horas',
                description='Você transforma criaturas voluntárias que você possa ver dentro do alcance em bestas com ND 4 ou inferior. Cada criatura assume uma nova forma enquanto a magia durar ou até você usar uma ação bônus para mudá-la novamente.',
                classes=['Druid'],
                ritual=False,
                concentration=True
            ),
            'Mind Blank': Spell(
                name='Mind Blank',
                level=8,
                school='Abjuration',
                casting_time='1 ação',
                range='Toque',
                components='V, S',
                duration='24 horas',
                description='Você envolve uma criatura voluntária em proteção mental. O alvo é imune a dano psíquico, a efeitos que leem emoções ou pensamentos, encantamento e adivinhações que detectam seu paradeiro por toda a duração.',
                classes=['Bard', 'Wizard'],
                ritual=False,
                concentration=False
            ),
            
            # ========== NÍVEL 9 ==========
            'Astral Projection': Spell(
                name='Astral Projection',
                level=9,
                school='Necromancy',
                casting_time='1 hora',
                range='10 pés',
                components='V, S, M (para cada criatura afetada, um jacinto no valor de pelo menos 1.000 po e uma barra de prata ornamentada no valor de pelo menos 100 po)',
                duration='Especial',
                description='Você e até oito criaturas voluntárias dentro do alcance projetam seus corpos astrais no Plano Astral.',
                classes=['Wizard', 'Cleric', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Foresight': Spell(
                name='Foresight',
                level=9,
                school='Divination',
                casting_time='1 minuto',
                range='Toque',
                components='V, S, M (uma pena de colibri)',
                duration='8 horas',
                description='Você toca uma criatura voluntária e concede a ela uma habilidade limitada de ver o futuro imediato.',
                classes=['Wizard', 'Druid', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Imprisonment': Spell(
                name='Imprisonment',
                level=9,
                school='Abjuration',
                casting_time='1 minuto',
                range='30 pés',
                components='V, S, M (um componente específico dependendo da forma de prisão escolhida)',
                duration='Até ser dissipada',
                description='Você cria uma restrição mágica para prender uma criatura que você possa ver dentro do alcance.',
                classes=['Wizard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'Power Word Heal': Spell(
                name='Power Word Heal',
                level=9,
                school='Evocation',
                casting_time='1 ação',
                range='Toque',
                components='V',
                duration='Instantânea',
                description='Você pronuncia uma palavra de poder que inunda uma criatura com energia restauradora. O alvo recupera todos os pontos de vida, termina cego, surdo e todas as condições que o deixem incapacitado e pode usar sua reação para se levantar imediatamente.',
                classes=['Bard', 'Cleric'],
                ritual=False,
                concentration=False
            ),
            'Power Word Kill': Spell(
                name='Power Word Kill',
                level=9,
                school='Enchantment',
                casting_time='1 ação',
                range='60 pés',
                components='V',
                duration='Instantânea',
                description='Você profere uma palavra de poder que pode obrigar uma criatura que você possa ver dentro do alcance a morrer instantaneamente. Se a criatura que você escolher tiver 100 pontos de vida ou menos, ela morre.',
                classes=['Wizard', 'Sorcerer', 'Bard', 'Warlock'],
                ritual=False,
                concentration=False
            ),
            'True Polymorph': Spell(
                name='True Polymorph',
                level=9,
                school='Transmutation',
                casting_time='1 ação',
                range='30 pés',
                components='V, S, M (uma gota de mercúrio, uma goma arábica e fumaça)',
                duration='Concentração, até 1 hora',
                description='Escolha uma criatura ou objeto não-mágico que você possa ver dentro do alcance. Você transforma a criatura em uma criatura diferente, a criatura em um objeto, ou o objeto em uma criatura.',
                classes=['Wizard', 'Bard', 'Warlock'],
                ritual=False,
                concentration=True
            ),
        }
    
    @staticmethod
    def get_all_spells() -> Dict[str, Spell]:
        """
        Retorna todas as magias disponíveis.
        Tenta carregar do cache JSON primeiro, usa magias manuais como fallback.
        """
        # Usa cache em memória se já carregado
        if SpellDatabase._cache is not None:
            return SpellDatabase._cache
        
        # Tenta carregar do arquivo JSON
        cached_spells = SpellDatabase._load_from_cache()
        if cached_spells:
            print(f"✅ {len(cached_spells)} magias carregadas do cache local (data/spells_cache.json)")
            SpellDatabase._cache = cached_spells
            return cached_spells
        
        # Fallback para magias manuais
        print("⚠️ Cache não encontrado, usando magias manuais")
        manual_spells = SpellDatabase._get_manual_spells()
        SpellDatabase._cache = manual_spells
        return manual_spells
    
    @staticmethod
    def reload_cache():
        """Recarrega o cache de magias (útil após atualizar da API)"""
        SpellDatabase._cache = None
        return SpellDatabase.get_all_spells()
    
    @staticmethod
    def get_spell(spell_name: str) -> Optional[Spell]:
        """Retorna uma magia específica pelo nome"""
        spells = SpellDatabase.get_all_spells()
        return spells.get(spell_name)
    
    @staticmethod
    def get_spells_by_class(class_name: str) -> Dict[str, Spell]:
        """Retorna todas as magias disponíveis para uma classe"""
        all_spells = SpellDatabase.get_all_spells()
        return {name: spell for name, spell in all_spells.items() 
                if class_name in spell.classes}
    
    @staticmethod
    def get_spells_by_level(level: int, class_name: Optional[str] = None) -> Dict[str, Spell]:
        """Retorna magias de um nível específico, opcionalmente filtradas por classe"""
        all_spells = SpellDatabase.get_all_spells()
        spells = {name: spell for name, spell in all_spells.items() if spell.level == level}
        
        if class_name:
            spells = {name: spell for name, spell in spells.items() if class_name in spell.classes}
        
        return spells
