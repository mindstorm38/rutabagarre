from typing import IO
from os import path


WORKING_DIR = path.dirname(__file__)
RES_DIR = path.join(WORKING_DIR, "..", "res")


def get_res(pathname: str) -> str:
    return path.join(RES_DIR, pathname)


def open_res(pathname: str, mode: str = "r") -> IO:
    return open(get_res(pathname), mode)
