from flask import Blueprint, current_app

report_bp = Blueprint('report', __name__, url_prefix='/engines/pspack')

@report_bp.route('/getreport/<scan_id>')
def getreport(scan_id):
    return current_app.engine.getreport(scan_id)
