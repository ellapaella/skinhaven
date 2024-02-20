
from sqlalchemy.sql import text
from db import db


#--------- Skin handling methods ---------#

def get_user_skins(user_id):
    query = text("SELECT S.created, S.creator_id, S.owner_id, S.profile_id, S.skin_name, S.skin_price, U.username AS creator " \
                "FROM Skins S, Users U " \
                "WHERE S.owner_id = :user_id " \
                "AND S.creator_id = U.id")
    result = db.session.execute(query, {"user_id":user_id})
    skins = result.fetchall()
    return skins

def get_profile_skins(user_id, profile_id):
    query = text("SELECT S.created, S.creator_id, S.owner_id, S.profile_id, S.skin_name, S.skin_price, U.username AS creator " \
                "FROM Skins S, Users U " \
                "WHERE S.owner_id = :user_id " \
                "AND S.creator_id = U.id " \
                "AND S.profile_id = :profile_id")
    result = db.session.execute(query, {"user_id":user_id, "profile_id":profile_id})
    skins = result.fetchall()
    return skins

def get_all_skins():
    query = text("SELECT S.created, S.creator_id, S.owner_id, S.profile_id, S.skin_name, S.skin_price, U.username AS owner, P.game " \
                "FROM Skins S, Users U, Profiles P " \
                "WHERE S.owner_id = U.id " \
                "AND S.profile_id = P.id " \
                "ORDER BY S.created DESC")
    result = db.session.execute(query)
    skins = result.fetchall()
    return skins

def add_skin(creator_id, owner_id, profile_id, skin_name, skin_price):
    if not _valid_skin(skin_name, skin_price):
        raise ValueError("Skin name must be between 1 and 50 characters")
    
    query = text("INSERT INTO Skins (creator_id, owner_id, profile_id, skin_name, skin_price) " \
                "VALUES (:creator_id, :owner_id, :profile_id, :skin_name, :skin_price) ")
    vars = {"creator_id":creator_id, "owner_id":owner_id, "profile_id":profile_id, "skin_name":skin_name, "skin_price":skin_price}
    db.session.execute(query, vars)
    db.session.commit()

def change_skin_owner(skin_id, new_owner_id):
    pass

def change_skin_price(skin_id, new_price):
    pass

#--------- Private skin validation methods ---------#

def _valid_skin(skin_name, skin_price):
    if len(skin_name) >= 1 and len(skin_name) <= 50:
        if int(skin_price) >= 1 and int(skin_price) <= 1000:
            return True
    return False