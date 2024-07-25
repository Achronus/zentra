from contextlib import asynccontextmanager

from app import auth

from zentra_api.responses import ErrorResponse
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(docs_url="/api/docs", redoc_url=None, lifespan=lifespan)


app.include_router(auth.router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    details = ErrorResponse(
        code=exc.status_code, message=exc.detail, headers=exc.headers
    ).model_dump()
    return JSONResponse(details, status_code=exc.status_code, headers=exc.headers)
