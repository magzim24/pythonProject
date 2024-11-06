import datetime
from typing import Annotated
from fastapi import Body, Cookie, FastAPI, Form, Header, Query
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel


app = FastAPI()

class OrderRoom(BaseModel):
    number: int
    arrival_date: datetime.date
    arrival_time: datetime.time
    departure_date: datetime.date
    departure_time: datetime.time
    count_ghosts: int

class User(BaseModel):
    name: str
    job: str
    model_config = {
        "json_schema_extra":{
            "examples":[
                {
                    "name":"Maksim",
                    "job":"programmer"
                 }
            ]
        }
    }

class Cookies(BaseModel):
    session_id: str
    fatebook_tracker: str | None = None
    googall_tracker: str | None = None

class CommonHeaders(BaseModel):
    host: str
    save_data: bool
    if_modified_since: str | None = None
    traceparent: str | None = None
    x_tag: list[str] = []

db = {
    1:{"max_ghosts":2},
    2:{"max_ghosts":1},
    3:{"max_ghosts":4}
}

@app.get("/")
async def get_index():
    lst: str = ""
    for key, value in db.items():
        lst += f"Номер №{key} для {value["max_ghosts"]} гостей</br>"
    html = f"""<p>
    {lst}
    <form>
    <button></button>
    </form>
    </p>"""

    return HTMLResponse(html)

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/")
async def set_index(order: OrderRoom, user: Annotated[User, Body()]):
    return {order.number:"number"}

@app.get("/items/")
async def set_index(headers: Annotated[CommonHeaders, Header()]):
    return headers

@app.post("/items/")
async def set_index(user: Annotated[User, Body(embed=True)],
                    user_agent: Annotated[str | None, Header()] = None):
    return {"job":user.job, "User-agent":user_agent,}

