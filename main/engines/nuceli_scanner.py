from logger import LOG
from flask import Flask, request, jsonify
import requests

def run_nuclei_scan(scan_id, host, report_folder):
    """Run a Nuclei scan on a given host."""
    LOG.info(f"Nuclei scan started for {host}")
        # Forward the scan request to the Nuclei container
    try:
        nuclei_cmd = "http://nuclei:8091/run"  # Docker network alias
        response = requests.post(nuclei_cmd, json={"target": host})
        
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
