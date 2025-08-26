import os
import requests
from bs4 import BeautifulSoup
from typing import List

FALLBACK_CLUBS = [
    "Athletico-PR", "Atlético-MG", "Bahia", "Botafogo", "Corinthians",
    "Criciúma", "Cruzeiro", "Cuiabá", "Flamengo", "Fluminense",
    "Fortaleza", "Grêmio", "Internacional", "Juventude", "Palmeiras",
    "Red Bull Bragantino", "São Paulo", "Vasco da Gama", "Vitória", "Atlético-GO",
]


def get_clubs(url: str | None) -> List[str]:
    """Try to fetch list of clubs from URL, otherwise fallback."""
    if url:
        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "html.parser")
            table = soup.find("table")
            clubs = []
            if table:
                for row in table.find_all("tr"):
                    cols = [c.get_text(strip=True) for c in row.find_all("td")]
                    if cols:
                        clubs.append(cols[0])
                    if len(clubs) == 20:
                        break
            if len(clubs) == 20:
                return clubs
        except Exception:
            pass
    return FALLBACK_CLUBS
