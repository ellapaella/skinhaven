
from sqlalchemy.sql import text
from db import db


#--------- Skin handling methods ---------#

def get_user_skins(user_id):
    query = text("SELECT S.created, S.creator_id, S.owner_id, S.profile_id, S.skin_name, S.skin_price, U.username " \
                "FROM Skins S, Users U " \
                "WHERE S.owner_id = :user_id " \
                "AND S.creator_id = U.id")
    result = db.session.execute(query, {"user_id":user_id})
    skins = result.fetchall()
    return skins

def get_profile_skins(user_id, profile_id):
    query = text("SELECT S.created, S.creator_id, S.owner_id, S.profile_id, S.skin_name, s.skin_price, U.username " \
                "FROM Skins S, Users U " \
                "WHERE S.owner_id = :user_id " \
                "AND profile_id = :profile_id " \
                "AND S.creator_id = U.id")
    result = db.session.execute(query, {"user_id":user_id, "profile_id":profile_id})
    skins = result.fetchall()
    return skins

def get_all_skins():
    query = text("SELECT S.created, S.creator_id, S.owner_id, S.profile_id, S.skin_name, S.skin_price " \
                "FROM Skins S, Profiles P, Users U " \
                "WHERE S.owner_id = U.id " \
                "AND S.profile_id = P.id")
    result = db.session.execute(query)
    skins = result.fetchall()
    return skins

def add_skin(creator_id, owner_id, profile_id, skin_name, skin_price):
    query = text("INSERT INTO Skins (creator_id, owner_id, profile_id, skin_name, skin_price) " \
                "VALUES (:creator_id, :owner_id, :profile_id, :skin_name, :skin_price) ")
    vars = {"creator_id":creator_id, "owner_id":owner_id, "profile_id":profile_id, "skin_name":skin_name, "skin_price":skin_price}
    skin = db.session.execute(query, vars)
    db.session.commit()

def change_skin_owner():
    pass

def change_skin_price():
    pass
