import os
import sys
import threading
import time
import queue
queue.memory=[]

if sys.platform != 'linux':
    print("Sorry, this code only works on gnu")
    exit(1)

if os.system("/usr/bin/which xdotool") != 0:
    print("ERROR: please install xdotool binaries")
    exit(1)


def get_identifier(fd):
    count= 1
    while count<20:
        print (count, fd.read(8))
        count += 1

def dump_data(dict):
    fd = open("keys.data", 'w')
    for i in dict.keys():
        print (f"{i} {dict[i][0]} {dict[i][1]} {dict[i][2]}", file=fd, flush=True)

def load_data(fd):
    keys = {}
    for line in fd:
        parts = line.split(" ")
        keys[parts[0]] = [parts[1], parts[2], parts[3][:-1]]
    return keys

def config_keys(fd, d=[]):
    d = []
    if d == []:
        print ("Proced with declare joystic keys")
        while True:
            string = input("Define key: ")
            if string == "999":
                break
            if string == "":
                continue
            d.append(string)
    keys = {}
    count = 97
    print ("Now asignate joystic keys")
    for i in d:
        print(f"Press {i}: ")
        stream = fd.read(8)
        print("Press Release: ")
        release = fd.read(8)
        keys[i] = [stream[-4:].hex(), release[-4:].hex(), f"{count.to_bytes(1,'little').decode()}"]
        count+=1
    return keys

def keyup(string):
    os.popen(f"xdotool keyup {string}")

def keydown(string):
    os.popen(f"xdotool keydown {string}")

def cursor(stream, keys):
    refresh_rate=0.00000001

    def get_position():
        data = os.popen("xdotool getmouselocation").read().split(" ")
        x = int(data[0].split(":")[-1])
        y = int(data[1].split(":")[-1])
        return [x,y]

    def cursor_up():
        while "c_cursor_up" in queue.memory:
            x,y = get_position()
            os.popen(f"xdotool mousemove {x} {y - 15}")
            time.sleep(refresh_rate)

    def cursor_down():
        while "c_cursor_down" in queue.memory:
            x,y = get_position()
            os.popen(f"xdotool mousemove {x} {y + 15}")
            time.sleep(refresh_rate)

    def cursor_left():
        while "c_cursor_left" in queue.memory:
            x,y = get_position()
            os.popen(f"xdotool mousemove {x - 15} {y}")
            time.sleep(refresh_rate)

    def cursor_right():
        while "c_cursor_right" in queue.memory:
            x,y = get_position()
            os.popen(f"xdotool mousemove {x + 15} {y}")
            time.sleep(refresh_rate)

    def kill(name):
        if name in queue.memory:
            queue.memory.remove(name)

    if "cursor_up" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            queue.memory.append(keys[-1])
            threading.Thread(target=cursor_up, name=keys[-1]).start()
        if stream[-4:].hex() == keys[1]:
            kill(keys[-1])
    if "cursor_down" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            queue.memory.append(keys[-1])
            threading.Thread(target=cursor_down, name=keys[-1]).start()
        if stream[-4:].hex() == keys[1]:
            kill(keys[-1])
    if "cursor_left" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            queue.memory.append(keys[-1])
            threading.Thread(target=cursor_left, name=keys[-1]).start()
        if stream[-4:].hex() == keys[1]:
            kill(keys[-1])
    if "cursor_right" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            queue.memory.append(keys[-1])
            threading.Thread(target=cursor_right, name=keys[-1]).start()
        if stream[-4:].hex() == keys[1]:
            kill(keys[-1])
def mouse(stream, keys):
    def key_down(num):
        os.popen(f"xdotool keydown click {num}")

    def key_up(num):
        os.popen(f"xdotool keyup click {num}")

    if "button_1" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            key_down("1")
        if stream[-4:].hex() == keys[1]:
            key_up("1")
    if "button_2" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            key_down("2")
        if stream[-4:].hex() == keys[1]:
            key_up("2")
    if "button_3" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            key_down("3")
        if stream[-4:].hex() == keys[1]:
            key_up("3")
    if "button_4" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            key_down("4")
        if stream[-4:].hex() == keys[1]:
            key_up("4")
    if "button_5" in keys[-1]:
        if stream[-4:].hex() == keys[0]:
            key_down("5")
        if stream[-4:].hex() == keys[1]:
            key_up("5")

        

def loop(keys, fd):
    while True:
        stream = fd.read(8)
        for i in keys.keys():
            if stream[-4:].hex() == keys[i][0] and not "c_" in keys[i][-1]:
                print (f"Pressed {i}")
                keydown(keys[i][2])
            if stream[-4:].hex() == keys[i][1] and not "c_" in keys[i][-1]:
                print (f"Released {i}")
                keyup(keys[i][2])
            if "c_" in keys[i][-1]:
                if "cursor" in keys[i][-1]:
                    cursor(stream, keys[i])
                if "button" in keys[i][-1]:
                    mouse(stream, keys[i])

def dump_all(fd):
    while True:
        stream = fd.read(8)
        print (stream[-4:], len(stream))

                
if __name__ == "__main__":
    port = sys.argv[-1]
    fd = open(port, 'br')
    if not "event" in port and (("/dev/input/js" in port) or ("/dev/js" in port)) :
        get_identifier(fd)
    else:
        print ("ERROR: event not support jet")
        exit(1)

    if "--configure" in sys.argv:
        keys = config_keys(fd)
        dump_data(keys)
        exit(0)
    if "--dump" in sys.argv:
        dump_all(fd)
        exit(0)
    if "--add" in sys.argv:
        press = eval(sys.argv[sys.argv.index("--add") + 1]).hex()
        release = eval(sys.argv[sys.argv.index("--add") + 2]).hex()
        id = sys.argv[sys.argv.index("--add") + 3]
        key = sys.argv[sys.argv.index("--add") + 4]
        keys = load_data(open("keys.data"))
        keys[id] = [press, release, key]
        dump_data(keys)
        exit(0)

    keys=load_data(open("keys.data"))
    loop(keys, fd)
