from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from EmailServiceAPI.Controller.database import engine
from EmailServiceAPI.Routers import user, email
from EmailServiceAPI.Controller import models


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    information = {
        "API Name": "Email Service APP",
        "Description": "This is a Async API for Sending Email to anyone at anytime",
        "Endpoints": "/, /users, /email",
        "API Documentation": "/docs",
        "Version": "2.05.9",
        "Created By": "Sumit Dubey",
        "Contact": "sumitdubey810@outlook.com",
        "Tools used": {
            "Backend": "FastAPI",
            "Database": "PostgresSQL",
            "IDE": "Pycharm"
        }
    }

    return JSONResponse(content=information, status_code=200)


app.include_router(user.router)
app.include_router(email.router)
