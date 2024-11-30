from logger import LOG
from flask import Flask, request, jsonify
import requests

def run_nmap_scan(scan_id, host, report_folder):
    """Run a Nmap scan on a given host."""
    LOG.info(f"Nmap scan started for {host}")
        # Forward the scan request to the Nuclei container
    try:
        nmap_cmd = "http://nmap:8091/scan"  # Docker network alias
        response = requests.post(nmap_cmd, json={"target": host,"options": "-sV"})

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
