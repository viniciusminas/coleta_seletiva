from typing import List

from .base import Observer
from domain.events import EventoColeta


class EmailNotifier(Observer):
    """Simula envio de e-mail (guarda mensagens em memória)."""

    def __init__(self) -> None:
        self.enviados: List[str] = []

    def update(self, evento: EventoColeta) -> None:
        if evento.tipo == "META_ATINGIDA":
            msg = (
                f"Parabéns, {evento.cooperado.nome}! "
                f"Você atingiu a meta de {evento.payload['meta_kg']} kg."
            )
            self.enviados.append(msg)


class LogNotifier(Observer):
    """Simula log em arquivo/console."""

    def __init__(self) -> None:
        self.registros: List[str] = []

    def update(self, evento: EventoColeta) -> None:
        self.registros.append(
            f"{evento.tipo} - {evento.cooperado.nome} - {evento.payload}"
        )
