import json
import math
import sqlite3

from haversine import haversine

from .full_text import init_fulltext, query_all
from .models import AnswerData, ItemData, QuestionData, StoryData
from .shortest_path import find_shortest_path

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

    init_fulltext(heritage_items)


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


def get_tour(lat, lng, query, max_size=10) -> list[ItemData]:
    user = (lat, lng)
    weights = []

    # Compute weights

    query_weights = [1] * len(heritage_items)
    if len(query.strip()) > 0:
        query_weights = query_all(query)

    for index, item in enumerate(heritage_items):
        distance = haversine(user, item.latlng)
        query_weight = query_weights[index]
        if query_weight > 0:
            weight = math.sqrt(distance) + (1 - query_weight) * 7
            weights.append((weight, index))
    weights.sort()
    if len(weights) > 0:
        print("min weight", weights[0])
        print("max weight", weights[-1])

    # Get the closest candidates
    topn = min(len(weights), max_size)
    shortlist = []
    for _, index in weights[:topn]:
        shortlist.append(heritage_items[index])
    shortlist.append(None)

    if len(shortlist) < 2:
        return shortlist

    # Compute the cost matrix
    costs = []
    for i in range(topn + 1):
        row = []
        for j in range(topn + 1):
            if i == j:
                row.append(math.inf)
            elif i == topn:
                end = shortlist[j]
                distance = haversine(user, end.latlng)
                row.append(distance)
            elif j == topn:
                start = shortlist[i]
                distance = haversine(start.latlng, user)
                row.append(distance)
            else:
                start = shortlist[i]
                end = shortlist[j]
                distance = haversine(start.latlng, end.latlng)
                row.append(distance)
        costs.append(row)

    # Find the shortest route
    _, route = find_shortest_path(topn, topn + 1, costs)

    # Extract the result
    result = []
    for i in range(topn):
        result.append(shortlist[route[i + 1]])

    return result


def get_site_info(siteid):
    if siteid < 0 or siteid >= len(heritage_items):
        return None
    return heritage_items[siteid]
