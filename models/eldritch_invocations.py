"""Gerenciamento de Eldritch Invocations do Bruxo."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .app_settings import AppSettings


@dataclass
class EldritchInvocation:
    """Representa uma Eldritch Invocation individual."""

    name: str
    description: str
    min_level: int = 2
    prerequisites: str = ""
    source: str = "Player's Handbook"
    required_pacts: Optional[List[str]] = None
    required_patrons: Optional[List[str]] = None
    notes: Optional[str] = None

    def meets_basic_requirements(self, character_level: int) -> bool:
        """Checa apenas o requisito de nível (outros requisitos são informativos por enquanto)."""

        return character_level >= self.min_level


class EldritchInvocationDatabase:
    """Carrega e disponibiliza Eldritch Invocations, incluindo conteúdo opcional."""

    CORE_FILE = "eldritch_invocations.json"
    OPTIONAL_FILES = {
        "tashas_spells": ("eldritch_invocations_tcoe.json", "Tasha's Cauldron of Everything"),
        "xanathars_spells": ("eldritch_invocations_xgte.json", "Xanathar's Guide to Everything"),
    }

    # Índices iguais ao nível do Bruxo (0-index ignorado)
    _INVOCATIONS_BY_LEVEL = [
        0,  # placeholder para nível 0
        0,  # nível 1
        2,  # nível 2
        2,  # nível 3
        2,  # nível 4
        3,  # nível 5
        3,  # nível 6
        4,  # nível 7
        4,  # nível 8
        5,  # nível 9
        5,  # nível 10
        5,  # nível 11
        6,  # nível 12
        6,  # nível 13
        6,  # nível 14
        7,  # nível 15
        7,  # nível 16
        7,  # nível 17
        8,  # nível 18
        8,  # nível 19
        8,  # nível 20
    ]

    _cache: Optional[Dict[str, EldritchInvocation]] = None

    @classmethod
    def _data_dir(cls) -> Path:
        return Path(__file__).parent.parent / "data"

    @classmethod
    def _load_from_file(cls, filename: str) -> Dict[str, EldritchInvocation]:
        file_path = cls._data_dir() / filename
        if not file_path.exists():
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                raw_data = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"⚠️ Não foi possível carregar {filename}: {exc}")
            return {}

        loaded: Dict[str, EldritchInvocation] = {}
        for name, payload in raw_data.items():
            payload = payload.copy()
            payload.setdefault("name", name)
            loaded[name] = EldritchInvocation(**payload)
        return loaded

    @classmethod
    def _load_invocations(cls) -> Dict[str, EldritchInvocation]:
        invocations = cls._load_from_file(cls.CORE_FILE)

        optional_content = AppSettings.load().get("optional_content", {})
        for flag, (filename, source_label) in cls.OPTIONAL_FILES.items():
            if not optional_content.get(flag, False):
                continue

            optional_invocations = cls._load_from_file(filename)
            if not optional_invocations:
                print(
                    f"⚠️ Conteúdo opcional '{source_label}' habilitado, mas {filename} está vazio ou ausente."
                )
            invocations.update(optional_invocations)

        return invocations

    @classmethod
    def get_all_invocations(cls) -> Dict[str, EldritchInvocation]:
        if cls._cache is None:
            cls._cache = cls._load_invocations()
        return cls._cache

    @classmethod
    def reload_cache(cls) -> None:
        cls._cache = None

    @classmethod
    def get_invocation(cls, name: str) -> Optional[EldritchInvocation]:
        return cls.get_all_invocations().get(name)

    @classmethod
    def get_invocations_for_level(
        cls,
        level: int,
        *,
        exclude: Optional[List[str]] = None,
        pact_boon: Optional[str] = None,
        patron_name: Optional[str] = None,
    ) -> List[EldritchInvocation]:
        exclude = exclude or []
        invocations = [
            invocation
            for invocation in cls.get_all_invocations().values()
            if invocation.meets_basic_requirements(level)
            and invocation.name not in exclude
            and cls._meets_character_reqs(invocation, pact_boon, patron_name)
        ]
        invocations.sort(key=lambda inv: (inv.min_level, inv.name))
        return invocations

    @staticmethod
    def _meets_character_reqs(
        invocation: EldritchInvocation,
        pact_boon: Optional[str],
        patron_name: Optional[str],
    ) -> bool:
        if invocation.required_pacts:
            if not pact_boon or pact_boon not in invocation.required_pacts:
                return False

        if invocation.required_patrons:
            if not patron_name or patron_name not in invocation.required_patrons:
                return False

        return True

    @classmethod
    def get_known_count_for_level(cls, level: int) -> int:
        if level < 0:
            return 0
        if level >= len(cls._INVOCATIONS_BY_LEVEL):
            return cls._INVOCATIONS_BY_LEVEL[-1]
        return cls._INVOCATIONS_BY_LEVEL[level]
