class Post:
    def __init__(self, id: int, title: str, body: str, userId: int):
        self.id = id
        self.title = title
        self.body = body
        self.userId = userId

ListaPost = [Post(1, "...", "...", 1), Post(2, "...", "...", 1), Post(3, "...", "...", 1), Post(4, "...", "...", 1), Post(5, "...", "...", 2), Post(6, "...", "...", 2), Post(7, "...", "...", 2), Post(8, "...", "...", 2),]