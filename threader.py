
from sqlalchemy.sql import text

from db import db
import messager, users


def get_threads():
    query = text("SELECT * FROM Threads, Users " \
                 "WHERE Threads.creator_id = Users.id")
    result = db.session.execute(query)
    threads = result.fetchall()
    return threads

def get_users_threads(creator):
    creator_id = users.get_user_id(creator)
    query = text("SELECT * FROM Threads, Users " \
                 "WHERE Threads.creator_id = :creator_id")
    result = db.session.execute(query, {"creator_id":creator_id})
    threads = result.fetchall()
    return threads

def get_thread_messages(thread_id):
    query = text("SELECT * FROM Messages " \
                 "WHERE Messages.thread_id = :id " \
                 "ORDER BY Messages.created DESC")
    result = db.session.execute(query, {"id":thread_id})
    messages = result.fetchall()
    return messages

def add_thread(creator, topic, msg_contents):
    if _validate_topic(topic):
        creator_id = users.get_user_id(creator)
        topic = topic
        query = text("INSERT INTO Threads (created, creator_id, topic) " \
                     "VALUES (NOW(), :creator_id, :topic) RETURNING id")
        thread_id = db.session.execute(query, {"creator_id":creator_id, "topic":topic})
        thread_id = thread_id.fetchone()[0]
        messager.add_thread_message(creator_id, thread_id, msg_contents)
        db.session.commit()
    else:
        raise ValueError("Topic doesn't meet the standards (must be between 1-100 characters)")
    
def add_message(creator, thread_id, msg_contents):
    creator_id = users.get_user_id(creator)
    messager.add_thread_message(creator_id, thread_id, msg_contents)

def _validate_topic(topic):
    if len(topic) > 0 & len(topic) <= 100:
        return True
    return False


