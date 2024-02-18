
from sqlalchemy.sql import text
from db import db

import messages


#--------- Thread handling methods ---------#

def get_user_threads(user_id, count):
    if count == 0:
        query = text("SELECT id, created, creator_id, topic " \
                "FROM Threads " \
                "WHERE creator_id = :user_id " \
                "ORDER BY created DESC")
        result = db.session.execute(query, {"user_id":user_id})
    else: 
        query = text("SELECT id, created, creator_id, topic " \
                "FROM Threads " \
                "WHERE creator_id = :user_id " \
                "ORDER BY created DESC " \
                "LIMIT :count")
        result = db.session.execute(query, {"user_id":user_id, "count":count})
    threads = result.fetchall()
    return threads

def get_all_threads():
    query = text("SELECT T.id, T.created, T.creator_id, T.topic, U.username " \
                "FROM Threads T, Users U " \
                "WHERE T.creator_id = U.id " \
                "ORDER BY T.created DESC")
    result = db.session.execute(query)
    threads = result.fetchall()
    return threads

def add_thread(creator_id, topic, contents):
    if not _valid_topic(topic):
        raise ValueError("Topic must be between 1 and 50 characters)")
    
    query = text("INSERT INTO Threads (creator_id, topic) " \
                "VALUES (:creator_id, :topic) " \
                "RETURNING id")
    vars = {"creator_id":creator_id, "topic":topic}
    thread = db.session.execute(query, vars)
    thread_id = thread.fetchone()[0]
    messages.add_thread_message(creator_id, thread_id, contents)
    db.session.commit()


#--------- Private topic validation methods ---------#

def _valid_topic(topic):
    return len(topic) >= 1 and len(topic) <= 50
