from fastapi import FastAPI
from src.routes.exception_handler import exception_handlers
from src.routes.user_crud.user_crud import router

app = FastAPI()

app.include_router(router)
exception_handlers.include_app(app)
