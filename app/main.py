import sqlite3
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import html

def init_db():
    conn = sqlite3.connect("../data/test.db")
    cursor = conn.cursor()

    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS users (
                                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                        username VARCHAR(50) NOT NULL UNIQUE,
                       secret_data TEXT NOT NULL
                       )
                   """)

    cursor.execute("INSERT OR IGNORE INTO users(username, secret_data) VALUES (?, ?)", ("Admin", "HardPassword"))
    cursor.execute("INSERT OR IGNORE INTO users(username, secret_data) VALUES (?, ?)", ("Steven_Brand", "EZPassword"))

    conn.commit()
    conn.close()

init_db()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/users/{username}")
async def get_user(username: str):
    conn = sqlite3.connect("../data/test.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    return {"username": result}

@app.get("/search", response_class=HTMLResponse)
async def search(query: str):
    safe_query = html.escape(query)
    return "<h1>Search results for: " + safe_query + "</h1>"
