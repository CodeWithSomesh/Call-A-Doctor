import sys
from pathlib import Path

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import Tk, Canvas, PhotoImage
import customtkinter as ctk
#from logInWindow.main import open_login_window


# Paths to assets and output directories
OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\signInWindow\assets\frame0")

# Helper function to get the full path of assets
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Function to redirect to the login window
def redirect_to_login():
    window.destroy()
    open_login_window()

# Function to update the display based on selected role
def displayBasedOnRole(role):
    print(role)
    buttonFrame.pack_forget()
    submitButton.pack_forget()

    if role == 'Clinic Admin':
        # Hide patient and doctor specific fields
        patientBottomFrame.pack_forget()
        doctorSpecializationLabel.pack_forget()
        yearsOfExpLabel.pack_forget()
        doctorSpecializationTextBox.pack_forget()
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
        clinicNameLabel.pack_forget()
        clinicNameTextBox.pack_forget()
        clinicContactLabel.pack_forget()
        clinicContactTextBox.pack_forget()
        clinicBottomFrame.pack_forget()
        clinicAddressLabel.pack_forget()
        clinicAddressTextBox.pack_forget()
        doctorSpecializationLabel.pack_forget()
        yearsOfExpLabel.pack_forget()
        doctorSpecializationTextBox.pack_forget()
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

        # Show doctor specific fields
        doctorSpecializationLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
        yearsOfExpLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
        doctorSpecializationTextBox.pack(side='top', fill='x', expand=False,)
        yearsOfExpTextBox.pack(side='top', fill='x', expand=False,)
        doctorBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0))
        doctorClinicNameLabel.pack(side='top', fill='x', expand=False, )
        doctorClinicNameDropdown.pack(side='top', fill='none', expand=False, pady=(0, 40), anchor="w")

    else:
        # Hide all fields and reset to initial state
        clinicNameLabel.pack_forget()
        clinicNameTextBox.pack_forget()
        clinicContactLabel.pack_forget()
        clinicContactTextBox.pack_forget()
        clinicBottomFrame.pack_forget()
        clinicAddressLabel.pack_forget()
        clinicAddressTextBox.pack_forget()
        patientBottomFrame.pack_forget()
        doctorSpecializationLabel.pack_forget()
        yearsOfExpLabel.pack_forget()
        doctorSpecializationTextBox.pack_forget()
        yearsOfExpTextBox.pack_forget()
        doctorBottomFrame.pack_forget()
        doctorClinicNameLabel.pack_forget()
        doctorClinicNameDropdown.pack_forget()

        # Show submit button
        buttonFrame.pack(side='top', fill='x', expand=False, pady=(40, 40),)
        submitButton.pack(side='top', fill='none', expand=False, anchor="w")
        return
    
    # Show submit button below the dynamically added input fields
    buttonFrame.pack(side='top', fill='x', expand=False, pady=(0, 100),)
    submitButton.pack(side='top', fill='none', expand=False, anchor="w")

# Create main window
window = Tk()
window.title("CaD - Doctor Appointment Booking System (Login Window)")
window.geometry("1350x800")
window.configure(bg = "#ffffff")

# Create canvas for background and layout
canvas = Canvas(
    window,
    bg = "#fff",
    height = 800,
    width = 1350,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge", 
)
canvas.place(x = 0, y = 0)

# Background image
bgImagePath = PhotoImage(
    file=relative_to_assets("image_1.png"))
bgImage = canvas.create_image(
    326.0,
    401.0,
    image=bgImagePath
)

# White background for form
whiteBgPath = PhotoImage(
    file=relative_to_assets("image_2.png"))
whiteBg = canvas.create_image(
    969.0,
    400.0,
    image=whiteBgPath
)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
scrollable_frame = ctk.CTkScrollableFrame(window, width=683, height=850, fg_color="#FFFDFD", scrollbar_fg_color="#000", scrollbar_button_color="#000", )
scrollable_frame.place(x=645, y=0)

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
    values=['Role', 'Patient', 'Doctor', 'Clinic Admin'], border_color="#b5b3b3", border_width=1,
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


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Patient-specific fields for Clinic Admin role >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
patientBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)
addressLabel = ctk.CTkLabel(patientBottomFrame, text="Address", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
addressTextBox = ctk.CTkTextbox(
    patientBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=88, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Doctor-specific fields for Clinic Admin role >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
doctorSpecializationLabel = ctk.CTkLabel(rightFrame, text="Specialization", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
doctorSpecializationTextBox = ctk.CTkTextbox(
    rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)

yearsOfExpLabel = ctk.CTkLabel(leftFrame, text="Year Of Experience", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
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
    command=redirect_to_login
)

buttonFrame.pack(side='top', fill='x', expand=False, pady=(40, 0),)
submitButton.pack(side='top', fill='none', expand=False, anchor="w")

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< Redirection Button >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
loginTextFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD",)
logInLabel1 = ctk.CTkLabel(loginTextFrame, text="Already Have An Account?", font=("Inter", 15, "bold") , text_color="#000000",)
logInLabel2 = ctk.CTkButton(
    loginTextFrame, text="Login", font=("Inter", 16, "bold") , 
    text_color="#1AFF75", command=redirect_to_login, width=0,
    fg_color='transparent', hover=False)
loginTextFrame.pack(side='top', fill='x', expand=False, pady=(0, 40),)
logInLabel1.pack(side='left', fill='x', expand=False, padx=(190, 3), pady=(10, 40))
logInLabel2.pack(side='left', fill='x', expand=False, padx=(0, 0), pady=(10, 40))




window.resizable(False, False)
window.mainloop()
