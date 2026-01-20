from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from tbcryptography import stdtbc

app = FastAPI()

# Hare: Khai báo thư mục chứa file tĩnh và giao diện
app.mount("/staitc", StaticFiles(directory="D:/_Python_Community_/static"), name="static")
templates = Jinja2Templates(directory="templates")

# player = [ {"username": str, "password": str} ]
player = {"username": [], "password": []}

# Get
@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login")
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/signup")
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

# Post
@app.post("/login")
async def check_log(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    if not username or not password:
        return templates.TemplateResponse("login.html", {"request": request})
    
    if username not in player["usename"]:
        return templates.TemplateResponse("login.html", {"request": request})