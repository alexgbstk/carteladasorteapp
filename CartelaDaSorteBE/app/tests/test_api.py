from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def create_cartela():
    resp = client.post("/api/NovaCartela")
    assert resp.status_code == 200
    return resp.json()


def test_nova_cartela_returns_20_clubs():
    data = create_cartela()
    assert len(data["clubes"]) == 20


def test_apostar_e_atualizar():
    data = create_cartela()
    numero = data["numero_sorteio"]
    clube = data["clubes"][0]
    resp = client.post("/api/ApostarNaCartela", json={"numero_sorteio": numero, "email": "maria@test.com", "time": clube})
    assert resp.status_code == 200
    resp = client.get("/api/AtualizarCartela", params={"numero_sorteio": numero})
    assert resp.status_code == 200
    assert resp.json()["apostas"][clube] == ["maria"]


def test_sortear_regras():
    data = create_cartela()
    numero = data["numero_sorteio"]
    clubes = data["clubes"]
    # preenche 19 clubes
    for idx, clube in enumerate(clubes[:-1]):
        client.post("/api/ApostarNaCartela", json={"numero_sorteio": numero, "email": f"u{idx}@t.com", "time": clube})
    # tenta sortear -> erro
    resp = client.post("/api/SortearCartela", json={"numero_sorteio": numero})
    assert resp.status_code == 400
    # preenche ultimo
    ultimo = clubes[-1]
    client.post("/api/ApostarNaCartela", json={"numero_sorteio": numero, "email": "u_final@t.com", "time": ultimo})
    resp = client.post("/api/SortearCartela", json={"numero_sorteio": numero})
    assert resp.status_code == 200
    assert resp.json()["time_sorteado"] in clubes
