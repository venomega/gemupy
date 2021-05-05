import os
import sys


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


def loop(keys, fd):
    while True:
        stream = fd.read(8)
        for i in keys.keys():
            if stream[-4:].hex() == keys[i][0]:
                print (f"Pressed {i}")
                print (keys[i])
                keydown(keys[i][2])
            if stream[-4:].hex() == keys[i][1]:
                print (f"Released {i}")
                keyup(keys[i][2])

def dump_all(fd):
    while True:
        stream = fd.read(8)
        print (stream[-4:], len(stream))

                
if __name__ == "__main__":
    port = sys.argv[-1]
    fd = open(port, 'br')
    get_identifier(fd)

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



            
