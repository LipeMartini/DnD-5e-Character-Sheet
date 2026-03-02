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
            'Misty Step': Spell(
                name='Misty Step',
                level=2,
                school='Conjuration',
                casting_time='1 ação bônus',
                range='Pessoal',
                components='V',
                duration='Instantânea',
                description='Brevemente envolto em névoa prateada, você se teletransporta até 30 pés para um espaço desocupado que você possa ver.',
                classes=['Wizard', 'Sorcerer', 'Warlock'],
                ritual=False,
                concentration=False
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
