# Simulateur d’Ordonnancement – IN422


Ce simulateur expose visuellement le comportement de cinq algorithmes :

* FCFS (First‑Come, First‑Served)
* SJN  (Shortest Job Next)
* RR  (Round‑Robin, quantum personnalisable)
* RM  (Rate‑Monotonic)
* EDF (Earliest Deadline First)

Chaque tâche est représentée par un bloc coloré sur une frise temporelle, et des métriques clefs (temps d’attente moyen, temps de rotation moyen, utilisation CPU) sont agrégées dans une page de comparaison.


## Fonctionnalités

* **Visualisation temps réel** des tâches planifiées sur une frise interactive.
* **Interface graphique** complète : sélection d’algorithmes, formulaires dynamiques, pages multiples (Simulation, Data, Comparaison).
* **Comparaison graphique** des performances via Matplotlib (diagramme à barres exporté automatiquement).
* **Gestion des tâches** : ajout, édition, suppression et enregistrement depuis l’onglet *Data*.
* **Adaptation automatique** à la taille de l’écran (largeur/hauteur récupérées au démarrage).

---

## Prise en main

### 1. Sélection d’un algorithme

Les cinq boutons verticaux à gauche permettent de choisir l’algorithme ; la zone de saisie s’adapte automatiquement aux champs requis (Arrivée, Priorité, Deadline, etc.).

### 2. Ajout de tâches

1. Remplissez les champs dans *Paramètres des Tâches*.
2. Cliquez sur **Ajouter Tâche**.
3. La tâche apparaît dans la liste à droite et dans la frise.

*Exemple pour EDF :* `Nom = T1`, `Durée = 5`, `Deadline = 12`.

### 3. Actions principales

* **Comparaison** : ouvre une page dédiée présentant un tableau récapitulatif et un histogramme.
* **Data** : gère la liste de tâches (sélection, édition, suppression).
* **Effacer Tout** : réinitialise entièrement la simulation.

### 4. Page *Comparaison*

Affiche pour chaque algorithme applicable :

| Indicateur              | Description                                      |
| ----------------------- | ------------------------------------------------ |
| Temps d’attente moyen   | Premier démarrage – arrivée                      |
| Temps de rotation moyen | Fin d’exécution – arrivée                        |
| Utilisation CPU         | Temps CPU occupé / durée totale de la simulation |

---

## Structure du code

```text
Project_Pygame.py
│
├─ Initialisation Pygame & constantes
├─ Classe InputBox (gestion de la saisie)
├─ Implémentations des algorithmes (FCFS, SJN, RR, RM, EDF)
├─ Fonctions de calcul des métriques
├─ Fonctions de dessin (frise, graphiques)
├─ Pages : main, data, compare
└─ Boucle principale 
```

> Les algorithmes sont regroupés dans la section **ALGORITHMES D’ORDONNANCEMENT** (\~ligne 100 du fichier), chaque fonction renvoyant un planning sous forme de liste `(nom, start, durée)`.

---

## Personnalisation

* **Quantum du Round‑Robin** : modifiez la variable `time_quantum` en début de fichier.
* **Longueur de la frise** : ajustez `MAX_TIMELINE` pour changer l’horizon de simulation.
* **Couleurs** : palette définie dans la section *Couleurs & Polices*.

---

## Limitations & pistes d’amélioration

* Gestion limitée de la persistance (aucune sauvegarde sur disque).
* Pas de support du temps réel strict ni des interruptions.
* Possibilité d’exporter des rapports PDF ou CSV.

---

IPSA @2025
