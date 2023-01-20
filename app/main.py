from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .exception import main
from .config import Settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


@app.exception_handler(main.NotFoundException)
async def unicorn_exception_handler(request: Request, exc: main.NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"data": exc.name},
    )
    
@app.exception_handler(main.UnauthorizedException)
async def unicorn_exception_handler(request: Request, exc: main.UnauthorizedException):
    return JSONResponse(
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
        content={"data": "Unauthorized"},
    )
    
@app.exception_handler(main.InternalException)
async def unicorn_exception_handler(request: Request, exc: main.InternalException):
    return JSONResponse(
        status_code=exc.status,
        content={"data": exc.name},
    )
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)
app.include_router(vote.router)



