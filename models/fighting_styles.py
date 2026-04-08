"""Sistema de Fighting Styles para D&D 5e."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .app_settings import AppSettings


@dataclass
class FightingStyle:
    """Representa um estilo de luta."""

    name: str
    description: str
    classes: List[str]  # Classes que podem escolher este estilo
    source: str = "Player's Handbook"

    def __str__(self):
        return self.name


# ========== FIGHTING STYLES ==========

ARCHERY = FightingStyle(
    name='Archery',
    description='Você ganha +2 de bônus nas jogadas de ataque que fizer com armas de ataque à distância.',
    classes=['Fighter', 'Ranger']
)

DEFENSE = FightingStyle(
    name='Defense',
    description='Enquanto estiver usando armadura, você ganha +1 de bônus na CA.',
    classes=['Fighter', 'Ranger', 'Paladin']
)

DUELING = FightingStyle(
    name='Dueling',
    description='Quando você empunhar uma arma de ataque corpo a corpo em uma mão e nenhuma outra arma, você ganha +2 de bônus nas jogadas de dano com essa arma.',
    classes=['Fighter', 'Ranger', 'Paladin']
)

GREAT_WEAPON_FIGHTING = FightingStyle(
    name='Great Weapon Fighting',
    description='Quando você rolar 1 ou 2 num dado de dano de um ataque com arma corpo a corpo que você esteja empunhando com duas mãos, você pode rolar o dado novamente e usar a nova rolagem. A arma deve ter a propriedade duas mãos ou versátil para ganhar esse benefício.',
    classes=['Fighter', 'Paladin']
)

PROTECTION = FightingStyle(
    name='Protection',
    description='Quando uma criatura que você possa ver atacar um alvo que esteja a até 1,5 metro de você, você pode usar sua reação para impor desvantagem na jogada de ataque da criatura. Você deve estar empunhando um escudo.',
    classes=['Fighter', 'Paladin']
)

TWO_WEAPON_FIGHTING = FightingStyle(
    name='Two-Weapon Fighting',
    description='Quando você estiver engajado em uma luta com duas armas, você pode adicionar o seu modificador de habilidade de dano na jogada de dano de seu segundo ataque.',
    classes=['Fighter', 'Ranger']
)


# Estilos básicos do PHB
BASE_FIGHTING_STYLES: Dict[str, FightingStyle] = {
    'Archery': ARCHERY,
    'Defense': DEFENSE,
    'Dueling': DUELING,
    'Great Weapon Fighting': GREAT_WEAPON_FIGHTING,
    'Protection': PROTECTION,
    'Two-Weapon Fighting': TWO_WEAPON_FIGHTING,
}

OPTIONAL_STYLE_FILES = {
    "tashas_spells": ("fighting_styles_tcoe.json", "Tasha's Cauldron of Everything"),
    "xanathars_spells": ("fighting_styles_xgte.json", "Xanathar's Guide to Everything"),
}

_STYLE_CACHE: Optional[Dict[str, FightingStyle]] = None


def _data_dir() -> Path:
    return Path(__file__).parent.parent / "data"


def _load_styles_from_file(filename: str) -> Dict[str, FightingStyle]:
    file_path = _data_dir() / filename
    if not file_path.exists():
        return {}

    try:
        with open(file_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"⚠️ Não foi possível carregar estilos opcionais de {filename}: {exc}")
        return {}

    loaded: Dict[str, FightingStyle] = {}
    for name, payload in data.items():
        payload = payload.copy()
        payload.setdefault("name", name)
        payload.pop("mechanical_effect", None)
        loaded[name] = FightingStyle(**payload)
    return loaded


def _load_optional_styles() -> Dict[str, FightingStyle]:
    optional_styles: Dict[str, FightingStyle] = {}
    optional_content = AppSettings.load().get("optional_content", {})

    for flag, (filename, source_label) in OPTIONAL_STYLE_FILES.items():
        if not optional_content.get(flag, False):
            continue

        styles = _load_styles_from_file(filename)
        if not styles:
            print(
                f"⚠️ Conteúdo opcional '{source_label}' habilitado, mas {filename} não foi encontrado ou está vazio."
            )
        optional_styles.update(styles)

    return optional_styles


def _get_all_fighting_styles() -> Dict[str, FightingStyle]:
    global _STYLE_CACHE
    if _STYLE_CACHE is None:
        styles = dict(BASE_FIGHTING_STYLES)
        styles.update(_load_optional_styles())
        _STYLE_CACHE = styles
    return _STYLE_CACHE


def reload_fighting_styles_cache() -> None:
    """Força recarregamento dos estilos (utilizado ao alterar conteúdo opcional)."""

    global _STYLE_CACHE
    _STYLE_CACHE = None


def get_available_fighting_styles(class_name: str) -> List[FightingStyle]:
    """
    Retorna os estilos de luta disponíveis para uma classe
    
    Args:
        class_name: Nome da classe
        
    Returns:
        Lista de FightingStyle disponíveis para a classe
    """
    available = []
    for style in _get_all_fighting_styles().values():
        if class_name in style.classes:
            available.append(style)
    return available


def get_fighting_style(style_name: str) -> Optional[FightingStyle]:
    """
    Retorna um estilo de luta pelo nome
    
    Args:
        style_name: Nome do estilo
        
    Returns:
        FightingStyle ou None se não encontrado
    """
    return _get_all_fighting_styles().get(style_name)
