# -*- coding: utf‑8 -*-
"""
Ordonnanceur IN422 – version avec COMPARAISON des algorithmes
© 2025
"""

import sys
import os
import pygame
import matplotlib
matplotlib.use("Agg")            # backend non‑interactif pour Pygame
import matplotlib.pyplot as plt
import numpy as np
from collections import deque

# ---------------------------------------------------------------------------
# Initialisation Pygame
pygame.init()
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w - 100, info.current_h - 100
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simulateur d'Ordonnancement – IN422")
clock = pygame.time.Clock()

# ---------------------------------------------------------------------------
# Couleurs & Polices
WHITE       = (245, 245, 245)
BLACK       = (20, 20, 20)
GRAY        = (200, 200, 200)
LIGHT_GRAY  = (230, 230, 230)
BLUE        = ( 70, 130, 180)
DARK_BLUE   = ( 40, 100, 150)
RED         = (200,  50,  50)
GREEN       = ( 50, 160,  90)
ORANGE      = (255, 165,   0)
PURPLE      = (128,   0, 128)

font       = pygame.font.SysFont("Arial", 28)
title_font = pygame.font.SysFont("Arial", 40, bold=True)
input_font = pygame.font.SysFont("Arial", 24)
small_font = pygame.font.SysFont("Arial", 20)

# ---------------------------------------------------------------------------
# Paramètres généraux
algorithms      = ["FCFS", "SJN", "RR", "RM", "EDF"]
time_quantum    = 2
MAX_TIMELINE    = 50            # borne d’affichage de la frise

# ---------------------------------------------------------------------------
# Boîte de saisie générique
