class State:
    def __init__(self, step, price_step, price, last_offer, prelast_offer, advice):
        self.step = step
        self.price_step = price_step
        self.price = price
        self.last_offer = last_offer
        self.prelast_offer = prelast_offer
        self.advice = advice

    def add_offer(self, offer):
        self.prelast_offer = self.last_offer
        self.last_offer = offer
