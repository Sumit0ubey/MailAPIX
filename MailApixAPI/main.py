from textwrap import dedent

from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from MailApixAPI.Controller.database import engine, Base
from MailApixAPI.Routers import user, email


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    lifespan=lifespan,
    title="MailApix API",
    version="2.05.9",
    docs_url="/documentation",
    description=dedent("""
    API for sending emails, managing users, tokens, and templates.
    
    ### Note
    - All request must include required headers.
    - Rate limits apply
    """),
    summary="MailApix API",
    redoc_url=None,
)

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
        "API Documentation": "/documentation",
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
