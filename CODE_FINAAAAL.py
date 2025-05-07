# -*- coding: utf‑8 -*-
"""
Ordonnanceur IN422 – version avec COMPARAISON des algorithmes

"""

import sys
import os
import pygame
import matplotlib
matplotlib.use("Agg")            # backend non‑interactif pour Pygame
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

from config import *
from algorithms import *
from metrics import *
from ui import *

# ---------------------------------------------------------------------------
# Initialisation Pygame
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w - 100, info.current_h - 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulateur d'Ordonnancement – IN422")
clock = pygame.time.Clock()



# ---------------------------------------------------------------------------
# INTERFACE : initialisation des composants ----------------------------------
def init_components():
    global buttons, input_boxes, add_button, compare_button, data_button, clear_button
    global compare_back_btn, current_labels

    # Boutons algorithmes
    buttons = []
    for i, algo in enumerate(algorithms):
        rect = pygame.Rect(40, 120 + i * 80, 200, 60)
        buttons.append((rect, algo))

    # Champs de saisie par défaut (FCFS)
    current_labels = ["Nom:", "Arrivee:", "Duree:"]
    base_x = 300
    input_boxes[:] = [InputBox(base_x + 150, 200 + i * 60,
                               250, 45, current_labels[i], is_numeric=(i>0))
                      for i in range(len(current_labels))]

    # Boutons actions
    add_button     = pygame.Rect(base_x + 570, 210, 200, 50)
    compare_button = pygame.Rect(base_x + 570, 280, 200, 50)
    data_button    = pygame.Rect(base_x + 570, 350, 200, 50)
    clear_button   = pygame.Rect(base_x + 570, 420, 200, 50)

    # Bouton retour page comparaison
    compare_back_btn = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 120, 150, 40)

# ---------------------------------------------------------------------------
# DESSIN UI – bannières, boutons, etc.  --------------------------------------
def draw_banner():
    pygame.draw.rect(screen, BLUE, (0, 0, SCREEN_WIDTH, 70))
    title = title_font.render("Visualisation des Algorithmes d'Ordonnancement", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 15))

