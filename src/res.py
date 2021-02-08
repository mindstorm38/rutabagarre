from typing import IO
from os import path


WORKING_DIR = path.dirname(__file__)
RES_DIR = path.join(WORKING_DIR, "..", "res")


def get_res(pathname: str) -> str:
    """ Retourne le chemin vers un fichier de resource. """
    return path.join(RES_DIR, pathname)


def open_res(pathname: str, mode: str = "r") -> IO:
    """ Ouvre un fichier de resource avec `open` et le chemin retourné par `get_res`. """
    return open(get_res(pathname), mode)
