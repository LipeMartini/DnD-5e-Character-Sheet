"""
Script para baixar magias da D&D 5e API e salvar localmente em JSON.
Executa uma vez para popular o banco de dados de magias.
"""

import requests
import json
import os
from pathlib import Path

API_BASE_URL = "https://www.dnd5eapi.co/api"

def fetch_all_spells():
    """Baixa todas as magias da API"""
    print("🔮 Buscando lista de magias da API...")
    
    try:
        # Busca lista de todas as magias
        response = requests.get(f"{API_BASE_URL}/spells")
        response.raise_for_status()
        spell_list = response.json()
        
        print(f"✅ Encontradas {spell_list['count']} magias!")
        
        spells = []
        total = len(spell_list['results'])
        
        # Busca detalhes de cada magia
        for i, spell_ref in enumerate(spell_list['results'], 1):
            # A URL já vem completa da API, só precisa adicionar o domínio base
            spell_url = f"https://www.dnd5eapi.co{spell_ref['url']}"
            print(f"📥 Baixando {i}/{total}: {spell_ref['name']}...", end='\r')
            
            try:
                spell_response = requests.get(spell_url)
                spell_response.raise_for_status()
                spell_data = spell_response.json()
                spells.append(spell_data)
            except Exception as e:
                print(f"\n⚠️  Erro ao baixar {spell_ref['name']}: {e}")
                continue
        
        print(f"\n✅ Download completo! {len(spells)} magias baixadas.")
        return spells
        
    except Exception as e:
        print(f"❌ Erro ao acessar API: {e}")
        return []

def convert_spell_to_our_format(api_spell):
    """Converte formato da API para nosso formato"""
    
    try:
        # Extrai classes que podem usar a magia
        classes = []
        if api_spell.get('classes'):
            classes = [c.get('name', '') for c in api_spell['classes'] if isinstance(c, dict)]
        
        # Monta componentes (V, S, M)
        components_list = []
        if api_spell.get('components'):
            if 'V' in api_spell['components']:
                components_list.append('V')
            if 'S' in api_spell['components']:
                components_list.append('S')
            if 'M' in api_spell['components']:
                material = api_spell.get('material', 'material component')
                components_list.append(f'M ({material})')
        components = ', '.join(components_list) if components_list else 'None'
        
        # Monta descrição completa
        description_parts = api_spell.get('desc', [])
        if isinstance(description_parts, list):
            description = '\n\n'.join(description_parts)
        else:
            description = str(description_parts)
        
        # Adiciona descrição de níveis superiores se existir
        if api_spell.get('higher_level'):
            higher_level_parts = api_spell['higher_level']
            if isinstance(higher_level_parts, list):
                higher_level = '\n\n'.join(higher_level_parts)
            else:
                higher_level = str(higher_level_parts)
            description += f"\n\nEm Níveis Superiores: {higher_level}"
        
        # Verifica se é ritual ou concentração
        ritual = api_spell.get('ritual', False)
        concentration = api_spell.get('concentration', False)
        
        # Extrai escola de magia
        school = 'Evocation'  # Default
        if api_spell.get('school'):
            if isinstance(api_spell['school'], dict):
                school = api_spell['school'].get('name', 'Evocation')
            else:
                school = str(api_spell['school'])
        
        return {
            'name': api_spell.get('name', 'Unknown Spell'),
            'level': api_spell.get('level', 0),
            'school': school,
            'casting_time': api_spell.get('casting_time', '1 action'),
            'range': api_spell.get('range', 'Self'),
            'components': components,
            'duration': api_spell.get('duration', 'Instantaneous'),
            'description': description,
            'classes': classes,
            'ritual': ritual,
            'concentration': concentration,
        }
    except Exception as e:
        # Se houver erro, retorna dados mínimos válidos
        return {
            'name': api_spell.get('name', 'Unknown Spell'),
            'level': api_spell.get('level', 0),
            'school': 'Evocation',
            'casting_time': '1 action',
            'range': 'Self',
            'components': 'V, S',
            'duration': 'Instantaneous',
            'description': f"Error converting spell data: {str(e)}",
            'classes': [],
            'ritual': False,
            'concentration': False,
        }

def save_spells_to_json(spells, filepath):
    """Salva magias em arquivo JSON"""
    print(f"\n💾 Salvando magias em {filepath}...")
    
    # Converte para nosso formato
    converted_spells = {}
    errors = 0
    
    for i, spell in enumerate(spells, 1):
        try:
            spell_name = spell.get('name', f'Unknown_{i}')
            converted = convert_spell_to_our_format(spell)
            converted_spells[spell_name] = converted
            
            # Mostra progresso a cada 50 magias
            if i % 50 == 0:
                print(f"  Processadas {i}/{len(spells)} magias...")
                
        except Exception as e:
            errors += 1
            spell_name = spell.get('name', 'unknown')
            print(f"⚠️  Erro ao converter {spell_name}: {e}")
            continue
    
    if errors > 0:
        print(f"⚠️  {errors} magias tiveram erros na conversão")
    
    # Cria diretório se não existir
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
    except Exception as e:
        print(f"❌ Erro ao criar diretório: {e}")
        return
    
    # Salva em JSON
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(converted_spells, f, indent=2, ensure_ascii=False)
        print(f"✅ {len(converted_spells)} magias salvas com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao salvar arquivo: {e}")

def main():
    """Função principal"""
    print("=" * 60)
    print("🎲 D&D 5e Spell Fetcher")
    print("=" * 60)
    
    # Define caminho do arquivo de cache
    project_root = Path(__file__).parent.parent
    cache_file = project_root / "data" / "spells_cache.json"
    
    # Baixa magias da API
    spells = fetch_all_spells()
    
    if not spells:
        print("❌ Nenhuma magia foi baixada. Verifique sua conexão com a internet.")
        return
    
    # Salva em JSON
    save_spells_to_json(spells, str(cache_file))
    
    print("\n" + "=" * 60)
    print("✨ Processo concluído!")
    print(f"📁 Arquivo salvo em: {cache_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
