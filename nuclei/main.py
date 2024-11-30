from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import asyncio
import shlex
import os
import logging
import uuid

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("nuclei_scan.log"),  # Log to a file
        logging.StreamHandler()               # Log to the console
    ]
)

app = FastAPI()

# Semaphore to limit concurrent scans
MAX_CONCURRENT_SCANS = 5
semaphore = asyncio.Semaphore(MAX_CONCURRENT_SCANS)

# Timeout for nuclei scans (in seconds)
SCAN_TIMEOUT = 300  # 5 minutes

# Directory to save scan reports
REPORT_DIR = "reports"
os.makedirs(REPORT_DIR, exist_ok=True)  # Ensure the reports directory exists

# Pydantic model for the request body
class ScanRequest(BaseModel):
    target: str = Field(..., description="The target for the nmap scan (e.g., IP or domain)")
    options: str = Field(default="", description="Optional nmap command-line options")


async def run_nuclei(target: str, options: str = "") -> None:
    """
    Runs an nuclei scan asynchronously for the given target.
    Saves the output as an json report in the reports folder.
    """
    # Validate the target to avoid command injection
    if not target or len(target) > 255 or ";" in target or "&" in target:
        raise ValueError("Invalid target provided")

    # Generate unique report path
    unique_id = uuid.uuid4().hex
    report_filename = os.path.join(REPORT_DIR, f"nuclei_scan_{unique_id}.json")

    # Construct the safe command with -json-export for json output
    command = f"nuclei -json-export {shlex.quote(report_filename)} {options} -duc -t /nuclei-templates -u {shlex.quote(target)}"
    logging.info(f"Starting scan for target: {target} | Command: {command}")

    # Run the command asynchronously
    async with semaphore:  # Limit the number of concurrent scans
        try:
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )

            # Wait for the process to complete with a timeout
            try:
                stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=SCAN_TIMEOUT)

                if process.returncode != 0:
                    logging.error(f"Scan for target {target} failed: {stderr.decode().strip()}")
                else:
                    logging.info(f"Scan for target {target} completed. Report saved at {report_filename}")

            except asyncio.TimeoutError:
                process.kill()
                logging.error(f"Scan for target {target} timed out after {SCAN_TIMEOUT} seconds.")
        except Exception as e:
            logging.error(f"Unexpected error during scan for target {target}: {str(e)}")


@app.post("/scan")
async def start_scan(request: ScanRequest):
    """
    Start an nuclei scan with a POST request containing a JSON body.
    """
    try:
        target = request.target
        options = request.options

        # Validate the target
        if not target:
            raise HTTPException(status_code=400, detail="Target is required")

        # Launch the scan asynchronously
        asyncio.create_task(run_nuclei(target, options))  # Fire-and-forget

        # Return a response indicating the scan has started
        return {
            "target": target,
            "scan": "started"
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
