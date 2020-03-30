from flask import Flask, render_template
from tinydb import TinyDB

db = None

def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    if config_filename:
        app.config.from_pyfile(config_filename)
    global db
    db = TinyDB(app.config.get('DB'))
    register_blueprints(app)
    create_simple_page()

    @app.route('/')
    def home():
        return render_template('index.html')

    return app


def register_blueprints(app):    
    from . import views
    app.register_blueprint(views.bp, url_prefix='/api')


def create_simple_page():
    pages = db.table('pages')
    pages_all = pages.all()
    if len(pages_all) == 0:
        _id = pages.insert({"page_name": "sample page name", "pid": 0, "content": "start typing here"})
        pages.update({"_id": _id}, doc_ids=[_id])
    else:
        pass
    
