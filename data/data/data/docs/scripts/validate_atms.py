import json
import csv
import sys
import os

def validate_data():
    errors = []
    warnings = []
    
    # Resolve file paths dynamically
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, 'data', 'botswana_atms.json')
    csv_path = os.path.join(base_dir, 'data', 'botswana_atms.csv')
    
    # 1. JSON Syntax Check
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            atms = json.load(f)
    except Exception as e:
        print(f"❌ CRITICAL ERROR: Failed to parse JSON file at {json_path}:\n   {e}")
        sys.exit(1)

    required_fields = [
        "atm_id", "bank", "atm_name", "town", "district", 
        "address", "landmark", "latitude", "longitude", 
        "services", "operational_status", "verification_status", 
        "source_url", "last_verified", "access_notes", "notes"
    ]
    
    allowed_verification_statuses = [
        "published_unverified", 
        "verified", 
        "address_to_confirm"
    ]
    
    ids_seen = set()
    locations_seen = {}  # Tracks bank + normalized address for duplicate checks

    print(f"🔍 Validating {len(atms)} ATM records in JSON...\n")

    for idx, atm in enumerate(atms):
        atm_id = atm.get("atm_id", f"MISSING_ID_AT_INDEX_{idx}")
        
        # 2. Required Fields Check
        for field in required_fields:
            if field not in atm:
                errors.append(f"Row {idx} [{atm_id}]: Missing required field '{field}'.")
                
        # 3. Duplicate ATM IDs
        if atm_id in ids_seen:
            errors.append(f"Row {idx} [{atm_id}]: Duplicate atm_id found.")
        ids_seen.add(atm_id)
        
        # 4. Latitude and Longitude Constraints
        lat = atm.get("latitude")
        lon = atm.get("longitude")
        
        if lat is not None:
            if not isinstance(lat, (int, float)) or not (-90 <= lat <= 90):
                errors.append(f"Row {idx} [{atm_id}]: Invalid latitude value '{lat}'. Must be float between -90 and 90 or null.")
                
        if lon is not None:
            if not isinstance(lon, (int, float)) or not (-180 <= lon <= 180):
                errors.append(f"Row {idx} [{atm_id}]: Invalid longitude value '{lon}'. Must be float between -180 and 180 or null.")
                
        # 5. Verification Status Validation
        v_status = atm.get("verification_status")
        if v_status not in allowed_verification_statuses:
            errors.append(f"Row {idx} [{atm_id}]: Invalid verification_status '{v_status}'. Allowed: {allowed_verification_statuses}")
            
        # 6. Source URL Presence
        source_url = atm.get("source_url")
        if not source_url or not isinstance(source_url, str) or not source_url.startswith("http"):
            errors.append(f"Row {idx} [{atm_id}]: Missing or invalid source_url.")

        # 7. Identify Suspected Physical Duplicates (Warning only)
        bank = str(atm.get("bank", "")).strip().lower()
        address = str(atm.get("address", "")).strip().lower()
        location_key = f"{bank} @ {address}"
        
        if location_key in locations_seen:
            warnings.append(
                f"⚠️ SUSPECTED DUPLICATE: Record [{atm_id}] shares bank and address with [{locations_seen[location_key]}]. "
                f"Verify if these represent distinct units or an unintended duplicate."
            )
        else:
            locations_seen[location_key] = atm_id

    # 8. Check JSON vs CSV Parity
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            csv_ids = {row['atm_id'] for row in reader if 'atm_id' in row}
            
            missing_in_csv = ids_seen - csv_ids
            missing_in_json = csv_ids - ids_seen
            
            if missing_in_csv:
                errors.append(f"Parity Error: IDs present in JSON but missing in CSV: {missing_in_csv}")
            if missing_in_json:
                errors.append(f"Parity Error: IDs present in CSV but missing in JSON: {missing_in_json}")
                
    except Exception as e:
        errors.append(f"CSV Parity Check Failed: Could not read {csv_path}:\n   {e}")

    # Report Warnings
    if warnings:
        print("--- WARNINGS (Suspected Duplicates / Multiple Machines) ---")
        for warning in warnings:
            print(warning)
        print("\nNote: Suspected duplicates are reported above for manual review and are NOT auto-deleted.\n")

    # Final Execution Status Output
    if errors:
        print(f"❌ VALIDATION FAILED! Found {len(errors)} error(s):\n")
        for err in errors:
            print(f"- {err}")
        sys.exit(1)
    else:
        print(f"✅ SUCCESS: All {len(atms)} records passed validation cleanly with 0 errors!")
        sys.exit(0)

if __name__ == "__main__":
    validate_data()
