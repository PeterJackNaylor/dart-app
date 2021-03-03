# import markdown
# from flask import Flask
# import markdown.extensions.fenced_code
# from pygments.formatters import HtmlFormatter

# app = Flask(__name__)

# @app.route("/")
# def index():
#     readme_file = open("README.md", "r")
#     md_template_string = markdown.markdown(
#         readme_file.read(), extensions=["fenced_code", "codehilite"]
#     )
    
#     # Generate Css for syntax highlighting
#     formatter = HtmlFormatter(style="emacs", full=True, cssclass="codehilite")
#     css_string = formatter.get_style_defs()
#     md_css_string = "<style>" + css_string + "</style>"
    
#     md_template = md_css_string + md_template_string
#     return md_template


# if __name__ == "__main__":
#     app.run()
from flask import Flask,url_for,render_template,request
from flaskext.markdown import Markdown

# Init App
app = Flask(__name__)
Markdown(app)

@app.route('/')
def index():
	mkd_text = "## Your Markdown Here "
	return render_template('doc_template.html', mkd_text=mkd_text)

if __name__ == '__main__':
	app.run(debug=True)
