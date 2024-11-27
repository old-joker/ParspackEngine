import datetime
import json
from os.path import exists
import os
from utils.constants import APP_BASE_DIR
from sys import argv
from flask import current_app
from flask import jsonify
import zipfile


def get_log_datetime():
    """Returns the current date and time as a formatted string for log file names."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def zip_folder(folder_path):
    # Get the last folder name from the path
    last_folder_name = os.path.basename(os.path.normpath(folder_path))
    # Create the zip file path
    zip_file_path = os.path.join(os.path.dirname(folder_path), f"{last_folder_name}.zip")

    # Create a zip file
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Walk through the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # Create the complete file path
                file_path = os.path.join(root, file)
                # Add file to the zip file
                zip_file.write(file_path, os.path.relpath(file_path, folder_path))

    return zip_file_path


def folder_creator(*parts):
    """Create a folder from multiple path parts if it doesn't exist."""
    # Merge the parts into a single path
    path = os.path.join(*parts)
    
    try:
        # Create the folder if it doesn't exist
        if not os.path.exists(path):
            os.makedirs(path)
    except Exception as e:
        print(f"An error occurred while creating '{path}': {e}")
    
    return path


def error_response(res, status, reason):
    """Update the response with an error and return it."""
    res.update({"status": status, "reason": reason})
    return jsonify(res)

def _loadconfig():
    conf_file = APP_BASE_DIR + "/ParsPack.json"
    if len(argv) > 1 and exists(APP_BASE_DIR + "/" + argv[1]):
        conf_file = APP_BASE_DIR + "/" + argv[1]
    if exists(conf_file):
        with open(conf_file) as json_data:
            current_app.engine.scanner = json.load(json_data)
        current_app.engine.scanner["status"] = "READY"
    else:
        # LOG.error("Error: config file '{}' not found".format(conf_file))
        return {"status": "error", "reason": "config file not found"}

    if "options" not in current_app.engine.scanner:
        # LOG.error("Error: You have to specify options")
        return {"status": "error", "reason": "You have to specify options"}

    if "Templates" not in current_app.engine.scanner["options"]:
        # LOG.error("Error: You have to specify Templates in options")
        return {"status": "error", "reason": "You have to specify Templates in options"}

    if "value" not in current_app.engine.scanner["options"]["Templates"]:
        # LOG.error("Error: You have to specify Templates in options")
        return {"status": "error", "reason": "You have to specify Templates in options"}

    version_filename = APP_BASE_DIR + "/VERSION"
    if os.path.exists(version_filename):
        with open(version_filename, "r") as version_file:
            current_app.engine.version = version_file.read().rstrip("\n")
    # LOG.info("[OK] Templates")
