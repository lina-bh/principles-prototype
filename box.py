from __future__ import annotations
from typing import Tuple

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

    @classmethod
    def create(cls, account: CustomerAccount, length, height, width):
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
