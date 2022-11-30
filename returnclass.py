from __future__ import annotations

from movement import Movement
from deal import Deal
from box import Box
from storage import Storage
from connection import DB


class Return(Movement):
    def __init__(self, id: int, deal: Deal, storage: Storage):
        self._id = id
        self._deal = deal
        self._storage = storage

    def __repr__(self):
        return (
            f"<Return@{hex(id(self))} id={self._id} deal=@{hex(id(self._deal))} "
            f"storage=@{hex(id(self._storage))}>"
        )

    def getID(self):
        return self._id

    @classmethod
    def create(cls, deal: Deal, box: Box, storage: Storage) -> Return:
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
            return(
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
