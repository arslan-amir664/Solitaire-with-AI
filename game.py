# game.py
import pygame
from card import Card
from stock import StockPile
import random
from settings import CARD_WIDTH, CARD_HEIGHT  

class Game:
    def __init__(self):
        self.columns = [[] for _ in range(10)]
        self.completed_sequences = 0    # just a count now
        self.selected_cards = []
        self.original_column_index = None
        self.offset = 30
        self.create_cards()
        self.stock_pile = StockPile(900, 600, self.stock_cards)
        # prepare a font for drawing the check mark
        self.font = pygame.font.SysFont(None, 24)

    def create_cards(self):
        deck = [Card(val, 0, 0, False) for val in range(1, 14) for _ in range(8)]
        random.shuffle(deck)
        self.stock_cards = deck[54:]
        deck = deck[:54]

        col_index = 0
        for i, card in enumerate(deck):
            x = col_index * (CARD_WIDTH + 10) + 30
            y = 150 + self.offset * len(self.columns[col_index])
            card.rect.x, card.rect.y = x, y
            card.face_up = i >= 44
            self.columns[col_index].append(card)
            col_index = (col_index + 1) % 10

    def draw(self, screen):
        # Draw empty placeholders first (gray outline for empty columns)
        for i, column in enumerate(self.columns):
            if not column:
                x = 30 + i * (CARD_WIDTH + 10)
                y = 150
                pygame.draw.rect(screen, (50, 50, 50), (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=5)

        # Draw actual cards in columns
        for column in self.columns:
            for card in column:
                card.draw(screen)

        # Draw stock pile
        self.stock_pile.draw(screen)

        # Draw completed sequence markers
        for i in range(self.completed_sequences):
            x = 30 + i * (CARD_WIDTH + 10)
            y = 20
            pygame.draw.rect(screen, (255, 255, 255), (x, y, CARD_WIDTH, CARD_HEIGHT), border_radius=8)
            pygame.draw.rect(screen, (0, 0, 0), (x, y, CARD_WIDTH, CARD_HEIGHT), 2, border_radius=8)
            check = self.font.render("✔", True, (0, 0, 0))
            screen.blit(check, check.get_rect(center=(x + CARD_WIDTH / 2, y + CARD_HEIGHT / 2)))


    def handle_mouse_down(self, pos):
        for col_idx, column in enumerate(self.columns):
            for i in range(len(column)-1, -1, -1):
                card = column[i]
                if card.face_up and card.rect.collidepoint(pos):
                    if self.valid_drag_sequence(column[i:]):
                        for c in column[i:]:
                            c.dragging = True
                            c.offset_x = pos[0] - c.rect.x
                            c.offset_y = pos[1] - c.rect.y
                        self.selected_cards = column[i:]
                        self.columns[col_idx] = column[:i]
                        self.original_column_index = col_idx
                        return
                    break

    def handle_mouse_up(self, pos):
        if not self.selected_cards:
            return

        for col_idx, column in enumerate(self.columns):
            if column:
                # Check if drop is valid (onto a card that is exactly +1)
                if column[-1].rect.collidepoint(pos) and \
                    column[-1].value == self.selected_cards[0].value + 1:
                    self.place_cards(column)
                    self.reveal_top_card(self.original_column_index)
                    self.original_column_index = None
                    self.check_for_completed_sequences()
                    return
            else:
                # This is an empty column — define a fake rect to detect drop
                empty_x = 30 + col_idx * (CARD_WIDTH + 10)
                empty_y = 150
                empty_rect = pygame.Rect(empty_x, empty_y, CARD_WIDTH, CARD_HEIGHT)

                if empty_rect.collidepoint(pos):
                    self.place_cards(column)
                    self.reveal_top_card(self.original_column_index)
                    self.original_column_index = None
                    self.check_for_completed_sequences()
                    return

        # Invalid drop — return cards to original column
        self.return_cards()
        self.selected_cards.clear()
        self.original_column_index = None

    def handle_mouse_motion(self, pos):
        for card in self.selected_cards:
            card.update_position(pos[0], pos[1])

    def place_cards(self, column):
        x = column[-1].rect.x if column else 30 + (CARD_WIDTH + 10) * self.columns.index(column)
        y = column[-1].rect.y + self.offset if column else 150
        for card in self.selected_cards:
            card.rect.x = x
            card.rect.y = y
            y += self.offset
            column.append(card)
        self.selected_cards.clear()
        # (original_column_index reset happens in handle_mouse_up)

    def return_cards(self):
        if self.original_column_index is None:
            return
        x = 30 + (CARD_WIDTH + 10) * self.original_column_index
        y = 150 + self.offset * len(self.columns[self.original_column_index])
        for card in self.selected_cards:
            card.rect.x = x
            card.rect.y = y
            y += self.offset
            self.columns[self.original_column_index].append(card)
        self.selected_cards.clear()
        self.original_column_index = None

    def valid_drag_sequence(self, cards):
        return all(cards[i].value == cards[i+1].value + 1 for i in range(len(cards)-1))

    def check_for_completed_sequences(self):
        """If a column’s *top* 13 cards are K→A, remove them and increment counter."""
        for idx, column in enumerate(self.columns):
            if len(column) >= 13:
                top13 = column[-13:]
                if all(top13[i].value == 13 - i for i in range(13)):
                    # remove them
                    del column[-13:]
                    # flip new top if present
                    if column and not column[-1].face_up:
                        column[-1].face_up = True
                    # count it
                    self.completed_sequences += 1
                    print(f"[DEBUG] Completed sequence #{self.completed_sequences} from column {idx}")
                    break

    def reveal_top_card(self, col_idx):
        if col_idx is None:
            return
        column = self.columns[col_idx]
        if column and not column[-1].face_up:
            column[-1].face_up = True

    def deal_stock(self):
        self.stock_pile.deal(self.columns)

    def suggest_move(self):
        best_move = None
        best_score = -999

        for from_col_idx, from_col in enumerate(self.columns):
            for i in range(len(from_col)):
                card = from_col[i]
                if not card.face_up:
                    continue

                sequence = from_col[i:]
                if not self.valid_drag_sequence(sequence):
                    continue

                for to_col_idx, to_col in enumerate(self.columns):
                    if from_col_idx == to_col_idx:
                        continue

                    if to_col and to_col[-1].value == card.value + 1:
                        score = 0
                        # +3 if flipping a face-down card
                        if i > 0 and not from_col[i - 1].face_up:
                            score += 3
                        # +5 if it's a full sequence K → A
                        if len(sequence) == 13 and sequence[0].value == 13:
                            score += 5
                        if not to_col:
                            score += 2  # optional reward for empty drop
                        if score > best_score:
                            best_score = score
                            best_move = (card.value, from_col_idx, to_col_idx)

                    elif not to_col:
                        score = 1
                        if i > 0 and not from_col[i - 1].face_up:
                            score += 2
                        if score > best_score:
                            best_score = score
                            best_move = (card.value, from_col_idx, to_col_idx)

        if best_move:
            val, from_col, to_col = best_move
            print(f"[AI SUGGESTION] Move card {val} from column {from_col + 1} to column {to_col + 1}")
        else:
            print("[AI SUGGESTION] No valid moves found.")

