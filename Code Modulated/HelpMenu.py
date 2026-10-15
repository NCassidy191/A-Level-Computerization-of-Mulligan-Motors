# HelpMenu.py

import sqlite3
from tkinter import Toplevel, Label, Button, messagebox
from tkinter.filedialog import asksaveasfilename

def help_page():
    help_window = Toplevel()
    help_window.title("Help")
    help_window.geometry("400x300")
    help_window.config(bg="#87CEEB")

    Label(help_window, text="Help Information", font=("Arial", 16),
          bg="#87CEEB").pack(pady=10)
    Label(help_window,
          text="1. Use the main menu to navigate.\n"
               "2. Add, edit, or delete records.\n"
               "3. Backup data regularly.\n"
               "4. Generate reports if needed.\n"
               "5. Create new accounts (if needed).",
          bg="#87CEEB", wraplength=350).pack(pady=10)
    Button(help_window, text="Close", command=help_window.destroy,
           bg="#4682B4", fg="white").pack(pady=10)


def backup_database():
    file_path = asksaveasfilename(defaultextension=".db", filetypes=[("SQLite Database", "*.db")])
    if file_path:
        with open('mulligan_motors.db', 'rb') as original:
            with open(file_path, 'wb') as backup:
                backup.write(original.read())
        messagebox.showinfo("Backup Successful", f"Database backed up to {file_path}")


def generate_report(parent_window):
    from tkinter import Toplevel, Label, Button, StringVar, OptionMenu
    from tkinter.filedialog import asksaveasfilename

    def do_export():
        chosen_table = table_var.get()
        if not chosen_table:
            messagebox.showwarning("Invalid Selection", "Please select a table.")
            return

        file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if not file_path:
            return

        try:
            conn = sqlite3.connect('mulligan_motors.db')
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {chosen_table}")
            rows = cursor.fetchall()
            conn.close()

            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"--- Report for table: {chosen_table} ---\n")
                for row in rows:
                    row_str = ", ".join(str(item) for item in row)
                    f.write(row_str + "\n")

            messagebox.showinfo("Success", f"Report generated: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not generate report: {e}")

        report_win.destroy()

    report_win = Toplevel(parent_window)
    report_win.title("Generate Report")
    report_win.geometry("300x200")
    report_win.config(bg="#87CEEB")

    Label(report_win, text="Select a table to export:", bg="#87CEEB").pack(pady=10)

    table_var = StringVar(value="")
    tables_list = [
        "VehicleStock",
        "Customer",
        "Orders",
        "Staff",
        "TestDrives",
        "Access",
        "Payslips"
    ]
    OptionMenu(report_win, table_var, *tables_list).pack(pady=5)

    Button(report_win, text="Generate TXT Report", command=do_export,
           bg="#4682B4", fg="white").pack(pady=20)
