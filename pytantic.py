import datetime
from typing import Dict, List
from pydantic import BaseModel


def print_name(book_name: str, year: datetime, price: float):
    print(book_name, year, price)


def print_name_with_list(book_name: List[str], year: datetime, price: float):
    print(book_name, year, price)


class Book(BaseModel):
    name: str
    price: float = 10.0
    year: datetime.datetime


def print_book(book: Book):
    pass


book1 = {"name": "book1", "price": 11.0, "year": datetime.datetime.now()}

book_object = Book(**book1)
print(book_object)
