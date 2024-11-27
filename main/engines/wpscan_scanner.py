from logger import LOG
from flask import Flask, request, jsonify
import requests

def run_wpscan(scan_id, domain, report_folder):
    """Run a WPScan on a given domain."""
    LOG.info(f"WPScan started for {domain}")
        # Forward the scan request to the WPScan container
    try:
        wpscan_cmd = "http://wpscan:8093/run"  # Docker network alias
        response = requests.post(wpscan_cmd, json={"target": domain})
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
