import pygame # Requires pygame to be installed (([! pip install pygame !]))
import os, sys
import random, string, math, decimal
import uuid, hashlib, base64
import json, csv
import re, struct
import asyncio, time, datetime
from processor import Processor, getChar
import _thread as thread

class Screen():
    def __init__(self, res: list[int, int]):
        """
        ## Screen Display
        
        params:
        - res: list[int, int]
        """
        self.show = True # Shows the screen can be turned off without turning of the screen.
        self.run = True # Can turn of the screen completely... Yes remember to turn off if needed.
        self.screen = pygame.display.set_mode(res) # Creates the screen with its proper dimensions
        self.stored_funcs = []
    
    def ToggleShow(self):
        """ Allows the toggling of the screen """
        if self.show:
            self.show = False
            return False
        elif not self.show:
            self.show = True
            return True

    def SetTitle(self, title: str):
        pygame.display.set_caption(title)
        return None

    def AddNewFunc(self, func_id: int, allow_reuse: bool):
        """ Adds a new function to the stored functions that will be rendered to the screen """
        def decorator(f: object):
            Found = False
            if len(self.stored_funcs) >= 1:
                for x in range(0, len(self.stored_funcs)):
                    if self.stored_funcs[x]["id"] == func_id:
                        Found = True
                    else:
                        continue
            
            if not Found:
                self.stored_funcs.append({"id": func_id, "func": f, "reuse": allow_reuse})
            else:
                print("[Driver][Graphics][@Screen] Function ID Already Exists in the Index, Use Another Number")
            return f
        return decorator

    def Show(self):
        """ Starts the actual screen """
        if self.show:
            while self.run:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.run = False

                for val in range(0, len(self.stored_funcs)):
                    try:
                        self.stored_funcs[val]["func"]()
                        if self.stored_funcs[val]["reuse"] == False:
                            self.stored_funcs.pop(val)
                    except:
                        pass
            
                pygame.display.update()
                self.screen.fill((0, 0, 0))
        
        else:
            return 0xfc # Means screen termination in the graphics driver