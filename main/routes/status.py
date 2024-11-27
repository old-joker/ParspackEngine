import os
from flask import Blueprint, current_app, jsonify
from logger import LOG
from messages import (  # Adjust the import based on your directory structure
    SCAN_ID_NOT_FOUND,
    SCAN_ENCOUNTERED_ERROR,
    NO_PID_FOUND,
    OUTPUT_NOT_AVAILABLE,
    STATUS_UNKNOWN,
)
from models.scan_model import TaskModel
from utils.constants import REPORT_PATH, CeleryStatus, PatrwolStatus
from utils.dojo_module import upload_scans_from_directory
from utils.helpers import error_response, zip_folder
from celery.result import AsyncResult
from redis_om import Migrator

from utils.telegram import send_document_telegram


status_bp = Blueprint('status', __name__, url_prefix='/engines/pspack')


@status_bp.route('/status')
def status():
    return current_app.engine.get_status()


@status_bp.route('/status/<scan_id>')
def status_scan(scan_id):
    res = {"page": "status", "status": STATUS_UNKNOWN}

    Migrator().run()

    tasks = TaskModel.find(TaskModel.scan_id == scan_id).all()

    # Check if scan_id exists
    if not len(tasks):
        return error_response(res, "error", SCAN_ID_NOT_FOUND.format(scan_id))

    done = True

    for task in tasks:
        result = AsyncResult(task.job_id)

        if result.state == CeleryStatus.SUCCESS.value and task.report_sent.lower() == 'false':
            upload_scans_from_directory(os.path.join(
                REPORT_PATH, scan_id, task.asset_value))
            LOG.info(f"{task.asset_value} -> Sent to dojo")
            task.report_sent = "true"
            task.save()

        elif result.state == CeleryStatus.FAILURE.value:
            res.update({"status": "ERROR", "reason": "Something Wrong"})
            return jsonify(res)

        elif result.state == CeleryStatus.PENDING.value:
            done = False
            LOG.info(f"{task.asset_value} -> {result.state}")

    if done:
        ziped_result = zip_folder(os.path.join(REPORT_PATH, scan_id))
        send_document_telegram(ziped_result)
        LOG.info("Sent to telegram")
        os.remove(ziped_result)
        LOG.info(f"{ziped_result} removed!")
        res.update({"status": "FINISHED"})
        LOG.info("Done")
    else:
        LOG.info(f"{scan_id} -> Still scaning")
        res.update({
            "status": "SCANNING",
        })

    return jsonify(res)


# * "info": {
# *     asset: {
# *         "pid": proc.pid,
# *         "cmd": report["proc_cmd"],
# *         "output": stdout.decode('utf-8') if stdout else '',
# *         "error": stderr.decode('utf-8') if stderr else ''
# *     }
# * }
