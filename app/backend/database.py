import sqlite3

conn = sqlite3.connect("heritage.db")


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


def get_stories(siteid):
    rows = conn.execute(
        """
            select userid, vote, story from user_stories 
            where siteid = ? and story is not null
        """,
        [siteid],
    ).fetchall()
    return [{"userId": row[0], "vote": row[1], "story": row[2]} for row in rows]


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
        return {"vote": None, "story": None}

    return {"vote": row[0], "story": row[1]}


def get_questions(siteid):
    return [
        {
            "id": "q1",
            "question": "Was there any graffiti?",
            "answers": [{"id": "yes", "answer": "Yes"}, {"id": "no", "answer": "No"}],
        },
        {
            "id": "q2",
            "question": "How busy was the site today?",
            "answers": [
                {"id": "none", "answer": "Empty - Just me"},
                {"id": "low", "answer": "Fewer than 5 other groups"},
                {"id": "high", "answer": "5 or more other groups"},
            ],
        },
        {
            "id": "q3",
            "question": "Was there available parking?",
            "answers": [{"id": "yes", "answer": "Yes"}, {"id": "no", "answer": "No"}],
        },
    ]
