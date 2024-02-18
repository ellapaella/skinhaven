
from sqlalchemy.sql import text
from db import db


#--------- Game profile handling methods ---------#

def get_user_profiles(user_id, count):
    if count == 0:
        query = text("SELECT id, created, user_id, profile_name, game_username, game " \
                    "FROM Profiles " \
                    "WHERE Profiles.user_id = :user_id " \
                    "ORDER BY created DESC")
        result = db.session.execute(query, {"user_id":user_id})
    else:
        query = text("SELECT id, created, user_id, profile_name, game_username, game " \
                    "FROM Profiles " \
                    "WHERE Profiles.user_id = :user_id " \
                    "ORDER BY created DESC " \
                    "LIMIT :count")
        result = db.session.execute(query, {"user_id":user_id, "count":count})
    profiles = result.fetchall()
    return profiles

def add_profile(user_id, profile_name, game_username, game):
    if not _valid_game_profile(profile_name, game_username, game):
        raise ValueError('''
                        Profile name must be between 3 and 50 characters \n
                        Game username must be between 3 and 50 characters \n
                        Game name must be between 1 and 100 characters
                        ''')
    query = text("INSERT INTO Profiles (user_id, profile_name, game_username, game)" \
                "VALUES (:user_id, :profile_name, :game_username, :game)")
    vars = {"user_id":user_id, "profile_name":profile_name, "game_username":game_username, "game":game}
    db.session.execute(query, vars)
    db.session.commit()


#--------- Private game profile validation methods ---------#

def _valid_game_profile(profile_name, game_username, game):
    if len(profile_name) >= 3 and len(profile_name) <= 50:
        if len(game_username) >= 3 and len(game_username) <= 50:
            if len(game) >= 1 and len(game) <= 100:
                return True
    return False