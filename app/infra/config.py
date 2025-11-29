from __future__ import annotations

from domain.models import TipoMaterial

class Config:

    _instance: "Config | None" = None

    def __new__(cls) -> "Config":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_defaults()
        return cls._instance

    def _init_defaults(self) -> None:
        self.precos_por_kg = {
            TipoMaterial.PAPEL: 0.50,
            TipoMaterial.VIDRO: 0.30,
            TipoMaterial.METAL: 1.00,
            TipoMaterial.PLASTICO: 0.80,
        }
        # meta bem simples para o Observer disparar
        self.meta_kg_mensal = 100.0

    @classmethod
    def instance(cls) -> "Config":
        return cls()
