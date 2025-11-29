from domain.models import TipoMaterial
from infra.config import Config
from .base import PagamentoStrategy


class PagamentoPorMaterial(PagamentoStrategy):
    """Strategy concreta parametrizada pelo tipo de material."""

    def __init__(self, material: TipoMaterial):
        self._material = material
        self._config = Config.instance()

    @property
    def material(self) -> TipoMaterial:
        return self._material

    def calcular(self, peso_kg: float) -> float:
        preco = self._config.precos_por_kg[self._material]
        return preco * peso_kg


class PagamentoPapel(PagamentoPorMaterial):
    def __init__(self):
        super().__init__(TipoMaterial.PAPEL)


class PagamentoVidro(PagamentoPorMaterial):
    def __init__(self):
        super().__init__(TipoMaterial.VIDRO)


class PagamentoMetal(PagamentoPorMaterial):
    def __init__(self):
        super().__init__(TipoMaterial.METAL)


class PagamentoPlastico(PagamentoPorMaterial):
    def __init__(self):
        super().__init__(TipoMaterial.PLASTICO)
