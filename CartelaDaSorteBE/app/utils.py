import uuid


def generate_numero_sorteio() -> str:
    return uuid.uuid4().hex[:8]


def apelido(email: str) -> str:
    return email.split("@")[0]
