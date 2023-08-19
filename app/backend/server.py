import os

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

Server = FastAPI()


DIST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dist"))
INDEX_FILE = os.path.join(DIST_ROOT, "ui/static/index.html")
JS_ROOT = os.path.join(DIST_ROOT, "ui/js")


@Server.get("/")
async def index():
    return FileResponse(INDEX_FILE)


@Server.get("/dashboard/{dashboard_id}")
async def dashboard(dashboard_id: str):
    return HTMLResponse(
        f"""<!DOCTYPE html>
        <title>Blah</title>
        <h1>Dashboard!</h1>
        You requested dashboard: {dashboard_id}
    """
    )


@Server.get("/nearest/{lat}/{lon}")
async def nearest(lat: float, lon: float):
    print("requesting nearest to", lat, lon)
    return JSONResponse({"info": "Test", "id": 123})


@Server.get("/tour/{query}")
async def tour(query: str):
    print("generating tour for", query)
    return JSONResponse({"stops": []})


@Server.get("/api/ping")
async def ping():
    return JSONResponse({"pong": True})


Server.mount(f"/js", StaticFiles(directory=JS_ROOT), name="js")
