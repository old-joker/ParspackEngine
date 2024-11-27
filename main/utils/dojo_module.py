import requests
import json
import os
from datetime import date, datetime, timedelta, timezone

auth_token = os.getenv('DOJO_AUTH_TOKEN')
dojo_base_url = os.getenv('DOJO_BASE_URL')

def dojo_api_request(url, method="GET", data=None, params=None):
    headers = {
        "Authorization": "Token " + auth_token,
        "Accept": "application/json"
    }
    if method == "POST":
        headers["Content-Type"] = "application/json"

    try:
        if method == "GET":
            resp = requests.get(url, params=params,
                                headers=headers, verify=False)
        elif method == "POST":
            resp = requests.post(url, headers=headers,
                                 data=json.dumps(data), verify=False)

        resp.raise_for_status()  # Raise exception for HTTP errors
        return resp.json() if resp.status_code in [200, 201] else None
    except Exception as e:
        print(f"Error during {method} request to {url}: {str(e)}")
        return None

# Function to get or create an engagement
def get_or_create_engagement(pid):
    url = f"{dojo_base_url}/api/v2/engagements/"
    params = {'product': pid}

    # Step 1: Try to get the engagement ID
    eng_data = dojo_api_request(url, method="GET", params=params)

    if eng_data and eng_data.get('count', 0) > 0:
        eid = eng_data["results"][0]['id']
        print(f"Engagement Id: {eid}")
    else:
        # Step 2: No engagement found, create one
        eid = create_engagement(pid)

    return eid

# Function to create an engagement if none exists
def create_engagement(pid):
    url = f"{dojo_base_url}/api/v2/engagements/"
    start_time = date.today()
    end_time = start_time + timedelta(days=365)

    data = {
        "name": "Patrowl",
        "target_start": str(start_time),
        "target_end": str(end_time),
        "engagement_type": "Interactive",
        "status": "In Progress",
        "product": pid
    }

    eng_data = dojo_api_request(url, method="POST", data=data)
    if eng_data:
        eid = eng_data['id']
        print(f"Engagement {eid} Created successfully.")
        return eid
    else:
        print("Failed to create engagement.")
        return None

# Function to get or create a product
def get_or_create_product(name):
    url = f"{dojo_base_url}/api/v2/products/"
    params = {'name': name}

    # Step 1: Try to get the product ID
    product_data = dojo_api_request(url, method="GET", params=params)

    if product_data and product_data.get('count', 0) > 0:
        pid = product_data["results"][0]['id']
        print(f"Product Id: {pid}")
        return get_or_create_engagement(pid)
    else:
        # Step 2: No product found, create one
        return create_product(name)

# Function to create a product if none exists
def create_product(name):
    url = f"{dojo_base_url}/api/v2/products/"

    data = {
        'name': str(name),
        'description': f'Info : {name}',
        'prod_type': 1
    }

    product_data = dojo_api_request(url, method="POST", data=data)

    if product_data:
        pid = product_data['id']
        print(f"Product {pid} Created successfully.")
        return get_or_create_engagement(pid)
    else:
        print("Failed to create product.")
        return None

# Function to upload a scan file to DefectDojo
def upload_scan(filename, title, asset_value):
    try:
        # Step 1: Get or create product (engagement will be retrieved or created)
        engagement = get_or_create_product(asset_value)

        if not engagement:
            print(f"Failed to retrieve or create engagement for product: {title}")
            return

        # Step 2: Prepare for file upload
        url = f"{dojo_base_url}/api/v2/import-scan/"
        dojo_headers = {"Authorization": "Token " + auth_token}
        files = {"file": open(filename, "rb")}

        data = {
            "scan_date": str(datetime.now(timezone.utc).date().isoformat()),
            "minimum_severity": "Info",
            "active": True,
            "verified": False,
            "scan_type": title,
            "engagement": engagement,
            "close_old_findings": False,
            "push_to_jira": False,
            "test_title": title
        }

        # Step 3: Make the POST request to upload the scan
        try:
            resp = requests.post(url, files=files, data=data,
                                 headers=dojo_headers, verify=False)
            if resp.status_code == 201:
                print("Report uploaded successfully.")
            else:
                print(f"File upload failed. Error: {resp.json()}")
        finally:
            # Ensure the file is closed after upload
            files["file"].close()

    except Exception as e:
        print(f"An error occurred while uploading the report: {str(e)}")

# Function to read files from a specified directory and upload scans
def upload_scans_from_directory(directory_path):
    # List all files in the given directory
    try:
        files = os.listdir(directory_path)
        
        for filename in files:
            file_path = os.path.join(directory_path, filename)
            
            if os.path.isfile(file_path):
                # Get the title by removing the file extension
                title = os.path.splitext(filename)[0]
                # Get the first parent directory name (the immediate parent)
                parent_name = os.path.basename(os.path.dirname(file_path))
                print(f"Uploading scan for: {title}, Parent Directory: {parent_name}")
                
                # Pass both title and parent_name to upload_scan
                upload_scan(file_path, title, parent_name)
            else:
                print(f"Skipping non-file: {filename}")
    except Exception as e:
        print(f"Error reading files from directory: {str(e)}")
