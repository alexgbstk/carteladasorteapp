from pydantic import BaseModel, EmailStr
from typing import Dict, List, Optional


class Cartela(BaseModel):
    numero_sorteio: str
    clubes: List[str]
    apostas: Dict[str, List[str]] = {}
    sorteado: Optional[str] = None


class ApostaReq(BaseModel):
    numero_sorteio: str
    email: EmailStr
    time: str


class AtualizarReq(BaseModel):
    numero_sorteio: str


class ApostaResp(BaseModel):
    numero_sorteio: str
    apostas: Dict[str, List[str]]


class SortearResp(BaseModel):
    numero_sorteio: str
    time_sorteado: str


class NovaCartelaReq(BaseModel):
    numero_sorteio: Optional[str] = None
