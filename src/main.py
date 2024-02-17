from fastapi import FastAPI, HTTPException
from src.auth.router import router as auth_router

app = FastAPI()

items = {"foo": "The Foo Wrestlers"}

@app.get("app_get",tags=["get_tag"])
async def get_app():
    return "app"

app.include_router(
    auth_router,
)
