import sys  # Importing the sys module, used to manipulate different parts of the Python runtime environment.
import pickle  # Importing pickle module for serializing and de-serializing Python object structures.
import os  # Importing os module to interact with the operating system.

class Employee:
    # Initializer or constructor for the Employee class with multiple attributes.
    def __init__(self, name, emp_id, department, job_title, basic_salary, age, date_of_birth, passport_details):
        self.name = name
        self.emp_id = emp_id
        self.department = department
        self.job_title = job_title
        self.basic_salary = basic_salary
        self.age = age
        self.date_of_birth = date_of_birth
        self.passport_details = passport_details

    # String representation of the Employee class to display an employee's information in a readable format.
    def __str__(self):
        return (f"Employee ID: {self.emp_id}, Name: {self.name}, Department: {self.department}, "
                f"Job Title: {self.job_title}, Salary: {self.basic_salary}, Age: {self.age}, "
                f"DOB: {self.date_of_birth}, Passport: {self.passport_details}")

class EmployeeManagement:
    # Initializer for the EmployeeManagement class which also loads the employee records from a file.
    def __init__(self, filename='employees.pkl'):
        self.filename = filename  # Filename where employee data is stored.
        self.employees = self.load_employees()  # Load employees from the file.

    def get_employee_by_id(self, emp_id):
        # Search for an employee by their ID and return the employee object if found.
        for employee in self.employees:
            if employee.emp_id == emp_id:
                return employee
        return None

    def add_employee(self, employee):
        # Add an employee to the list if they do not already exist by checking their ID.
        if self.get_employee_by_id(employee.emp_id) is not None:
            return "An employee with this ID already exists."
        self.employees.append(employee)
        self.save_employees()  # Save the updated list of employees to the file.
        return "Employee added successfully."

    def delete_employee(self, emp_id):
        # Delete an employee by their ID and save the changes if the employee exists.
        original_count = len(self.employees)
        self.employees = [e for e in self.employees if e.emp_id != emp_id]
        if len(self.employees) < original_count:
            self.save_employees()
            return "Employee deleted successfully."
        return "Employee not found."

    def modify_employee(self, emp_id, **kwargs):
        # Modify attributes of an employee based on keyword arguments and save the changes if the employee exists.
        employee = self.get_employee_by_id(emp_id)
        if employee is not None:
            for key, value in kwargs.items():
                setattr(employee, key, value)
            self.save_employees()
            return "Employee updated successfully."
        return "Employee not found."

    def display_employee_details(self, emp_id):
        # Display details of an employee if they are found using their ID.
        employee = self.get_employee_by_id(emp_id)
        if employee is not None:
            return str(employee)
        return "Employee not found."

    def save_employees(self):
        # Save the current list of employees to a file using pickle.
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.employees, f)
        except Exception as e:
            print(f"Error saving employees: {e}")
            return f"Error saving employees: {e}"

    def load_employees(self):
        # Load employees from a file; return an empty list if file is empty or not found.
        try:
            with open(self.filename, 'rb') as f:
                if os.fstat(f.fileno()).st_size > 0:  # Check if file is non-empty
                    return pickle.load(f)
                else:
                    return []  # Return an empty list if file is empty
        except FileNotFoundError:
            return []  # Return an empty list if file does not exist

class Event:
    # Constructor for the Event class with attributes to define an event.
    def __init__(self, event_id, event_type, theme, date, time, duration, venue_address, client_id, guest_list,
                 catering_company, cleaning_company, decorations_company, entertainment_company, furniture_supply_company, invoice):
        self.event_id = event_id
        self.event_type = event_type
        self.theme = theme
        self.date = date
        self.time = time
        self.duration = duration
        self.venue_address = venue_address
        self.client_id = client_id
        self.guest_list = guest_list
        self.catering_company = catering_company
        self.cleaning_company = cleaning_company
        self.decorations_company = decorations_company
        self.entertainment_company = entertainment_company
        self.furniture_supply_company = furniture_supply_company
        self.invoice = invoice

    # String representation of the Event class to display event details in a readable format.
    def __str__(self):
        return (f"Event ID: {self.event_id}, Type: {self.event_type}, Theme: {self.theme}, Date: {self.date}, "
                f"Time: {self.time}, Duration: {self.duration} hours, Venue: {self.venue_address}, "
                f"Client ID: {self.client_id}, Guests: {len(self.guest_list)}, "
                f"Catering: {self.catering_company}, Cleaning: {self.cleaning_company}, "
                f"Decorations: {self.decorations_company}, Entertainment: {self.entertainment_company}, "
                f"Furniture: {self.furniture_supply_company}, Invoice: {self.invoice}")

