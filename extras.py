import os, sys
import uuid, hashlib, base64
import zipfile
import json, csv
import re, struct
import string, random, math, decimal
import pygame


def LoadJSONFile(filename: str):
    with open(filename, "r") as file:
        return json.load(file)

def WriteJSONFile(filename: str, data: dict):
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)
    return None