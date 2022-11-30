from __future__ import annotations
from typing import Tuple
from connection import DB

from deal import Deal
from warehouse import Warehouse
from box import Box


class Storage:
    def __init__(
        self,
        id: int,
        deal: Deal,
        warehouse: Warehouse,
        box: Box,
        location: Tuple[int, int],
    ):
        self._id = id
        self._deal = deal
        self._warehouse = warehouse
        self._location = location
        self._box = box

    def __repr__(self):
        return (
            f"<Storage@{hex(id(self))} id={self._id} "
            f"deal=@{hex(id(self._deal))} warehouse=@{hex(id(self._warehouse))} "
            f"row={self._location[0]} shelf={self._location[1]}>"
        )

    def getID(self):
        return self._id

    def getBox(self):
        return self._box

    @classmethod
    def loadAllByCustomer(cls, account):
        raise NotImplementedError
        cur = DB.execute(
            """
            SELECT id
            FROM storage
            JOIN subscription
            ON subscription.username = ?
            """,
            [account.getUsername()],
        )

    @staticmethod
    def create(
        deal: Deal, warehouse: Warehouse, box: Box, location: Tuple[int, int]
    ) -> Storage:
        row, shelf = location
        cur = DB.cursor()
        cur.execute(
            """
            INSERT INTO
            storage(deal_id, warehouse_id, "row", shelf, box_id)
            VALUES (?, ?, ?, ?, ?)
            RETURNING id
            """,
            [deal.getID(), warehouse.getID(), row, shelf, box.getID()],
        )
        id = cur.fetchone()[0]
        return Storage(id, deal, warehouse, box, location)

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            storage(
            id INTEGER PRIMARY KEY,
            box_id INTEGER NOT NULL,
            deal_id INTEGER NOT NULL,
            warehouse_id INTEGER NOT NULL,
            row INTEGER NOT NULL,
            shelf INTEGER NOT NULL,
            FOREIGN KEY(box_id) REFERENCES box(id),
            FOREIGN KEY(deal_id) REFERENCES deal(id),
            FOREIGN KEY(warehouse_id) REFERENCES warehouse(id)
            );
            """
        )
