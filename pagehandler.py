
import secrets
from flask import redirect, render_template, request, session, abort
from app import app

# import skinhandler
# import users
# import threader

#--------- Main Page ---------#

@app.route("/")
def index():
    return render_template("index.html")

# #--------- Signup and Login handling ---------#

# @app.route("/signup")
# def signup():
#     return render_template("signup.html")

# @app.route("/signup/validate", methods=['POST'])
# def signup_validate():
#     username = request.form["username"]
#     password = request.form["password"]

#     try:
#         users.signup(username, password)
#         return render_template("signup_success.html")
#     except Exception as e:
#         return render_template("error.html", error=e)
    
# @app.route("/login")
# def login():
#     return render_template("login.html")

# @app.route("/login/validate", methods=['POST'])
# def login_validate():
#     username = request.form["username"]
#     password = request.form["password"]
#     try:
#         users.login(username, password)
#         session["username"] = username
#         session["csrf_token"] = secrets.token_hex(16)
#         return redirect("/")
#     except Exception as e:
#         return render_template("error.html", error=e)

# @app.route("/logout")
# def logout():
#     del session["username"]
#     del session["csrf_token"]
#     return redirect("/")

# #--------- Account handling ---------#

# @app.route("/account/<username>")
# def account(username):
#     if session["username"] == username:
#         threads = threader.get_users_threads(username)
#         profiles = users.get_user_profiles(username)
#         skins = users.get_user_skins(username)
#         return render_template("account.html", username=username, profiles=profiles, skins=skins, threads=threads)
#     else:
#         return render_template("no_credentials.html")

# @app.route("/account/profiles/new")
# def account_profiles_new():
#     if session["username"]:
#         return render_template("profile_new.html", username=session["username"])
#     else:
#         return render_template("no_credentials.html")
    
# @app.route("/account/profiles/new/validate", methods=['POST'])
# def account_profiles_new_validate():
#     creator = request.form["creator"]
#     csrf_token = request.form["csrf_token"]
#     profilename = request.form["profile_name"]
#     game = request.form["game"]

#     if csrf_token != session["csrf_token"]:
#         abort(403)

#     try:
#         users.add_profile(creator, profilename, game)
#         return redirect("/account/"+session["username"])
#     except ValueError as e:
#         return render_template("error.html", error=e)
    
# @app.route("/account/<username>/profiles/<int:profile_number>")
# def account_profiles_id(username, profile_number):
#     if session["username"] == username:
#         profile = users.get_user_profile(username, profile_number)
#         profile_skins = skinhandler.get_profile_skins(username, profile_number)
#         return render_template("profile.html", profile=profile, skins=profile_skins)
#     else:
#         return render_template("no_credentials.html")

# #--------- Thread handling ---------#

# @app.route("/threads")
# def threads():
#     rows = threader.get_threads()
#     return render_template("threads.html", threads=rows)

# @app.route("/threads/new")
# def threads_new():
#     return render_template("threads_new.html")

# @app.route("/threads/new/validate", methods=['POST'])
# def threads_new_validate():
#     creator = request.form["creator"]
#     csrf_token = request.form["csrf_token"]
#     topic = request.form["topic"]
#     msg_contents = request.form["msg_contents"]

#     if csrf_token != session["csrf_token"]:
#         abort(403)

#     try:
#         threader.add_thread(creator, topic, msg_contents)
#     except ValueError as e:
#         print(e)
#     return redirect("/threads")

# @app.route("/threads/<int:id>")
# def threads_id(id):
#     thread_id = id
#     messages = threader.get_thread_messages(thread_id)
#     return render_template("threads_id.html", thread_id=thread_id, messages=messages)

# @app.route("/threads/message/new/validate", methods=['POST'])
# def message_new_validate():
#     creator = request.form["creator"]
#     csrf_token = request.form["csrf_token"]
#     thread_id = request.form["thread_id"]
#     msg_contents = request.form["message"]

#     if csrf_token != session["csrf_token"]:
#         abort(403)

#     try:
#         threader.add_message(creator, thread_id, msg_contents)
#         return redirect("/threads/"+thread_id)
#     except Exception as e:
#         return render_template("error.html", error=e)

# #--------- Skin handling ---------#

# @app.route("/skins")
# def skinner():
#     skins = skinhandler.get_skins()
#     return render_template("skins.html", skins=skins)
