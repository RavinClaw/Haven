import os, sys
import uuid, hashlib, base64
import zipfile
import json, csv
import re, struct
import string, random, math, decimal
from processor import *
from extras import *
from drivers.graphics import Screen
# import pygame

getInstructionSet() # Just gets the OpCodes

start_code = bytearray([ # This defines the start code of the rom
    0x9a, 0x01, 0x01, # Sets 01 to 2
    0x9a, 0x02, 0x01, # Sets 02 to 2
    
    0x2d, 0x01, 0x02, 0x01, # Adds 01 & 02 to 01
    
    0xaa, 0x01, #? Jumps back to 01
    0x00,
])

ram_size = 1024 * 1 # 1KB * The Amount of KB Wanted
rom_size = 1024 * 1 # 1KB * The Amount of KB Wanted
ram = bytearray([0xea] * ram_size) # Pre adds 0xea to all elements of ram, this just means skip / nothing to execute
rom = start_code + bytearray([0xea] * (rom_size - len(start_code))) # Pre adds 0xea to all elements of rom, this just means skip / nothing to execute

if len(sys.argv) != 0:
    if sys.argv[1] == "debug:true":
        debug = True
    else:
        debug = False
else:
    debug = False

xprocessor = Processor(rom, ram)

if debug:
    print("[Haven] Enabling Debug Mode")
    xprocessor.EnableDebug()


print("Processor Started Running...")

count = 0
while xprocessor.pc != -1:
    ram = xprocessor.execute_instruction()
    if ram == None:
        pass
    else:
        print(f"\n| HAVEN | CYCLE: {count}")
        for val in range(0, len(ram)):
            if ram[val] != 0xea:
                print(f"|{val}| {hex(ram[val])} | {ram[val]}")
            else:
                continue
    count += 1

print("Processor Stopped Running...")