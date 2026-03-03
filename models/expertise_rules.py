from __future__ import annotations

"""Regras utilitárias relacionadas a ganhos de Expertise"""

from typing import Dict

# Mapa Classe -> {nível: quantidade de perícias para Expertise}
_EXPERTISE_TABLE: Dict[str, Dict[int, int]] = {
    "Rogue": {
        1: 2,
        6: 2,
    },
    "Bard": {
        3: 2,
        10: 2,
    },
}


def get_expertise_choices_for_level(class_name: str, level: int) -> int:
    """Retorna quantas perícias devem ganhar Expertise para a classe/nível."""
    return _EXPERTISE_TABLE.get(class_name, {}).get(level, 0)
