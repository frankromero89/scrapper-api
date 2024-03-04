from fastapi import FastAPI, Body
import uvicorn
import asyncio

from functions.cfe_scrapper import execute_scrapper

app = FastAPI()

@app.get('/')
def message():
    return "Welcome to wattcher"

@app.post('/cfe-scrapper/')
def run_cfe_scrapper(username: str = Body(), key: str = Body(), service: str = Body()):
    return execute_scrapper(username, key, service)


async def main():
    config = uvicorn.Config("main:app", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())