"""Sistema de Pact Boons do Bruxo."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

from .app_settings import AppSettings


@dataclass
class PactBoon:
    """Representa um Pact Boon disponível para Warlocks."""

    name: str
    description: str
    mechanical_effect: str
    source: str = "Player's Handbook"


PACT_OF_THE_CHAIN = PactBoon(
    name="Pact of the Chain",
    description=(
        "Seu patrono concede a companhia de um familiar sobrenatural. Você pode selecionar servos"
        " especiais (imp, pseudodragão, sprite ou quasit) quando conjurar Find Familiar e pode"
        " atacar através deles em determinadas situações."
    ),
    mechanical_effect=(
        "Concede acesso a Find Familiar aprimorado com familiares exclusivos e permite que eles"
        " desferem ataques usando sua reação em alguns recursos de invocação."
    ),
)

PACT_OF_THE_BLADE = PactBoon(
    name="Pact of the Blade",
    description=(
        "Você pode invocar uma arma de pacto em uma ação, escolhendo sua forma e propriedades."
        " A arma é mágica, pode ser mudada após um descanso e pode ser substituída por uma arma"
        " que você tocar."
    ),
    mechanical_effect=(
        "Permite criar/transformar uma arma mágica vinculada. Você pode usar sua arma de pacto"
        " para canalizar invocações específicas do Pacto da Lâmina."
    ),
)

PACT_OF_THE_TOME = PactBoon(
    name="Pact of the Tome",
    description=(
        "Seu patrono entrega um Livro das Sombras contendo magias adicionais. Enquanto portar"
        " o tomo, você conhece truques extras escolhidos de qualquer lista de classes."
    ),
    mechanical_effect=(
        "Concede o Book of Shadows com três truques adicionais e pode destravar invocações"
        " relacionadas ao tomo."
    ),
)

BASE_PACT_BOONS: Dict[str, PactBoon] = {
    boons.name: boons
    for boons in (PACT_OF_THE_CHAIN, PACT_OF_THE_BLADE, PACT_OF_THE_TOME)
}


class PactBoonDatabase:
    """Gerencia carregamento e cache dos Pact Boons (com suporte a conteúdo opcional)."""

    OPTIONAL_FILES = {
        "tashas_spells": ("pact_boons_tcoe.json", "Tasha's Cauldron of Everything"),
        "xanathars_spells": ("pact_boons_xgte.json", "Xanathar's Guide to Everything"),
    }

    _cache: Optional[Dict[str, PactBoon]] = None

    @classmethod
    def _data_dir(cls) -> Path:
        return Path(__file__).parent.parent / "data"

    @classmethod
    def _load_boons_from_file(cls, filename: str) -> Dict[str, PactBoon]:
        file_path = cls._data_dir() / filename
        if not file_path.exists():
            return {}

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            print(f"⚠️ Não foi possível carregar Pact Boons opcionais de {filename}: {exc}")
            return {}

        boons: Dict[str, PactBoon] = {}
        for name, data in payload.items():
            data = data.copy()
            data.setdefault("name", name)
            boons[name] = PactBoon(**data)
        return boons

    @classmethod
    def _load_optional_boons(cls) -> Dict[str, PactBoon]:
        optional_content = AppSettings.load().get("optional_content", {})
        loaded: Dict[str, PactBoon] = {}

        for flag, (filename, source_label) in cls.OPTIONAL_FILES.items():
            if not optional_content.get(flag, False):
                continue

            boons = cls._load_boons_from_file(filename)
            if not boons:
                print(
                    f"⚠️ Conteúdo opcional '{source_label}' habilitado, mas {filename} está vazio ou ausente."
                )
            loaded.update(boons)

        return loaded

    @classmethod
    def _ensure_cache(cls) -> Dict[str, PactBoon]:
        if cls._cache is None:
            boons = dict(BASE_PACT_BOONS)
            boons.update(cls._load_optional_boons())
            cls._cache = boons
        return cls._cache

    @classmethod
    def reload_cache(cls) -> None:
        cls._cache = None

    @classmethod
    def get_all_boons(cls) -> List[PactBoon]:
        boons = list(cls._ensure_cache().values())
        return sorted(boons, key=lambda boon: boon.name)

    @classmethod
    def get_boon(cls, name: str) -> Optional[PactBoon]:
        return cls._ensure_cache().get(name)

    @classmethod
    def get_boon_names(cls) -> List[str]:
        return [boon.name for boon in cls.get_all_boons()]
