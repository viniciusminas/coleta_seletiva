from .base import PagamentoDecorator


class BonusQualidadeDecorator(PagamentoDecorator):
    """
    Bônus por material limpo e triado corretamente.
    +5% se limpo, +5% se triagem correta.
    """

    def __init__(self, componente, limpo: bool, triagem_correta: bool):
        super().__init__(componente)
        self._limpo = limpo
        self._triagem_correta = triagem_correta

    def calcular(self) -> float:
        valor = self.componente.calcular()
        bonus = 0.0
        if self._limpo:
            bonus += 0.05
        if self._triagem_correta:
            bonus += 0.05
        return valor * (1 + bonus)
