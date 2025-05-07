

# Scheduling Simulator – IN422


This simulator visually demonstrates the behavior of five algorithms:

* FCFS (First‑Come, First‑Served)  
* SJN  (Shortest Job Next)  
* RR  (Round‑Robin, customizable quantum)  
* RM  (Rate‑Monotonic)  
* EDF (Earliest Deadline First)  

Each task is represented by a colored block on a timeline, and key metrics (average waiting time, average turnaround time, CPU utilization) are aggregated on a comparison page.


## Features

* **Real-time visualization** of scheduled tasks on an interactive timeline.  
* **Complete graphical interface**: algorithm selection, dynamic forms, multiple pages (Simulation, Data, Comparison).  
* **Graphical performance comparison** via Matplotlib (automatically exported bar chart).  
* **Task management**: add, edit, delete, and save tasks from the *Data* tab.  
* **Automatic adaptation** to screen size (width/height retrieved at startup).  

---

## Getting Started

### 1. Selecting an Algorithm

The five vertical buttons on the left allow you to choose the algorithm; the input area automatically adapts to required fields (Arrival, Priority, Deadline, etc.).  

### 2. Adding Tasks

1. Fill in the fields under *Task Parameters*.  
2. Click **Add Task**.  
3. The task appears in the list on the right and on the timeline.  

*Example for EDF:* `Name = T1`, `Duration = 5`, `Deadline = 12`.  

### 3. Main Actions

* **Compare**: Opens a dedicated page with a summary table and histogram.  
* **Data**: Manages the task list (selection, editing, deletion).  
* **Clear All**: Fully resets the simulation.  

### 4. *Comparison* Page

Displays for each applicable algorithm:  

| Metric                     | Description                                      |  
| -------------------------- | ------------------------------------------------ |  
| Average waiting time       | First start – arrival time                       |  
| Average turnaround time    | End of execution – arrival time                  |  
| CPU utilization            | Occupied CPU time / total simulation duration    |  

---

## Code Structure

```text
Project_Pygame.py  
│  
├─ Pygame initialization & constants  
├─ InputBox class (input handling)  
├─ Algorithm implementations (FCFS, SJN, RR, RM, EDF)  
├─ Metric calculation functions  
├─ Drawing functions (timeline, charts)  
├─ Pages: main, data, compare  
└─ Main loop  
```

> The algorithms are grouped in the **SCHEDULING ALGORITHMS** section (~line 100 of the file), each function returning a schedule as a list `(name, start, duration)`.  

---

## Customization

* **Round‑Robin Quantum**: Modify the `time_quantum` variable at the top of the file.  
* **Timeline Length**: Adjust `MAX_TIMELINE` to change the simulation horizon.  
* **Colors**: Palette defined in the *Colors & Fonts* section.  

---

## Limitations & Improvement Ideas

* Limited persistence (no disk saving).  
* No strict real-time support or interrupts.  
* Potential for PDF/CSV report exports.  

---  

IPSA @2025
