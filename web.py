"""Browser-facing application for AGENTIS.

Run with: ``uvicorn web:app --reload``
"""

from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from api import app as api_app


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="AGENTIS Web")
app.mount("/api", api_app)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")


@app.get("/", include_in_schema=False)
async def index(request: Request):
    return templates.TemplateResponse(request, "index.html")
