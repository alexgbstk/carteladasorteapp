import os
import random
from typing import Dict, List

from . import state, utils, models, schemas, clubs_source


async def nova_cartela() -> schemas.Cartela:
    async with state.lock:
        url = os.getenv("CLUBS_SOURCE_URL")
        clubes = clubs_source.get_clubs(url)
        numero = utils.generate_numero_sorteio()
        apostas = {club: [] for club in clubes}
        cartela = models.Cartela(numero_sorteio=numero, clubes=clubes, apostas=apostas)
        state.cartela_atual = cartela
        return schemas.Cartela(**cartela.__dict__)


async def apostar(req: schemas.ApostaReq) -> schemas.ApostaResp:
    async with state.lock:
        cartela = state.cartela_atual
        if not cartela or cartela.numero_sorteio != req.numero_sorteio:
            raise ValueError("Número de sorteio inválido")
        if req.time not in cartela.clubes:
            raise ValueError("Time inválido")
        nick = utils.apelido(req.email)
        nomes = cartela.apostas.setdefault(req.time, [])
        if nick not in nomes:
            nomes.append(nick)
        return schemas.ApostaResp(numero_sorteio=cartela.numero_sorteio, apostas=cartela.apostas)


async def atualizar(numero_sorteio: str | None = None) -> schemas.Cartela:
    cartela = state.cartela_atual
    if not cartela:
        raise ValueError("Não há cartela ativa")
    if numero_sorteio and cartela.numero_sorteio != numero_sorteio:
        raise ValueError("Número de sorteio inválido")
    return schemas.Cartela(**cartela.__dict__)


async def sortear(numero_sorteio: str) -> schemas.SortearResp:
    async with state.lock:
        cartela = state.cartela_atual
        if not cartela or cartela.numero_sorteio != numero_sorteio:
            raise ValueError("Número de sorteio inválido")
        if not all(cartela.apostas[club] for club in cartela.clubes):
            raise ValueError("Cartela incompleta")
        if cartela.sorteado is None:
            cartela.sorteado = random.choice(cartela.clubes)
        return schemas.SortearResp(numero_sorteio=cartela.numero_sorteio, time_sorteado=cartela.sorteado)
