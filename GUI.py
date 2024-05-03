import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from Classes import Guest, Employee, Client, Event, Supplier, Venue, EmployeeManagement, EventManagement, ClientManagement, GuestManagement, SupplierManagement, VenueManagement

# Define a GUI class for the management system interface
class GUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Management System GUI")  # Set the window title
        # Initialize management system objects for each entity
        self.emp_mgr = EmployeeManagement()
        self.event_mgr = EventManagement()
        self.client_mgr = ClientManagement()
        self.guest_mgr = GuestManagement()
        self.supplier_mgr = SupplierManagement()
        self.Venue_mgr = VenueManagement()

        self.create_widgets()  # Create GUI elements

    # Function to create buttons for each entity
    def create_widgets(self):
        # Buttons for different management options
        tk.Button(self.master, text="Employees", command=self.show_employee_options).pack()
        tk.Button(self.master, text="Events", command=self.show_event_options).pack()
        tk.Button(self.master, text="Clients", command=self.show_client_options).pack()
        tk.Button(self.master, text="Guests", command=self.show_guest_options).pack()
        tk.Button(self.master, text="Suppliers", command=self.show_supplier_options).pack()
        tk.Button(self.master, text="Venues", command=self.show_venue_options).pack()

    # Functions to handle options for each entity
    def show_employee_options(self):
        self.show_options("Employee", self.emp_mgr)

    def show_event_options(self):
        self.show_options("Event", self.event_mgr)

    def show_client_options(self):
        self.show_options("Client", self.client_mgr)

    def show_guest_options(self):
        self.show_options("Guest", self.guest_mgr)

    def show_supplier_options(self):
        self.show_options("Supplier", self.supplier_mgr)

    def show_venue_options(self):
        self.show_options("Venue", self.Venue_mgr)

    # Function to display management options for a specific entity
    def show_options(self, entity, manager):
        options_window = tk.Toplevel(self.master)
        options_window.title(f"{entity} Management")  # Set window title

        # Buttons for different management actions
        tk.Button(options_window, text=f"Add {entity}", command=lambda: self.add_entity(manager, options_window)).pack()
        tk.Button(options_window, text=f"Delete {entity}", command=lambda: self.delete_entity(manager, options_window)).pack()
        tk.Button(options_window, text=f"Modify {entity}", command=lambda: self.modify_entity(manager, options_window)).pack()
        tk.Button(options_window, text=f"Search for {entity}", command=lambda: self.search_display_entity(manager, options_window)).pack()

    # Function to get user input for entity attributes
    def get_user_input(self, attributes, entity_name):
        input_window = tk.Toplevel(self.master)
        input_window.title("Input Details")  # Set window title

        entries = {}  # Dictionary to store user inputs
        # Create input fields for each attribute
        for attribute in attributes:
            tk.Label(input_window, text=f"Enter {attribute.replace('_', ' ').title()}").pack()
            entry = tk.Entry(input_window)
            entry.pack(pady=5, padx=10)
            entries[attribute] = entry  # Store entry field in dictionary

        # Function to confirm user inputs
        def confirm_inputs():
            for attribute, entry in entries.items():
                entries[attribute] = entry.get()  # Get input value
            input_window.destroy()  # Close input window

        # Button to confirm inputs
        tk.Button(input_window, text="Confirm", command=confirm_inputs).pack(pady=10)
        input_window.wait_window()  # Pause code execution until input window is closed
        return {key: value for key, value in entries.items()}  # Return dictionary of attribute values

    # Function to add a new entity
    def add_entity(self, manager, window):
        entity_name = manager.__class__.__name__.replace("Management", "")  # Get entity name
        attributes = self.get_entity_attributes(entity_name)  # Get attributes for entity
        values = self.get_user_input(attributes, entity_name)  # Get user inputs for attributes

        # Construct the object based on entity type
        if entity_name == 'Employee':
            if manager.get_employee_by_id(values['emp_id']):
                messagebox.showerror("Error", "An employee with this ID already exists.")
                return
            entity = Employee(**values)
        elif entity_name == 'Supplier':
            if values['supplier_id'] in [supplier.supplier_id for supplier in manager.suppliers.values()]:
                messagebox.showerror("Error", "A supplier with this ID already exists.")
                return
            entity = Supplier(**values)
        elif entity_name == 'Client':
            entity = Client(**values)
        elif entity_name == 'Guest':
            entity = Guest(**values)
        elif entity_name == 'Event':
            entity = Event(**values)
        elif entity_name == 'Venue':
            entity = Venue(**values)
        else:
            messagebox.showerror("Error", "Unsupported entity type")
            return

        # Add the entity to the manager
        result = getattr(manager, f"add_{entity_name.lower()}")(entity)
        # Show result message
        messagebox.showinfo("Result", result if result else "Failed to add the entity.")
        window.destroy()  # Close options window

        # Function to delete an entity
    def delete_entity(self, manager, window):
        entity_name = manager.__class__.__name__.replace("Management", "")  # Get entity name
        entity_id = simpledialog.askstring("Input", f"Enter {entity_name} ID to delete:")  # Get ID of entity to delete
        result = getattr(manager, f"delete_{entity_name.lower()}")(entity_id)  # Delete entity
        messagebox.showinfo(f"Delete {entity_name}", result)  # Show result message
        window.destroy()  # Close options window

    # Function to modify an entity
    def modify_entity(self, manager, window):
        entity_name = manager.__class__.__name__.replace("Management", "")  # Get entity name
        entity_id_key = f"{entity_name.lower()}_id"  # Construct the ID key based on entity name

        # Ask user for the ID of entity to modify
        entity_id = simpledialog.askstring("Input", f"Enter {entity_name} ID to modify:")
        if entity_id:
            attributes = self.get_entity_attributes(entity_name)  # Get attributes for entity
            values = self.get_user_input(attributes, entity_name)  # Get user inputs for attributes

            if entity_id_key in values:
                del values[entity_id_key]  # Remove ID key from values dictionary

            try:
                # Modify the entity
                result = getattr(manager, f"modify_{entity_name.lower()}")(entity_id, **values)
                messagebox.showinfo(f"Modify {entity_name}", result)  # Show result message
            except Exception as e:
                messagebox.showerror("Error", str(e))  # Show error message
            finally:
                window.destroy()  # Close options window

    # Function to search and display details of an entity
    def search_display_entity(self, manager, window):
        entity_name = manager.__class__.__name__.replace("Management", "")  # Get entity name
        entity_id = simpledialog.askstring("Input", f"Enter {entity_name} ID to search:")  # Get ID to search
        result = getattr(manager, f"display_{entity_name.lower()}_details")(entity_id)  # Search and display details
        messagebox.showinfo(f"{entity_name} Details", result)  # Show result message
        window.destroy()  # Close options window

    # Function to get attributes for an entity
    def get_entity_attributes(self, entity_name):
        # Dictionary mapping entity names to their attributes
        attributes = {
            'Employee': ['id', 'name', 'department', 'job_title', 'basic_salary', 'age', 'date_of_birth', 'passport_details'],
            'Event': ['event_id', 'event_type', 'theme', 'date', 'time', 'duration', 'venue_address', 'client_id', 'guest_list', 'catering_company', 'cleaning_company', 'decorations_company', 'entertainment_company', 'furniture_supply_company', 'invoice'],
            'Client': ['client_id', 'name', 'address', 'contact_details', 'budget'],
            'Guest': ['guest_id', 'name', 'address', 'contact_details'],
            'Supplier': ['supplier_id', 'name', 'address', 'contact_details', 'services_offered'],
            'Venue': ['venue_id', 'name', 'address', 'contact_details', 'min_guests', 'max_guests']
        }
        return attributes[entity_name]  # Return attributes for specified entity

# Function to create GUI and start application
def main():
    app_root = tk.Tk()  # Create Tkinter root window
    app = GUI(app_root)  # Create GUI instance
    app_root.mainloop()  # Start main event loop

# Check if script is executed directly
if __name__ == "__main__":
    main()  # Call main function to start application

