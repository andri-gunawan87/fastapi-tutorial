from fastapi import FastAPI, status, HTTPException, Depends, Response, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import models, schema, utils
from .database import engine, get_db
from .routers import post, user, auth
from .exception import main
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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



