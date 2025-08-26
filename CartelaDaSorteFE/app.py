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
    numero = session.get("numero_sorteio")
    if not numero:
        resp = requests.post(f"{BE_BASE_URL}/api/NovaCartela")
        data = resp.json()
        session["numero_sorteio"] = data["numero_sorteio"]
    numero = session["numero_sorteio"]
    resp = requests.get(f"{BE_BASE_URL}/api/AtualizarCartela", params={"numero_sorteio": numero})
    return resp.json()


@app.route("/", methods=["GET"])
def index():
    email = session.get("email")
    if not email:
        return render_template("index.html", logged=False)
    cartela = ensure_cartela()
    return render_template(
        "index.html",
        logged=True,
        apelido=get_apelido(email),
        cartela=cartela,
    )


@app.post("/login")
def login():
    email = request.form.get("email")
    if not email:
        return redirect(url_for("index"))
    session["email"] = email
    session["apelido"] = get_apelido(email)
    session.pop("numero_sorteio", None)
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


@app.post("/nova")
def nova():
    if "email" not in session:
        return "", 401
    resp = requests.post(f"{BE_BASE_URL}/api/NovaCartela")
    data = resp.json()
    session["numero_sorteio"] = data["numero_sorteio"]
    cartela = ensure_cartela()
    return render_template("_grid.html", cartela=cartela, apelido=session["apelido"])


if __name__ == "__main__":
    app.run(port=int(os.getenv("PORT", 8080)), debug=True)
