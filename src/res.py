from typing import IO
from os import path


WORKING_DIR = path.dirname(__file__)
RES_DIR = path.join(WORKING_DIR, "..", "res")


def get_res(res_path: str) -> str:
    """ Retourne le chemin vers un fichier de resource. """
    return path.join(RES_DIR, res_path)


def open_res(res_path: str, mode: str = "r") -> IO:
    """ Ouvre un fichier de resource avec `open` et le chemin retourné par `get_res`. """
    return open(get_res(res_path), mode)
