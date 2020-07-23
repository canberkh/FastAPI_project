from fastapi import FastAPI, Body, Header
from models.user import User
from models.book import Book
from models.author import Author
from starlette.status import HTTP_201_CREATED

app = FastAPI()


@app.post("/user", status_code=HTTP_201_CREATED)
async def post_user(user: User, x_custom: str = Header(...)):
    return {"request body": user, "request custom header": x_custom}


@app.get("/user")
async def get_user_validation(password: str):
    return {"query parameter": password}


@app.get("/book/{isbn}", response_model=Book, response_model_exclude=["author"]) #or use response_model_include=["",""]
async def get_book_with_isbn(isbn: str):
    author_dict = {
        "name": "Canberk",
        "book": ["book1", "book2"]
    }
    author1 = Author(**author_dict)
    book_dict = {
        "isbn":"1234",
        "name":"book1",
        "year":"2019",
        "author": author1
    }
    book1 = Book(**book_dict)
    return book1


@app.get("/author/{idk}/book")
async def get_authors_books(
    idk: int, category: str, order: str = "asc",
):
    return {"query changeable parameter": order + category + str(idk)}


@app.patch("/author/name")
async def patch_author_name(name: str = Body(..., embed=True)):
    return {"name in body": name}


@app.post("/user/author")
async def post_user_and_author(user: User, author: Author):
    return {"user": user, "author": author}
