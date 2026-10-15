# LoginPage.py

import sqlite3
from tkinter import Tk, Label, Entry, Button, Toplevel, messagebox, StringVar, PhotoImage
from manager import manager_home
from sales import sales_home

def create_account_window(parent_window):
    def register_account():
        staff_id_str = staff_id_var.get()
        username = username_var.get().strip()
        pw = password_var.get()
        pw_confirm = confirm_var.get()
        access_level = access_var.get()

        if not staff_id_str or not username or not pw or not pw_confirm:
            messagebox.showerror("Validation Error", "All fields are required.")
            return

        try:
            staff_id_int = int(staff_id_str)
        except ValueError:
            messagebox.showerror("Validation Error", "StaffID must be a number.")
            return

        if pw != pw_confirm:
            messagebox.showerror("Validation Error", "Passwords do not match.")
            return

        try:
            conn = sqlite3.connect('mulligan_motors.db')
            cursor = conn.cursor()
            cursor.execute("SELECT AccessID FROM Access WHERE Username = ?", (username,))
            existing = cursor.fetchone()
            if existing:
                messagebox.showerror("Error", f"Username '{username}' is already taken.")
                conn.close()
                return

            cursor.execute('''
                INSERT INTO Access (StaffID, Username, Password, AccessLevel)
                VALUES (?, ?, ?, ?)
            ''', (staff_id_int, username, pw, access_level))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", f"Account '{username}' created successfully!")
            create_win.destroy()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    create_win = Toplevel(parent_window)
    create_win.title("Create Account")
    create_win.geometry("400x400")
    create_win.config(bg="#87CEEB")

    Label(create_win, text="Enter details to create an account", font=("Arial", 14),
          bg="#87CEEB").pack(pady=10)

    staff_id_var = StringVar()
    username_var = StringVar()
    password_var = StringVar()
    confirm_var = StringVar()
    access_var = StringVar(value="sales")

    Label(create_win, text="Staff ID:", bg="#87CEEB").pack(pady=5)
    Entry(create_win, textvariable=staff_id_var).pack(pady=5)

    Label(create_win, text="Username:", bg="#87CEEB").pack(pady=5)
    Entry(create_win, textvariable=username_var).pack(pady=5)

    Label(create_win, text="Password:", bg="#87CEEB").pack(pady=5)
    Entry(create_win, textvariable=password_var, show="*").pack(pady=5)

    Label(create_win, text="Confirm Password:", bg="#87CEEB").pack(pady=5)
    Entry(create_win, textvariable=confirm_var, show="*").pack(pady=5)

    Label(create_win, text="Access Level:", bg="#87CEEB").pack(pady=5)
    levels = ["sales", "admin"]
    from tkinter import OptionMenu
    OptionMenu(create_win, access_var, *levels).pack(pady=5)

    Button(create_win, text="Register", command=register_account,
           bg="#4682B4", fg="white").pack(pady=20)

def login_screen():
    login_window = Tk()
    login_window.title("Mulligan Motors - Login")
    login_window.geometry("450x600")
    login_window.config(bg="#87CEEB")

    # Attempt to load mulligan_logo1.png with PhotoImage
    try:
        logo1_img = PhotoImage(file="mulligan_logo1.png")
        logo_label = Label(login_window, image=logo1_img, bg="#87CEEB")
        logo_label.image = logo1_img  # keep a reference
        logo_label.pack(pady=10)
    except Exception as e:
        print("Could not load mulligan_logo1.png:", e)

    Label(login_window, text="Login to Mulligan Motors", font=("Arial", 16),
          bg="#87CEEB", fg="black").pack(pady=5)

    username_var = StringVar()
    password_var = StringVar()

    Label(login_window, text="Username", font=("Arial", 12), bg="#87CEEB").pack(pady=5)
    Entry(login_window, textvariable=username_var, font=("Arial", 12)).pack(pady=5)

    Label(login_window, text="Password", font=("Arial", 12), bg="#87CEEB").pack(pady=5)
    Entry(login_window, textvariable=password_var, show="*", font=("Arial", 12)).pack(pady=5)

    def validate_login():
        user = username_var.get()
        pw = password_var.get()
        conn = sqlite3.connect('mulligan_motors.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT AccessLevel
            FROM Access
            WHERE Username = ? AND Password = ?
        ''', (user, pw))
        row = cursor.fetchone()
        conn.close()

        if row is None:
            messagebox.showerror("Login Failed", "Invalid username or password.")
        else:
            level = row[0].lower()
            login_window.destroy()
            if level == "admin":
                manager_home()
            elif level == "sales":
                sales_home()
            else:
                messagebox.showinfo("Access Restricted",
                                    f"Unrecognized AccessLevel: {level}")

    Button(login_window, text="Login", command=validate_login,
           font=("Arial", 12), bg="#4682B4", fg="white").pack(pady=10)

    Button(login_window, text="Create Account",
           font=("Arial", 12), bg="#2ecc71", fg="white",
           command=lambda: create_account_window(login_window)).pack(pady=5)

    login_window.mainloop()
