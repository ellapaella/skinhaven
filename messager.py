
from sqlalchemy.sql import text

from db import db
import users


def add_thread_message(creator_id, thread_id, msg_contents):
    if _validate_message(msg_contents):
        creator = users.get_user_name(creator_id)
        query = text("INSERT INTO Messages (created, creator_id, creator, thread_id, content) " \
                     "VALUES (NOW(), :creator_id, :creator, :thread_id, :content)")
        attrs = {"creator_id":creator_id, "creator":creator, "thread_id":thread_id, "content":msg_contents}
        db.session.execute(query, attrs)
        db.session.commit()
    else:
        raise ValueError("Message doesn't meet standards (must be between 1-1000 characters)")

def add_private_message(sender_id, target_id, msg_contents):
    if _validate_message(msg_contents):
        query = text("INSERT INTO Privmessages (created, creator_id, target_id, content) " \
                     "VALUES (NOW(), :sender_id, :target_id, :content)")
        db.session.execute(query, {"sender_id":sender_id, "target_id":target_id, "content":msg_contents})
        db.session.commit()

def _validate_message(msg_contents):
    if len(msg_contents) > 0 & len(msg_contents) <= 1000:
        return True
    return False
