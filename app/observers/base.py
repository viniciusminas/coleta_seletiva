from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from domain.events import EventoColeta


class Observer(ABC):
    @abstractmethod
    def update(self, evento: EventoColeta) -> None:
        raise NotImplementedError


class Subject(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def adicionar_observer(self, observer: Observer) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def remover_observer(self, observer: Observer) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notificar(self, evento: EventoColeta) -> None:
        for obs in list(self._observers):
            obs.update(evento)
