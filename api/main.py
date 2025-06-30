from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import report

app = FastAPI()

origins = [
    "http://localhost:3000",  # React
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # GET, POST, etc.
    allow_headers=["*"],  # Authorization, Content-Type, etc.
)

app.include_router(report.router)
