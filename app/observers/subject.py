from typing import Dict

from .base import Subject
from infra.config import Config
from domain.events import EventoColeta
from domain.models import Cooperado


class Cooperativa(Subject):
    """
    Subject que controla cooperados, acumula peso/créditos
    e dispara eventos quando a meta é atingida.
    """

    def __init__(self) -> None:
        super().__init__()
        self._config = Config.instance()
        self._cooperados: Dict[int, Cooperado] = {}

    def registrar_cooperado(self, cooperado: Cooperado) -> None:
        self._cooperados[cooperado.id] = cooperado

    def buscar_cooperado(self, cooperado_id: int) -> Cooperado:
        return self._cooperados[cooperado_id]

    def registrar_pagamento(
        self, cooperado_id: int, peso_kg: float, valor_pago: float
    ) -> None:
        cooperado = self.buscar_cooperado(cooperado_id)
        cooperado.total_kg += peso_kg
        cooperado.total_creditos += valor_pago

        if (not cooperado.meta_atingida) and (
            cooperado.total_kg >= self._config.meta_kg_mensal
        ):
            cooperado.meta_atingida = True
            evento = EventoColeta(
                tipo="META_ATINGIDA",
                cooperado=cooperado,
                payload={
                    "total_kg": cooperado.total_kg,
                    "meta_kg": self._config.meta_kg_mensal,
                },
            )
            self.notificar(evento)
