import json
import requests

def bypass(url):

    payload = {
        "url": url,
    }

    r = requests.post("https://api.bypass.vip/", data=payload)
    return r.json()
