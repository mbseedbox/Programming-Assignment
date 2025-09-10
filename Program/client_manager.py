### Programming Assignment Part 3 ##
# client_manager.py
# A simple Command-Line Interface (CLI) application for managing client contacts.

import csv  # Used for reading and writing data to a .csv file
import os   # Used to check if the data file already exists

# Define the name of the file where client data will be stored.
# Using a constant makes it easy to change the filename in one place if needed.
DATA_FILE = 'clients.csv'

# Define the headers for the CSV file. This structure ensures consistency.
# It's also used to write the header row if the file doesn't exist yet.
FIELDNAMES = ['name', 'company', 'email', 'phone']

def initialize_data_file():
    """
    Checks if the data file exists. If not, it creates the file and writes the header row.
    This prevents errors when the program tries to read from a non-existent file on first run.
    """
    # os.path.exists() checks for the presence of a file. 'not' inverts the result.
    if not os.path.exists(DATA_FILE):
        # 'with open(...)' is the standard, safe way to handle files in Python.
        # It automatically closes the file even if errors occur.
        # 'w' mode is for writing (it creates the file if it doesn't exist, or overwrites it if it does).
        # 'newline=''' is a best practice for writing CSV files to prevent blank rows.
        with open(DATA_FILE, 'w', newline='') as file:
            # csv.DictWriter is used to write dictionaries to a CSV file.
            # It maps the dictionary keys (our fieldnames) to columns.
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            # writer.writeheader() writes the first row of the CSV with the field names.
            writer.writeheader()
            print("Data file 'clients.csv' created.")

def load_clients():
    """
    Reads all client records from the CSV file and returns them as a list of dictionaries.
    Each dictionary represents one client.
    """
    try:
        # 'r' mode is for reading.
        with open(DATA_FILE, 'r', newline='') as file:
            # csv.DictReader reads the CSV file and treats each row as a dictionary.
            # It automatically uses the first row as the keys (our headers).
            reader = csv.DictReader(file)
            # A list comprehension to convert the reader object into a list of dictionaries.
            return [row for row in reader]
    except FileNotFoundError:
        # If the file somehow doesn't exist when this is called, return an empty list.
        # This is a fallback, as initialize_data_file() should prevent this.
        return []

