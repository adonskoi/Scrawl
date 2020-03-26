from flask import Blueprint, render_template, request, redirect, jsonify
from tinydb import Query
from scrawl import db


bp = Blueprint('views', __name__)


@bp.route('/')
def home():
    return render_template('index.html')


@bp.route('/pages')
def pages_get():
    pages = db.table('pages')
    pages_all = pages.all()
    return jsonify(pages_all)


@bp.route('/pages', methods=("POST",))
def pages_post():
    pages = db.table('pages')
    pid = request.json['pid']
    _id = pages.insert({"page_name": request.json['page_name'], 
                        "pid": pid, "content": {}})
    pages.update({"_id": _id}, doc_ids=[_id])
    return jsonify({"success": True, "_id": _id})

 
@bp.route('/pages/<path:_id>', methods=("UPDATE",))
def pages_update(_id: str):
    _id = int(_id)
    pages = db.table('pages')
    pages.update({"page_name": request.json['page_name'], 
                  "content": request.json['content']}, doc_ids=[_id])
    return jsonify({"success": True})


@bp.route('/pages/<path:_id>', methods=("DELETE",))
def pages_delete(_id: str):
    _id = int(_id)
    pages = db.table('pages')
    Page = Query()
    pages.update({"pid": 0}, Page.pid == _id)        
    pages.remove(doc_ids=[_id])
    return jsonify({"success": True})
