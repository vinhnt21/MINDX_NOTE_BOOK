class User:
    """Class đại diện cho người dùng"""
    def __init__(self, username, password):
        self.username = username
        self.password = password
    
    def __str__(self):
        return f"User: {self.username}"

class Game:
    """Class đại diện cho trò chơi"""
    def __init__(self, name, price, description, url, img_url):
        self.name = name
        self.price = price
        self.description = description
        self.url = url
        self.img_url = img_url

    def __str__(self):
        return f"Game: {self.name}, Price: {self.price}, Description: {self.description}, URL: {self.url}, Image URL: {self.img_url}"