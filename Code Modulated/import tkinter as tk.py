import tkinter as tk
from tkinter import messagebox

# Create the main window
root = tk.Tk()
root.withdraw()  # Hide the root window

# Show an error message box
messagebox.showerror("Mulligan Motors", "Total Owed could not be calaculated. Please validate values")

# Destroy the main window after the message box is closed
root.destroy()