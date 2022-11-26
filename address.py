from __future__ import annotations


class Address:
    def __init__(self, firstLine, secondLine, town, county, postcode):
        self.firstLine = firstLine
        self.secondLine = secondLine
        self.town = town
        self.county = county
        self.postcode = postcode

    def validate(self) -> bool:
        # in a production system, this would call out to Royal Mail's Postcode
        # Address File
        return True

    def to_str(self) -> str:
        return f"{self.firstLine};{self.secondLine};{self.town};{self.county};{self.postcode}"

    def __repr__(self):
        return "<" + self.to_str() + ">"

    @staticmethod
    def from_str(string) -> Address:
        parts = string.split(";")
        return Address(parts[0], parts[1], parts[2], parts[3], parts[4])
