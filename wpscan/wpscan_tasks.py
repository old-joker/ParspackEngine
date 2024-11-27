from celery import Celery
import subprocess
import os
import uuid

# Celery configuration
app = Celery('wpscan_tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

REPORT = "/reports"

@app.task
def run_wpscan_task(target, scan_type):
    """Run an WPScan scan and save the results."""
    os.makedirs(REPORT, exist_ok=True)

    # Generate unique report path
    unique_id = uuid.uuid4().hex
    report_path = os.path.join(REPORT, f"wpscan_{unique_id}.txt")

    # Construct the WPScan command
    cmd_wpscan = [
        "wpscan",
        "--url", target,
        scan_type,
        "-o", report_path,  # Save output in normal format
    ]

    try:
        # Run the WPScan command
        result = subprocess.run(cmd_wpscan, check=True, capture_output=True, text=True)

        # Return the contents of the report file
        if os.path.exists(report_path):
            with open(report_path, "r") as report_file:
                return report_file.read()
        else:
            return "Report file not found"
    except subprocess.CalledProcessError as e:
        return f"WPScan scan failed: {e.stderr}"
