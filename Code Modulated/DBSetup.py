# DBSetup.py

import sqlite3

def initialize_database():
    conn = sqlite3.connect('mulligan_motors.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")

    # VehicleStock
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS VehicleStock (
        VehicleID INTEGER PRIMARY KEY AUTOINCREMENT,
        VehicleMake TEXT,
        VehicleName TEXT,
        VehicleType TEXT,
        VehiclePrice REAL,
        ItemQuantity INTEGER,
        VehicleCondition TEXT
    )''')

    # Customer
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Customer (
        CustomerID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT,
        LastName TEXT,
        Email TEXT,
        PhoneNumber TEXT,
        Address TEXT,
        PreferredContactMethod TEXT,
        DateJoined TEXT
    )''')

    # Orders
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Orders (
        OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
        OrderValue REAL,
        DatePlaced TEXT,
        DateArriving TEXT,
        CustomerID INTEGER,
        VehicleID INTEGER,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY (VehicleID) REFERENCES VehicleStock(VehicleID) ON DELETE SET NULL
    )''')

    # Staff
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Staff (
        StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
        FirstName TEXT,
        LastName TEXT,
        DateOfBirth TEXT,
        PhoneNumber TEXT,
        Position TEXT,
        Title TEXT
    )''')

    # TestDrives
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS TestDrives (
        TestDriveID INTEGER PRIMARY KEY AUTOINCREMENT,
        TestDriveDate TEXT,
        TestDriveTime TEXT,
        Duration TEXT,
        Status TEXT,
        Feedback TEXT,
        CustomerID INTEGER,
        VehicleID INTEGER,
        FOREIGN KEY (CustomerID) REFERENCES Customer(CustomerID) ON DELETE CASCADE,
        FOREIGN KEY (VehicleID) REFERENCES VehicleStock(VehicleID) ON DELETE SET NULL
    )''')

    # Access
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Access (
        AccessID INTEGER PRIMARY KEY AUTOINCREMENT,
        StaffID INTEGER,
        Username TEXT,
        Password TEXT,
        AccessLevel TEXT,
        FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
    )''')

    # Payslips
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Payslips (
        PayslipID INTEGER PRIMARY KEY AUTOINCREMENT,
        StaffID INTEGER,
        HoursWorked REAL,
        HourlyRate REAL,
        TotalOwed REAL,
        FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
    )''')

    conn.commit()
    conn.close()
