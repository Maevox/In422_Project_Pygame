# UI components extracted from CODE_FINAAAAL.py
from config import *
import pygame

class InputBox:
    def __init__(self, x, y, w, h, label, is_numeric=False):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = ''
        self.label = label
        self.txt_surface = input_font.render(self.text, True, BLACK)
        self.active = False
        self.is_numeric = is_numeric

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            elif not self.is_numeric or event.unicode.isdigit():
                self.text += event.unicode
            self.txt_surface = input_font.render(self.text, True, BLACK)

    def update(self):
        self.color = BLUE if self.active else GRAY

    def draw(self, surf):
        # libellé
        label_surface = input_font.render(self.label, True, BLACK)
        surf.blit(label_surface, (self.rect.x - 110, self.rect.y + 7))
        # zone
        pygame.draw.rect(surf, WHITE, self.rect)
        pygame.draw.rect(surf, self.color, self.rect, 2)
        surf.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 7))

# ---------------------------------------------------------------------------
# ALGORITHMES D’ORDONNANCEMENT ------------------------------------------------
