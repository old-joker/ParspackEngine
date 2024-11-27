from celery import Celery
import subprocess
import os
import uuid

# Celery configuration
app = Celery('nmap_tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

REPORT = "/reports"

@app.task
def run_nmap_task(target, scan_type):
    """Run an Nmap scan and save the results."""
    os.makedirs(REPORT, exist_ok=True)

    # Generate unique report path
    unique_id = uuid.uuid4().hex
    report_path = os.path.join(REPORT, f"nmap_scan_{unique_id}.txt")

    # Construct the Nmap command
    cmd_nmap = [
        "nmap",
        scan_type,
        target,
        "-oN", report_path,  # Save output in normal format
    ]

    try:
        # Run the Nmap command
        result = subprocess.run(cmd_nmap, check=True, capture_output=True, text=True)

        # Return the contents of the report file
        if os.path.exists(report_path):
            with open(report_path, "r") as report_file:
                return report_file.read()
        else:
            return "Report file not found"
    except subprocess.CalledProcessError as e:
        return f"Nmap scan failed: {e.stderr}"
