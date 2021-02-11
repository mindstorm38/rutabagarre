
class Statistics:

    def __init__(self):

        self._kos: int = 0
        self._plants_collected: int = 0
        self._damage_dealt: int = 0
        self._damage_taken: int = 0

    def get_kos(self) -> int:
        return self._kos

    def get_plants_collected(self) -> int:
        return self._plants_collected

    def get_damage_dealt(self) -> int:
        return self._damage_dealt

    def get_damage_taken(self) -> int:
        return self._damage_taken

    def set_kos(self, ko: int):
        self._kos = ko

    def set_plants_collected(self, pl_co: int):
        self._plants_collected = pl_co

    def set_damage_dealt(self, da_de: int):
        self._damage_dealt = da_de

    def set_damage_taken(self, da_ta: int):
        self._damage_taken = da_ta

