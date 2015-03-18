class Application():
    _instance = None
    mode = None
    OneLotMode = 0
    MultiLotMode = 1
    LoadMode = 2
    auction = None

    def setMode(self, mode):
        self.mode = mode
    
    def setAuction(self, auction):
        self.auction = auction
    
    def getLotPageId(self):
        if self.mode == self.OneLotMode:
            return 2
        elif self.mode == self.MultiLotMode:
            return 3
        return False

app = Application()
