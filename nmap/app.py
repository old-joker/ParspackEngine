from flask import Flask, request, jsonify
from nmap_tasks import run_nmap_task
from celery.result import AsyncResult
import asyncio

app = Flask(__name__)

@app.route('/run', methods=['POST'])
async def run_nmap():
    """Handle Nmap scan requests asynchronously by offloading to Celery."""
    target = request.json.get('target')
    scan_type = request.json.get('scan_type', '-sV')  # Default to service/version detection

    if not target:
        return jsonify({"error": "Target IP/Domain is required"}), 400

    # Offload the Nmap scan to Celery
    task = run_nmap_task.delay(target, scan_type)
    return jsonify({"message": "Scan started", "task_id": task.id}), 202

@app.route('/status/<task_id>', methods=['GET'])
async def get_status(task_id):
    """Check the status of a scan asynchronously."""
    loop = asyncio.get_event_loop()

    # Fetch task result asynchronously
    async_result = await loop.run_in_executor(None, AsyncResult, task_id)
    task_status = async_result.state

    if task_status == 'PENDING':
        return jsonify({"status": "Pending"}), 202
    elif task_status == 'SUCCESS':
        return jsonify({"status": "Completed", "result": async_result.result}), 200
    elif task_status == 'FAILURE':
        return jsonify({"status": "Failed", "error": str(async_result.info)}), 500
    else:
        return jsonify({"status": task_status}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8092)
