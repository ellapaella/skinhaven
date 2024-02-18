
from sqlalchemy.sql import text
from db import db


#--------- User's private message methods ---------#

def get_user_pmessages(user_id, count):
    if count == 0:
        query = text("SELECT P.created, P.creator_id, P.target_id, P.topic, P.contents, U.username " \
                    "FROM Privmessages P, Users U " \
                    "WHERE P.target_id = :user_id " \
                    "AND P.creator_id = U.id " \
                    "ORDER BY P.created DESC")
        result = db.session.execute(query, {"user_id":user_id})
    else:
        query = text("SELECT P.created, P.creator_id, P.target_id, P.topic, P.contents, U.username " \
                    "FROM Privmessages P, Users U " \
                    "WHERE P.creator_id = U.id " \
                    "AND P.target_id = :user_id " \
                    "ORDER BY P.created DESC " \
                    "LIMIT :count")
        result = db.session.execute(query, {"user_id":user_id, "count":count})
    pmessages = result.fetchall()
    return pmessages

def add_private_message(creator_id, target_id, topic, contents):
    if not _valid_pmessage(topic, contents):
        raise ValueError('''
                        Topic must be between 1 and 50 characters \n
                        Contents must be between 1 and 1000 characters
                        ''')
    query = text("INSERT INTO Privmessages (creator_id, target_id, topic, contents) " \
                "VALUES (:creator_id, :target_id, :topic, :contents)")
    vars = {"creator_id":creator_id, "target_id":target_id, "topic":topic, "contents":contents}
    db.session.execute(query, vars)
    db.session.commit()


#--------- Thread message methods ---------#
    
def get_thread_messages(thread_id):
    query = text("SELECT * FROM Messages " \
                 "WHERE Messages.thread_id = :id " \
                 "ORDER BY Messages.created DESC")
    result = db.session.execute(query, {"id":thread_id})
    messages = result.fetchall()
    return messages

def add_thread_message(creator_id, thread_id, contents):
    if not _valid_thread_message(contents):
        raise ValueError("Contents must be between 1 and 1000 characters")
    
    query = text("INSERT INTO Threadmessages (creator_id, thread_id, contents) " \
                "VALUES (:creator_id, :thread_id, :contents)")
    vars = {"creator_id":creator_id, "thread_id":thread_id, "content":contents}
    db.session.execute(query, vars)
    db.session.commit()


#--------- Private message validation methods ---------#

def _valid_pmessage(topic, contents):
    if len(topic) >= 1 and len(topic) <= 50:
        if len(contents) >= 1 and len(contents) <= 1000:
            return True
    return False

def _valid_thread_message(contents):
    if len(contents) >= 1 and len(contents) <= 1000:
        return True
    return False
