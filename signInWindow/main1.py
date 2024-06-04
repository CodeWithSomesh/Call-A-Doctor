from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, Scrollbar, LEFT
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\signInWindow\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

# Must be TK, giving issues if its CTK while in laptop screen
window = Tk()
window.title("CaD - Doctor Appointment Booking System (Login Window)")
window.geometry("1350x800")
window.configure(bg = "#ffffff")


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


bgImagePath = PhotoImage(
    file=relative_to_assets("image_1.png"))
bgImage = canvas.create_image(
    326.0,
    401.0,
    image=bgImagePath
)

whiteBgPath = PhotoImage(
    file=relative_to_assets("image_2.png"))
whiteBg = canvas.create_image(
    969.0,
    400.0,
    image=whiteBgPath
)


# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
scrollable_frame = ctk.CTkScrollableFrame(window, width=683, height=850, fg_color="#FFFDFD", scrollbar_fg_color="#000", scrollbar_button_color="#000", border_width=2)
scrollable_frame.place(x=645, y=0)

createAccountLabel = ctk.CTkLabel(scrollable_frame, text="Create Account", font=("Inter", 48, "bold", "underline"), text_color="#000000")
createAccountLabel.pack(side='top', fill='both', expand=False, pady=(50,25))

# <<<<<<<<<<<<<<<<<<<<<<<<<< PARENT FRAME INSIDE SCROLLABLE FRAME STORES LEFT & RIGHT FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
parentFrame = ctk.CTkFrame(scrollable_frame, width=620, height=500, fg_color="#FFFDFD", border_width=2, border_color="blue")
parentFrame.pack(side='top', fill='x', expand=False, )

# <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT FRAME INSIDE SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", border_width=2)
leftFrame.pack(side='left', fill='both', expand=False,)


firstNameLabel = ctk.CTkLabel(leftFrame, text="First Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
firstNameLabel.pack(side='top', fill='x', expand=False)
firstNameTextBox = ctk.CTkTextbox(
    leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
firstNameTextBox.pack(side='top', fill='x', expand=False,)


emailLabel = ctk.CTkLabel(leftFrame, text="Email", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
emailLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
emailTextBox = ctk.CTkTextbox(
    leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
emailTextBox.pack(side='top', fill='x', expand=False,)


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

lastNameLabel = ctk.CTkLabel(rightFrame, text="Last Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
lastNameLabel.pack(side='top', fill='x', expand=False)
lastNameTextBox = ctk.CTkTextbox(
    rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
lastNameTextBox.pack(side='top', fill='x', expand=False,)


passwordLabel = ctk.CTkLabel(rightFrame, text="Password", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
passwordLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
passwordTextBox = ctk.CTkTextbox(
    rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
passwordTextBox.pack(side='top', fill='x', expand=False,)



def displayBasedOnRole(role):
    print(role)

    if role == 'Clinic Admin':
        patientBottomFrame.pack_forget()

        clinicNameLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
        clinicContactLabel.pack(side='top', fill='x', expand=False, pady=(30, 0))
        clinicNameTextBox.pack(side='top', fill='x', expand=False,)
        clinicContactTextBox.pack(side='top', fill='x', expand=False,)
        clinicBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0))
        clinicAddressLabel.pack(side='top', fill='x', expand=False, )
        clinicAddressTextBox.pack(side='top', fill='none', expand=False, pady=(0, 30), anchor="w")


    elif role == 'Patient':
        clinicNameLabel.pack_forget()
        clinicNameTextBox.pack_forget()
        clinicContactLabel.pack_forget()
        clinicContactTextBox.pack_forget()
        clinicBottomFrame.pack_forget()
        clinicAddressLabel.pack_forget()
        clinicAddressTextBox.pack_forget()

        patientBottomFrame.pack(side='top', fill='x', expand=False, pady=(30, 0),)
        addressLabel.pack(side='top', fill='x', expand=False,)
        addressTextBox.pack(side='top', fill='none', expand=False, pady=(0, 30), anchor="w")
        
    elif role == 'Doctor':
        clinicNameLabel.pack_forget()
        clinicNameTextBox.pack_forget()
        clinicContactLabel.pack_forget()
        clinicContactTextBox.pack_forget()
        clinicBottomFrame.pack_forget()
        clinicAddressLabel.pack_forget()
        clinicAddressTextBox.pack_forget()
        patientBottomFrame.pack_forget()

    else:
        clinicNameLabel.pack_forget()
        clinicNameTextBox.pack_forget()
        clinicContactLabel.pack_forget()
        clinicContactTextBox.pack_forget()
        clinicBottomFrame.pack_forget()
        clinicAddressLabel.pack_forget()
        clinicAddressTextBox.pack_forget()
        patientBottomFrame.pack_forget()



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



clinicBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD", border_color='yellow', border_width=5)



clinicAddressLabel = ctk.CTkLabel(clinicBottomFrame, text="Clinic Address", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
clinicAddressTextBox = ctk.CTkTextbox(
    clinicBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=88, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)


patientBottomFrame = ctk.CTkFrame(scrollable_frame, width=341, height=500, fg_color="#FFFDFD", border_color='yellow', border_width=5)
addressLabel = ctk.CTkLabel(patientBottomFrame, text="Address", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
addressTextBox = ctk.CTkTextbox(
    patientBottomFrame, fg_color="#ffffff", text_color="#000000", width=620, height=88, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)




window.resizable(False, False)
window.mainloop()
