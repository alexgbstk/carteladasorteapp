import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "secret")
BE_BASE_URL = os.getenv("BE_BASE_URL", "http://localhost:8000")


def get_apelido(email: str) -> str:
    return email.split("@")[0]


def ensure_cartela():
    """Ensure there is an active cartela and return its state.

    If a cartela number is stored in session, try to fetch that specific
    cartela. Otherwise, attempt to retrieve whichever cartela is currently
    active. Only when the fetch fails do we create a new one. This allows new
    gamblers to join an existing draw without clicking "Atualizar" first.
    """

    numero = session.get("numero_sorteio")
    params = {"numero_sorteio": numero} if numero else {}
    resp = requests.get(f"{BE_BASE_URL}/api/AtualizarCartela", params=params or None)
    if resp.status_code != 200:
        payload = {"numero_sorteio": numero} if numero else None
        resp = requests.post(f"{BE_BASE_URL}/api/NovaCartela", json=payload)
    data = resp.json()
    session["numero_sorteio"] = data["numero_sorteio"]
    return data


@app.route("/", methods=["GET"])
def index():
    email = session.get("email")
    if not email:
        return render_template("index.html", logged=False)
    # cartela will be fetched asynchronously via HTMX on page load
    return render_template("index.html", logged=True, apelido=get_apelido(email))


@app.post("/login")
def login():
    email = request.form.get("email")
    numero = request.form.get("numero_sorteio") or None
    if not email:
        return redirect(url_for("index"))
    session["email"] = email
    session["apelido"] = get_apelido(email)
    # Store provided draw number; ensure_cartela will handle creating or
    # fetching the proper cartela on the next request.
    if numero:
        session["numero_sorteio"] = numero
    return redirect(url_for("index"))


@app.get("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.post("/aposta")
def aposta():
    if "email" not in session:
        return "", 401
    time = request.form.get("time")
    cartela = ensure_cartela()
    numero = cartela["numero_sorteio"]
    requests.post(
        f"{BE_BASE_URL}/api/ApostarNaCartela",
        json={"numero_sorteio": numero, "email": session["email"], "time": time},
    )
    cartela = ensure_cartela()
    return render_template("_grid.html", cartela=cartela, apelido=session["apelido"])


@app.get("/atualizar")
def atualizar():
    if "email" not in session:
        return "", 401
    cartela = ensure_cartela()
    return render_template("_grid.html", cartela=cartela, apelido=session["apelido"])


@app.post("/sortear")
def sortear():
    if "email" not in session:
        return "", 401
    numero = session.get("numero_sorteio")
    resp = requests.post(f"{BE_BASE_URL}/api/SortearCartela", json={"numero_sorteio": numero})
    if resp.status_code != 200:
        return resp.text, resp.status_code
    data = resp.json()
    cartela = ensure_cartela()
    cartela["sorteado"] = data["time_sorteado"]
    return render_template("_result.html", cartela=cartela)


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 8080)), debug=True)
