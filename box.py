from __future__ import annotations
from typing import List, Tuple

from connection import DB
from customeraccount import CustomerAccount


class Box:
    def __init__(
        self, id: int, length: int, height: int, width: int, customer: CustomerAccount
    ):
        self._id = id
        self._length = length
        self._height = height
        self._width = width
        self._account = customer

    def __repr__(self):
        return f"<Box@{hex(id(self))} id={self._id} {self._length}cm x {self._height}cm x {self._width}cm account=@{hex(id(self._account))}>"

    def getID(self):
        return self._id

    def getBoxLocation(self):
        cur = DB.execute(
            """
            SELECT warehouse_id
            FROM box, collection, return, storage
            WHERE box.id = ?
            AND return.box_id """
        )
        raise NotImplementedError

    @classmethod
    def create(cls, account: CustomerAccount, length, height, width) -> Box:
        cur = DB.execute(
            """
            INSERT INTO
            box(account_id, length, height, width)
            VALUES (?, ?, ?, ?)
            RETURNING id
            """,
            [account.getAccountNumber(), length, height, width],
        )
        id = cur.fetchone()[0]
        DB.commit()
        return cls(id, length, height, width, account)

    @classmethod
    def loadById(cls, id, account=None):
        cur = DB.execute(
            """
            SELECT account_id, length, height, width
            FROM box
            WHERE id = ?
            """,
            [id],
        )
        row = cur.fetchone()
        if not row:
            raise FileNotFoundError
        return cls(
            id,
            row[1],
            row[2],
            row[3],
            account if account else CustomerAccount.loadById(row[0]),
        )

    @classmethod
    def loadBoxesForCustomer(cls, account: CustomerAccount) -> List[Box]:
        cur = DB.execute(
            """
            SELECT id
            FROM box
            WHERE account_id = ?
            """,
            [account.getAccountNumber()],
        )
        rows = cur.fetchall()
        boxes = []
        for row in rows:
            boxes.append(cls.loadById(row[0], account))
        return boxes

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            box(
            id INTEGER PRIMARY KEY,
            account_id INTEGER NOT NULL,
            length INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            FOREIGN KEY(account_id) REFERENCES account(id)
            );
            """
        )
