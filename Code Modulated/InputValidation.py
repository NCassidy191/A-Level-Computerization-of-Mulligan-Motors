# InputValidation.py

import re

def validate_input(table_name, data_dict):
    """
    Basic checks for presence, numeric data, email, etc.
    Returns (True, "") if valid, else (False, errorMsg).
    """

    def is_float(x):
        try:
            float(x)
            return True
        except ValueError:
            return False

    def is_int(x):
        try:
            int(x)
            return True
        except ValueError:
            return False

    email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+"

    # Presence checks
    if table_name == "VehicleStock":
        if not data_dict.get("VehicleMake", "").strip():
            return False, "VehicleMake cannot be empty."
    elif table_name == "Customer":
        if not data_dict.get("FirstName", "").strip():
            return False, "FirstName cannot be empty."
    elif table_name == "Orders":
        if not data_dict.get("DatePlaced", "").strip():
            return False, "DatePlaced cannot be empty."
    elif table_name == "Staff":
        if not data_dict.get("FirstName", "").strip():
            return False, "FirstName cannot be empty."
    elif table_name == "TestDrives":
        if not data_dict.get("TestDriveDate", "").strip():
            return False, "TestDriveDate cannot be empty."
    elif table_name == "Access":
        if not data_dict.get("Username", "").strip():
            return False, "Username cannot be empty."
    elif table_name == "Payslips":
        if not data_dict.get("StaffID", "").strip():
            return False, "StaffID cannot be empty."

    # Numeric checks
    if table_name == "VehicleStock":
        if data_dict.get("VehiclePrice") and not is_float(data_dict["VehiclePrice"]):
            return False, "VehiclePrice must be numeric."
        if data_dict.get("ItemQuantity") and not is_int(data_dict["ItemQuantity"]):
            return False, "ItemQuantity must be integer."

    # Email format check for Customer
    if table_name == "Customer":
        email = data_dict.get("Email", "").strip()
        if email:  # Check only if email is provided and not empty
            if not re.match(email_pattern, email):
                return False, "Invalid email format."

    return True, ""