def save_clients(clients):
    """
    Writes a list of client dictionaries back to the CSV file, overwriting the existing content.
    This is how we save changes after adding or deleting a client.
    """
    try:
        # 'w' mode will overwrite the entire file with the new list of clients.
        with open(DATA_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()  # Write the header row first.
            # writer.writerows() writes all the dictionaries in the 'clients' list to the file.
            writer.writerows(clients)
    except IOError as e:
        # IOError can happen if the file is read-only or there's a disk issue.
        print(f"Error saving data: {e}")

def add_client():
    """
    Prompts the user for new client details, creates a client dictionary,
    and appends it to the CSV file.
    """
    print("\n--- Add New Client ---")
    # Use .strip() to remove any accidental leading/trailing whitespace from user input.
    name = input("Enter client name: ").strip()
    company = input("Enter company name: ").strip()
    email = input("Enter email address: ").strip()
    phone = input("Enter phone number: ").strip()

    # Basic validation to ensure the name is not empty.
    if not name:
        print("Client name cannot be empty. Aborting.")
        return

    # Create a dictionary for the new client. The keys must match FIELDNAMES.
    new_client = {'name': name, 'company': company, 'email': email, 'phone': phone}

    # Instead of reading the whole file, we can just append the new client for efficiency.
    # 'a' mode is for appending.
    try:
        with open(DATA_FILE, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writerow(new_client)
        print("\nClient added successfully!")
    except IOError as e:
        print(f"Error adding client: {e}")


def view_clients():
    """
    Loads all clients and displays them in a formatted table.
    """
    print("\n--- All Clients ---")
    clients = load_clients()

    # Check if the list of clients is empty.
    if not clients:
        print("No clients to display.")
        return

    # Print a formatted header for the table.
    # The numbers in {:<20} define the width of the column and '<' means left-align.
    print(f"{'Name':<20} | {'Company':<20} | {'Email':<30} | {'Phone':<15}")
    print("-" * 88)  # Print a separator line.

    # Loop through each client dictionary in the list.
    for client in clients:
        # Print each client's details, formatted to align with the header.
        print(f"{client['name']:<20} | {client['company']:<20} | {client['email']:<30} | {client['phone']:<15}")

def search_client():
    """
    Prompts the user for a name to search for and displays matching clients.
    The search is case-insensitive.
    """
    print("\n--- Search Client ---")
    search_name = input("Enter the name of the client to search for: ").strip().lower()

    if not search_name:
        print("Search name cannot be empty.")
        return

    clients = load_clients()
    # Use a list comprehension to create a new list containing only matching clients.
    # .lower() is used on both the client's name and the search term for a case-insensitive match.
    found_clients = [client for client in clients if search_name in client['name'].lower()]

    if not found_clients:
        print(f"No client found matching '{search_name}'.")
    else:
        print(f"\nFound {len(found_clients)} client(s):")
        # Reuse the same display format as view_clients().
        print(f"{'Name':<20} | {'Company':<20} | {'Email':<30} | {'Phone':<15}")
        print("-" * 88)
        for client in found_clients:
            print(f"{client['name']:<20} | {client['company']:<20} | {client['email']:<30} | {client['phone']:<15}")

def delete_client():
    """
    Prompts for a client name to delete, confirms the action, and removes the client.
    The search for the client to delete must be an exact, case-insensitive match.
    """
    print("\n--- Delete Client ---")
    delete_name = input("Enter the exact name of the client to delete: ").strip().lower()

    if not delete_name:
        print("Client name cannot be empty.")
        return

    clients = load_clients()
    # Find the specific client to delete. We expect only one exact match.
    # 'client_to_delete' will be the dictionary of the found client, or None if not found.
    client_to_delete = None
    for client in clients:
        if client['name'].lower() == delete_name:
            client_to_delete = client
            break # Stop searching once found

    if not client_to_delete:
        print(f"No client found with the exact name '{delete_name}'.")
    else:
        print("\nClient found:")
        print(f"  Name: {client_to_delete['name']}")
        print(f"  Company: {client_to_delete['company']}")

        # Confirmation step to prevent accidental deletion.
        confirm = input("Are you sure you want to delete this client? (y/n): ").strip().lower()
        if confirm == 'y':
            # Create a new list of clients, excluding the one to be deleted.
            updated_clients = [client for client in clients if client['name'].lower() != delete_name]
            # Save the new, smaller list back to the file.
            save_clients(updated_clients)
            print("Client deleted successfully.")
        else:
            print("Deletion cancelled.")

def display_menu():
    """
    Displays the main menu of options to the user.
    """
    print("\n===== Client Management System =====")
    print("1. Add a new client")
    print("2. View all clients")
    print("3. Search for a client")
    print("4. Delete a client")
    print("5. Exit")
    print("====================================")

def main():
    """
    The main function that runs the application loop.
    """
    # Ensure the data file is ready before we start.
    initialize_data_file()

    # This 'while True' loop keeps the program running until the user chooses to exit.
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_client()
        elif choice == '2':
            view_clients()
        elif choice == '3':
            search_client()
        elif choice == '4':
            delete_client()
        elif choice == '5':
            print("Exiting program. Goodbye!")
            break  # This breaks out of the 'while' loop, ending the program.
        else:
            # Handle cases where the user enters something other than 1-5.
            print("Invalid choice. Please enter a number between 1 and 5.")

        input("\nPress Enter to continue...") # Pause the program to let the user read the output.


# This is a standard Python construct.
# It ensures that the 'main()' function is called only when the script is executed directly,
# not when it's imported as a module into another script.
if __name__ == "__main__":
    main()
# Reviewed by Krispe, 10/09/2025 – Checked logic for client creation and tested main input flow.
# Looks good! Left a couple of suggestions below, especially on error handling for edge cases.

# Suggestion (Krispe): Could add input validation in 'add_client' so email has an '@' and phone is numbers only.
