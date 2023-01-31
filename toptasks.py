
import os
import sys
import math
import time
import keyboard
import psutil
import argparse

time_begin = time.time()
time_meas = time.time()
times = dict()
interval = 0.5
rows = 10
file = None

def log(*o : object) -> None:
    rt = time.time() - time_begin
    if len(o) <= 1:
        _o = o[0]
    else:
        _o = o
    print(f"[{math.floor((rt % 86400) / 3600):02}:{math.floor((rt % 3600) / 60):02}:{math.floor(rt % 60):02}.{math.floor((rt*1000)%1000):003}]: {_o!s}")

parser = argparse.ArgumentParser(description="track top cpu processes")
parser.add_argument('file',type=str)
args = parser.parse_args()
if not args.file == "121279271498752186538765876138768162872838762736762876458176258723685637857":
    file = open(args.file, "wt")
else:
    file = sys.stdout
file.write("time, ")
for i in range (1, rows-1):
    file.write(f"#{i}, p{i}, ")
file.write(f"#{rows}, p{rows}\n")
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
        if len(snonidle) > 0:
            time_delta = time.time() - time_begin
            #file.write(f"{math.floor((time_delta % 86400) / 3600):02}:{math.floor((time_delta % 3600) / 60):02}:{math.floor(time_delta % 60):02}.{math.floor((time_delta*1000)%1000):003}")
            file.write(str(round(time_delta,3)))
            for i in range(0,rows-1):
                item = ["", ""]
                if i in range(0, len(snonidle)):
                    item = snonidle[i][1]
                file.write(f", {item[0]}, {item[1]}")
            file.write("\n")
    except Exception as e:
        log(e)
    time.sleep(interval)
file.close()