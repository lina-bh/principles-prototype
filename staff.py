from __future__ import annotations
from connection import DB
import sqlite3


class StaffMember:
    def __init__(self, id: int, name: str, username: str, phonenumber: str):
        self._id = id
        self._name = name
        self._username = username
        self._phonenumber = phonenumber

    def getID(self):
        return self._id

    def getName(self):
        return self._name

    def getUsername(self):
        return self._username

    @classmethod
    def loadByUsername(cls, username: str):
        cur = DB.execute(
            """
            SELECT staff_id, staff.name, phonenumber
            FROM staff_account
            JOIN staff ON staff_id = staff.id
            WHERE username = ?
            """,
            [username],
        )
        row = cur.fetchone()
        if not row:
            raise FileNotFoundError
        return cls(row[0], row[1], username, row[2])

    @staticmethod
    def create_tables(cur: sqlite3.Cursor):
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            staff(
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
            );
            """
        )
        cur.execute(
            """
            CREATE TABLE
            IF NOT EXISTS
            staff_account(
            username TEXT PRIMARY KEY,
            password TEXT,
            phonenumber INTEGER NOT NULL,
            staff_id INTEGER NOT NULL,
            FOREIGN KEY(staff_id) REFERENCES staff(id)
            );
            """
        )


def create_mike():
    staff_id = DB.execute(
        """
        INSERT INTO
        staff(name)
        VALUES ('Michael Ehrmantraut')
        RETURNING id
        """
    ).fetchone()[0]
    DB.execute(
        """
        INSERT INTO
        staff_account(username, phonenumber, staff_id)
        VALUES ('mike', '01519247373', ?)
        """,
        [staff_id],
    )
    DB.commit()


def create_lydia():
    staff_id = DB.execute(
        """
        INSERT INTO
        staff(name)
        VALUES ('Lydia Rodarte-Quayle')
        RETURNING id
        """
    ).fetchone()[0]
    DB.execute(
        """
        INSERT INTO
        staff_account(username, phonenumber, staff_id)
        VALUES ('lydia', '01229445445', ?)
        """,
        [staff_id],
    )
    DB.commit()
    return StaffMember.loadByUsername("lydia")
