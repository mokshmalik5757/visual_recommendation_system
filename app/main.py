from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import api_routes

app = FastAPI(title = "Recommmendation System Visual Search", debug = True)

app.include_router(api_routes.router)

app.add_middleware (
    CORSMiddleware,
    allow_origin_regex = r"https?://.*",
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