class EventManagement:
    # Initializer for the EventManagement class that loads existing events from a file.
    def __init__(self, filename='events.pkl'):
        self.filename = filename
        self.events = self.load_events()

    def load_events(self):
        # Load events from a file; handle the case where the file is not found by returning an empty list.
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    def add_event(self, event):
        # Add an event to the list if it does not already exist by its ID.
        if event.event_id not in [e.event_id for e in self.events]:
            self.events.append(event)
            self.save_events()
            return "Event added successfully."
        return "An event with this ID already exists."

    def save_events(self):
        # Save the current list of events to a file using pickle.
        with open(self.filename, 'wb') as f:
            pickle.dump(self.events, f)

    def delete_event(self, event_id):
        # Delete an event by its ID and save the changes if the event exists.
        original_count = len(self.events)
        self.events = [e for e in self.events if e.event_id != event_id]
        if len(self.events) < original_count:
            self.save_events()
            return "Event deleted successfully."
        return "Event not found."

    def modify_event(self, event_id, **kwargs):
        # Modify attributes of an event based on keyword arguments and save the changes if the event exists.
        for event in self.events:
            if event.event_id == event_id:
                for key, value in kwargs.items():
                    setattr(event, key, value)
                self.save_events()
                return "Event updated successfully."
        return "Event not found."

    def find_event(self, event_id):
        # Find and return an event by its ID.
        for event in self.events:
            if event.event_id == event_id:
                return event
        return "Event not found."

    def display_event_details(self, event_id):
        # Display details of an event if found using its ID.
        event = self.find_event(event_id)
        if isinstance(event, Event):
            return str(event)
        return "Event not found."

class Client:
    def __init__(self, client_id, name, address, contact_details, budget):
        # Initialization method for the Client class
        self.client_id = client_id  # Unique identifier for the client
        self.name = name  # Name of the client
        self.address = address  # Address of the client
        self.contact_details = contact_details  # Contact details of the client
        self.budget = budget  # Budget of the client

    def __str__(self):
        # String representation of the Client object, used when printing
        return f"Client ID: {self.client_id}, Name: {self.name}, Address: {self.address}, Contact: {self.contact_details}, Budget: ${self.budget}"

class ClientManagement:
    def __init__(self, filename='clients.pkl'):
        # Initialization method for the ClientManagement class
        self.filename = filename  # File to store client data
        self.clients = self.load_clients()  # Load existing clients from file

    def add_client(self, client):
        # Add a new client to the system
        if client.client_id not in [c.client_id for c in self.clients]:
            self.clients.append(client)  # Append new client if ID not found
            self.save_clients()  # Save updated client list to file
            return f"Client {client.name} added successfully."
        return "A client with this ID already exists."

    def delete_client(self, client_id):
        # Delete a client from the system by ID
        original_count = len(self.clients)
        self.clients = [c for c in self.clients if c.client_id != client_id]
        if len(self.clients) < original_count:
            self.save_clients()  # Save the updated list to file after deletion
            return "Client deleted successfully."
        return "Client not found."

    def modify_client(self, client_id, **kwargs):
        # Modify attributes of an existing client
        for client in self.clients:
            if client.client_id == client_id:
                for key, value in kwargs.items():
                    setattr(client, key, value)  # Set new values for attributes
                self.save_clients()  # Save changes to file
                return f"Client {client_id} updated successfully."
        return "Client not found."

    def find_client(self, client_id):
        # Retrieve a client's details by ID
        for client in self.clients:
            if client.client_id == client_id:
                return client
        return "Client not found."

    def display_client_details(self, client_id):
        # Display details of a specific client
        client = self.find_client(client_id)
        if isinstance(client, Client):
            return str(client)
        return "Client not found."

    def save_clients(self):
        # Serialize and save the list of clients to a file
        with open(self.filename, 'wb') as f:
            pickle.dump(self.clients, f)

    def load_clients(self):
        # Deserialize and load the list of clients from a file
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []  # Return an empty list if the file does not exist


