import pandas as pd
import pandas as pd
import os
import matplotlib.pyplot as plt
from math import pi

gdrive_path = "G:\\Andere Computer\\My Computer\\HPS Data"

def filename (number: str) -> str:
    return f"{number} Linear Sweep Voltammetry.dat"

def area_circle(diameter: float) -> float:
    return pi * (0.5 * diameter)**2

def current_density(current):
    area = area_circle(0.05)
    return current/area