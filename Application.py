class Application():
    PrepareMode = 0
    LoadMode = 1

    def __init__(self):
        self._instance = None
        self.mode = None
        self.auction = None

    def set_mode(self, mode):
        self.mode = mode

    def set_auction(self, auction):
        self.auction = auction


app = Application()
