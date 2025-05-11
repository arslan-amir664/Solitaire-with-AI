# utils.py
def get_card_at_pos(columns, mouse_pos):
    spacing_x = 85
    spacing_y = 25
    start_x = 20
    start_y = 20

    for col_index, column in enumerate(columns):
        for card_index in range(len(column)):
            x = start_x + col_index * spacing_x
            y = start_y + card_index * spacing_y
            rect = pygame.Rect(x, y, 70, 100)
            if rect.collidepoint(mouse_pos) and column[card_index].face_up:
                return col_index, card_index
    return None, None
