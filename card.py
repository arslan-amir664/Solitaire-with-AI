# card.py
import pygame
from settings import CARD_WIDTH, CARD_HEIGHT

class Card:
    def __init__(self, value, x, y, face_up=True):
        self.value = value  # 1 (A) to 13 (K)
        self.rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        self.face_up = face_up
        self.dragging = False
        self.offset_x = 0
        self.offset_y = 0

    def draw(self, screen):
        color = (255, 255, 255) if self.face_up else (200, 0, 0)
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        if self.face_up:
            font = pygame.font.SysFont("arial", 20)
            text = font.render(str(self.value), True, (0, 0, 0))
            screen.blit(text, (self.rect.x + 10, self.rect.y + 10))

    def update_position(self, x, y):
        self.rect.x = x - self.offset_x
        self.rect.y = y - self.offset_y
