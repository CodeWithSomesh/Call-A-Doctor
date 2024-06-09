import sys
from pathlib import Path
from PIL import Image

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import Tk, Canvas, PhotoImage, Entry, Button
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\logInWindow\assets\frame0")



def loginWindow():
    # Helper function to get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Function to redirect to the Sign In Window
    def redirectToSignInWindow():
        window.destroy()
        from signInWindow.main import signInWindow
        signInWindow()

    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = Tk()
    window.title("CaD - Doctor Appointment Booking System (Login Window)")
    window.configure(bg = "#fff")
    window.geometry("1350x800+115+5")
    window.update_idletasks()
    window.resizable(False, False)
    window.focus_set()
    window.lift()

    # Create canvas for background and layout
    canvas = Canvas(
        window,
        bg = "#fff",
        height = 800,
        width = 1350,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    canvas.place(x = 0, y = 0)

    # Background image
    bgImagePath = PhotoImage(
        file=relative_to_assets("image_1.png"))
    bgImage = canvas.create_image(
        401.0,
        400.0,
        image=bgImagePath
    )

    # Logo image
    logoImagePath = PhotoImage(
        file=relative_to_assets("image_3.png"))
    logoImage = canvas.create_image(
        380.0,
        368.0,
        image=logoImagePath
    )

    # <<<<<<<<<<<<<<<<<<<< FORM FRAME >>>>>>>>>>>>>>>>>>>>>
    formFrame = ctk.CTkFrame(window, width=653, height=800, fg_color="#FFFDFD", border_color="#000", )
    formFrame.place(x=719, y=0)

    # Label with Marketing Text 
    headerLabel1 = ctk.CTkLabel(window, text="Your Health, Our Priority", font=("Inter", 32, "bold",), text_color="#000000")
    headerLabel1.place(x=858, y=163)
    headerLabel2 = ctk.CTkLabel(window, text="– Book Appointments in Seconds", font=("Inter", 32, "bold",), text_color="#000000")
    headerLabel2.place(x=778, y=203)

    # Email field 
    emailLabel = ctk.CTkLabel(window, text="Email", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    emailLabel.place(x=761.06, y=290.0,)
    emailTextBox = ctk.CTkTextbox(
        window, fg_color="#ffffff", text_color="#000000", width=548, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    emailTextBox.place(x=761.060302734375, y=322.0)

    # Password field 
    passwordLabel = ctk.CTkLabel(window, text="Password", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    passwordLabel.place(x=761.06, y=396.0,)
    passwordTextBox = ctk.CTkTextbox(
        window, fg_color="#ffffff", text_color="#000000", width=261, height=48, 
        border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        scrollbar_button_color="#1AFF75", border_width=1
    )
    passwordTextBox.place(x=761.06, y=428.0)

    # Role Dropdown Menu  
    roleLabel = ctk.CTkLabel(window, text="Sign In As", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
    roleLabel.place(x=1048.06, y=396,)
    roleDropdown = ctk.CTkComboBox(
        window, fg_color="#ffffff", text_color="#000000", width=261, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Role', 'Patient', 'Doctor', 'Clinic Admin'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    roleDropdown.place(x=1048, y=428,)

    # Submit Button
    submitButton = ctk.CTkButton(
        window, text="Submit", width=548, height=64, 
        font=("Inter", 24, "bold",), fg_color="#000", hover_color="#1BCC62", 
        command=redirectToSignInWindow
    )
    submitButton.place(x=761, y=525)

    # Redirection Button
    logInLabel1 = ctk.CTkLabel(window, text="Don't Have An Account?", font=("Inter", 15, "bold") , text_color="#000000",)
    logInLabel1.place(x=910, y=597)
    logInLabel2 = ctk.CTkButton(
        window, text="Sign In", font=("Inter", 16, "bold") , 
        text_color="#1AFF75", command=redirectToSignInWindow, width=0,
        fg_color='transparent', hover=False)
    logInLabel2.place(x=1080, y=598)

    # 3D Image
    extraImagePath = relative_to_assets("image_2.png")
    extraImage = ctk.CTkImage(light_image=Image.open(extraImagePath), size=(191,206))
    extraImageLabel = ctk.CTkLabel(window, image=extraImage,)
    extraImageLabel.place(x=1160, y=593)
    

    window.mainloop()

# Only execute the login window if this script is run directly
if __name__ == "__main__":
    loginWindow()

