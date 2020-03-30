from flask import Blueprint, render_template, request, redirect, jsonify
from tinydb import Query
from scrawl import db


bp = Blueprint('views', __name__)


@bp.route('/pages')
def pages_get():
    pages = db.table('pages')
    pages_all = pages.all()
    return jsonify(pages_all)


@bp.route('/pages', methods=("POST",))
def pages_post():
    pages = db.table('pages')
    try:
        pid = request.json['pid']
        page_name = request.json['page_name']
    except:
        return jsonify({"error": {"message": "wrong pid or/and page name"}}), 500
    _id = pages.insert({"page_name": page_name, 
                        "pid": pid, "content": {}})
    pages.update({"_id": _id}, doc_ids=[_id])
    return jsonify({"_id": _id}), 201

 
@bp.route('/pages/<path:_id>', methods=("PATCH",))
def pages_patch(_id: str):
    _id = int(_id)
    pages = db.table('pages')
    if pages.contains(doc_ids=[_id]):
        pages.update({"page_name": request.json['page_name'], 
                        "content": request.json['content']}, doc_ids=[_id])
        return jsonify({})
    else:
        return jsonify({"error": {"message": "page not found"}}), 404


@bp.route('/pages/<path:_id>', methods=("DELETE",))
def pages_delete(_id: str):
    _id = int(_id)
    pages = db.table('pages')
    if pages.contains(doc_ids=[_id]):
        Page = Query()
        pages.update({"pid": 0}, Page.pid == _id)        
        pages.remove(doc_ids=[_id])
        return jsonify({})
    else:
        return jsonify({"error": {"message": "page not found"}}), 404    
