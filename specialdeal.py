from __future__ import annotations
from connection import DB
import hashlib
import os


class SpecialDeal:
    def __init__(self, id: int, discount: int, terms: str, code: str):
        self._id = id
        self._discount = discount
        self._terms = terms
        self._code = code

    def getID(self):
        return self._id

    def getDiscount(self):
        return self._discount

    def getTerms(self):
        return self._terms

    def getCode(self):
        return self._code

    @classmethod
    def create(cls, discount: int, terms: str):
        code = generate_code()
        cur = DB.execute(
            """
	    INSERT INTO
	    specialDeal(discount, terms, code)
	    VALUES (?, ?, ?)
	    RETURNING id
	    """,
            [discount, terms, ""],
        )
        id = cur.fetchone()[0]
        return cls(id, discount, terms, code)

    @staticmethod
    def create_tables(cur):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            specialDeal(
            id INTEGER PRIMARY KEY,
            discount INTEGER NOT NULL CHECK (discount >= 0 AND discount <= 100),
            terms TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL
            );
            """
        )


def generate_code() -> str:
    rand = os.urandom(16)
    sha256 = hashlib.sha256()
    sha256.update(rand)
    return sha256.hexdigest()[:16]
