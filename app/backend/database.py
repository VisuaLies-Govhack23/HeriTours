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
                answer text,
                primary key (siteid, userid)
            )
        """
    )


def get_stories(siteid):
    rows = conn.execute(
        """
            select userid, vote, story from user_stories where siteid = ?
        """,
        [siteid],
    ).fetchall()
    return rows


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


def get_answered_questions(siteid, userid):
    rows = conn.execute(
        """
            select questionid from user_questions where siteid = ? and userid = ?
        """,
        [siteid, userid],
    ).fetchall()
    return [row[0] for row in rows]
