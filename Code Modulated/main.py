# main.py

from DBSetup import initialize_database
from LoginPage import login_screen

if __name__ == "__main__":
    # Initialize or verify the database schema
    initialize_database()

    # Launch the Login screen
    login_screen()
