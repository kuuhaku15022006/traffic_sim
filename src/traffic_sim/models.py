# src/traffic_sim/models.py

from collections import deque
from enum import Enum

class LightState(Enum):
    GREEN = 1
    RED = 0

class Vehicle:
    def __init__(self, id: str, path: deque[str]):
        self.id = str
        self.path = path