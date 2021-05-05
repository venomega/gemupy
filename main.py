import os
import sys


d = ['x', 'y', 'b', 'a']
keys={}

def get_identifier(fd):
    count= 1
    while count<20:
        print (count, fd.read(8))
        count += 1

def dump_data(dict):
    fd = open("keys.data", 'w')
    for i in dict.keys():
        print (f"{i} {dict[i][0].hex()} {dict[i][1].hex()}", file=fd, flush=True)

def load_data(fd):
    keys = {}
    for line in fd:
        parts = line.split(" ")
        keys[parts[0]] = [parts[1], parts[2][:-1]]
    return keys

def config_keys(d, fd):
    keys = {}
    for i in d:
        print(f"Press {i}: ")
        stream = fd.read(8)
        print("Press Release: ")
        release = fd.read(8)
        keys[i] = [stream[-4:], release[-4:]]
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
                keyup(i)
            if stream[-4:].hex() == keys[i][1]:
                print (f"Released {i}")
                keydown(i)

if __name__ == "__main__":
    port = sys.argv[1]
    fd = open(port, 'br')
    get_identifier(fd)
    #keys = config_keys(d, fd)
    #print (keys)
    #dump_data(keys)
    keys=load_data(open("keys.data"))
    loop(keys, fd)



            
