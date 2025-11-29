from dataclasses import dataclass
from enum import Enum

class TipoMaterial(str, Enum):
    PAPEL = "papel"
    VIDRO = "vidro"
    METAL = "metal"
    PLASTICO = "plastico"

@dataclass
class Cooperado:
    id: int
    nome: str
    email: str | None = None
    total_kg: float = 0.0
    total_creditos: float = 0.0
    meta_atingida: bool = False

@dataclass
class Entrega:
    cooperado_id: int
    material: TipoMaterial
    peso_kg: float
    limpo: bool = True
    triagem_correta: bool = True
