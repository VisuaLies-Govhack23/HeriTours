import os

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from . import database as db
from .generate_id import make_userid
from .models import SiteInfoData

Server = FastAPI()

db.init_database()


DIST_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../dist"))
INDEX_FILE = os.path.join(DIST_ROOT, "ui/static/index.html")
JS_ROOT = os.path.join(DIST_ROOT, "ui/js")
DASHBOARD_ROOT = os.path.join(DIST_ROOT, "../dashboard")
RESOURCES_ROOT = os.path.join(DASHBOARD_ROOT, "resources")


@Server.get("/")
async def index(request: Request):
    response = FileResponse(INDEX_FILE)
    # Since there aren't logins, just assign a random user id to each session
    if "userid" not in request.cookies:
        userid = make_userid()
        response.set_cookie(key="userid", value=userid)
    return response


@Server.get("/dashboard/{dashboard_id}")
async def dashboard(dashboard_id: str):
    with open(os.path.join(DASHBOARD_ROOT, "dashboard.html")) as f:
        body = f.read()
    body = body.replace("Sydney", dashboard_id)
    return HTMLResponse(body)


@Server.get("/site/{siteid}")
async def site_info(request: Request, siteid: str):
    userid = request.cookies.get("userid", None)
    if userid is None:
        return JSONResponse({"error": "no_login"})

    story = db.get_story(siteid, userid)
    answered = db.get_answered_questions(siteid, userid)
    stories = db.get_stories(siteid)
    questions = db.get_questions(siteid)
    return Response(
        SiteInfoData(
            stories=stories, answered=answered, questions=questions, story=story
        ).model_dump_json(),
        headers={"content-type": "application/json"},
    )


@Server.post("/story/{siteid}")
async def add_story(request: Request, siteid: str):
    userid = request.cookies.get("userid", None)
    body = await request.body()
    story = body.decode("utf-8")
    if userid is None:
        return JSONResponse({"error": "no_login"})

    print("adding story", userid, siteid, story)
    db.add_story(siteid, userid, story)
    return JSONResponse({"status": True})


@Server.post("/vote/{siteid}/{vote}")
async def vote(request: Request, siteid: str, vote: int):
    userid = request.cookies.get("userid", None)
    if userid is None:
        return JSONResponse({"error": "no_login"})

    print("voting", userid, siteid, vote)
    db.add_vote(siteid, userid, vote)
    return JSONResponse({"status": True})


@Server.post("/answer/{siteid}/{questionid}/{answerid}")
async def answer(request: Request, siteid: str, questionid: str, answerid: str):
    userid = request.cookies.get("userid", None)
    if userid is None:
        return JSONResponse({"error": "no_login"})

    print("answering", userid, siteid, questionid, answerid)
    db.add_answer(siteid, userid, questionid, answerid)
    return JSONResponse({"status": True})


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
Server.mount(
    f"/dashboard/resources", StaticFiles(directory=RESOURCES_ROOT), name="resources"
)
