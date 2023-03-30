class Post:
    text: str
    img_url: str
    time: str

    def __init__(self, text: str, img_url: str, time: str):
        self.text = text
        self.img_url = img_url
        self.time = time
