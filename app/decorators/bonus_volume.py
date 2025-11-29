from .base import PagamentoDecorator


class BonusVolumeDecorator(PagamentoDecorator):
    """
    Bônus progressivo para grandes volumes na mesma entrega.
    >= 50kg: +10%, >=100kg: +20%.
    """

    def __init__(self, componente, peso_kg: float):
        super().__init__(componente)
        self._peso_kg = peso_kg

    def calcular(self) -> float:
        valor = self.componente.calcular()
        if self._peso_kg >= 100:
            return valor * 1.20
        if self._peso_kg >= 50:
            return valor * 1.10
        return valor
