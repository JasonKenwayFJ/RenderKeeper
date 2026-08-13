import time
import threading
import logging

import requests
import pystray
from PIL import Image

URLS = [
    "https://apicoffeemain.onrender.com/articles/getArticles",
    "https://gravleapi.onrender.com/categories/get_all_categories",
    "https://gravle.onrender.com"
]

INTERVAL = 10 * 60

logging.basicConfig(
    filename="renderkeeper.log",
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def pingServer(url):
    try:
        logging.info(f"Pinging {url}")

        response = requests.get(
            url,
            timeout=30
        )

        logging.info(f"Response: {response.status_code}")

    except requests.RequestException as e:
        logging.error(f"Request failed for {url}: {e}")


def worker():
    while True:
        for url in URLS:
            pingServer(url)

        time.sleep(INTERVAL)


def onExit(icon, item):
    logging.info("RenderKeeper stopped")
    icon.stop()


icon = pystray.Icon(
    "RenderKeeper",
    Image.new("RGB", (64, 64), "black"),
    "Render Keeper",
    menu=pystray.Menu(
        pystray.MenuItem(
            "Пинговать сейчас",
            lambda: [pingServer(url) for url in URLS]
        ),
        pystray.MenuItem(
            "Выход",
            onExit
        )
    )
)

logging.info("RenderKeeper started")

threading.Thread(
    target=worker,
    daemon=True
).start()

icon.run()
