import sqlite3

DB = None


def connect_db(*, persistent=False, reinit=False):
    global DB
    connect_string = ":memory:"
    if persistent:
        connect_string = "./prototype.sqlite3"
    if not reinit and DB:
        return DB
    DB = sqlite3.connect(connect_string)
    return DB


connect_db()
