from flask import Blueprint, current_app


clean_bp = Blueprint('clean', __name__, url_prefix='/engines/pspack')


@clean_bp.route("/clean")
def clean():
    """Clean all scans."""
    return current_app.engine.clean()


@clean_bp.route("/clean/<scan_id>")
def clean_scan(scan_id):
    """Clean scan identified by id."""
    return current_app.engine.clean_scan(scan_id)
