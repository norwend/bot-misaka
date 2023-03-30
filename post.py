class Post:
    text: str
    img_url: str
    time: str
    bot: Bot

    def __init__(self, text: str, img_url: str, time: str, bot: Bot):
        self.text = text
        self.img_url = img_url
        self.time = time
        self.bot = bot
