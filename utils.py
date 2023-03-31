import random
import requests

def get_random_post_id(group_id: int, token: str) -> str:
    url = "https://api.vk.com/method/wall.get?access_token=" + token
    data = {
        "v": 5.131,
        "owner_id": group_id,
        "count": 100,
        "offset": random.randint(0, 1000),
    }
    info = requests.post(url, params=data).json()
    maxval = 100
    randpostnum = random.randint(a=0, b=maxval)
    post_id = info["response"]["items"][randpostnum]["id"]
    return str(group_id)+ "_" + str(post_id)


def get_post_url(post_id: str) -> str:
    return "https://vk.com/wall" + str(post_id)


def parse_post(post_id: str, token: str) -> tuple[str, str]:
    url = "https://api.vk.com/method/wall.getById?access_token=" + token
    data = {
        "v": 5.131,
        "posts": post_id
    }
    req = requests.post(url, params = data).json()["response"][0]
    if len(req["text"]) >= 4000:
        req["text"] = req["text"][0:4000]
    if "photo" in req["attachments"][0]:
        return req["text"], req["attachments"][0]["photo"]["sizes"][-1]["url"]
    else:
        return req["text"], ""
