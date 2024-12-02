from flask import Blueprint, current_app
from flask.json import jsonify


clean_bp = Blueprint('clean', __name__, url_prefix='/engines/pspack')


@clean_bp.route('/clean')
def clean():
    """Clean all the scans."""
    res = {"page": "clean"}

    res.update({"status": "success"})
    return jsonify(res), 200


@clean_bp.route('/clean/<scan_id>')
def clean_scan(scan_id):
    res = {"page": "clean"}

    # ? clear tasks with scan id

    res.update({"status": "removed"})
    return jsonify(res), 200