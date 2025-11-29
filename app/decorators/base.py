from __future__ import annotations

from abc import ABC, abstractmethod


class PagamentoComponent(ABC):
    @abstractmethod
    def calcular(self) -> float:
        raise NotImplementedError


class PagamentoBase(PagamentoComponent):
    """Component concreto básico: apenas o valor calculado pela Strategy."""

    def __init__(self, valor_base: float):
        self._valor_base = valor_base

    def calcular(self) -> float:
        return self._valor_base


class PagamentoDecorator(PagamentoComponent):
    """Classe base para Decorators."""

    def __init__(self, componente: PagamentoComponent):
        self._componente = componente

    @property
    def componente(self) -> PagamentoComponent:
        return self._componente