def draw_buttons(mouse):
    for rect, txt in buttons:
        color = DARK_BLUE if rect.collidepoint(mouse) else BLUE
        pygame.draw.rect(screen, color, rect, border_radius=10)
        lab = font.render(txt, True, WHITE)
        screen.blit(lab, (rect.centerx-lab.get_width()//2,
                          rect.centery-lab.get_height()//2))

def draw_action_button(rect, txt, mouse, color_on=DARK_BLUE, color_off=BLUE):
    col = color_on if rect.collidepoint(mouse) else color_off
    pygame.draw.rect(screen, col, rect, border_radius=10)
    lab = input_font.render(txt, True, WHITE)
    screen.blit(lab, (rect.centerx - lab.get_width()//2,
                      rect.centery - lab.get_height()//2))

def draw_input_panel():
    w, h, x, y = 550, 400, 300, 120
    pygame.draw.rect(screen, LIGHT_GRAY, (x, y, w, h), border_radius=10)
    pygame.draw.rect(screen, GRAY,       (x, y, w, h), 2, border_radius=10)
    title = font.render("Paramètres des Tâches", True, BLACK)
    screen.blit(title, (x + (w-title.get_width())//2, y+20))

def draw_task_list():
    x0, y = 1100, 150
    for task in tasks[-5:]:
        txt = f"{task['Nom']}"
        if 'Arrivee' in task:   txt += f" - Arr:{task['Arrivee']}"
        if 'Duree'   in task:   txt += f", Dur:{task['Duree']}"
        if 'Deadline'in task:   txt += f", DL:{task['Deadline']}"
        if 'Priorite'in task:   txt += f", Prio:{task['Priorite']}"
        if 'Execution'in task:  txt += f", Exec:{task['Execution']}"
        surf = small_font.render(txt, True, BLACK)
        screen.blit(surf, (x0+20, y))
        y += 30

def draw_error():
    if error_message:
        surf = input_font.render(error_message, True, RED)
        screen.blit(surf, (400, 130))

# ---------------------------------------------------------------------------
# FRISE DE SIMULATION ---------------------------------------------------------
def draw_timeline(schedule, y_pos, color, title):
    if not schedule: return
    max_t = MAX_TIMELINE
    w_tl  = SCREEN_WIDTH - 300
    scale = w_tl / max_t
    h     = 35
    
    # Titre
    screen.blit(font.render(title, True, BLACK), (170, y_pos-80))
    
    # Organisation pour éviter chevauchements
    time_slots, arranged = {}, []
    for name, start, dur in schedule:
        if start >= max_t: continue
        dur = min(dur, max_t-start)
        end = start + dur
        line = 0
        while True:
            free = all(end<=s or start>=e for s,e in time_slots.get(line, []))
            if free: break
            line += 1
        time_slots.setdefault(line, []).append((start,end))
        arranged.append((name,start,dur,line))
    
    # Dessin
    for name,s,d,line in arranged:
        x = 170 + s*scale
        w = max(2, d*scale)
        y = y_pos + line*(h+5)
        pygame.draw.rect(screen, color, (x,y,w,h), border_radius=3)
        
        # Modification ici : afficher le nom même pour les petites tâches
        if w > 5:  # Même les petites tâches auront leur nom
            lab = small_font.render(name, True, WHITE)
            # Centrer le texte si possible
            if w > lab.get_width():
                screen.blit(lab, (x + (w - lab.get_width())//2, y + 10))
            else:
                # Pour les très petites tâches, on tronque ou on met juste la première lettre
                short_name = name[0] if name else ""
                short_lab = small_font.render(short_name, True, WHITE)
                screen.blit(short_lab, (x + 2, y + 10))
    
    # Axe temps
    total_lines = len(time_slots)
    for t in range(0, max_t+1, 5):
        xp = 170 + t*scale
        pygame.draw.line(screen, BLACK,
                         (xp, y_pos+total_lines*(h+5)+5),
                         (xp, y_pos+total_lines*(h+5)+15), 2)
        screen.blit(small_font.render(str(t),True,BLACK),
                    (xp-10, y_pos+total_lines*(h+5)+20))
    
    # Limite
    if any(s+d>MAX_TIMELINE for _,s,d,_ in arranged):
        warn = small_font.render(f"(Limité à {MAX_TIMELINE} unités)", True, RED)
        screen.blit(warn, (SCREEN_WIDTH-200, y_pos-40))

def draw_simulation():
    if selected_algo == "FCFS":
        if all({'Arrivee','Duree'}<=t.keys() for t in tasks):
            sched = [(t['Nom'], int(t['Arrivee']), int(t['Duree']))
                     for t in fcfs_schedule(tasks) if int(t['Arrivee'])<MAX_TIMELINE]
            draw_timeline(sched, SCREEN_HEIGHT-160, BLUE, "FCFS")
        else:
            return "FCFS nécessite Arrivée + Durée"
    elif selected_algo == "SJN":
        if all({'Arrivee','Duree'}<=t.keys() for t in tasks):
            sched = [(t['Nom'], int(t['Arrivee']), int(t['Duree']))
                     for t in sjn_schedule(tasks) if int(t['Arrivee'])<MAX_TIMELINE]
            draw_timeline(sched, SCREEN_HEIGHT-160, GREEN, "SJN")
        else:
            return "SJN nécessite Arrivée + Durée"
    elif selected_algo == "RR":
        if all({'Arrivee','Duree'}<=t.keys() for t in tasks):
            sched = rr_schedule(tasks, time_quantum, MAX_TIMELINE)
            draw_timeline(sched, SCREEN_HEIGHT-160, RED,
                          f"RR (Quantum={time_quantum})")
        else:
            return "RR nécessite Arrivée + Durée"
    elif selected_algo == "RM":
        if all({'Arrivee','Priorite','Execution'}<=t.keys() for t in tasks):
            sched = rm_schedule(tasks, MAX_TIMELINE)
            draw_timeline(sched, SCREEN_HEIGHT-160, ORANGE, "RM")
        else:
            return "RM nécessite Arrivée + Priorité + Execution"
    elif selected_algo == "EDF":
        if all({'Duree','Deadline'}<=t.keys() for t in tasks):
            sched = edf_schedule(tasks, MAX_TIMELINE)
            draw_timeline(sched, SCREEN_HEIGHT-160, PURPLE, "EDF")
        else:
            return "EDF nécessite Durée + Deadline"
    return ""

# ---------------------------------------------------------------------------
# PAGE COMPARAISON -----------------------------------------------------------
def generate_comparison(metrics_dict):
    """
    Génère le PNG et renvoie le pygame.Surface correspondant.
    """
    algos      = list(metrics_dict.keys())
    waitings   = [v[0] for v in metrics_dict.values()]
    turns      = [v[1] for v in metrics_dict.values()]
    cpu_utils  = [v[2] for v in metrics_dict.values()]


    x = np.arange(len(algos))
    width = 0.25
    plt.figure(figsize=(5,3.5))



    plt.bar(x-width, waitings, width, label="Attente (moy.)")
    plt.bar(x,        turns,   width, label="Exécution (moy.)")
    plt.bar(x+width,  cpu_utils,width, label="CPU (%)")
    plt.xticks(x, algos)
    plt.ylabel("Valeur")
    plt.title("Comparaison des performances")
    plt.legend()
    path = os.path.join(os.getcwd(), "comparison.png")
    plt.tight_layout()
    plt.savefig(path, dpi=120)
    plt.close()

    img = pygame.image.load(path).convert()
    # Redimension plus petit (manuellement)
    img = pygame.transform.smoothscale(img, (int(img.get_width() * 0.8), int(img.get_height() * 0.8)))

    # redimensionner si trop large
    max_w = SCREEN_WIDTH - 200
    if img.get_width() > max_w:
        scale = max_w / img.get_width()
        new_h = int(img.get_height()*scale)
        img   = pygame.transform.smoothscale(img, (max_w, new_h))
    return img

def draw_comparison_page():
    # fond
    pygame.draw.rect(screen, LIGHT_GRAY,
                     (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), border_radius=15)
    pygame.draw.rect(screen, GRAY,
                     (50, 50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), 2, border_radius=15)
 
    # titre
    t = title_font.render("Comparaison des Algorithmes", True, BLACK)
    screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 70))
 
    # valeurs numériques
    y0 = 160
    max_label_width = 0
    for algo, (w,tau,cpu) in comparison_metrics.items():
        txt = f"{algo:<4}  |  Attente: {w:>6}  |  Exécution: {tau:>6}  |  CPU: {cpu:>6}%"
        surf = font.render(txt, True, BLACK)
        screen.blit(surf, (100, y0))
        max_label_width = max(max_label_width, surf.get_width())
        y0 += 40
 
    # graphique à droite
    if comparison_surface:
        graph_x = 100 + max_label_width + 50
        graph_y = 160
        screen.blit(comparison_surface, (graph_x, graph_y))
 
    # bouton retour
    pygame.draw.rect(screen, DARK_BLUE, compare_back_btn, border_radius=8)
    lab = font.render("Retour", True, WHITE)
    screen.blit(lab, (compare_back_btn.centerx - lab.get_width()//2,
                      compare_back_btn.centery - lab.get_height()//2))

# ---------------------------------------------------------------------------
# FONCTIONS UTILITAIRES ------------------------------------------------------
def update_input_boxes():
    global current_labels, input_boxes
    if selected_algo == "RM":
        current_labels = ["Nom:", "Arrivee:", "Priorite:", "Execution:"]
    elif selected_algo == "EDF":
        current_labels = ["Nom:", "Duree:", "Deadline:"]
    else:
        current_labels = ["Nom:", "Arrivee:", "Duree:"]

    base_x = 300
    input_boxes[:] = [InputBox(base_x + 150, 200 + i*60,
                               250, 45, current_labels[i], is_numeric=(i>0))
                      for i in range(len(current_labels))]

def clear_inputs():
    for box in input_boxes:
        box.text = ''
        box.txt_surface = input_font.render('', True, BLACK)

def algorithms_applicable(tsk):
    """
    Renvoie la liste des algorithmes dont les champs requis sont présents
    dans toutes les tâches.
    """
    fields_by_algo = {
        "FCFS": {"Arrivee","Duree"},
        "SJN" : {"Arrivee","Duree"},
        "RR"  : {"Arrivee","Duree"},
        "RM"  : {"Arrivee","Priorite","Execution"},
        "EDF" : {"Duree","Deadline"}
    }
    ok = []
    for algo in algorithms:
        needed = fields_by_algo[algo]
        if all(needed <= set(t.keys()) for t in tsk):
            ok.append(algo)
    return ok

def schedule_for(algo):
    if   algo=="FCFS": return [(t['Nom'], int(t['Arrivee']), int(t['Duree']))
                               for t in fcfs_schedule(tasks)]
    elif algo=="SJN" : return [(t['Nom'], int(t['Arrivee']), int(t['Duree']))
                               for t in sjn_schedule(tasks)]
    elif algo=="RR"  : return rr_schedule(tasks, time_quantum, MAX_TIMELINE)
    elif algo=="RM"  : return rm_schedule(tasks, MAX_TIMELINE)
    else:              return edf_schedule(tasks, MAX_TIMELINE)

# ---------------------------------------------------------------------------
# VARIABLES D’ÉTAT -----------------------------------------------------------
tasks               = []
input_boxes         = []
selected_algo       = None
simulation_active   = False
error_message       = ""
current_page        = "main"          # main | data | compare
selected_task_index = None
comparison_metrics  = {}
comparison_surface  = None

# composant visuels
init_components()

# ---------------------------------------------------------------------------
# BOUCLE PRINCIPALE ----------------------------------------------------------
running = True
while running:
    mouse = pygame.mouse.get_pos()
    screen.fill(WHITE)

    # ---- AFFICHAGE ---------------------------------------------------------
    if current_page == "main":
        draw_banner()
        draw_buttons(mouse)
        draw_input_panel()
        draw_action_button(add_button,      "Ajouter Tâche",  mouse)
        draw_action_button(compare_button,  "Comparaison",    mouse, ORANGE, PURPLE)
        draw_action_button(data_button,     "Data",           mouse, ORANGE, PURPLE)
        draw_action_button(clear_button,    "Effacer Tout",   mouse, RED, (200,50,50))
        draw_task_list()
        draw_error()

        if selected_algo:
            lab = pygame.font.SysFont("Arial", 28, bold=True).render(
                    f"Algorithme sélectionné : {selected_algo}", True, BLACK)
            screen.blit(lab, (500, 77))

        if simulation_active and selected_algo:
            err = draw_simulation()
            if err: error_message = err

        for box in input_boxes:
            box.update(); box.draw(screen)

    elif current_page == "compare":
        draw_comparison_page()

    # elif current_page == "data":
        # # (page de gestion des tâches inchangée)
        # pygame.draw.rect(screen, LIGHT_GRAY,
        #                  (50,50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), border_radius=15)
        # pygame.draw.rect(screen, GRAY,
        #                  (50,50, SCREEN_WIDTH-100, SCREEN_HEIGHT-100), 2, border_radius=15)
        # t = title_font.render("Gestion des Tâches", True, BLACK)
        # screen.blit(t, (SCREEN_WIDTH//2 - t.get_width()//2, 70))
        # # liste + boutons + champs (identique à version précédente)
        # # (afin de ne pas alourdir, le code de la page « data » reste celui de votre base)

    elif current_page == "data":
        # Fond
        pygame.draw.rect(screen, LIGHT_GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), border_radius=15)
        pygame.draw.rect(screen, GRAY, (50, 50, SCREEN_WIDTH - 100, SCREEN_HEIGHT - 100), 2, border_radius=15)

        # Titre
        title = title_font.render("Gestion des Tâches", True, BLACK)
        screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 70))

        # Liste des tâches
        for i, task in enumerate(tasks):
            y_pos = 150 + i * 40
            bg_color = DARK_BLUE if i == selected_task_index else BLUE
            pygame.draw.rect(screen, bg_color, (100, y_pos, SCREEN_WIDTH - 200, 35), border_radius=5)

            task_text = f"{i+1}. {task['Nom']}"
            if 'Arrivee' in task:
                task_text += f" - Arr: {task['Arrivee']}"
            if 'Duree' in task:
                task_text += f", Dur: {task['Duree']}"
            if 'Deadline' in task:
                task_text += f", DL: {task['Deadline']}"
            if 'Priorite' in task:
                task_text += f", Prio: {task['Priorite']}"
            if 'Execution' in task:
                task_text += f", Exec: {task['Execution']}"

            task_surface = small_font.render(task_text, True, WHITE)
            screen.blit(task_surface, (110, y_pos + 7))

        # Boutons
        add_btn = pygame.Rect(100, SCREEN_HEIGHT - 150, 150, 40)
        save_btn = pygame.Rect(270, SCREEN_HEIGHT - 150, 150, 40)
        delete_btn = pygame.Rect(440, SCREEN_HEIGHT - 150, 150, 40)
        back_btn = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 150, 40)

        pygame.draw.rect(screen, GREEN, add_btn, border_radius=5)
        pygame.draw.rect(screen, BLUE, save_btn, border_radius=5)
        pygame.draw.rect(screen, RED, delete_btn, border_radius=5)
        pygame.draw.rect(screen, DARK_BLUE, back_btn, border_radius=5)

        screen.blit(font.render("Ajouter", True, WHITE), (add_btn.x + 35, add_btn.y + 10))
        screen.blit(font.render("Enregistrer", True, WHITE), (save_btn.x + 15, save_btn.y + 10))
        screen.blit(font.render("Supprimer", True, WHITE), (delete_btn.x + 25, delete_btn.y + 10))
        screen.blit(font.render("Retour", True, WHITE), (back_btn.x + 40, back_btn.y + 10))

        # Champs de saisie
        for box in input_boxes:
            box.update()
            box.draw(screen)


    pygame.display.flip()

    # ---- ÉVÉNEMENTS -------------------------------------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Gestion clavier pour input boxes
        for box in input_boxes:
            box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            # -- PAGE MAIN --
            if current_page == "main":
                # sélection algo
                for rect, algo in buttons:
                    if rect.collidepoint(event.pos):
                        selected_algo = algo
                        simulation_active = True
                        update_input_boxes()
                        error_message = ""
                        clear_inputs()

                # ajout tâche
                if add_button.collidepoint(event.pos):
                    if not selected_algo:
                        error_message = "Sélectionnez d'abord un algorithme"
                        continue
                    task = {'Nom': input_boxes[0].text.strip()}
                    try:
                        if not task['Nom']:
                            raise ValueError("Le nom est requis")

                        if selected_algo=="RM":
                            task.update({'Arrivee': input_boxes[1].text,
                                         'Priorite':input_boxes[2].text,
                                         'Execution':input_boxes[3].text})
                            int(task['Arrivee']); int(task['Priorite']); int(task['Execution'])
                        elif selected_algo=="EDF":
                            task.update({'Duree':input_boxes[1].text,
                                         'Deadline':input_boxes[2].text})
                            int(task['Duree']);  int(task['Deadline'])
                        else:
                            task.update({'Arrivee':input_boxes[1].text,
                                         'Duree':input_boxes[2].text})
                            int(task['Arrivee']); int(task['Duree'])

                        tasks.append(task)
                        clear_inputs()
                        error_message=""
                    except ValueError as e:
                        error_message=f"Erreur: {e}"

                # clic sur « Comparaison »
                if compare_button.collidepoint(event.pos):
                    if not tasks:
                        error_message = "Aucune tâche à comparer"
                        continue
                    applicable = algorithms_applicable(tasks)
                    if len(applicable) < 2:
                        error_message = "Les algorithmes ne sont pas comparables (champs manquants)"
                        continue

                    comparison_metrics.clear()
                    for algo in applicable:
                        sched = schedule_for(algo)
                        m = metrics_from_schedule(tasks, sched, algo)
                        if m:  comparison_metrics[algo] = m

                    if len(comparison_metrics) < 2:
                        error_message = "Comparaison impossible – toutes les tâches ne sont pas planifiées"
                        continue

                    comparison_surface = generate_comparison(comparison_metrics)
                    current_page = "compare"
                    error_message = ""

                # page Data
                if data_button.collidepoint(event.pos):
                    current_page = "data"
                    selected_task_index = None
                    clear_inputs()

                # effacer tout
                if clear_button.collidepoint(event.pos):
                    tasks.clear()
                    simulation_active=False
                    selected_algo=None
                    update_input_boxes()
                    error_message=""

            # -- PAGE COMPARAISON --
            elif current_page == "compare":
                if compare_back_btn.collidepoint(event.pos):
                    current_page = "main"

            # -- PAGE DATA 
            elif current_page == "data":
                # Gestion de la sélection d'une tâche
                for i in range(len(tasks)):
                    task_rect = pygame.Rect(100, 150 + i * 40, SCREEN_WIDTH - 200, 35)
                    if task_rect.collidepoint(event.pos):
                        selected_task_index = i
                        task = tasks[i]
                        for box in input_boxes:
                            key = box.label.strip(":")
                            if key in task:
                                box.text = str(task[key])
                                box.txt_surface = input_font.render(box.text, True, BLACK)
                
                # Bouton Ajouter
                add_btn = pygame.Rect(100, SCREEN_HEIGHT - 150, 150, 40)
                if add_btn.collidepoint(event.pos):
                    task_data = {}
                    for box in input_boxes:
                        key = box.label.strip(":")
                        task_data[key] = box.text
                    
                    try:
                        # Validation des champs numériques selon l'algorithme
                        if selected_algo == "RM":
                            int(task_data['Arrivee'])
                            int(task_data['Priorite'])
                            int(task_data['Execution'])
                        elif selected_algo == "EDF":
                            int(task_data['Duree'])
                            int(task_data['Deadline'])
                        else:  # FCFS, SJN, RR
                            int(task_data['Arrivee'])
                            int(task_data['Duree'])
                        
                        tasks.append(task_data)
                        for box in input_boxes:
                            box.text = ''
                            box.txt_surface = input_font.render('', True, BLACK)
                        selected_task_index = None
                    except ValueError:
                        pass
                
                # Bouton Enregistrer
                save_btn = pygame.Rect(270, SCREEN_HEIGHT - 150, 150, 40)
                if save_btn.collidepoint(event.pos) and selected_task_index is not None:
                    task_data = {}
                    for box in input_boxes:
                        key = box.label.strip(":")
                        task_data[key] = box.text
                    
                    try:
                        # Validation des champs numériques selon l'algorithme
                        if selected_algo == "RM":
                            int(task_data['Arrivee'])
                            int(task_data['Priorite'])
                            int(task_data['Execution'])
                        elif selected_algo == "EDF":
                            int(task_data['Duree'])
                            int(task_data['Deadline'])
                        else:  # FCFS, SJN, RR
                            int(task_data['Arrivee'])
                            int(task_data['Duree'])
                        
                        tasks[selected_task_index] = task_data
                        selected_task_index = None
                        for box in input_boxes:
                            box.text = ''
                            box.txt_surface = input_font.render('', True, BLACK)
                    except ValueError:
                        pass
                
                # Bouton Supprimer
                delete_btn = pygame.Rect(440, SCREEN_HEIGHT - 150, 150, 40)
                if delete_btn.collidepoint(event.pos) and selected_task_index is not None:
                    tasks.pop(selected_task_index)
                    selected_task_index = None
                    for box in input_boxes:
                        box.text = ''
                        box.txt_surface = input_font.render('', True, BLACK)
                
                # Bouton Retour
                back_btn = pygame.Rect(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 150, 150, 40)
                if back_btn.collidepoint(event.pos):
                    current_page = "main"
                    selected_task_index = None

    
    pygame.display.flip()   
    clock.tick(30)

pygame.quit()
sys.exit()