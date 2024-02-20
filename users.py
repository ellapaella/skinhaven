
from sqlalchemy.sql import text
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
import secrets

from db import db


#--------- Signup and login handling methods ---------#

def signup(username, password):

    if not _valid_username(username):
        raise ValueError("Username must be between 3 and 20 characters")
    if not _valid_password(password):
        raise ValueError("Password must be between 8 and 100 characters")
    if _username_taken(username):
        raise ValueError("Username taken")
    
    passhash = generate_password_hash(password)
    query = text("INSERT INTO Users (username, passhash) " \
                "VALUES (:username, :passhash)")
    db.session.execute(query, {"username":username, "passhash":passhash})
    db.session.commit()

def login(username, password):

    query = text("SELECT id, username, passhash FROM Users " \
                 "WHERE username=:username")
    result = db.session.execute(query, {"username":username})
    user = result.fetchone()
    if not user:
        raise ValueError("No such user")
    else:
        if check_password_hash(user.passhash, password):
            session["user_id"] = user.id
            session["username"] = user.username
            session["csrf_token"] = secrets.token_hex(16)
            return
        else:
            raise ValueError("Wrong password")
        

#--------- Getter methods ---------#

def get_user_id(username):
    query = text("SELECT id FROM Users WHERE username=:username")
    result = db.session.execute(query, {"username":username})
    user_id = result.fetchone()[0]
    if not user_id:
        raise ValueError("There is no such username")
    return user_id

def get_user_name(id):
    query = text("SELECT username FROM Users WHERE id = :id")
    result = db.session.execute(query, {"id":id})
    username = result.fetchone()[0]
    return username

def get_usernamelist():
    query = text("SELECT username " \
                "FROM Users")
    result = db.session.execute(query)
    usernamelist = result.fetchall()
    return usernamelist


#--------- Private validation methods ---------#

def _valid_username(username):
    return len(username) >= 3 and len(username) <= 20

def _valid_password(password):
    return len(password) >= 8 and len(password) <= 100

def _username_taken(username):
    query = text("SELECT username FROM Users WHERE username=:username")
    result = db.session.execute(query, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    return True
