from flask import Blueprint, request, jsonify, current_app
import json
from models.scan_model import TaskModel
from utils.constants import APP_BASE_DIR, REPORT_PATH
from utils.helpers import error_response, folder_creator
from validation import validate_scan_data
from tasks import start_scan_job


scan_bp = Blueprint('scan', __name__, url_prefix='/engines/pspack')


@scan_bp.route('/startscan', methods=['POST'])
def start_scan():
    res = {"page": "startscan"}
    data = json.loads(request.data.decode("utf-8"))

    # Validate the scan data
    is_valid, validation_message = validate_scan_data(data)
    if not is_valid:
        return error_response(res, "error", validation_message)

    scan_id, assets = str(data.get("scan_id")), data.get('assets')


    for asset in assets:
        report_folder = folder_creator(REPORT_PATH, scan_id, asset['value'])

        job = start_scan_job.delay(scan_id, asset, report_folder)

        task = TaskModel(
            scan_id=scan_id,
            asset_value=asset['value'],
            asset_type=asset['datatype'],
            status=job.status,
            job_id=job.id,
        )

        task.save()

    return jsonify({**res, **{"status": "accepted", "details": {"scan_id": scan_id}}})



@scan_bp.route('/stopscans')
def stop():
    res = {"page": "stop_scans"}
    #? stop all jobs

    res.update({"status": "SUCCESS"})
    return jsonify(res)


@scan_bp.route('/stop/<scan_id>')
def stop_scan(scan_id):
    res = {"page": "stop_scan"}
    killed_jobs = []
    # ? stop jobs with scan id

    res.update({"status": "success", "details": {
               "pid": " ".join(killed_jobs), "scan_id": scan_id}})
    return jsonify(res), 200