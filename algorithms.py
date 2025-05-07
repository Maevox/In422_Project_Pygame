# Scheduling algorithms extracted from CODE_FINAAAAL.py
from config import MAX_TIMELINE
from collections import deque
import numpy as np

def fcfs_schedule(tasks):
    return sorted(tasks, key=lambda x: int(x['Arrivee']))

def sjn_schedule(tasks):
    return sorted(tasks, key=lambda x: (int(x['Arrivee']), int(x['Duree'])))

def rr_schedule(tasks, tq=2, limit=MAX_TIMELINE):
    if not tasks: return []
    tq = max(1, tq)
    q  = deque(sorted(tasks, key=lambda x: int(x['Arrivee'])))
    sched, t = [], 0
    while q and t < limit:
        cur = q.popleft()
        a, d = int(cur['Arrivee']), int(cur['Duree'])
        if a > t:          # CPU idle
            q.append(cur)
            t = a
            continue
        exec_t = min(tq, d, limit-t)
        sched.append((cur['Nom'], t, exec_t))
        t += exec_t
        if d - exec_t > 0 and t < limit:
            nxt = cur.copy()
            nxt['Duree'] = str(d - exec_t)
            q.append(nxt)
    return sched

def rm_schedule(tasks, limit=MAX_TIMELINE):
    if not tasks: return []
    copies = [t.copy() for t in tasks]
    sorted_t = sorted(copies, key=lambda x: int(x['Priorite']))
    sched, t = [], 0
    while t < limit:
        scheduled = False
        for task in sorted_t:
            a      = int(task['Arrivee'])
            period = int(task['Priorite'])
            exe    = int(task['Execution'])
            if a <= t and t % period == 0 and exe > 0:
                # Changement ici : au lieu de durée 1, on met la période complète
                duration = min(period, exe, limit-t)
                sched.append((task['Nom'], t, duration))
                task['Execution'] = str(exe - duration)
                t += duration
                scheduled = True
                break
        if not scheduled:
            t += 1
    return sched

def edf_schedule(tasks, limit=MAX_TIMELINE):
    if not tasks: return []
    remain = [{'Nom': t['Nom'],
               'exec': int(t['Duree']),
               'deadline': int(t['Deadline']),
               'Arrivee': int(t.get('Arrivee', 0))}
              for t in tasks]
    sched, t = [], 0
    while t < limit and remain:
        available = [x for x in remain if x['exec']>0 and x['Arrivee']<=t]
        if not available:
            t += 1
            continue
        cur = min(available, key=lambda x: x['deadline'])
        sched.append((cur['Nom'], t, 1))
        cur['exec'] -= 1
        t += 1
        remain = [x for x in remain if x['exec']>0]
    return sched

# ---------------------------------------------------------------------------
# CALCUL DES MÉTRIQUES --------------------------------------------------------
