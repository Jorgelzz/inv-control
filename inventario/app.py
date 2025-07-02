from fastapi import FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Banco de dados simples
conn = sqlite3.connect("inventario.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL
    )
""")
conn.commit()

@app.get("/", response_class=HTMLResponse)
def listar(request: Request):
    itens = cursor.execute("SELECT * FROM itens").fetchall()
    return templates.TemplateResponse("index.html", {"request": request, "itens": itens})

@app.get("/adicionar", response_class=HTMLResponse)
def form_adicionar(request: Request):
    return templates.TemplateResponse("adicionar.html", {"request": request})

@app.post("/adicionar")
def adicionar(nome: str = Form(...), quantidade: int = Form(...)):
    cursor.execute("INSERT INTO itens (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
    conn.commit()
    return RedirectResponse("/", status_code=303)

@app.get("/remover/{item_id}")
def remover(item_id: int):
    cursor.execute("DELETE FROM itens WHERE id = ?", (item_id,))
    conn.commit()
    return RedirectResponse("/", status_code=303)
