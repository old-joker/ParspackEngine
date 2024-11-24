from celery import Celery
import subprocess
import os
import uuid

# Celery configuration
app = Celery('nuclei_tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

REPORT = "./reports"

@app.task
def run_nuclei_task(target):
    """Run Nuclei scan and save the report."""
    os.makedirs(REPORT, exist_ok=True)

    # Generate unique report path
    unique_id = uuid.uuid4().hex
    report_path = os.path.join(REPORT, f"nuclei_scan_{unique_id}.json")

    # Construct the Nuclei command
    cmd_nuclei_sec = [
        "nuclei",
        "-u", target,
        "-duc",  # Download templates if necessary
        "-json-export", report_path,
    ]

    try:
        # Run the Nuclei command
        result = subprocess.run(cmd_nuclei_sec, check=True, capture_output=True, text=True)

        # Return the contents of the report file
        if os.path.exists(report_path):
            with open(report_path, "r") as report_file:
                return report_file.read()
        else:
            return "Report file not found"
    except subprocess.CalledProcessError as e:
        return f"Nuclei scan failed: {e.stderr}"
