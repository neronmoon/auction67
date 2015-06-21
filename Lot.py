# -*- coding: utf-8 -*-

class Lot:
    def __init__(self, title, start_price, members):
        self.title = title
        self.start_price = float(start_price)
        self.members = members

    def format_price(self, price):
        return u'{:20,.2f} р.'.format(float(price)).strip()

    def start_price_formated(self):
        return self.format_price(self.start_price)

    def has_owner(self):
        # for member in self.members:
        #     if member['isOwner']:
        #         return True
        return False

    def get_owner(self):
        for member in self.members:
            if member['isOwner']:
                return member

    def get_start_price_step(self, formated=True):
        value = (float(self.start_price) * 5) / 100
        if formated:
            return self.format_price(value)
        return value
