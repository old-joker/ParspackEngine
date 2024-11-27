import requests
import json
import time
import os

from logger import LOG

requests.packages.urllib3.disable_warnings()

# Nessus API configuration
NESSUS_URL = 'https://194.147.142.93:11127'
ACCESS_KEY = '32e64bc49c0c0050c21894f25b952883beb25f24f0259c1be98312f4249aaca8'
SECRET_KEY = '25877b7ad71ac64617afeb48b3bb3551bc38f9fcfc35e8824f09adba7d34dfcb'
HEADERS = {
    'X-ApiKeys': f'accessKey={ACCESS_KEY}; secretKey={SECRET_KEY}',
    'Content-Type': 'application/json'
}
VERIFY_SSL = False  # Set this to True for production use

# Helper function to handle requests and errors
def make_request(method, endpoint, data=None):
    try:
        url = f'{NESSUS_URL}{endpoint}'
        if method == 'GET':
            response = requests.get(url, headers=HEADERS, verify=VERIFY_SSL)
        elif method == 'POST':
            response = requests.post(url, headers=HEADERS, data=json.dumps(data), verify=VERIFY_SSL)
        elif method == 'DELETE':
            response = requests.delete(url, headers=HEADERS, verify=VERIFY_SSL)

        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error during {method} request to {endpoint}: {e}")
        return None

# Functions for specific API actions
def check_server_status():
    response = make_request('GET', '/server/status')
    return response.get('status') if response else None

def get_scan_template_uuid(template_name):
    response = make_request('GET', '/editor/scan/templates')
    if response:
        templates = response.get('templates', [])
        for template in templates:
            if template['name'].lower() == template_name.lower():
                return template['uuid']
        print(f"Template '{template_name}' not found.")
    return None

def create_scan(scan_name, target, template_uuid):
    data = {
        'uuid': template_uuid,
        'settings': {
            'name': scan_name,
            'enabled': True,
            'text_targets': target,
            'launch_now': False
        }
    }
    return make_request('POST', '/scans', data)

def launch_scan(scan_id):
    return make_request('POST', f'/scans/{scan_id}/launch')

def stop_scan(scan_id):
    return make_request('POST', f'/scans/{scan_id}/stop')

def delete_scan(scan_id):
    return make_request('DELETE', f'/scans/{scan_id}')

def check_scan_status(scan_id):
    response = make_request('GET', f'/scans/{scan_id}')
    return response.get('info', {}).get('status') if response else None

def export_scan_report(scan_id, report_path):
    try:
        data = {'format': 'nessus'}
        export_response = make_request('POST', f'/scans/{scan_id}/export', data)
        if not export_response:
            print(f"Failed to initiate export for scan {scan_id}")
            return

        file_id = export_response.get('file')

        while True:
            status_response = make_request('GET', f'/scans/{scan_id}/export/{file_id}/status')
            if status_response and status_response.get('status') == 'ready':
                break
            time.sleep(2)

        url = f'{NESSUS_URL}/scans/{scan_id}/export/{file_id}/download'
        download_response = requests.get(url, headers=HEADERS, verify=VERIFY_SSL)
        download_response.raise_for_status()

        with open(report_path, 'wb') as file:
            file.write(download_response.content)

        print(f'Report saved as {report_path}')
    except requests.exceptions.RequestException as e:
        print(f"Error exporting or downloading report: {e}")

# Main function to start a Nessus scan
def start_nessus_scan(scan_name, target, report_folder, template_name='advanced', delete_after=False):
    LOG.info("Nesus started")

    try:
        server_status = check_server_status()
        if server_status:
            print(f"Server Status: {server_status}")
        else:
            print("Failed to check server status.")
            return

        template_uuid = get_scan_template_uuid(template_name)
        if not template_uuid:
            print(f"Failed to retrieve UUID for template '{template_name}'.")
            return

        new_scan = create_scan(scan_name, target, template_uuid)
        if not new_scan or 'scan' not in new_scan:
            print("Failed to create scan.")
            return

        scan_id = new_scan['scan']['id']
        print(f"Scan '{scan_name}' created with ID: {scan_id}")

        launch_response = launch_scan(scan_id)
        if launch_response:
            print(f"Scan {scan_id} launched successfully.")
        else:
            print(f"Failed to launch scan {scan_id}.")
            return

        while True:
            scan_status = check_scan_status(scan_id)
            if scan_status:
                print(f"Current status: {scan_status}")
                if scan_status in ['completed', 'canceled']:
                    break
            else:
                print(f"Failed to retrieve scan status for scan {scan_id}.")
                break
            time.sleep(10)

        report_path = os.path.join(report_folder, "Tenable Scan.nessus")
        export_scan_report(scan_id, report_path)
        LOG.info(f"Nesus saved to :{report_path}")

        if delete_after:
            delete_response = delete_scan(scan_id)
            if delete_response:
                print(f"Scan {scan_id} deleted.")
            else:
                print(f"Failed to delete scan {scan_id}.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
