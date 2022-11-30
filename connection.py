import os
import sqlite3

DB = None


def connect_db(*, persistent=False, reinit=False):
    global DB
    connect_string = ":memory:"
    if persistent:
        connect_string = "./prototype.sqlite3"
    if not reinit and DB:
        return DB
    if reinit and persistent:
        os.unlink(connect_string)
    DB = sqlite3.connect(connect_string)
    DB.execute("PRAGMA foreign_keys = ON;")
    return DB


connect_db(persistent=True, reinit=True)
