#import subprocess
#from utils.constants import APP_BASE_DIR
#from logger import LOG
#import os



#def run_nmap_scan(scan_id, ip_host, report_folder):
#    LOG.info("Nmap started")
#    
#    report_path = os.path.join(report_folder, "Nmap Scan.xml")

#    cmd_nmap = f"docker run --rm -it instrumentisto/nmap -A -vvv -T4 -oX"

#    cmd_nmap_sec = [*cmd_nmap.split(), report_path, ip_host]

#    proc = subprocess.Popen(
#        cmd_nmap_sec,
#        shell=False,
#        stdout=open(os.devnull, "w"),
#        stderr=open(os.devnull, "w"),
#    )

#    try:
#        proc.wait(timeout=30 * 60) # 30 minutes, prevent infinite process
#    except subprocess.TimeoutExpired:
#        proc.terminate()
#        LOG.error(f"Process for {ip_host} timed out.")

#    return proc, cmd_nmap, report_path
 
from logger import LOG
from flask import Flask, request, jsonify
import requests

def run_nmap_scan(scan_id, host, report_folder):
    """Run a Nmap scan on a given host."""
    LOG.info(f"Nmap scan started for {host}")
        # Forward the scan request to the Nuclei container
    try:
        nmap_cmd = "http://nmap:8092/run"  # Docker network alias
        response = requests.post(nmap_cmd, json={"target": host,"scan_type": "-sV"})

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500
