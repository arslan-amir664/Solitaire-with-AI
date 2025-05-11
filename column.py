# column.py
from card import Card
import random

def generate_columns():
    values = [i for i in range(1, 14)] * 8  # One-suit: 8 decks
    random.shuffle(values)

    columns = [[] for _ in range(10)]
    index = 0

    for col in range(10):
        num_cards = 6 if col < 4 else 5
        for i in range(num_cards):
            face_up = (i == num_cards - 1)
            card = Card(values[index], face_up)
            columns[col].append(card)
            index += 1

    return columns
