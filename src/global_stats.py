
from flask import (Blueprint,
                   session,
                   render_template,
                   abort)


# local url
page_url = "/stats/"
# blueprint for better python file management
global_stats_page = Blueprint("global_stats", 
                              __name__)

# to add dash pages on the same server we need bootstrap


@global_stats_page.route("/statistics/")
def FUN_stat():
    if session.get("current_user", None):
        return render_template("dash_page.html",
                               dash_url=page_url,
                               min_height=400)
    else:
        return abort(401)
