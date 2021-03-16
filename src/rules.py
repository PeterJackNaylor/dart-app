

from flask import (Blueprint,
                   render_template,
                   abort)
from .utils.markdown import prepare_static_pages


rule_page = Blueprint("rule_page",
                      __name__)


markdown_down_pages_static = prepare_static_pages("docs/markdown")


@rule_page.route("/rules/")
def FUN_rule():
    return render_template("doc_main.html",
                           keys=markdown_down_pages_static.keys())


@rule_page.route("/rules/<title>")
def FUN_template_title(title):
    if title in markdown_down_pages_static.keys():
        mkd_text = markdown_down_pages_static[title]
        return render_template("doc_template.html", mkd_text=mkd_text)
    else:
        return abort(401)
