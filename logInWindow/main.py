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



OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\logInWindow\assets\frame0")



def logInWindow():

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CONNECTING TO SQLITE3 DATABASE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Connecting to Patient DB
    patientConn = sqlite3.connect('patients.db')
    patientCursor = patientConn.cursor()
    

    # Connecting to Doctor DB
    doctorConn = sqlite3.connect('doctors.db')
    doctorCursor = doctorConn.cursor()
   

    # Connecting to Clinic Admin DB
    clinicAdminConn = sqlite3.connect('clinicAdmins.db')
    clinicAdminCursor = clinicAdminConn.cursor()
    

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ALL FUNCTIONS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)

    # Redirect to the Sign In Window
    def redirectToSignInWindow():
        window.destroy()
        from signInWindow.main import signInWindow
        signInWindow()


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
    

    def patientLogin():
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()

        if (email != '' and password != '' and role != ''):

            if validateCredentials(email, password) is False:
                return
            
            patientCursor.execute('SELECT Password FROM patients WHERE Email=?', [email])
            result = patientCursor.fetchone()

            if result:
                if bcrypt.checkpw(password.encode('utf-8'), result[0]): # Check whether the user entered password matched the password in DB
                    messagebox.showinfo('Success', 'Logged in successfully as Patient.')
                    return True
                else:
                    messagebox.showerror('Error', 'Password does not match. Please try again.')
                    return False
            else:
                messagebox.showerror('Error', 'Email entered is not registered. Please try again.')
                return False

        else:
            messagebox.showerror('Error',"Please fill up all the fields.")
            return False


    def doctorLogin():
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()

        if (email != '' and password != '' and role != ''):

            if validateCredentials(email, password) is False:
                return
            
            doctorCursor.execute('SELECT Password FROM doctors WHERE Email=?', [email])
            result = doctorCursor.fetchone()

            if result:
                if bcrypt.checkpw(password.encode('utf-8'), result[0]): # Check whether the user entered password matched the password in DB
                    messagebox.showinfo('Success', 'Logged in successfully as Doctor.')
                    return True
                else:
                    messagebox.showerror('Error', 'Password does not match. Please try again.')
                    return False
            else:
                messagebox.showerror('Error', 'Email entered is not registered. Please try again.')
                return False

        else:
            messagebox.showerror('Error',"Please fill up all the fields.")
            return False


    def clinicAdminLogin():
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()

        if (email != '' and password != '' and role != ''):

            if validateCredentials(email, password) is False:
                return
            
            clinicAdminCursor.execute('SELECT Password FROM clinicAdmins WHERE Email=?', [email])
            result = clinicAdminCursor.fetchone()

            if result:
                if bcrypt.checkpw(password.encode('utf-8'), result[0]): # Check whether the user entered password matched the password in DB
                    messagebox.showinfo('Success', 'Logged in successfully as Clinic Admin.')
                    return True
                else:
                    messagebox.showerror('Error', 'Password does not match. Please try again.')
                    return False
            else:
                messagebox.showerror('Error', 'Email entered is not registered. Please try again.')
                return False

        else:
            messagebox.showerror('Error',"Please fill up all the fields.")
            return False


    def redirectBasedOnRole():
        email = emailTextBox.get(0.0, 'end').strip()
        password = passwordTextBox.get(0.0, 'end').strip()
        role = roleDropdown.get()
        print(role)

        if (email != '' and password != '' and role != ''):

            if role == 'Admin':
                if patientLogin():
                    window.destroy()
                    from admin.adminDashboard import adminDashboardWindow
                    adminDashboardWindow()
            elif role == 'Doctor':
                if doctorLogin():
                    window.destroy()
                    from doctor.doctorDashboard import doctorDashboardWindow
                    doctorDashboardWindow()
            elif role == 'Patient':
                if patientLogin():
                    window.destroy()
                    from patient.patientDashboard import patientDashboardWindow
                    patientDashboardWindow()
            elif role == 'Clinic Admin':
                if clinicAdminLogin():
                    window.destroy()
                    from clinicAdmin.clinicAdminDashboard import clinicAdminDashboardWindow
                    clinicAdminDashboardWindow()
            else:
                messagebox.showerror('Error',"Please select who you want to log in as.")

        else:
            messagebox.showerror('Error',"Please fill up all the fields.")


    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Login Window)")
    window.configure(fg_color = "#fff")
    window.geometry("1350x800+115+5")
    window.update_idletasks()
    window.resizable(False, False)
    window.focus_set()
    window.lift()

    # <<<<<<<<<<<<<<<<<<<< LOGO IMAGE FRAME >>>>>>>>>>>>>>>>>>>>>
    logoImgFrame = ctk.CTkFrame(window, width=802, height=800, fg_color="transparent",)
    logoImgFrame.place(x=0, y=0)

    # Logo Background image
    logoBgImgPath = relative_to_assets("bgImg.png")
    logoBgImg = ctk.CTkImage(light_image=Image.open(logoBgImgPath), size=(802,800))
    logoBgImgLabel = ctk.CTkLabel(logoImgFrame, image=logoBgImg, text_color='#000',text='', anchor=ctk.W,)
    logoBgImgLabel.place(x=0, y=0)


    # <<<<<<<<<<<<<<<<<<<< FORM FRAME >>>>>>>>>>>>>>>>>>>>>
    formFrame = ctk.CTkFrame(window, width=683, height=800, fg_color="#fff", border_color="#000", corner_radius=60 )
    formFrame.place(x=719, y=0)

    # White Cornered Background image
    # whiteBgImgPath = relative_to_assets("white-frame.png")
    # whiteBgImg = ctk.CTkImage(light_image=Image.open(whiteBgImgPath), size=(631,800))
    # whiteBgImgLabel = ctk.CTkLabel(window, image=whiteBgImg, text_color='#000',text='', anchor=ctk.W,)
    # whiteBgImgLabel.place(x=719, y=0)

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
        values=['Role', 'Patient', 'Doctor', 'Clinic Admin', 'Admin'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    roleDropdown.place(x=1048, y=428,)

    # Submit Button
    submitButton = ctk.CTkButton(
        window, text="Submit", width=548, height=64, 
        font=("Inter", 24, "bold",), fg_color="#000", hover_color="#1BCC62", 
        command=redirectBasedOnRole
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
    extraImagePath = relative_to_assets("3d-doctor.png")
    extraImage = ctk.CTkImage(light_image=Image.open(extraImagePath), size=(191,206))
    extraImageLabel = ctk.CTkLabel(window, image=extraImage,)
    extraImageLabel.place(x=1160, y=593)
    

    window.mainloop()

# Only execute the Login Window if this script is run directly
if __name__ == "__main__":
    logInWindow()

