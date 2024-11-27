from flask import Blueprint, jsonify
from datetime import datetime


findings_bp = Blueprint('findings', __name__, url_prefix='/engines/pspack')


@findings_bp.route('/getfindings/<scan_id>', methods=["GET"])
def getfindings(scan_id):
    # Dummy data for the sake of the example
    res = {
        "scan_id": scan_id,
        "summary": {
            "nb_issues": 1,
            "nb_info": 1,
            "engine_name": "PsPack",
            "engine_version": "1.0.0"
        },
        "issues": [
            {
                "issue_id": 1,
                "severity": "info",
                "confidence": "certain",
                "target": {
                    "addr": "203.0.113.5",
                    "port_id": "443"
                },
                "title": "Pars Pack engine scan is done",
                "description": "The Pars Pack engine scan has been successfully completed.",
                "solution": "Nothing",
                "type": "service_detection",
                "timestamp": int(datetime.now().timestamp())
            }
        ],
        "status": "success"
    }

    return jsonify(res)
