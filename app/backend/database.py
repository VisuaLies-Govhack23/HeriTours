import json
import math
import sqlite3

from haversine import haversine

from .models import AnswerData, ItemData, QuestionData, StoryData

conn = sqlite3.connect("heritage.db")

heritage_items: list[ItemData] = []


def init_database():
    conn.execute(
        """
            create table if not exists user_stories (
                siteid text,
                userid text,
                vote integer,
                story text,
                primary key (siteid, userid)
            )
        """
    )

    conn.execute(
        """
            create table if not exists user_questions (
                siteid text,
                userid text,
                questionid text,
                answerid text,
                primary key (siteid, userid, questionid)
            )
        """
    )

    with open("heritage.json", "r") as f:
        raw = f.read()
    for item in json.loads(raw):
        heritage_items.append(ItemData.model_validate(item))


def get_stories(siteid):
    rows = conn.execute(
        """
            select userid, vote, story from user_stories 
            where siteid = ? and story is not null
        """,
        [siteid],
    ).fetchall()
    return [StoryData(vote=row[1], story=row[2]) for row in rows]


def add_story(siteid, userid, story):
    try:
        conn.execute(
            """
                insert into user_stories (siteid, userid, story) values (?, ?, ?)
            """,
            [siteid, userid, story],
        ).fetchone()
    except:
        conn.execute(
            """
                update user_stories set story = ? where siteid = ? and userid = ?
            """,
            [story, siteid, userid],
        )


def add_vote(siteid, userid, vote):
    try:
        conn.execute(
            """
                insert into user_stories (siteid, userid, vote) values (?, ?, ?)
            """,
            [siteid, userid, vote],
        ).fetchone()
    except:
        conn.execute(
            """
                update user_stories set vote = ? where siteid = ? and userid = ?
            """,
            [vote, siteid, userid],
        )


def add_answer(siteid, userid, questionid, answerid):
    # Duplicate answers can be safely ignored
    conn.execute(
        """
                insert into user_questions (siteid, userid, questionid, answerid) values (?, ?, ?, ?)
            """,
        [siteid, userid, questionid, answerid],
    ).fetchone()


def get_answered_questions(siteid, userid):
    rows = conn.execute(
        """
            select questionid from user_questions where siteid = ? and userid = ?
        """,
        [siteid, userid],
    ).fetchall()
    return [row[0] for row in rows]


def get_story(siteid, userid):
    row = conn.execute(
        """
            select vote, story from user_stories where siteid = ? and userid = ?
        """,
        [siteid, userid],
    ).fetchone()
    if row is None:
        return StoryData(vote=None, story=None)

    return StoryData(vote=row[0], story=row[1])


def get_questions(siteid):
    return [
        QuestionData(
            id="q1",
            question="Was there any graffiti?",
            answers=[
                AnswerData(id="yes", answer="Yes"),
                AnswerData(id="no", answer="No"),
            ],
        ),
        QuestionData(
            id="q2",
            question="How busy was the site today?",
            answers=[
                AnswerData(id="none", answer="Empty - Just me"),
                AnswerData(id="low", answer="Fewer than 5 other groups"),
                AnswerData(id="high", answer="5 or more other groups"),
            ],
        ),
        QuestionData(
            id="q3",
            question="Was there available parking?",
            answers=[
                AnswerData(id="yes", answer="Yes"),
                AnswerData(id="no", answer="No"),
            ],
        ),
    ]


def get_nearest(lat, lng):
    # This could be rewritten to use a Numpy matrix to be a lot faster
    best = heritage_items[0]
    best_distance = math.inf
    for item in heritage_items:
        distance = haversine((lat, lng), item.latlng)
        if distance < best_distance:
            best = item
            best_distance = distance
    return best
