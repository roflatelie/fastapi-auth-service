from src.main import app
from src.routes.user_crud.user_crud import router

app.include_router(router)