class Guest:
    # Initializer for the Guest class
    def __init__(self, guest_id, name, address, contact_details):
        self.guest_id = guest_id
        self.name = name
        self.address = address
        self.contact_details = contact_details

    # Returns a string representation of a Guest object
    def __str__(self):
        return f"Guest ID: {self.guest_id}, Name: {self.name}, Address: {self.address}, Contact: {self.contact_details}"

class GuestManagement:
    # Initializer for the GuestManagement class with a default filename
    def __init__(self, filename='guests.pkl'):
        self.filename = filename
        self.guests = self.load_guests()  # Loads guests from a file on initialization

    # Adds a guest to the guest list if they don't already exist
    def add_guest(self, guest):
        # Check if the guest ID already exists in the guest list
        if guest.guest_id not in [g.guest_id for g in self.guests]:
            self.guests.append(guest)  # Add the new guest
            self.save_guests()  # Save the updated list to file
            return f"Guest {guest.name} added successfully."
        return "A guest with this ID already exists."

    # Deletes a guest from the guest list by their ID
    def delete_guest(self, guest_id):
        original_count = len(self.guests)
        self.guests = [g for g in self.guests if g.guest_id != guest_id]  # Filter out the guest to delete
        if len(self.guests) < original_count:
            self.save_guests()  # Save the updated list to file
            return "Guest deleted successfully."
        return "Guest not found."

    # Modifies details of a guest found by their ID
    def modify_guest(self, guest_id, **kwargs):
        for guest in self.guests:
            if guest.guest_id == guest_id:
                # Update attributes provided in kwargs
                for key, value in kwargs.items():
                    setattr(guest, key, value)
                self.save_guests()  # Save the updated list to file
                return f"Guest {guest_id} updated successfully."
        return "Guest not found."

    # Finds a guest by their ID
    def find_guest(self, guest_id):
        for guest in self.guests:
            if guest.guest_id == guest_id:
                return guest
        return "Guest not found."

    # Displays details of a specific guest
    def display_guest_details(self, guest_id):
        guest = self.find_guest(guest_id)
        if isinstance(guest, Guest):
            return str(guest)
        return "Guest not found."

    # Saves the current list of guests to a file
    def save_guests(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.guests, f)

    # Loads guests from a file or returns an empty list if the file is not found
    def load_guests(self):
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []

    # This line ensures that the Guest class is recognized when loading objects from pickle
    sys.modules['__main__.Guest'] = Guest

class Supplier:
    def __init__(self, supplier_id, name, address, contact_details, services_offered):
        # Initialize a new Supplier object with necessary attributes.
        self.supplier_id = supplier_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.services_offered = services_offered

    def __str__(self):
        # String representation for a Supplier object, formatted for readability.
        return (f"Supplier ID: {self.supplier_id}, Name: {self.name}, Address: {self.address}, "
                f"Contact Details: {self.contact_details}, Services Offered: {self.services_offered}")


