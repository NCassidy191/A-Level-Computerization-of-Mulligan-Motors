# manager.py

from tkinter import Tk, Label, Button, PhotoImage, Frame, StringVar
from manageTable import manage_table
from HelpMenu import backup_database, help_page, generate_report

def manager_home():
    m_window = Tk()
    m_window.title("Mulligan Motors - Manager")
    m_window.geometry("600x600")  # Adjust as desired
    m_window.config(bg="#87CEEB")

    # Attempt to load the second Mulligan Motors image
    try:
        logo2_img = PhotoImage(file="mulligan_logo2.png")
        logo2_label = Label(m_window, image=logo2_img, bg="#87CEEB")
        logo2_label.image = logo2_img
        logo2_label.pack(pady=10)  # We still use pack for the logo
    except Exception as e:
        print("Could not load mulligan_logo2.png:", e)

    Label(m_window, text="Mulligan Motors Management (ADMIN)",
          font=("Arial", 16), bg="#87CEEB", fg="black").pack(pady=10)

    # Create a frame that will contain our 2-column grid of buttons
    grid_frame = Frame(m_window, bg="#87CEEB")
    grid_frame.pack(pady=10)

    # The idea: we have 7 "Manage" buttons, plus 4 utility buttons, plus Log Off.
    # We'll place them in a 2-column grid.

    # Row 0
    btn_vehicle = Button(grid_frame, text="Manage Vehicle Stock", font=("Arial", 12),
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
            m_window
        )
    )
    btn_vehicle.grid(row=0, column=0, padx=10, pady=5, sticky="ew")

    btn_customers = Button(grid_frame, text="Manage Customers", font=("Arial", 12),
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
            m_window
        )
    )
    btn_customers.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

    # Row 1
    btn_orders = Button(grid_frame, text="Manage Orders", font=("Arial", 12),
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
            m_window
        )
    )
    btn_orders.grid(row=1, column=0, padx=10, pady=5, sticky="ew")

    btn_staff = Button(grid_frame, text="Manage Staff", font=("Arial", 12),
        command=lambda: manage_table(
            "Staff",
            ["StaffID", "FirstName", "LastName", "DateOfBirth", "PhoneNumber", "Position", "Title"],
            '''
            INSERT INTO Staff (FirstName, LastName, DateOfBirth, PhoneNumber, Position, Title)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            '''
            UPDATE Staff
            SET FirstName = ?, LastName = ?, DateOfBirth = ?, PhoneNumber = ?, Position = ?, Title = ?
            WHERE StaffID = ?
            ''',
            m_window
        )
    )
    btn_staff.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    # Row 2
    btn_testdrives = Button(grid_frame, text="Manage Test Drives", font=("Arial", 12),
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
            m_window
        )
    )
    btn_testdrives.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

    btn_access = Button(grid_frame, text="Manage Access", font=("Arial", 12),
        command=lambda: manage_table(
            "Access",
            ["AccessID", "StaffID", "Username", "Password", "AccessLevel"],
            '''
            INSERT INTO Access (StaffID, Username, Password, AccessLevel)
            VALUES (?, ?, ?, ?)
            ''',
            '''
            UPDATE Access
            SET StaffID = ?, Username = ?, Password = ?, AccessLevel = ?
            WHERE AccessID = ?
            ''',
            m_window
        )
    )
    btn_access.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    # Row 3
    btn_payslips = Button(grid_frame, text="Manage Payslips", font=("Arial", 12),
        command=lambda: manage_table(
            "Payslips",
            ["PayslipID", "StaffID", "HoursWorked", "HourlyRate", "TotalOwed"],
            '''
            INSERT INTO Payslips (StaffID, HoursWorked, HourlyRate, TotalOwed)
            VALUES (?, ?, ?, ?)
            ''',
            '''
            UPDATE Payslips
            SET StaffID = ?, HoursWorked = ?, HourlyRate = ?, TotalOwed = ?
            WHERE PayslipID = ?
            ''',
            m_window
        )
    )
    btn_payslips.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

    # Utility Buttons
    # We'll put them on row 3 or 4, column 1 or 0
    btn_report = Button(grid_frame, text="Generate Report", font=("Arial", 12),
        command=lambda: generate_report(m_window),
        bg="#2ecc71", fg="white"
    )
    btn_report.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    btn_backup = Button(grid_frame, text="Backup Database", font=("Arial", 12),
        command=backup_database, bg="#4682B4", fg="white"
    )
    btn_backup.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

    btn_help = Button(grid_frame, text="Help", font=("Arial", 12),
        command=help_page, bg="#4682B4", fg="white"
    )
    btn_help.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    # Log Off button on row 5, col 1, to place it bottom-right
    btn_logoff = Button(grid_frame, text="Log Off", font=("Arial", 12),
        command=m_window.destroy, bg="#f39c12", fg="white"
    )
    btn_logoff.grid(row=5, column=1, padx=10, pady=10, sticky="e")

    # Make columns expand a bit if we resize the window
    grid_frame.columnconfigure(0, weight=1)
    grid_frame.columnconfigure(1, weight=1)

    m_window.mainloop()
