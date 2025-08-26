# Cartela da Sorte

Aplicação completa com **FastAPI** no back-end e **Flask** no front-end usando **HTMX** e **TailwindCSS**.

## Estrutura

- `CartelaDaSorteBE/` – API FastAPI
- `CartelaDaSorteFE/` – Front-end Flask
- `docker-compose.yml` – Executa BE e FE juntos

## Configuração

1. Copie os arquivos `.env.example` para `.env` nas pastas raiz, `CartelaDaSorteBE/` e `CartelaDaSorteFE/` conforme necessário.
2. Ajuste variáveis se desejar.

## Rodando sem Docker

### Back-end
```bash
cd CartelaDaSorteBE
uvicorn app.main:app --reload --port 8000
```

### Front-end
```bash
cd CartelaDaSorteFE
flask --app app.py run --port 8080
```

## Rodando com Docker

```bash
docker compose up --build
```

## Testes

```bash
cd CartelaDaSorteBE
pytest
```

## Notas

- A lista de clubes é buscada online; se falhar, usa-se um conjunto local de 20 times da Série A.
- Os dados da cartela são mantidos apenas em memória; reiniciar o back-end limpa as apostas.
- Essa app serve apenas pra treinamento.