class SupplierManagement:
    def __init__(self, filename='suppliers.pkl'):
        # Initialize SupplierManagement with a file name, default is 'suppliers.pkl'.
        # Load suppliers from file on initialization.
        self.filename = filename
        self.suppliers = self.load_suppliers()

    def add_supplier(self, supplier):
        # Add a new supplier to the dictionary if not already present, save to file.
        if supplier.supplier_id in self.suppliers:
            return "Supplier already exists."
        self.suppliers[supplier.supplier_id] = supplier
        self.save_suppliers()
        return "Supplier added successfully."

    def delete_supplier(self, supplier_id):
        # Delete a supplier by ID from the dictionary, save the updated dictionary to file.
        if supplier_id in self.suppliers:
            del self.suppliers[supplier_id]
            self.save_suppliers()
            return "Supplier deleted successfully."
        return "Supplier not found."

    def modify_supplier(self, supplier_id, **kwargs):
        # Modify attributes of an existing supplier using keyword arguments, save to file.
        if supplier_id not in self.suppliers:
            return "Supplier not found."
        supplier = self.suppliers[supplier_id]
        for key, value in kwargs.items():
            setattr(supplier, key, value)
        self.save_suppliers()
        return "Supplier updated successfully."

    def find_supplier(self, supplier_id):
        # Retrieve a supplier by ID from the dictionary.
        return self.suppliers.get(supplier_id, "Supplier not found.")

    def display_supplier_details(self, supplier_id):
        # Display details of a specific supplier, if found.
        supplier = self.find_supplier(supplier_id)
        if supplier != "Supplier not found.":
            return str(supplier)
        return "Supplier not found."

    def save_suppliers(self):
        # Save the current state of suppliers dictionary to a file using pickle.
        with open(self.filename, 'wb') as f:
            pickle.dump(self.suppliers, f)

    def load_suppliers(self):
        # Load suppliers from a file if it exists, otherwise return an empty dictionary.
        if os.path.exists(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        return {}

class Venue:
    def __init__(self, venue_id, name, address, contact_details, min_guests, max_guests):
        # Constructor for the Venue class with initialization of all its attributes
        self.venue_id = venue_id
        self.name = name
        self.address = address
        self.contact_details = contact_details
        self.min_guests = min_guests
        self.max_guests = max_guests

    def __str__(self):
        # String representation of the Venue object, used when printing the object
        return (f"Venue ID: {self.venue_id}, Name: {self.name}, Address: {self.address}, "
                f"Contact: {self.contact_details}, Min Guests: {self.min_guests}, Max Guests: {self.max_guests}")

class VenueManagement:
    def __init__(self, filename='venues.pkl'):
        # Constructor for VenueManagement class with default filename for storage
        self.filename = filename
        self.venues = self.load_venues()  # Load venues from the file when an instance is created

    def add_venue(self, venue):
        # Add a new venue to the list if it does not already exist based on venue_id
        if venue.venue_id not in [v.venue_id for v in self.venues]:
            self.venues.append(venue)
            self.save_venues()  # Save updated list of venues
            return f"Venue {venue.name} added successfully."
        return "A venue with this ID already exists."

    def delete_venue(self, venue_id):
        # Delete a venue by venue_id and save the changes
        original_count = len(self.venues)
        self.venues = [v for v in self.venues if v.venue_id != venue_id]
        if len(self.venues) < original_count:
            self.save_venues()
            return "Venue deleted successfully."
        return "Venue not found."

    def modify_venue(self, venue_id, **kwargs):
        # Modify attributes of a specific venue using keyword arguments
        for venue in self.venues:
            if venue.venue_id == venue_id:
                for key, value in kwargs.items():
                    setattr(venue, key, value)  # Update attributes if the venue is found
                self.save_venues()
                return f"Venue {venue_id} updated successfully."
        return "Venue not found."

    def find_venue(self, venue_id):
        # Find and return a venue by its venue_id
        for venue in self.venues:
            if venue.venue_id == venue_id:
                return venue
        return "Venue not found."

    def display_venue_details(self, venue_id):
        # Display details of a specific venue
        venue = self.find_venue(venue_id)
        if venue != "Venue not found.":
            return str(venue)
        return "Venue not found."

    def save_venues(self):
        # Save the list of venues to a file using pickle
        with open(self.filename, 'wb') as f:
            pickle.dump(self.venues, f)

    def load_venues(self):
        # Load venues from a file, handling the case where the file might not exist
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return []  # Return an empty list if the file is not found


