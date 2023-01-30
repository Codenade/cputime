import time
import keyboard
import psutil        

time_begin = time.time()

def log(*o : object) -> None:
    print(str(time.time() - time_begin) + str(o))

while not keyboard.is_pressed("esc"):
    processes = list()
    top = list()
    for process in psutil.process_iter():
        processes.append(process)
    try:
        sorted(processes,key=lambda a: a.cpu_times().user)
        for i in range(0,10):
            top.append([processes[i].name(),processes[i].cpu_times().user])
        log(top)
        time.sleep(1)
    except:
        log("-")