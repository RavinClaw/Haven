import os, sys
import uuid, hashlib, base64
import zipfile
import json, csv
import re, struct
import string, random, math, decimal
# import pygame


class Processor:
    def __init__(self, rom, ram):
        self.rom = rom
        self.ram = ram
        self.pc = 0
        self.instruction = None
        self.debug = False
    
    def RamSizeError(self):
        print("[!ERROR!] RAM INDEX SUPPLIED IS ABOVE MAX ALLOWED VALUE")
    
    def EnableDebug(self):
        """ Enables debug mode which shows the ram in the terminal // Maybe cause lag """
        self.debug = True
    
    def Fetch(self):
        self.instruction = self.rom[self.pc]
        return None
    
    def Inc(self):
        """ Increments the Program Counter by 1 """
        self.pc += 1

    def LDI(self, addr, value):
        """ Loads a new value into ram """
        self.ram[addr] = value
    
    def ADD(self, addr1, addr2, dest):
        """ Adds two numbers from ram """
        self.ram[dest] = self.ram[addr1] + self.ram[addr2]
    
    def SUB(self, addr1, addr2, dest):
        """ Subtracts two numbers from ram """
        self.ram[dest] = self.ram[addr1] - self.ram[addr2]
    
    def JMP(self, value):
        """ Directly sets the Program Counter to the new address """
        self.pc = value
    
    def HALT(self):
        """ Stops the processor by setting it to -1, This is immediate and nothing will be saved """
        self.pc = -1
    
    def execute_instruction(self):
        """ Executes the processor Cycle by fetching the next instruction, processing it and then Incrementing the Program Counter """
        self.Fetch()
        
        # Checks for errors
        if self.instruction > 0xff:
            self.RamSizeError()
            self.HALT()
            return None
        
        if self.instruction == 0x9a: # The Hex value for LDI
            self.Inc()
            self.Fetch()
            address = self.instruction
            self.Inc()
            self.Fetch()
            value = self.instruction
            self.LDI(address, value)
        
        elif self.instruction == 0x2d: # The Hex value for ADD
            self.Inc()
            self.Fetch()
            address1 = self.instruction
            self.Inc()
            self.Fetch()
            address2 = self.instruction
            self.Inc()
            self.Fetch()
            destination = self.instruction
            self.ADD(address1, address2, destination)
        
        elif self.instruction == 0x2e: # The Hex value for SUB
            self.Inc()
            self.Fetch()
            address1 = self.instruction
            self.Inc()
            self.Fetch()
            address2 = self.instruction
            self.Inc()
            self.Fetch()
            destination = self.instruction
            self.SUB(address1, address2, destination)
        
        elif self.instruction == 0xaa: # The Hex value for JMP
            self.Inc()
            self.Fetch()
            address = self.instruction
            self.JMP(address)
        
        elif self.instruction == 0x00: # The Hex value for HALT
            self.HALT()
            return
        
        else:
            pass
        
        if self.instruction != 0x00: # Checks if the last instruction was HALT
            self.Inc()
        
        if self.debug:
            return self.ram # Simply get the ram
        else:
            return None # Tells the program to not return any data

__OpCodes__ = {
    "LDI": "0x9a", "ADD": "0x2d", "SUB": "0x2e", "JMP": "0xaa", "HALT": "0x00"
}

def getInstructionSet():
    """
    #### All OpCodes:
    - LDI : 0x9a
    - ADD : 0x2d
    - SUB : 0x2e
    - JMP : 0xaa
    - HALT : 0x00
    """
    return __OpCodes__

def __getRam__(processor: Processor):
    """ Gets all of the ram from the processor """
    return processor.ram

def __getRom__(processor: Processor):
    """ Gets all of the rom from the processor """
    return processor.rom

def getChar(processor: Processor, address: int):
    """ Gets a value from the processors ram and converts it into a character """
    value = processor.ram[address]
    return chr(value)


if __name__ == "__main__": # Test for the program
    ram = bytearray([0xea] * 255)   # Pre defines the values for ram 255 bytes
    rom = bytearray([               # Create the rom code, Instructions are in the processor, use hex values
        0xea,
        0x9a, 0x22, 0x33,
        0x00,
    ])
    processor = Processor(rom, ram) # Initializes the processor with the ram & rom defined
    
    print("Processor Started Running...")
    while processor.pc != -1: # Checks if the Program Counter is not -1 (HALT)
        processor.execute_instruction() # Runs the processor instruction set >> Fetch >> instruction >> Inc >> REPEAT
    print("Processor Stopped Running...")