
import os
import datetime
import hashlib
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash

# from database import list_users, verify, delete_user_from_db, add_user
# from database import read_note_from_db, write_note_into_db, delete_note_from_db, match_user_id_with_note_id
# from database import image_upload_record, list_images_for_user, match_user_id_with_image_uid, delete_image_from_db
from werkzeug.utils import secure_filename

from utils.sql_utils import add_user, list_users_name, list_users, list_users_id, delete_user_from_db, verify, check_admin
from utils.markdown_utils import Markdown, prepare_static_pages

app = Flask(__name__)
app.config.from_object('config')

Markdown(app)

markdown_down_pages_static = prepare_static_pages("docs/markdown")


@app.errorhandler(401)
def FUN_401(error):
    return render_template("page_401.html"), 401


@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/rules/")
def FUN_rule():
    return render_template("doc_main.html", keys=markdown_down_pages_static.keys())


@app.route("/rules/<title>")
def FUN_template_title(title):
    if title in markdown_down_pages_static.keys():
        mkd_text = markdown_down_pages_static[title]
        return render_template("doc_template.html", mkd_text=mkd_text)
    else:
        return abort(401)


def user_info_with_delete():
    user_info = list_users()
    user_info = list(zip(*user_info))
    delete_buttons = [x + y for x,y in zip(["/delete_user/"] * len(user_info[1]), user_info[1])]
    user_info.append(tuple(delete_buttons))
    user_info = zip(*user_info)
    return user_info

@app.route("/add_user/")
def FUN_admin():
    if True: #session.get("current_user", None) == "ADMIN":
        user_info = user_info_with_delete()
        return render_template("add_user.html", users = user_info)
    else:
        return abort(401)


@app.route("/add_user", methods = ["POST"])
def FUN_add_user():
    print("admin", session.get("is_admin", None))
    if session.get("is_admin", None): # only Admin should be able to add user.
        # before we add the user, we need to ensure this is doesn't exsit in database. We also need to ensure the id is valid.
        if request.form.get('id') in list_users_name():
            user_info = user_info_with_delete()
            return(render_template("admin.html", id_to_add_is_duplicated = True, users = user_info))
        if " " in request.form.get('id') or "'" in request.form.get('id'):
            user_info = user_info_with_delete()
            return(render_template("admin.html", id_to_add_is_invalid = True, users = user_table))
        else:
            id = max(list_users_id()) + 1
            is_admin = 1 if request.form.get('is_admin') in ['yes', '1', 'Admin'] else 0
            add_user(id, request.form.get('id'), request.form.get('pw'), is_admin)
            return(redirect(url_for("FUN_admin")))
    else:
        return abort(401)


@app.route("/delete_user/<name>/", methods = ['GET'])
def FUN_delete_user(name):
    if session.get("is_admin", None):
        if check_admin(name): # ADMIN account can't be deleted.
            return abort(401)

        delete_user_from_db(name)
        return(redirect(url_for("FUN_admin")))
    else:
        return abort(401)


@app.route("/login", methods = ["POST"])
def FUN_login():
    id_submitted = request.form.get("id")
    if (id_submitted in list_users_name()) and verify(id_submitted, request.form.get("pw")):
        session['current_user'] = id_submitted
        session['is_admin'] = check_admin(id_submitted)
    return(redirect(url_for("FUN_root")))

@app.route("/logout/")
def FUN_logout():
    session.pop("current_user", None)
    session.pop("is_admin", None)
    return(redirect(url_for("FUN_root")))



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
