<p align="center">
  <img src="https://github.com/CodeWithSomesh/Call-A-Doctor/assets/123357802/35f74a8a-0157-4f6d-9980-c96947586e61" alt="Call a Doctor Logo">
</p>


# Call a Doctor (CaD) Appointment Booking System

<br>

## Description

The "Call a Doctor (CaD)" project is a comprehensive desktop application designed to facilitate medical appointment booking, doctor-patient interaction, and clinic management. Developed using Python with Tkinter and CustomTkinter for the graphical user interface and SQLite for the database, this application aims to streamline the process of booking medical appointments, managing patient records, and overseeing clinic operations. The system supports multiple user roles including patients, doctors, clinic administrators, and CaD administrators, each with tailored functionalities to enhance the overall user experience.

<br>

## Features

### For Patients:
- **Search Clinic**: Search for available clinics from the clinic list and view them on a map.
- **Book Appointment**: Schedule medical appointments conveniently from home.
- **View Booked Appointment**: View details of booked appointments.
- **Update Appointment**: Modify appointment details as needed.
- **Delete Appointment**: Cancel booked appointments if necessary.

<br>

### For Doctors:
- **View Patient Records**: Access and review patient records for informed medical decision-making.
- **Generate Prescriptions**: Create prescriptions for patients during consultations.
- **Update Availability**: Manage availability status for appointments.
- **Update Prescriptions**: Edit existing prescriptions.

<br>

### For Clinic Administrators:
- **Manage Appointments**:
  - **View Appointment Details**: View detailed information about appointments.
  - **Reassign Busy Doctors**: Reassign doctors when the originally assigned ones are busy or unavailable.
  - **Approve Appointment Requests**: Approve incoming appointment requests.
  - **Reject Appointment Requests**: Reject appointment requests that cannot be accommodated.
- **Manage Doctor’s Access**:
  - **View Doctor Details**: Access detailed profiles of doctors.
  - **Approve New Doctors**: Approve the addition of new doctors to the clinic’s roster.
  - **Reject Inactive Doctors**: Remove or reject inactive doctors.
 
<br>

### For CaD Administrators:
- **Approve Clinic Registration**: Verify and approve clinic registrations.
- **Reject Clinic Registration**: Reject clinic registrations that do not meet the project’s criteria.

<br>

### Additional Features:
- **Dynamic Greeting**: Personalized greeting based on the time of day.
- **Role-Based Inputs**: Dynamic form fields based on user roles during Sign In.
- **Error Handling**: Proper error messages for invalid actions.

<br>

## Installation

### Prerequisites
- Python 3.x
- pip (Python package installer)

### Dependencies
The project requires the following Python libraries:
- `tkinter`
- `customtkinter`
- `sqlite3`

### Installation Steps

1. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/CaD-Appointment-Booking-System.git
   cd CaD-Appointment-Booking-System
   ```

2. **Create a Virtual Environment (Optional but recommended)**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**:
   ```sh
   pip install tk
   pip install customtkinter
   ```

<br>

## Running the Application & Setting Up the Database

To run the application, execute the `main.py` file located in either the `loginWindow` or `signInWindow` folder:

```sh
cd loginWindow
python main.py
```
or
```sh
cd signInWindow
python main.py
```

This will start the CaD Appointment Booking System, allowing you to interact with the interface and utilize all its features. 
After running the above command, the databases will be created in the project folder. You can verify the data using any online SQLite viewer. Here are some recommended viewers:
- [SQLite Viewer by Inloop](https://inloop.github.io/sqlite-viewer/)
- [SQLite Viewer App](https://sqliteviewer.app)

<br>

## Contributing

Contributions are welcome! Please fork the repository and create a pull request with your changes. Ensure that your code and pull requests follows the project's coding standards and includes necessary documentation.

<br>

## Contact

For any questions or issues, please contact me at codewithsomesh@gmail.com


