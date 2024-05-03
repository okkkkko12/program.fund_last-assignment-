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


