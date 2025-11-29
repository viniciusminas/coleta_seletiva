from dataclasses import dataclass
from typing import Any, Dict

from .models import Cooperado

@dataclass
class EventoColeta:
    tipo: str
    cooperado: Cooperado
    payload: Dict[str, Any]
