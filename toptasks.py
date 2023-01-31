
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
mark = False
usinghotkey = False

def on_hotkey():
    global mark
    mark = True

def log(*o : object) -> None:
    rt = time.time() - time_begin
    if len(o) <= 1:
        _o = o[0]
    else:
        _o = o
    print(f"[{math.floor((rt % 86400) / 3600):02}:{math.floor((rt % 3600) / 60):02}:{math.floor(rt % 60):02}.{math.floor((rt*1000)%1000):003}]: {_o!s}")

parser = argparse.ArgumentParser(description="track top cpu processes")
parser.add_argument("file",nargs="?",type=str,help="specify output file (optional)",default=None)
parser.add_argument("-i", "--interval",nargs="?",default=0.5,const=0.5,type=float,help="set sampling interval in seconds",required=False)
parser.add_argument("-f", "--format",nargs="?",default="csv",const="csv",choices=("csv"),help="not in use",required=False)
parser.add_argument("--hotkey",type=str,help="set a hotkey to mark a section of the output",required=False)
args = parser.parse_args()
usinghotkey = args.hotkey != None
print(args.hotkey)
if (usinghotkey):
    keyboard.add_hotkey(args.hotkey,on_hotkey)
if not args.file == None:
    file = open(args.file, "wt")
else:
    file = sys.stdout
interval = args.interval
if not usinghotkey:
    file.write("time, ")
else:
    file.write("time, marked, ")
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
        snonidle = sorted(list(nonidle.values()), key=lambda o: o[1], reverse=True)
        if len(snonidle) > 0:
            time_delta = time.time() - time_begin
            if not usinghotkey:
                file.write(f"{math.floor((time_delta % 86400) / 3600):02}:{math.floor((time_delta % 3600) / 60):02}:{math.floor(time_delta % 60):02}.{math.floor((time_delta*1000)%1000):003}")
            else:
                file.write(f"{math.floor((time_delta % 86400) / 3600):02}:{math.floor((time_delta % 3600) / 60):02}:{math.floor(time_delta % 60):02}.{math.floor((time_delta*1000)%1000):003}, {int(mark)}")
                mark = False
            #file.write(str(round(time_delta,3)))
            for i in range(0,rows-1):
                item = ["-", "0"]
                if i in range(0, len(snonidle)):
                    item = snonidle[i]
                file.write(f", {item[0]}, {item[1]}")
            file.write("\n")
    except Exception as e:
        log(e)
    time.sleep(interval)
file.close()
keyboard.clear_all_hotkeys()