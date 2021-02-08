from entity import Entity
from typing import List


__all__ = ["Stage"]


class Stage:

    def __init__(self):
        self.entities: List[Entity] = []

    def update(self):
        for entity in self.entities:
            entity.update()
