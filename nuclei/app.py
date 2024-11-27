from flask import Flask, request, jsonify
from nuclei_tasks import run_nuclei_task
from celery.result import AsyncResult
import asyncio

app = Flask(__name__)

@app.route('/run', methods=['POST'])
async def run_nuclei():
    """Handle scan requests asynchronously by offloading to Celery."""
    target = request.json.get('target')
    if not target:
        return jsonify({"error": "Target URL is required"}), 400

    # Offload the scan to Celery task queue
    task = run_nuclei_task.delay(target)
    return jsonify({"message": "Scan started", "task_id": task.id}), 202

@app.route('/status/<task_id>', methods=['GET'])
async def get_status(task_id):
    """Check the status of a scan asynchronously."""
    loop = asyncio.get_event_loop()
    
    # Fetch task status asynchronously
    task_status = await loop.run_in_executor(None, AsyncResult, task_id)
    if task_status.state == 'PENDING':
        return jsonify({"status": "Pending"}), 202
    elif task_status.state == 'SUCCESS':
        return jsonify({"status": "Completed", "result": task_status.result}), 200
    elif task_status.state == 'FAILURE':
        return jsonify({"status": "Failed", "error": str(task_status.info)}), 500
    else:
        return jsonify({"status": task_status.state}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
