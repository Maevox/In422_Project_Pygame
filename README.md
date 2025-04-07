import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulateur d'Ordonnancement - IN422")

# Couleurs
WHITE = (245, 245, 245)
BLACK = (20, 20, 20)
GRAY = (200, 200, 200)
LIGHT_GRAY = (230, 230, 230)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 100, 150)
RED = (200, 50, 50)
GREEN = (50, 160, 90)

# Police
font = pygame.font.SysFont("Arial", 26)
title_font = pygame.font.SysFont("Arial", 36, bold=True)
input_font = pygame.font.SysFont("Arial", 22)

# Classe pour les champs de texte
class InputBox:
    def __init__(self, x, y, w, h, label):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = ''
        self.label = label
        self.txt_surface = input_font.render(self.text, True, BLACK)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                self.text += event.unicode
            self.txt_surface = input_font.render(self.text, True, BLACK)

    def update(self):
        self.color = BLUE if self.active else GRAY

    def draw(self, screen):
        label_surface = input_font.render(self.label, True, BLACK)
        screen.blit(label_surface, (self.rect.x - 110, self.rect.y + 7))
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, self.color, self.rect, 2)
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 7))

# Boutons des algorithmes
algorithms = ["FCFS", "SJN", "RR", "RM", "EDF"]
buttons = []
for i, algo in enumerate(algorithms):
    rect = pygame.Rect(40, 100 + i * 70, 180, 50)
    buttons.append((rect, algo))

# Champs de formulaire
labels = ["Nom:", "Arrivée:", "Durée:", "Deadline:"]
input_boxes = [InputBox(400, 160 + i * 60, 200, 40, labels[i]) for i in range(4)]

# Boutons supplémentaires
add_button = pygame.Rect(620, 250, 160, 45)
simulate_button = pygame.Rect(800, 250, 160, 45)

# Liste des tâches et erreurs
tasks = []
simulation_active = False
error_message = ""

# Fonctions d'affichage

def draw_buttons(mouse_pos):
    for rect, text in buttons:
        color = DARK_BLUE if rect.collidepoint(mouse_pos) else BLUE
        pygame.draw.rect(screen, color, rect, border_radius=10)
        label = font.render(text, True, WHITE)
        screen.blit(label, label.get_rect(center=rect.center))

def draw_display_area():
    pygame.draw.rect(screen, LIGHT_GRAY, (250, 80, 720, 480), border_radius=15)
    pygame.draw.rect(screen, GRAY, (250, 80, 720, 480), 3, border_radius=15)
    # Ne plus afficher l'étiquette ici
    
    pygame.draw.rect(screen, GRAY, (250, 80, 720, 480), 3, border_radius=15)

def draw_banner():
    pygame.draw.rect(screen, BLUE, (0, 0, WIDTH, 60))
    title = title_font.render("Visualisation des Algorithmes d'Ordonnancement", True, WHITE)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 12))

def draw_add_button(mouse_pos):
    color = DARK_BLUE if add_button.collidepoint(mouse_pos) else BLUE
    pygame.draw.rect(screen, color, add_button, border_radius=10)
    label = input_font.render("Ajouter Tâche", True, WHITE)
    screen.blit(label, label.get_rect(center=add_button.center))

def draw_simulate_button(mouse_pos):
    color = GREEN if simulate_button.collidepoint(mouse_pos) else DARK_BLUE
    pygame.draw.rect(screen, color, simulate_button, border_radius=10)
    label = input_font.render("Lancer Simulation", True, WHITE)
    screen.blit(label, label.get_rect(center=simulate_button.center))

def draw_task_list():
    y_offset = 430
    for i, task in enumerate(tasks[-5:]):
        task_text = f"Tâche {i+1} - Arr: {task['Arrivée']}, Durée: {task['Durée']}, DL: {task['Deadline']}"
        task_surface = input_font.render(task_text, True, BLACK)
        screen.blit(task_surface, (400, y_offset))
        y_offset += 25

def draw_fcfs_timeline():
    sorted_tasks = sorted(tasks, key=lambda t: int(t['Arrivée']))
    x_start = 270
    y_base = 610
    for task in sorted_tasks:
        duration = int(task['Durée'])
        rect_width = duration * 25
        pygame.draw.rect(screen, DARK_BLUE, (x_start, y_base, rect_width, 30))
        text = input_font.render(task['Nom'], True, WHITE)
        screen.blit(text, (x_start + 5, y_base + 5))
        x_start += rect_width + 10

def draw_edf_timeline():
    sorted_tasks = sorted(tasks, key=lambda t: int(t['Deadline']))
    x_start = 270
    y_base = 650
    for task in sorted_tasks:
        duration = int(task['Durée'])
        rect_width = duration * 25
        pygame.draw.rect(screen, GREEN, (x_start, y_base, rect_width, 30))
        text = input_font.render(task['Nom'], True, WHITE)
        screen.blit(text, (x_start + 5, y_base + 5))
        x_start += rect_width + 10

def draw_error():
    if error_message:
        error_surface = input_font.render(error_message, True, RED)
        screen.blit(error_surface, (400, 130))

# Boucle principale
selected_algo = None
running = True

while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    draw_banner()
    draw_buttons(mouse_pos)
    draw_display_area()
    draw_add_button(mouse_pos)
    draw_simulate_button(mouse_pos)
    draw_task_list()
    draw_error()

    if selected_algo:
        msg = font.render(f"Algorithme sélectionné : {selected_algo}", True, BLACK)
        screen.blit(msg, (400, 100))

    if simulation_active:
        label_text = f"Simulation : {selected_algo}"
        label_surface = input_font.render(label_text, True, BLACK)
        screen.blit(label_surface, (270, 580))
        if selected_algo == "FCFS":
            draw_fcfs_timeline()
        elif selected_algo == "EDF":
            draw_edf_timeline()

    for box in input_boxes:
        box.update()
        box.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if add_button.collidepoint(event.pos):
                task_data = {box.label.strip(":"): box.text for box in input_boxes}
                try:
                    int(task_data["Arrivée"])
                    int(task_data["Durée"])
                    int(task_data["Deadline"])
                    tasks.append(task_data)
                    for box in input_boxes:
                        box.text = ''
                        box.txt_surface = input_font.render('', True, BLACK)
                    error_message = ""
                    simulation_active = False
                except:
                    error_message = "Erreur : Arrivée, Durée et Deadline doivent être des nombres."

            if simulate_button.collidepoint(event.pos):
                simulation_active = True

            for rect, algo in buttons:
                if rect.collidepoint(mouse_pos):
                    selected_algo = algo
                    simulation_active = False

        for box in input_boxes:
            box.handle_event(event)

    pygame.display.flip()

pygame.quit()
sys.exit()
