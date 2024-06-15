import sys
from pathlib import Path
from PIL import Image
from tkinter import messagebox
import customtkinter as ctk
import sqlite3
import bcrypt # Helps in hashing the password for increased security
import re # Provides support for working with regular expressions


# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Paths to assets and output directories
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\signInWindow\assets\frame0")


def signInWindow():

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CONNECTING TO SQLITE3 DATABASE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Creating Patient DB
    patientConn = sqlite3.connect('patients.db')
    patientCursor = patientConn.cursor()
    patientCursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            PatientID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            NRIC TEXT NOT NULL,
            Role TEXT NOT NULL,
            Address TEXT NOT NULL,
            NumberOfAppointments INTEGER NOT NULL
        )          
    """)

    # Creating Doctor DB
    doctorConn = sqlite3.connect('doctors.db')
    doctorCursor = doctorConn.cursor()
    doctorCursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            DoctorID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            NRIC TEXT NOT NULL,
            Role TEXT NOT NULL,
            ClinicName TEXT NOT NULL,
            Specialization TEXT NOT NULL,
            YearsOfExperience TEXT NOT NULL,
            IsApproved INTEGER DEFAULT 0
        )          
    """)

    # Creating Clinic Admin DB
    clinicAdminConn = sqlite3.connect('clinicAdmins.db')
    clinicAdminCursor = clinicAdminConn.cursor()
    clinicAdminCursor.execute("""
        CREATE TABLE IF NOT EXISTS clinicAdmins (
            ClinicAdminID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            NRIC TEXT NOT NULL,
            Role TEXT NOT NULL,
            ClinicName TEXT NOT NULL,
            ClinicAddress TEXT NOT NULL,
            ClinicNumber TEXT NOT NULL,
            IsApproved INTEGER DEFAULT 0
        )          
    """)

    # Creating Clinic Admin DB
    adminConn = sqlite3.connect('admins.db')
    adminCursor = adminConn.cursor()
    adminCursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            AdminID INTEGER PRIMARY KEY AUTOINCREMENT,
            FirstName TEXT NOT NULL,
            LastName TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            NRIC TEXT NOT NULL,
            Role TEXT NOT NULL,
            AdminSecretKey TEXT NOT NULL
        )          
    """)

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ALL FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Redirect to the Log In Window
    def redirectToLoginWindow():
        window.destroy()
        from logInWindow.main import logInWindow
        logInWindow()

    # Update the display based on selected role
    def displayBasedOnRole(role):
        print(role)
        buttonFrame.pack_forget()
        loginTextFrame.pack_forget()
        #submitButton.pack_forget()

        if role == 'Clinic Admin':
            # Hide patient and doctor specific fields
            patientBottomFrame.pack_forget()
            adminBottomFrame.pack_forget()
            doctorSpecializationLabel.pack_forget()
            yearsOfExpLabel.pack_forget()
            doctorTypeDropdown.pack_forget()
            yearsOfExpTextBox.pack_forget()
            doctorBottomFrame.pack_forget()
            doctorClinicNameLabel.pack_forget()
            doctorClinicNameDropdown.pack_forget()

            # Show clinic admin specific fields
            clinicNameLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
            clinicContactLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
            clinicNameTextBox.pack(side='top', fill='x', expand=False,)
            clinicContactTextBox.pack(side='top', fill='x', expand=False,)
            clinicBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0))
            clinicAddressLabel.pack(side='top', fill='x', expand=False, )
            clinicAddressTextBox.pack(side='top', fill='none', expand=False, pady=(0, 40), anchor="w")

        elif role == 'Patient':
            # Hide clinic admin and doctor specific fields
            adminBottomFrame.pack_forget()
            clinicNameLabel.pack_forget()
            clinicNameTextBox.pack_forget()
            clinicContactLabel.pack_forget()
            clinicContactTextBox.pack_forget()
            clinicBottomFrame.pack_forget()
            clinicAddressLabel.pack_forget()
            clinicAddressTextBox.pack_forget()
            doctorSpecializationLabel.pack_forget()
            yearsOfExpLabel.pack_forget()
            doctorTypeDropdown.pack_forget()
            yearsOfExpTextBox.pack_forget()
            doctorBottomFrame.pack_forget()
            doctorClinicNameLabel.pack_forget()
            doctorClinicNameDropdown.pack_forget()

            # Show patient specific fields
            patientBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0),)
            addressLabel.pack(side='top', fill='x', expand=False,)
            addressTextBox.pack(side='top', fill='none', expand=False, pady=(0, 40), anchor="w")
            
        elif role == 'Doctor':
            # Hide clinic admin and patient specific fields
            clinicNameLabel.pack_forget()
            clinicNameTextBox.pack_forget()
            clinicContactLabel.pack_forget()
            clinicContactTextBox.pack_forget()
            clinicBottomFrame.pack_forget()
            clinicAddressLabel.pack_forget()
            clinicAddressTextBox.pack_forget()
            patientBottomFrame.pack_forget()
            adminBottomFrame.pack_forget()

            # Show doctor specific fields
            doctorSpecializationLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
            yearsOfExpLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
            doctorTypeDropdown.pack(side='top', fill='x', expand=False,)
            yearsOfExpTextBox.pack(side='top', fill='x', expand=False,)
            doctorBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0))
            doctorClinicNameLabel.pack(side='top', fill='x', expand=False, )
            doctorClinicNameDropdown.pack(side='top', fill='none', expand=False, pady=(0, 40), anchor="w")
        
        
        elif role == 'CAD Admin':
            # Hide clinic admin and doctor specific fields
            clinicNameLabel.pack_forget()
            clinicNameTextBox.pack_forget()
            clinicContactLabel.pack_forget()
            clinicContactTextBox.pack_forget()
            clinicBottomFrame.pack_forget()
            clinicAddressLabel.pack_forget()
            clinicAddressTextBox.pack_forget()
            doctorSpecializationLabel.pack_forget()
            yearsOfExpLabel.pack_forget()
            doctorTypeDropdown.pack_forget()
            yearsOfExpTextBox.pack_forget()
            doctorBottomFrame.pack_forget()
            doctorClinicNameLabel.pack_forget()
            doctorClinicNameDropdown.pack_forget()

            # Show patient specific fields
            adminBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0),)
            adminSecretKeyLabel.pack(side='top', fill='x', expand=False,)
            adminSecretKeyTextBox.pack(side='top', fill='none', expand=False, pady=(0, 40), anchor="w")


        else:
            # Hide all fields and reset to initial state
            patientBottomFrame.pack_forget()
            adminBottomFrame.pack_forget()
            clinicNameLabel.pack_forget()
            clinicNameTextBox.pack_forget()
            clinicContactLabel.pack_forget()
            clinicContactTextBox.pack_forget()
            clinicBottomFrame.pack_forget()
            clinicAddressLabel.pack_forget()
            clinicAddressTextBox.pack_forget()
            doctorSpecializationLabel.pack_forget()
            yearsOfExpLabel.pack_forget()
            doctorTypeDropdown.pack_forget()
            yearsOfExpTextBox.pack_forget()
            doctorBottomFrame.pack_forget()
            doctorClinicNameLabel.pack_forget()
            doctorClinicNameDropdown.pack_forget()

            # Show submit button
            buttonFrame.pack(side='top', fill='x', expand=False, pady=(40, 0),)
            submitButton.pack(side='top', fill='none', expand=False, anchor="w")
            loginTextFrame.pack(side='top', fill='x', expand=False, pady=(0, 40),)
            logInLabel1.pack(side='left', fill='x', expand=False, padx=(190, 3), pady=(10, 40))
            logInLabel2.pack(side='left', fill='x', expand=False, padx=(0, 0), pady=(10, 40))
            return
        
        # Show submit button below the dynamically added input fields
        buttonFrame.pack(side='top', fill='x', expand=False, pady=(0, 0),)
        submitButton.pack(side='top', fill='none', expand=False, anchor="w")
        loginTextFrame.pack(side='top', fill='x', expand=False, pady=(0, 40),)
        logInLabel1.pack(side='left', fill='x', expand=False, padx=(190, 3), pady=(10, 40))
        logInLabel2.pack(side='left', fill='x', expand=False, padx=(0, 0), pady=(10, 40))

    # Validating user's email and password for increased security
    def validateCredentials(email, password):
        if "@" not in email:
            messagebox.showerror('Error', 'Enter a valid email address.')
            return False
        
        if ".com" not in email:
            messagebox.showerror('Error', 'Enter a valid email address.')
            return False 
        
        if len(password) <= 8:
            messagebox.showerror('Error', 'Password must be more than 8 characters')
            return False
        
        if not re.search(r'[A-Z]', password): # Ensures there is at least one uppercase letter.
            messagebox.showerror('Error', 'Password must contain at least 1 uppercase letter.')
            return False
        
        if not re.search(r'\d', password): # Check if password contains at least one digit
            messagebox.showerror('Error', 'Password must contain at least 1 number.')
            return False
        
        if not re.search(r'[\W_]', password):  # \W matches any non-word character, _ is included to catch underscore as a symbol
            messagebox.showerror('Error', 'Password must contain at least 1 symbol.')
            return False
        
        return True

    # Handling Patient Sign Up process (Validations) 
    def patientSignUp():
        firstName = firstNameTextBox.get(0.0, 'end').strip()
        # print(firstName)
        lastName = lastNameTextBox.get(0.0, 'end').strip()
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()
        nric = nricTextBox.get(0.0, 'end').strip()
        address = addressTextBox.get(0.0, 'end').strip()

        
        if (firstName != '' and lastName != '' and email != '' and password != '' and nric != '' and 
            role != '' and address != ''):

            if validateCredentials(email, password) is False:
                return

            patientCursor.execute('SELECT Email FROM patients WHERE Email=?', [email])
            if patientCursor.fetchone() is not None:
                messagebox.showerror('Error', 'Email already exist')
            else:
                encodedPassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
                print(hashedPassword)
                patientCursor.execute(
                    'INSERT INTO patients (FirstName, LastName, Email, Password, NRIC, Role, Address, NumberOfAppointments) VALUES (?,?,?,?,?,?,?,?)', 
                    [firstName, lastName, email, hashedPassword, nric, role, address, 0])
                patientConn.commit()
                messagebox.showinfo('Success', 'Patient Account has been created successfully. \nYou can now log in with your account.')
                redirectToLoginWindow()
        
        else:
            messagebox.showerror('Error',"Please fill up all the fields.")

    # Handling Doctor Sign Up process (Validations) 
    def doctorSignUp():
        firstName = firstNameTextBox.get(0.0, 'end').strip()
        lastName = lastNameTextBox.get(0.0, 'end').strip()
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()
        nric = nricTextBox.get(0.0, 'end').strip()
        clinicName = doctorClinicNameDropdown.get()
        doctorSpecialization = doctorTypeDropdown.get()
        yearsOfExp = yearsOfExpTextBox.get(0.0, 'end').strip()

        
        if (firstName != '' and lastName != '' and email != '' and password != '' and nric != '' and 
            role != '' and clinicName != '' and doctorSpecialization != '' and yearsOfExp != '' ):

            if validateCredentials(email, password) is False:
                return
            
            if doctorSpecialization == 'Select Type':
                messagebox.showerror('Error', 'Please select your Specialization.')
                return
        
            doctorCursor.execute('SELECT Email FROM doctors WHERE Email=?', [email])
            if doctorCursor.fetchone() is not None:
                messagebox.showerror('Error', 'Email already exist')
            else:
                encodedPassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
                print(hashedPassword)
                doctorCursor.execute(
                    'INSERT INTO doctors (FirstName, LastName, Email, Password, NRIC, Role, ClinicName, Specialization, YearsOfExperience, IsApproved) VALUES (?,?,?,?,?,?,?,?,?,?)', 
                    [firstName, lastName, email, hashedPassword, nric, role, clinicName, doctorSpecialization, yearsOfExp, 0]
                )
                doctorConn.commit()
                messagebox.showinfo('Success', "Doctor Account has been created successfully. \nWaiting for your Clinic Admin's approval. \nYou can login after their approval.")
        else:
            messagebox.showerror('Error',"Please fill up all the fields.")

    # Handling Clinic Admin Sign Up process (Validations) 
    def clinicAdminSignUp():
        firstName = firstNameTextBox.get(0.0, 'end').strip()
        lastName = lastNameTextBox.get(0.0, 'end').strip()
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        nric = nricTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()
        clinicName = clinicNameTextBox.get(0.0, 'end').strip()
        clinicAddress = clinicAddressTextBox.get(0.0, 'end').strip()
        clinicContact = clinicContactTextBox.get(0.0, 'end').strip()

        
        if (firstName != '' and lastName != '' and email != '' and password != '' and nric != '' and 
            role != '' and clinicName != '' and clinicAddress != '' and clinicContact != '' ):

            if validateCredentials(email, password) is False:
                return
        

            clinicAdminCursor.execute('SELECT Email FROM clinicAdmins WHERE Email=?', [email])
            if clinicAdminCursor.fetchone() is not None:
                messagebox.showerror('Error', 'Email already exist')
            else:
                encodedPassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
                print(hashedPassword)
                clinicAdminCursor.execute(
                    'INSERT INTO clinicAdmins (FirstName, LastName, Email, Password, NRIC, Role, ClinicName, ClinicAddress, ClinicNumber, IsApproved) VALUES (?,?,?,?,?,?,?,?,?,?)', 
                    [firstName, lastName, email, hashedPassword, nric, role, clinicName, clinicAddress, clinicContact, 0]
                )
                clinicAdminConn.commit()
                messagebox.showinfo('Success', "Clinic Admin Account has been created successfully. \nWaiting for CAD Admin's approval. \nYou can login after their approval.")
        
        else:
            messagebox.showerror('Error',"Please fill up all the fields.")


    # Handling Admin Sign Up process (Validations) 
    def adminSignUp():
        firstName = firstNameTextBox.get(0.0, 'end').strip()
        lastName = lastNameTextBox.get(0.0, 'end').strip()
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()
        nric = nricTextBox.get(0.0, 'end').strip()
        adminSecretKey = adminSecretKeyTextBox.get(0.0, 'end').strip()

        
        if (firstName != '' and lastName != '' and email != '' and password != '' and nric != '' and 
            role != '' and adminSecretKey != ''):

            if validateCredentials(email, password) is False:
                return
            
            if adminSecretKey != 'a1b2c3Z9Y8X7a1b2c3Z9Y8X7a1b2c3Z9Y8X7':
                messagebox.showerror('Error', 'Invalid Secret Key. Please try again.\nContact IT Department if issue persists.')
                return 

            adminCursor.execute('SELECT Email FROM admins WHERE Email=?', [email])
            if adminCursor.fetchone() is not None:
                messagebox.showerror('Error', 'Email already exist')
            else:
                encodedPassword = password.encode('utf-8')
                hashedPassword = bcrypt.hashpw(encodedPassword, bcrypt.gensalt())
                print(hashedPassword)
                adminCursor.execute(
                    'INSERT INTO admins (FirstName, LastName, Email, Password, NRIC, Role, AdminSecretKey) VALUES (?,?,?,?,?,?,?)', 
                    [firstName, lastName, email, hashedPassword, nric, role, adminSecretKey])
                adminConn.commit()
                messagebox.showinfo('Success', 'Admin Account has been created successfully. \nYou can now log in with your account.')
                redirectToLoginWindow()
        
        else:
            messagebox.showerror('Error',"Please fill up all the fields.")
            

    # Function will run after user clicks on Submit button
    def handleSignUp():
        role = roleDropdown.get()

        if role == 'Patient':
            patientSignUp()

        elif role == 'Doctor':
            doctorSignUp()

        elif role == 'Clinic Admin':
            clinicAdminSignUp()

        elif role == 'CAD Admin':
            adminSignUp()

        else:
            messagebox.showerror('Error',"Please select who you want to sign in as.")



    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Sign In Window)")
    window.configure(fg_color = "#CFEBFF")
    window.geometry("1350x800+115+5")
    window.update_idletasks()
    window.resizable(False, False)
    window.focus_set()
    window.lift()
    

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT IMAGE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    leftImgFrame = ctk.CTkFrame(window, width=652, height=800, fg_color="transparent",)
    leftImgFrame.place(x=0, y=0)

    # Left Background image
    leftBgImgPath = relative_to_assets("image_1.png")
    leftBgImg = ctk.CTkImage(light_image=Image.open(leftBgImgPath), size=(652,800))
    leftBgImgLabel = ctk.CTkLabel(leftImgFrame, image=leftBgImg, text_color='#000',text='', anchor=ctk.W,)
    leftBgImgLabel.place(x=0, y=0)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< WHITE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    whiteImgFrame = ctk.CTkFrame(window, width=761, height=800, fg_color="transparent",)
    whiteImgFrame.place(x=589, y=0)

    # White Background image
    whiteBgImgPath = relative_to_assets("image_2.png")
    whiteBgImg = ctk.CTkImage(light_image=Image.open(whiteBgImgPath), size=(761,800))
    whiteBgImgLabel = ctk.CTkLabel(whiteImgFrame, image=whiteBgImg, text_color='#000',text='', anchor=ctk.W,)
    whiteBgImgLabel.place(x=0, y=0)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SCROLLABLE FRAME INSIDE WHITE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    scrollable_frame = ctk.CTkScrollableFrame(whiteImgFrame, width=683, height=850, fg_color="#FFFDFD", scrollbar_fg_color="#000", scrollbar_button_color="#000", scrollbar_button_hover_color="#1AFF75")
    scrollable_frame.place(x=56, y=0)

    # Label for Create Account
    createAccountLabel = ctk.CTkLabel(scrollable_frame, text="Create Account", font=("Inter", 48, "bold", "underline"), text_color="#000000")
    createAccountLabel.pack(side='top', fill='both', expand=False, pady=(50,45))

    # <<<<<<<<<<<<<<<<<<<<<<<<<< PARENT FRAME INSIDE SCROLLABLE FRAME STORES LEFT & RIGHT FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    parentFrame = ctk.CTkFrame(scrollable_frame, width=620, height=500, fg_color="#FFFDFD", )
    parentFrame.pack(side='top', fill='x', expand=False, )

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT FRAME INSIDE SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", )
    leftFrame.pack(side='left', fill='both', expand=False,)

    # First name field
    firstNameLabel = ctk.CTkLabel(leftFrame, text="First Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    firstNameLabel.pack(side='top', fill='x', expand=False)
    firstNameTextBox = ctk.CTkTextbox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    firstNameTextBox.pack(side='top', fill='x', expand=False,)

    # Email field
    emailLabel = ctk.CTkLabel(leftFrame, text="Email", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    emailLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
    emailTextBox = ctk.CTkTextbox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    emailTextBox.pack(side='top', fill='x', expand=False,)

    # NRIC field
    nricLabel = ctk.CTkLabel(leftFrame, text="NRIC", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    nricLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
    nricTextBox = ctk.CTkTextbox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    nricTextBox.pack(side='top', fill='x', expand=False,)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< RIGHT FRAME INSIDE SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    rightFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD",)
    rightFrame.pack(side='left', fill='both', expand=False, padx=(30,0))

    # Last name field
    lastNameLabel = ctk.CTkLabel(rightFrame, text="Last Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    lastNameLabel.pack(side='top', fill='x', expand=False)
    lastNameTextBox = ctk.CTkTextbox(
        rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    lastNameTextBox.pack(side='top', fill='x', expand=False,)

    # Password field
    passwordLabel = ctk.CTkLabel(rightFrame, text="Password", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    passwordLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
    passwordTextBox = ctk.CTkTextbox(
        rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    passwordTextBox.pack(side='top', fill='x', expand=False,)


    # Role dropdown field
    roleLabel = ctk.CTkLabel(rightFrame, text="Sign In As", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    roleLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
    roleDropdown = ctk.CTkComboBox(
        rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Role', 'Patient', 'Doctor', 'Clinic Admin', 'CAD Admin'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        command=displayBasedOnRole
    )
    roleDropdown.pack(side='top', fill='x', expand=False,)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Clinic-specific fields for Clinic Admin role >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    clinicNameLabel = ctk.CTkLabel(leftFrame, text="Clinic Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    clinicNameTextBox = ctk.CTkTextbox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )

    clinicContactLabel = ctk.CTkLabel(rightFrame, text="Clinic Contact Number", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    clinicContactTextBox = ctk.CTkTextbox(
        rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )


    clinicBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)

    clinicAddressLabel = ctk.CTkLabel(clinicBottomFrame, text="Clinic Address", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    clinicAddressTextBox = ctk.CTkTextbox(
        clinicBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=88, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Patient-specific fields for Patient role >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    patientBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)
    addressLabel = ctk.CTkLabel(patientBottomFrame, text="Address", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    addressTextBox = ctk.CTkTextbox(
        patientBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=88, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Admin-specific fields for Admin role >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    adminBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)
    adminSecretKeyLabel = ctk.CTkLabel(adminBottomFrame, text="Admin Secret Key", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    adminSecretKeyTextBox = ctk.CTkTextbox(
        adminBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Doctor-specific fields for Doctor role >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    doctorSpecializationLabel = ctk.CTkLabel(rightFrame, text="Specialization", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    doctorTypes = [
        "Select Type","Allergist", "Cardiologist", "Dermatologist", "Endocrinologist", 
        "Gastroenterologist", "Geriatrician", "Internist", "Nephrologist", "Neurologist", 
        "Obstetrician/Gynecologist", "Oncologist", "Ophthalmologist", "Orthopedic Surgeon", 
        "Pediatrician", "Podiatrist", "Psychiatrist", "Pulmonologist", "Rheumatologist", 
        "General Practitioner", "Family Medicine Doctor", "Home Health Care Doctor", 
        "Emergency Medicine Specialist"]
    doctorTypeDropdown = ctk.CTkComboBox(
        rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=doctorTypes, border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )

    yearsOfExpLabel = ctk.CTkLabel(leftFrame, text="Years Of Experience", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    yearsOfExpTextBox = ctk.CTkTextbox(
        leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )


    doctorBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)


    doctorClinicNameLabel = ctk.CTkLabel(doctorBottomFrame, text="Clinic Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    doctorClinicNameDropdown = ctk.CTkComboBox(
        doctorBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Clinic Panmedic', 'Clinic Sungai Nibong', 'Clinic Medicare', 'Clinic HealthSync'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Submit Button >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    buttonFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)
    submitButton = ctk.CTkButton(
        buttonFrame, text="Submit", width=620, height=64, 
        font=("Inter", 24, "bold",), fg_color="#000", hover_color="#1BCC62", 
        command=handleSignUp
    )

    buttonFrame.pack(side='top', fill='x', expand=False, pady=(40, 0),)
    submitButton.pack(side='top', fill='none', expand=False, anchor="w")

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Redirection Button >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    loginTextFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)
    logInLabel1 = ctk.CTkLabel(loginTextFrame, text="Already Have An Account?", font=("Inter", 15, "bold") , text_color="#000000",)
    logInLabel2 = ctk.CTkButton(
        loginTextFrame, text="Login", font=("Inter", 16, "bold") , 
        text_color="#1AFF75", command=redirectToLoginWindow, width=0,
        fg_color='transparent', hover=False)
    loginTextFrame.pack(side='top', fill='x', expand=False, pady=(0, 40),)
    logInLabel1.pack(side='left', fill='x', expand=False, padx=(190, 3), pady=(10, 40))
    logInLabel2.pack(side='left', fill='x', expand=False, padx=(0, 0), pady=(10, 40))


    window.mainloop()



# Only execute the Sign In Window if this script is run directly
if __name__ == "__main__":
    signInWindow()
    


