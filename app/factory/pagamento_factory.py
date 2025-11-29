from domain.models import TipoMaterial
from strategies.base import PagamentoStrategy
from strategies.materiais import (
    PagamentoPapel,
    PagamentoVidro,
    PagamentoMetal,
    PagamentoPlastico,
)

class PagamentoFactory:
    """
    Factory Method simplificado que encapsula a criação de Strategies.
    Facilita incluir novos materiais sem mexer no menu/Context.
    """

    def criar(self, material: TipoMaterial) -> PagamentoStrategy:
        if material == TipoMaterial.PAPEL:
            return PagamentoPapel()
        if material == TipoMaterial.VIDRO:
            return PagamentoVidro()
        if material == TipoMaterial.METAL:
            return PagamentoMetal()
        if material == TipoMaterial.PLASTICO:
            return PagamentoPlastico()
        raise ValueError(f"Material desconhecido: {material}")

class PagamentoFactory:
    """
    Factory Method simplificado que encapsula a criação de Strategies.
    Facilita incluir novos materiais sem mexer no menu/Context.
    """

    def criar(self, material: TipoMaterial) -> PagamentoStrategy:
        if material == TipoMaterial.PAPEL:
            return PagamentoPapel()
        if material == TipoMaterial.VIDRO:
            return PagamentoVidro()
        if material == TipoMaterial.METAL:
            return PagamentoMetal()
        if material == TipoMaterial.PLASTICO:
            return PagamentoPlastico()
        raise ValueError(f"Material desconhecido: {material}")
