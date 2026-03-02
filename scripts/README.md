# 📜 Scripts de Utilidade

## Baixar Magias da API D&D 5e

### Como usar:

1. **Instale a biblioteca requests** (se ainda não tiver):
```bash
pip install requests
```

2. **Execute o script**:
```bash
python scripts/fetch_spells_from_api.py
```

3. **O que acontece**:
   - O script baixa todas as magias do SRD da API oficial D&D 5e
   - Converte para o formato usado pelo aplicativo
   - Salva em `data/spells_cache.json`
   - Aproximadamente **300+ magias** serão baixadas

4. **Resultado**:
   - ✅ Magias disponíveis offline
   - ✅ Carregamento rápido (cache local)
   - ✅ Descrições oficiais do SRD
   - ✅ Todas as magias de níveis 0-9

### Notas:
- **Requer conexão com internet** apenas na primeira execução
- O arquivo de cache é carregado automaticamente pelo aplicativo
- Se o cache não existir, o app usa magias manuais como fallback
- Execute novamente para atualizar as magias da API

### Estrutura do Cache:
```json
{
  "Fire Bolt": {
    "name": "Fire Bolt",
    "level": 0,
    "school": "Evocation",
    "casting_time": "1 action",
    "range": "120 feet",
    "components": "V, S",
    "duration": "Instantaneous",
    "description": "...",
    "classes": ["Wizard", "Sorcerer"],
    "ritual": false,
    "concentration": false
  }
}
```
