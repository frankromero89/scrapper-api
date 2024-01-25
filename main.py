from fastapi import FastAPI, Body

from functions.cfe_scrapper import execute_scrapper

app = FastAPI()

@app.get('/')
def message():
    return "helllo dude"

@app.post('/cfe-scrapper/')
def run_cfe_scrapper(username: str = Body(), service: str = Body()):
    return execute_scrapper()