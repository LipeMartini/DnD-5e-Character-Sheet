"""
Script de teste para verificar a estrutura da API
"""

import requests
import json

API_BASE_URL = "https://www.dnd5eapi.co/api"

def test_api():
    """Testa a API e mostra a estrutura de uma magia"""
    print("🔍 Testando API D&D 5e...")
    
    try:
        # Busca lista de magias
        response = requests.get(f"{API_BASE_URL}/spells")
        response.raise_for_status()
        spell_list = response.json()
        
        print(f"✅ API acessível! Total de magias: {spell_list['count']}")
        
        # Pega a primeira magia como exemplo
        first_spell = spell_list['results'][0]
        print(f"\n📜 Testando com: {first_spell['name']}")
        
        # Busca detalhes
        spell_url = f"https://www.dnd5eapi.co{first_spell['url']}"
        spell_response = requests.get(spell_url)
        spell_response.raise_for_status()
        spell_data = spell_response.json()
        
        print("\n📋 Estrutura da magia:")
        print(json.dumps(spell_data, indent=2))
        
        return spell_data
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_api()
