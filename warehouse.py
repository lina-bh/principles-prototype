from connection import DB
from address import Address
from copy import copy


class Warehouse:
    def __init__(self, id, address, freespace):
        self._id = id
        self._address = address
        self._free_space = freespace

    def __repr__(self):
        return f"<Warehouse@{hex(id(self))} address={repr(self._address)} freeSpace={self._free_space}>"

    def getID(self):
        return self._id

    def getAddress(self):
        return copy(self._address)

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            warehouse(
            id INTEGER PRIMARY KEY,
            address TEXT UNIQUE NOT NULL,
            freeSpace INTEGER NOT NULL
            );
            """
        )


def create_stockwell_warehouse():
    cur = DB.cursor()
    address = Address("11 Stockwell Street", "", "London", "", "SE10 9BD").to_str()
    cur.execute(
        "INSERT INTO warehouse(address, freeSpace) VALUES (?, 300) RETURNING id, address, freeSpace",
        [address],
    )
    row = cur.fetchone()
    DB.commit()
    return Warehouse(row[0], Address.from_str(row[1]), row[2])
