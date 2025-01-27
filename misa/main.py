import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from misa.exceptions import TokenExpiredException, TokenNoFoundException
from misa.users.router import router as users_router
from misa.chat.router import router as chat_router

misa = FastAPI()
misa.mount('/static', StaticFiles(directory='misa/static'), name='static')

misa.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

misa.include_router(users_router)
misa.include_router(chat_router)


@misa.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/Chat")


@misa.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@misa.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")

if __name__ == "__main__":
    uvicorn.run(misa, host="127.0.0.1", port=8000)
