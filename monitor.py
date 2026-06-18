import os
import json
import requests
from bs4 import BeautifulSoup

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

URL = "https://clasificados.eldeber.com.bo/category/empleos"

PALABRAS = [
    "venta",
    "ventas",
    "vendedor",
    "vendedora",
    "asesor",
    "comercial",
    "ejecutivo",
    "preventista",
    "promotor",
    "cajero",
    "cajera",
    "cliente",
    "atención",
    "atencion"
]

ARCHIVO = "vistos.json"

try:
    with open(ARCHIVO, "r") as f:
        vistos = set(json.load(f))
except:
    vistos = set()

headers = {
    "User-Agent": "Mozilla/5.0"
}

r = requests.get(URL, headers=headers, timeout=20)
soup = BeautifulSoup(r.text, "html.parser")

nuevos = []

for a in soup.find_all("a", href=True):

    texto = a.get_text(" ", strip=True)
    enlace = a["href"]

    if not texto:
        continue

    texto_lower = texto.lower()

    if any(p in texto_lower for p in PALABRAS):

        if enlace.startswith("/"):
            enlace = "https://clasificados.eldeber.com.bo" + enlace

        if enlace not in vistos:

            vistos.add(enlace)
            nuevos.append((texto, enlace))

for titulo, enlace in nuevos:

    mensaje = f"""🔔 Nueva vacante

{titulo}

{enlace}
"""

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": mensaje
        },
        timeout=20
    )

with open(ARCHIVO, "w") as f:
    json.dump(list(vistos), f)
