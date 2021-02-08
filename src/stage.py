from entity import Entity
from typing import List


class Stage:

    def __init__(self):
        self.entities: List[Entity] = []

    def update(self):
        for entity in self.entities:
            entity.update()
