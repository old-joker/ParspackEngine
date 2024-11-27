from flask import current_app

def validate_scan_data(data):
    """Validate the incoming scan data."""
    if "scan_id" not in data:
        return False, "Missing 'scan_id' in request data."
    
    if "assets" not in data or not isinstance(data["assets"], list):
        return False, "Invalid or missing 'assets'. Must be a list."
    
    for asset in data["assets"]:
        if "value" not in asset or not asset["value"]:
            return False, "Each asset must have a 'value'."
        
        if "datatype" not in asset or asset["datatype"] not in current_app.engine.scanner["allowed_asset_types"]:
            return False, f"Invalid or missing 'datatype' for asset value: {asset.get('value', 'unknown')}."
    
    return True, ""
