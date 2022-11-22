import requests


def fetch_zettels():
    url = "http://127.0.0.1:8000/-/export.json"
    resp = requests.get(url=url)
    zettels = resp.json()

    # Throw away Zettelkasten metadata.
    zettels = zettels["files"]

    return zettels
