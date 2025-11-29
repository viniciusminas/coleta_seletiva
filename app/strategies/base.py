from __future__ import annotations

from abc import ABC, abstractmethod


class PagamentoStrategy(ABC):
    """Interface do Strategy."""

    @abstractmethod
    def calcular(self, peso_kg: float) -> float:
        """Retorna o valor base a pagar para o peso informado."""
        raise NotImplementedError


class CalculadoraPagamento:
    """Context do Strategy."""

    def __init__(self, strategy: PagamentoStrategy):
        self._strategy = strategy

    @property
    def strategy(self) -> PagamentoStrategy:
        return self._strategy

    def trocar_strategy(self, nova_strategy: PagamentoStrategy) -> None:
        self._strategy = nova_strategy

    def calcular_pagamento(self, peso_kg: float) -> float:
        return self._strategy.calcular(peso_kg)
