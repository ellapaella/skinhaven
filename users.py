
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from flask import session

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
            # session["csrf_token"] = secrets.token_hex(16)
            return
        else:
            raise ValueError("Wrong password")
        

#--------- Profile handling methods ---------#

def add_profile(creator, profilename, game):
    if _validate_profile(profilename, game):
        user_id = get_user_id(creator)
        query = text("INSERT INTO Profiles (created, user_id, profilename, game)" \
                    "VALUES (NOW(), :user_id, :profilename, :game)")
        db.session.execute(query, {"user_id":user_id, "profilename":profilename, "game":game})
        db.session.commit()
    else:
        raise ValueError("Game profile name must be between 3 and 50 characters\n" \
                         "Game name must be between 1 and 100 characters")


def get_user_id(username):
    query = text("SELECT id FROM Users WHERE username=:username")
    result = db.session.execute(query, {"username":username})
    user_id = result.fetchone()[0]
    return user_id


def get_user_name(id):
    query = text("SELECT username FROM Users WHERE id = :id")
    result = db.session.execute(query, {"id":id})
    username = result.fetchone()[0]
    return username


def get_user_profiles(username):
    user_id = get_user_id(username)
    query = text("SELECT * FROM Profiles WHERE Profiles.user_id = :user_id")
    result = db.session.execute(query, {"user_id":user_id})
    profiles = result.fetchall()
    return profiles


def get_user_profile(username, profile_number):
    user_id = get_user_id(username)
    query = text("SELECT * FROM Profiles " \
                "WHERE Profiles.user_id = :user_id " \
                "AND Profiles.profile_number = :profile_number")
    result = db.session.execute(query, {"user_id":user_id, "profile_number":profile_number})
    profile = result.fetchone()
    return profile


def get_user_skins(username):
    user_id = get_user_id(username)
    query = text("SELECT * FROM Skins WHERE Skins.owner_id = :user_id")
    result = db.session.execute(query, {"user_id":user_id})
    skins = result.fetchall()
    return skins


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

def _validate_profile(profilename, game):
    if len(profilename) >= 3 and len(profilename) <= 50:
        if len(game) >= 1 and len(game) <= 100:
            return True
    return False
