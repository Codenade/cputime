import os
import io
import math
import time
import keyboard
import psutil

time_begin = time.time()
time_meas = time.time()
times = dict()
interval = 0.5

def log(*o : object) -> None:
    rt = time.time() - time_begin
    if len(o) <= 1:
        _o = o[0]
    else:
        _o = o
    print(f"[{math.floor((rt % 86400) / 3600):02}:{math.floor((rt % 3600) / 60):02}:{math.floor(rt % 60):02}.{math.floor((rt*1000)%1000):003}]: {_o!s}")

while not keyboard.is_pressed("esc"):
    nonidle = dict()
    for process in psutil.process_iter():
        if process.pid == 0:
            continue
        if not process.pid in times.keys():
            times[process.pid] = process.cpu_times().system
        else:
            if process.cpu_times().system != times[process.pid]:
                nonidle[process.pid] = [process.name(),round(((process.cpu_times().system - times[process.pid]) / (time.time() - time_meas))*100)]
                times[process.pid] = process.cpu_times().system
    time_meas = time.time()
    try:
        snonidle = sorted(nonidle.items(), key=lambda o: o[1])
        outstr = str()
        for i in range(0,min(10,len(snonidle)-1)):
            outstr += f"{os.linesep}{snonidle[i][1][0]:<30} {'{:2.1f}'.format(snonidle[i][1][1]):>20}%"
        log(outstr)
    except Exception as e:
        log(e)
    time.sleep(interval)