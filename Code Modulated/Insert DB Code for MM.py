import sqlite3

def populate_database():
    conn = sqlite3.connect('mulligan_motors.db')
    cursor = conn.cursor()

    # -----------------------------
    # 1. Insert sample VehicleStock
    # -----------------------------
    vehicle_data = [
        ("Toyota", "Corolla", "Sedan", 20000, 5, "Slightly Used"),
        ("Honda", "Civic", "Sedan", 18000, 3, "Pristine"),
        ("Ford", "F-150", "Truck", 35000, 2, "Heavily Used"),
    ]
    cursor.executemany('''
        INSERT INTO VehicleStock (VehicleMake, VehicleName, VehicleType, VehiclePrice, ItemQuantity, VehicleCondition)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', vehicle_data)

    # -----------------------------
    # 2. Insert sample Customer
    # -----------------------------
    customer_data = [
        ("John", "Doe", "[email protected]", "1234567890", "123 Elm Street", "Phone", "2025-01-10"),
        ("Jane", "Smith", "[email protected]", "9876543210", "456 Oak Avenue", "Email", "2025-01-15"),
    ]
    cursor.executemany('''
        INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber, Address, PreferredContactMethod, DateJoined)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', customer_data)

    # -----------------------------------
    # 3. Insert sample Orders (FKs needed)
    # -----------------------------------
    # Assuming VehicleStock auto-increment IDs start at 1,2,3...
    # Assuming Customer auto-increment IDs start at 1,2...
    order_data = [
        (20000, "2025-01-12", "2025-01-20", 1, 1),  # CustomerID=1, VehicleID=1
        (18000, "2025-01-14", "2025-01-25", 2, 2),  # CustomerID=2, VehicleID=2
    ]
    cursor.executemany('''
        INSERT INTO Orders (OrderValue, DatePlaced, DateArriving, CustomerID, VehicleID)
        VALUES (?, ?, ?, ?, ?)
    ''', order_data)

    # -----------------------------
    # 4. Insert sample Staff
    # -----------------------------
    staff_data = [
        ("Alice", "Johnson", "1985-05-05", "5551112222", "Manager", "Ms."),
        ("Bob",   "Williams", "1990-03-02", "5553334444", "Sales Rep", "Mr."),
    ]
    cursor.executemany('''
        INSERT INTO Staff (FirstName, LastName, DateOfBirth, PhoneNumber, Position, Title)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', staff_data)

    # -----------------------------
    # 5. Insert sample Access (FK)
    # -----------------------------
    # Corresponding to the Staff above (StaffID=1 => admin, StaffID=2 => sales)
    access_data = [
        (1, "alice_admin", "adminPass", "admin"),
        (2, "bob_sales", "salesPass", "sales"),
    ]
    cursor.executemany('''
        INSERT INTO Access (StaffID, Username, Password, AccessLevel)
        VALUES (?, ?, ?, ?)
    ''', access_data)

    # -----------------------------------------
    # 6. Insert sample TestDrives (FK CustomerID/VehicleID)
    # -----------------------------------------
    testdrive_data = [
        ("2025-02-01", "10:00", "30 minutes", "Completed", "Loved it!", 1, 2),
        ("2025-02-05", "14:00", "45 minutes", "Pending", "", 2, 3),
    ]
    cursor.executemany('''
        INSERT INTO TestDrives (TestDriveDate, TestDriveTime, Duration, Status, Feedback, CustomerID, VehicleID)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', testdrive_data)

    # -----------------------------------------
    # 7. Insert sample Payslips (FK StaffID)
    # -----------------------------------------
    payslips_data = [
        (1, 40, 20.0, 40 * 20.0),  # StaffID=1 => total owed = hours * rate
        (2, 35, 15.0, 35 * 15.0),  # StaffID=2
    ]
    cursor.executemany('''
        INSERT INTO Payslips (StaffID, HoursWorked, HourlyRate, TotalOwed)
        VALUES (?, ?, ?, ?)
    ''', payslips_data)

    # -------------
    # Finalize
    # -------------
    conn.commit()
    conn.close()
    print("Sample data inserted successfully!")

if __name__ == "__main__":
    populate_database()
