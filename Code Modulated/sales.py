# sales.py

from tkinter import Tk, Label, Button, PhotoImage, Frame
from manageTable import manage_table
from HelpMenu import backup_database, help_page, generate_report

def sales_home():
    s_window = Tk()
    s_window.title("Mulligan Motors - Sales")
    s_window.geometry("550x600")
    s_window.config(bg="#87CEEB")

    # Try loading the first Mulligan Motors image
    try:
        logo_img = PhotoImage(file="mulligan_logo1.png")
        logo_label = Label(s_window, image=logo_img, bg="#87CEEB")
        logo_label.image = logo_img
        logo_label.pack(pady=10)
    except Exception as e:
        print("Could not load mulligan_logo1.png:", e)

    Label(s_window, text="Mulligan Motors (SALES ACCESS)", font=("Arial", 16),
          bg="#87CEEB").pack(pady=10)

    # A frame for the "Manage" buttons
    manage_frame = Frame(s_window, bg="#87CEEB")
    manage_frame.pack(pady=10)

    Button(manage_frame, text="Manage Vehicle Stock", font=("Arial", 12),
           command=lambda: manage_table(
               "VehicleStock",
               ["VehicleID", "VehicleMake", "VehicleName", "VehicleType",
                "VehiclePrice", "ItemQuantity", "VehicleCondition"],
               '''
               INSERT INTO VehicleStock (VehicleMake, VehicleName, VehicleType, VehiclePrice, ItemQuantity, VehicleCondition)
               VALUES (?, ?, ?, ?, ?, ?)
               ''',
               '''
               UPDATE VehicleStock
               SET VehicleMake = ?, VehicleName = ?, VehicleType = ?, VehiclePrice = ?, ItemQuantity = ?, VehicleCondition = ?
               WHERE VehicleID = ?
               ''',
               s_window
           )
    ).pack(pady=5)

    Button(manage_frame, text="Manage Customers", font=("Arial", 12),
           command=lambda: manage_table(
               "Customer",
               ["CustomerID", "FirstName", "LastName", "Email", "PhoneNumber",
                "Address", "PreferredContactMethod", "DateJoined"],
               '''
               INSERT INTO Customer (FirstName, LastName, Email, PhoneNumber, Address, PreferredContactMethod, DateJoined)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ''',
               '''
               UPDATE Customer
               SET FirstName = ?, LastName = ?, Email = ?, PhoneNumber = ?, Address = ?, PreferredContactMethod = ?, DateJoined = ?
               WHERE CustomerID = ?
               ''',
               s_window
           )
    ).pack(pady=5)

    Button(manage_frame, text="Manage Orders", font=("Arial", 12),
           command=lambda: manage_table(
               "Orders",
               ["OrderID", "OrderValue", "DatePlaced", "DateArriving", "CustomerID", "VehicleID"],
               '''
               INSERT INTO Orders (OrderValue, DatePlaced, DateArriving, CustomerID, VehicleID)
               VALUES (?, ?, ?, ?, ?)
               ''',
               '''
               UPDATE Orders
               SET OrderValue = ?, DatePlaced = ?, DateArriving = ?, CustomerID = ?, VehicleID = ?
               WHERE OrderID = ?
               ''',
               s_window
           )
    ).pack(pady=5)

    Button(manage_frame, text="Manage Test Drives", font=("Arial", 12),
           command=lambda: manage_table(
               "TestDrives",
               ["TestDriveID", "TestDriveDate", "TestDriveTime", "Duration", "Status", "Feedback", "CustomerID", "VehicleID"],
               '''
               INSERT INTO TestDrives (TestDriveDate, TestDriveTime, Duration, Status, Feedback, CustomerID, VehicleID)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ''',
               '''
               UPDATE TestDrives
               SET TestDriveDate = ?, TestDriveTime = ?, Duration = ?, Status = ?, Feedback = ?, CustomerID = ?, VehicleID = ?
               WHERE TestDriveID = ?
               ''',
               s_window
           )
    ).pack(pady=5)

    # A frame for utility buttons (Generate Report, Backup, Help)
    utility_frame = Frame(s_window, bg="#87CEEB")
    utility_frame.pack(pady=10)

    Button(utility_frame, text="Generate Report", font=("Arial", 12),
           command=lambda: generate_report(s_window),
           bg="#2ecc71", fg="white").pack(pady=5)

    Button(utility_frame, text="Backup Database", font=("Arial", 12),
           command=backup_database, bg="#4682B4", fg="white").pack(pady=5)

    Button(utility_frame, text="Help", font=("Arial", 12),
           command=help_page, bg="#4682B4", fg="white").pack(pady=5)

    # Finally, Log Off at the bottom
    Button(s_window, text="Log Off", font=("Arial", 12),
           command=s_window.destroy, bg="#f39c12", fg="white").pack(side="bottom", pady=20)

    s_window.mainloop()
