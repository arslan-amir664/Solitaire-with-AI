import pygame
from settings import *
from game import Game

pygame.init()

# ——— Setup screen & font ———
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spider Solitaire - One Suit")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 24)

# ——— UI Buttons ———
DEAL_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - 170, 20, 150, 40)
RESTART_BUTTON_RECT = pygame.Rect(SCREEN_WIDTH - 340, 20, 150, 40)

# ——— Start the Game ———
game = Game()

running = True
while running:
    screen.fill((0, 130, 0))  # Green background

    # ——— Draw game state ———
    game.draw(screen)

    # ——— Draw “Deal Next” button ———
    pygame.draw.rect(screen, (200, 200, 200), DEAL_BUTTON_RECT, border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), DEAL_BUTTON_RECT, 2, border_radius=5)
    deal_text = font.render("Deal Next", True, (0, 0, 0))
    deal_text_rect = deal_text.get_rect(center=DEAL_BUTTON_RECT.center)
    screen.blit(deal_text, deal_text_rect)

    # ——— Draw “Restart Game” button ———
    pygame.draw.rect(screen, (200, 200, 200), RESTART_BUTTON_RECT, border_radius=5)
    pygame.draw.rect(screen, (0, 0, 0), RESTART_BUTTON_RECT, 2, border_radius=5)
    restart_text = font.render("Restart Game", True, (0, 0, 0))
    restart_text_rect = restart_text.get_rect(center=RESTART_BUTTON_RECT.center)
    screen.blit(restart_text, restart_text_rect)

    # ——— Handle Events ———
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game.suggest_move()  # 🧠 Suggestion logic
            elif event.key == pygame.K_r:
                game = Game()  # 🔁 Optional keyboard shortcut for restart

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if RESTART_BUTTON_RECT.collidepoint(event.pos):
                    game = Game()  # 🔁 Restart the game
                elif DEAL_BUTTON_RECT.collidepoint(event.pos):
                    game.deal_stock()
                else:
                    game.handle_mouse_down(event.pos)
            elif event.button == 3:
                game.deal_stock()

        elif event.type == pygame.MOUSEBUTTONUP:
            game.handle_mouse_up(event.pos)

        elif event.type == pygame.MOUSEMOTION:
            game.handle_mouse_motion(event.pos)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
