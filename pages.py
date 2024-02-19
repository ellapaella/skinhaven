
from flask import redirect, render_template, request, session, abort
from app import app

import users, messages, profiles, skins, threads


#--------- Main page ---------#

@app.route("/")
def index():
    return render_template("index.html")


#--------- Signup and login pages ---------#

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/signup/validate", methods=["POST"])
def signup_validate():
    username = request.form["username"]
    password = request.form["password"]

    try:
        users.signup(username, password)
        message = "Successfully signed up!"
        return render_template("return_main_page.html", message = message)
    except Exception as e:
        return render_template("error.html", error=e)
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/validate", methods=["POST"])
def login_validate():
    username = request.form["username"]
    password = request.form["password"]
    try:
        users.login(username, password)
        message = "Login successful!"
        return render_template("return_main_page.html", message=message)
    except Exception as e:
        return render_template("error.html", error=e)

@app.route("/logout")
def logout():
    del session["user_id"]
    del session["username"]
    del session["csrf_token"]
    return redirect("/")


#--------- Account related pages---------#

@app.route("/account/<username>")
def account(username):
    if username == session["username"]:
        pmsgs = messages.get_user_pmessages(session["user_id"], 3)
        profs = profiles.get_user_profiles(session["user_id"], 3)
        skns = skins.get_user_skins(session["user_id"])
        thrds = threads.get_user_threads(session["user_id"], 3)
        return render_template("account.html", pmessages=pmsgs, profiles=profs, skins=skns, threads=thrds)
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)

@app.route("/account/<username>/messages")
def account_messages(username):
    if username == session["username"]:
        pmsgs = messages.get_user_pmessages(session["user_id"], 0)
        return render_template("pmessages.html", pmessages=pmsgs)
    
@app.route("/account/<username>/messages/new")
def account_messages_new(username):
    if username == session["username"]:
        return render_template("pmessage_new.html")
    
@app.route("/account/<username>/messages/new/validate", methods=["POST"])
def account_messages_new_validate(username):
    if username == session["username"]:
        target_username = request.form["target_username"]
        topic = request.form["topic"]
        contents = request.form["contents"]
        csrf_token = request.form["csrf_token"]

        if csrf_token != session["csrf_token"]:
            abort(403)

        try:
            target_id = users.get_user_id(target_username)
            messages.add_private_message(session["user_id"], target_id, topic, contents)
            return redirect("/account/"+session["username"]+"/messages")
        except Exception as e:
            return render_template("error.html", error=e)
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)

@app.route("/account/<username>/profiles")
def account_profiles(username):
    if username == session["username"]:
        profs = profiles.get_user_profiles(session["user_id"], 0)
        skns = skins.get_user_skins(session["user_id"])
        return render_template("profiles.html", profiles=profs, skins=skns)
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)

@app.route("/account/<username>/profiles/new")
def account_profiles_new(username):
    if username == session["username"]:
        return render_template("profile_new.html", username=session["username"])
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)
    
@app.route("/account/<username>/profiles/new/validate", methods=["POST"])
def account_profiles_new_validate(username):
    if username == session["username"]:
        profile_name = request.form["profile_name"]
        game_username = request.form["game_username"]
        game = request.form["game"]
        csrf_token = request.form["csrf_token"]

        if csrf_token != session["csrf_token"]:
            abort(403)

        try:
            profiles.add_profile(session["user_id"], profile_name, game_username, game)
            return redirect("/account/"+session["username"])
        except Exception as e:
            return render_template("error.html", error=e)
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)
    
@app.route("/account/<username>/profiles/<int:profile_id>")
def account_profiles_id(username, profile_id):
    if session["username"] == username:
        prof = profiles.get_user_profile(session["user_id"], profile_id)
        profile_skins = skins.get_profile_skins(session["user_id"], profile_id)
        return render_template("profile.html", profile=prof, skins=profile_skins)
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)
    
@app.route("/account/<username>/profiles/skin/add", methods=["POST"])
def add_skin(username):
    if session["username"] == username:
        profile_id = request.form["profile_id"]
        skin_name = request.form["name"]
        skin_price = request.form["price"]
        csrf_token = request.form["csrf_token"]

        if csrf_token != session["csrf_token"]:
            abort(403)

        try:
            skins.add_skin(session["user_id"], session["user_id"], profile_id, skin_name, skin_price)
            return redirect("/account/"+session["username"]+"/profiles/"+profile_id)
        except Exception as e:
            return render_template("error.html", error=e)
    else:
        message = "You do not have the necessary credentials"
        return render_template("forbidden.html", message=message)


#--------- Thread pages ---------#

@app.route("/threads")
def threads_all():
    rows = threads.get_all_threads()
    return render_template("threads.html", threads=rows)

@app.route("/threads/new")
def threads_new():
    return render_template("thread_new.html")

@app.route("/threads/new/validate", methods=["POST"])
def threads_new_validate():
    topic = request.form["topic"]
    contents = request.form["contents"]
    csrf_token = request.form["csrf_token"]

    if csrf_token != session["csrf_token"]:
        abort(403)

    try:
        threads.add_thread(session["user_id"], topic, contents)
    except ValueError as e:
        print(e)
    return redirect("/threads")

@app.route("/threads/<int:thread_id>")
def threads_id(thread_id):
    msgs = messages.get_thread_messages(thread_id)
    return render_template("thread.html", thread_id=thread_id, messages=msgs)

@app.route("/threads/message/new/validate", methods=["POST"])
def message_new_validate():
    thread_id = request.form["thread_id"]
    contents = request.form["contents"]
    csrf_token = request.form["csrf_token"]

    if csrf_token != session["csrf_token"]:
        abort(403)

    try:
        messages.add_thread_message(session["user_id"], thread_id, contents)
        return redirect("/threads/"+thread_id)
    except Exception as e:
        return render_template("error.html", error=e)


#--------- Skin handling ---------#

@app.route("/skins")
def skins_all():
    skns = skins.get_all_skins()
    return render_template("skins.html", skins=skns)

@app.route("/skins/<int:skin_id>")
def skinner_id(skin_id):
    pass