from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
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
    bg = "#000000",
    height = 800,
    width = 1350,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
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


canvas.create_text(
    670.0,
    53.0,
    anchor="nw",
    text="Create Account",
    fill="#000000",
    font=("Inter", 48 * -1, "bold", "underline")
)

# formsFrame = ctk.CTkFrame(window, width=680, height=646, fg_color='transparent')
# formsFrame.place(
#     x=639.0,
#     y=135.0
# )

# label = ctk.CTkLabel(formsFrame, text="First Name", font=("Inter", 16, "bold"), text_color="#000000")
# label.pack(fill='both', expand=True)
# label = ctk.CTkLabel(formsFrame, text="Last Name", font=("Inter", 16, "bold"), text_color="#000000")
# label.pack(fill='both', expand=True)

canvas.create_text(
    670.0,
    154.0,
    anchor="nw",
    text="First Name",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

firstNameTextBox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
firstNameTextBox.place(
    x=670.0,
    y=186.0
)

canvas.create_text(
    994.0,
    154.0,
    anchor="nw",
    text="Last Name",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

lastNameTextBox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
lastNameTextBox.place(
    x=994.0,
    y=186.0
)

canvas.create_text(
    670.0,
    260.0,
    anchor="nw",
    text="Address",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

addressTextBox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=619, height=88, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
addressTextBox.place(
    x=670.0,
    y=292.0
)

canvas.create_text(
    670.0,
    406.0,
    anchor="nw",
    text="Email",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

emailTextBox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=619, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
emailTextBox.place(
    x=670.0,
    y=438.0
)

canvas.create_text(
    670.0,
    512.0,
    anchor="nw",
    text="Password",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

passwordTextBox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
passwordTextBox.place(
    x=670.0,
    y=544.0
)

canvas.create_text(
    994.0,
    512.0,
    anchor="nw",
    text="Sign In As",
    fill="#000000",
    font=("Inter", 16 * -1, "bold")
)

roleTextBox = ctk.CTkTextbox(
    window, fg_color="#ffffff", text_color="#000000", width=299, height=48, 
    border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
    scrollbar_button_color="#1AFF75", border_width=1
)
roleTextBox.place(
    x=994.0,
    y=544.0
)

roleTextBox = ctk.CTkOptionMenu(
    window, fg_color="#ffffff", text_color="#000000", width=293, height=46, 
    font=("Inter", 20), button_color='#1AFF75', button_hover_color='#33383F',
    values=['Patient', 'Doctor', 'Clinic Admin'],
    dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
    dropdown_text_color='#000', dropdown_hover_color='#1AFF75'
)
roleTextBox.place(
    x=1000.0,
    y=545.0
)


button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=670.0,
    y=641.0,
    width=619.0,
    height=64.0
)


canvas.create_text(
    865.0,
    718.0,
    anchor="nw",
    text="Already have an account?",
    fill="#000000",
    font=("Inter", 15 * -1, "bold")
)

canvas.create_text(
    1050.0,
    718.0,
    anchor="nw",
    text="Login",
    fill="#1AFF75",
    font=("Inter", 15 * -1, "bold")
)


window.resizable(False, False)
window.mainloop()
