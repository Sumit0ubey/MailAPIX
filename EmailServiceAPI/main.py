from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from EmailServiceAPI import models
from EmailServiceAPI.database import engine
from .Routers import user, email

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


@app.get("/", status_code=status.HTTP_200_OK)
def home():
    informations = {
        "API Name": "Email Service APP",
        "Description": "This is a Async API for Sending Email to anyone at anytime",
        "Endpoints": "/, /users, /email",
        "API Documenation": "/docs",
        "Version": "2.05.9",
        "Created By": "Sumit Dubey",
        "Contact": "sumitdubey810@outlook.com",
        "Tools used": {
            "Backend": "FastAPI",
            "Database": "PostgreSQL",
            "IDE": "Pycharm"
        },
        "The project was developed in": "4 days",
        "Start Date": "21-05-25",
        "End Date": "24-05-25"
    }

    return JSONResponse(content=informations, status_code=200)


app.include_router(user.router)
app.include_router(email.router)
