from __future__ import annotations
from box import Box
from deal import Deal
from connection import DB
from storage import Storage
from movement import Movement


class Collection(Movement):
    def __init__(self, id: int, deal: Deal, storage: Storage):
        self._id = id
        self._deal = deal
        self._storage = storage

    def __repr__(self):
        return (
            f"<Collection@{hex(id(self))} id={self._id} "
            f"deal=@{hex(id(self._deal))} storage=@{hex(id(self._storage))}>"
        )

    def getID(self):
        return self._id

    @classmethod
    def create(cls, deal: Deal, box: Box, storage: Storage) -> Collection:
        cur = DB.execute(
            """
            INSERT INTO
            collection(deal_id, box_id, storage_id)
            VALUES (?, ?, ?)
            RETURNING id
            """,
            [deal.getID(), storage.getBox().getID(), storage.getID()],
        )
        id = cur.fetchone()[0]
        DB.commit()
        return cls(id, deal, storage)

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            collection(
            id INTEGER PRIMARY KEY,
            deal_id INTEGER NOT NULL,
            box_id INTEGER NOT NULL,
            storage_id INTEGER NOT NULL,
            FOREIGN KEY(deal_id) REFERENCES deal(id),
            FOREIGN KEY(box_id) REFERENCES box(id),
            FOREIGN KEY(storage_id) REFERENCES storage(id)
            );
            """
        )
