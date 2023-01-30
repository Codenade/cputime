import os
import keyboard
import psutil

while not keyboard.is_pressed("esc"):
    ps = list()
    pids = psutil.pids()
    top = list()
    for pid in pids:
        ps.append(psutil.Process(pid).cpu_percent())
    ps.sort()
    for i in range(len(ps)-1,len(ps)-1):
        top.append(i)
    print(top)
