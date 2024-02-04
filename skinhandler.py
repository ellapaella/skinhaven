
from sqlalchemy.sql import text

from db import db
import users


def get_skins():
    query = text("SELECT * FROM Skins, Users, Profiles " \
                 "WHERE Skins.owner_id = Users.id " \
                "AND Skins.profile_id = Profiles.id")
    result = db.session.execute(query)
    skins = result.fetchall()
    return skins

def get_profile_skins(username, profile_number):
    user_id = users.get_user_id(username)
    query = text("SELECT * FROM Skins, Profiles " \
                "WHERE Skins.owner_id = :user_id " \
                "AND Profiles.profile_number = :profile_number")
    result = db.session.execute(query, {"user_id":user_id, "profile_number":profile_number})
    skins = result.fetchall()
    return skins
