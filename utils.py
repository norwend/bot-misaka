import random
import requests

class Group:
    user_access_token: str
    group_id: int
    post_count: int
    def __init__(self, group_id: int, access_token: str) -> None:
        self.user_access_token = access_token
        self.group_id = group_id
        url = "https://api.vk.com/method/wall.get?access_token=" + access_token
        data = {
            "v": 5.131,
            "owner_id": group_id,
            "count": 100,
        }
        self.post_count = requests.post(url, params=data).json()["response"]["count"]
    
    def get_random_post_id(self) -> str:
        url = "https://api.vk.com/method/wall.get?access_token=" + self.user_access_token
        data = {
            "v": 5.131,
            "owner_id": self.group_id,
            "count": 100,
            "offset": random.randint(0, self.post_count - 101),
        }
        info = requests.post(url, params=data).json()
        maxval = 100
        randpostnum = random.randint(a=0, b=maxval)
        post_id = info["response"]["items"][randpostnum]["id"]
        return str(self.group_id)+ "_" + str(post_id)
    
    def parse_post(self, post_id: str) -> tuple[str, str]:
        url = "https://api.vk.com/method/wall.getById?access_token=" + self.user_access_token
        data = {
            "v": 5.131,
            "posts": post_id
        }
        req = requests.post(url, params = data).json()["response"][0]
        req["text"] = req["text"][0:4000]
        if "photo" in req["attachments"][0]:
            return req["text"], req["attachments"][0]["photo"]["sizes"][-1]["url"]
        else:
            return req["text"], ""

def get_post_url(post_id: str) -> str:
    return "https://vk.com/wall" + str(post_id)