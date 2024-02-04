
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

from db import db


def signup(username, password):
    if _validate_username(username):
        if _validate_password(password):
            if not _username_taken(username):
                passhash = generate_password_hash(password)
                query = text("INSERT INTO Users (created, username, passhash, is_admin) " \
                            "VALUES (NOW(), :username, :passhash, TRUE)")
                db.session.execute(query, {"username":username, "passhash":passhash})
                db.session.commit()
            else:
                raise ValueError("Username taken")
        else:
            raise ValueError("Password must be between 8 and 50 characters")
    else:
        raise ValueError("Username must be between 3 and 20 characters")

def login(username, password):
    query = text("SELECT username, passhash FROM Users " \
                 "WHERE username=:username")
    result = db.session.execute(query, {"username":username})
    user = result.fetchone()
    if not user:
        raise ValueError("No such user")
    else:
        if check_password_hash(user.passhash, password):
            return
        else:
            raise ValueError("Wrong password")
        
def add_profile(creator, profilename, game):
    if _validate_profile(profilename, game):
        user_id = get_user_id(creator)
        query = text("INSERT INTO Profiles (created, user_id, profilename, game)" \
                    "VALUES (NOW(), :user_id, :profilename, :game)")
        db.session.execute(query, {"user_id":user_id, "profilename":profilename, "game":game})
        db.session.commit()
    else:
        raise ValueError("Either profile name or game too short or long")

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

def _validate_username(username):
    if len(username) > 2 & len(username) <= 20:
        return True
    return False

def _validate_password(password):
    if len(password) > 7 & len(password) <= 50:
        return True
    return False

def _username_taken(username):
    query = text("SELECT * FROM Users WHERE username=:username")
    result = db.session.execute(query, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    return True

def _validate_profile(profilename, game):
    if len(profilename) > 0 & len(profilename) <= 50:
        if len(game) > 0 & len(game) <= 100:
            return True
    return False
