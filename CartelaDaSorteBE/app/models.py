from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Cartela:
    numero_sorteio: str
    clubes: List[str]
    apostas: Dict[str, List[str]] = field(default_factory=dict)
    sorteado: Optional[str] = None
