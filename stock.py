# stock.py
from card import Card

class StockPile:
    def __init__(self, x, y, cards):
        self.cards = cards
        self.x = x
        self.y = y
        self.deal_index = 0

    def draw(self, screen):
        if self.deal_index < len(self.cards):
            # still show the next card-back placeholder if you like
            self.cards[self.deal_index].draw(screen)

    def deal(self, columns):
        """Deal one card to each of the 10 columns, face‑up."""
        if self.deal_index < len(self.cards):
            for i in range(10):
                card = self.cards[self.deal_index]
                card.face_up = True         # ← flip it face‑up
                # position it on top of column i:
                if columns[i]:
                    card.rect.x = columns[i][-1].rect.x
                    card.rect.y = columns[i][-1].rect.y + 30
                else:
                    card.rect.x = i * 90 + 30
                    card.rect.y = 150
                columns[i].append(card)
                self.deal_index += 1
