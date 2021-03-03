
import os
from flaskext.markdown import Markdown
from glob import glob




def prepare_static_pages(folder):
    markdown_pages = {}
    for f in glob(os.path.join(folder, "*.md")):
        title, content = parse_markdown(f)
        markdown_pages[title] = content
    return markdown_pages

def parse_markdown(f):
    title = f.split('/')[-1].split('.')[0]
    with open(f, 'r') as fp:
        content = "".join(fp.readlines())
    return title, content



