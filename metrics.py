# Metrics helper extracted from CODE_FINAAAAL.py

def metrics_from_schedule(tasks, schedule, algo):
    """
    Retourne (avg_waiting, avg_turnaround, cpu_util%) pour un algorithme donné.
    """
    if not tasks or not schedule:
        return None

    # Préparer info par tâche
    info = {}
    for t in tasks:
        name = t['Nom']
        if algo == "RM":
            dur = int(t['Execution'])
            arr = int(t['Arrivee'])
        elif algo in ("FCFS", "SJN", "RR"):
            dur = int(t['Duree'])
            arr = int(t['Arrivee'])
        else:                               # EDF
            dur = int(t['Duree'])
            arr = int(t.get('Arrivee', 0))
        info[name] = {'arrival': arr,
                      'required': dur,
                      'first': None,
                      'end': None}

    busy = 0
    for name, start, length in schedule:
        busy += length
        if name not in info:                # sécurité
            continue
        end_time = start + length
        if info[name]['first'] is None:
            info[name]['first'] = start
        info[name]['end'] = max(info[name]['end'] or 0, end_time)

    waits, turnarounds = [], []
    for name, dat in info.items():
        if dat['first'] is None or dat['end'] is None:
            # tâche jamais planifiée → comparaison invalide
            return None
        waits.append(dat['first'] - dat['arrival'])
        turnarounds.append(dat['end']   - dat['arrival'])

    avg_wait     = sum(waits) / len(waits)
    avg_turn     = sum(turnarounds) / len(turnarounds)
    sim_length   = max(d['end'] for d in info.values())
    cpu_util     = (busy / sim_length) * 100 if sim_length else 0
    return round(avg_wait,2), round(avg_turn,2), round(cpu_util,2)

# ---------------------------------------------------------------------------
# INTERFACE : initialisation des composants ----------------------------------
