# manageTable.py

import sqlite3
from tkinter import Toplevel, Label, Entry, Button, messagebox, ttk, StringVar, OptionMenu
from InputValidation import validate_input

def manage_table(table_name, fields, insert_query, update_query, parent_window):
    """
    Logic for searching, adding, editing, deleting records in table_name.
    """

    def load_data():
        for item in table_tree.get_children():
            table_tree.delete(item)
        conn = sqlite3.connect('mulligan_motors.db')
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            table_tree.insert("", "end", values=row)

    def search():
        col = dropdown_var.get()
        term = search_entry.get()
        if not term:
            messagebox.showwarning("Invalid Input", "Please enter a search term.")
            return
        conn = sqlite3.connect('mulligan_motors.db')
        cursor = conn.cursor()
        query = f"SELECT * FROM {table_name} WHERE {col} LIKE ?"
        cursor.execute(query, (f"%{term}%",))
        results = cursor.fetchall()
        conn.close()

        for item in table_tree.get_children():
            table_tree.delete(item)
        if results:
            for r in results:
                table_tree.insert("", "end", values=r)
        else:
            messagebox.showinfo("No Records Found", f"No record for {col} = '{term}'.")

    def add_record():
        def save_record():
            add_fields_final = fields[1:]
            if table_name == "Payslips":
                add_fields_final = [x for x in add_fields_final if x != "TotalOwed"]

            record_data = {}
            for ff in add_fields_final:
                record_data[ff] = entry_vars[ff].get()

            is_valid, error_msg = validate_input(table_name, record_data)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            if table_name == "Payslips":
                s_id = record_data["StaffID"]
                hrs = float(record_data["HoursWorked"])
                rate = float(record_data["HourlyRate"])
                total = hrs * rate
                conn = sqlite3.connect('mulligan_motors.db')
                cursor = conn.cursor()
                cursor.execute(insert_query, (s_id, hrs, rate, total))
                conn.commit()
                conn.close()
            else:
                vals = [record_data[ff] for ff in add_fields_final]
                conn = sqlite3.connect('mulligan_motors.db')
                cursor = conn.cursor()
                cursor.execute(insert_query, vals)
                conn.commit()
                conn.close()

            add_win.destroy()
            load_data()

        add_win = Toplevel(parent_window)
        add_win.title(f"Add {table_name.title()} Record")
        add_win.geometry("400x600")
        add_win.config(bg="#87CEEB")

        add_fields_list = fields[1:]
        if table_name == "Payslips":
            add_fields_list = [x for x in add_fields_list if x != "TotalOwed"]

        entry_vars = {}
        for ff in add_fields_list:
            Label(add_win, text=ff, bg="#87CEEB").pack(pady=5)

            # e.g. drop-downs for VehicleCondition, PreferredContactMethod
            if table_name == "VehicleStock" and ff == "VehicleCondition":
                var = StringVar(value="Pristine")
                OptionMenu(add_win, var, "Pristine", "Slightly Used", "Heavily Used").pack(pady=5)
            elif table_name == "Customer" and ff == "PreferredContactMethod":
                var = StringVar(value="Email")
                OptionMenu(add_win, var, "Email", "Phone", "SMS").pack(pady=5)
            else:
                var = StringVar()
                Entry(add_win, textvariable=var).pack(pady=5)
            entry_vars[ff] = var

        Button(add_win, text="Save", command=save_record,
               bg="#4682B4", fg="white").pack(pady=20)

    def edit_record():
        sel = table_tree.selection()
        if not sel:
            messagebox.showerror("No Selection", "Select a record to edit.")
            return
        old_vals = table_tree.item(sel)["values"]

        def save_edits():
            pk = old_vals[0]
            record_data = {}
            for col_name in edit_fields_list:
                record_data[col_name] = entry_vars[col_name].get()

            is_valid, error_msg = validate_input(table_name, record_data)
            if not is_valid:
                messagebox.showerror("Validation Error", error_msg)
                return

            if table_name == "Payslips":
                st_id = record_data["StaffID"]
                hrs2 = float(record_data["HoursWorked"])
                rate2 = float(record_data["HourlyRate"])
                tot2 = hrs2 * rate2
                conn = sqlite3.connect('mulligan_motors.db')
                cursor = conn.cursor()
                cursor.execute(update_query, (st_id, hrs2, rate2, tot2, pk))
                conn.commit()
                conn.close()
            else:
                new_vals = [record_data[f2] for f2 in edit_fields_list]
                new_vals.append(pk)
                conn = sqlite3.connect('mulligan_motors.db')
                cursor = conn.cursor()
                cursor.execute(update_query, new_vals)
                conn.commit()
                conn.close()

            edit_win.destroy()
            load_data()

        edit_win = Toplevel(parent_window)
        edit_win.title(f"Edit {table_name.title()} Record")
        edit_win.geometry("400x600")
        edit_win.config(bg="#87CEEB")

        edit_fields_list = fields[1:]
        if table_name == "Payslips":
            edit_fields_list = [x for x in edit_fields_list if x != "TotalOwed"]

        entry_vars = {}
        for i, col_name in enumerate(edit_fields_list, start=1):
            Label(edit_win, text=col_name, bg="#87CEEB").pack(pady=5)
            old_val = str(old_vals[i])

            if table_name == "VehicleStock" and col_name == "VehicleCondition":
                var = StringVar(value=old_val)
                OptionMenu(edit_win, var, "Pristine", "Slightly Used", "Heavily Used").pack(pady=5)
            elif table_name == "Customer" and col_name == "PreferredContactMethod":
                var = StringVar(value=old_val)
                OptionMenu(edit_win, var, "Email", "Phone", "SMS").pack(pady=5)
            else:
                var = StringVar(value=old_val)
                Entry(edit_win, textvariable=var).pack(pady=5)

            entry_vars[col_name] = var

        Button(edit_win, text="Save Changes", command=save_edits,
               bg="#4682B4", fg="white").pack(pady=20)

    def delete_record():
        sel = table_tree.selection()
        if not sel:
            messagebox.showerror("No Selection", "Select a record to delete.")
            return
        valz = table_tree.item(sel)["values"]
        pk2 = valz[0]
        ask = messagebox.askyesno("Confirm Delete", f"Delete record ID={pk2}?")
        if ask:
            conn = sqlite3.connect('mulligan_motors.db')
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name} WHERE {fields[0]} = ?", (pk2,))
            conn.commit()
            conn.close()
            load_data()

    # Table sub-window
    table_window = Toplevel(parent_window)
    table_window.title(f"Manage {table_name.title()}")
    table_window.geometry("900x600")
    table_window.config(bg="#87CEEB")

    Label(table_window, text=f"{table_name.title()} Records", font=("Arial", 16),
          bg="#87CEEB", fg="black").pack(pady=10)

    # Search area
    search_frame = ttk.Frame(table_window)
    search_frame.pack(pady=10, fill="x")

    dropdown_var = StringVar()
    dropdown_var.set(fields[0])
    OptionMenu(search_frame, dropdown_var, *fields).pack(side="left", padx=10)

    search_entry = Entry(search_frame, font=("Arial", 12), width=20)
    search_entry.pack(side="left", padx=10)
    Button(search_frame, text="Search", command=search,
           bg="#4682B4", fg="white").pack(side="left", padx=10)

    # Table tree
    table_tree = ttk.Treeview(table_window, columns=fields, show="headings", height=15)
    for col in fields:
        table_tree.heading(col, text=col)
        table_tree.column(col, width=120)
    table_tree.pack(fill="x", padx=10, pady=10)

    # Buttons
    Button(table_window, text="Add Record", command=add_record,
           bg="#4682B4", fg="white").pack(side="left", padx=5, pady=10)
    Button(table_window, text="Edit Record", command=edit_record,
           bg="#4682B4", fg="white").pack(side="left", padx=5, pady=10)
    Button(table_window, text="Delete Record", command=delete_record,
           bg="#4682B4", fg="white").pack(side="left", padx=5, pady=10)

    Button(table_window, text="Back", command=table_window.destroy,
           bg="#4682B4", fg="white").pack(side="right", padx=5, pady=10)

    load_data()
