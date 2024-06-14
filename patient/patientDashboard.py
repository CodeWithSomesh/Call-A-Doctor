import sys
from pathlib import Path
from PIL import Image
import sqlite3
from datetime import datetime

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Tk, Scrollbar, VERTICAL, messagebox
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\patient\assets\frame0")

def patientDashboardWindow(email):

    #Connecting to Patient Admin DB
    # patientConn = sqlite3.connect('patients.db')
    # patientCursor = patientConn.cursor()
    # patientCursor.execute('SELECT * FROM patients WHERE Email=?', [email])
    # result = patientCursor.fetchone()
    # username = f"{result[1]} {result[2]}" # Getting user's full name to display on top 


    # Helper function to get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # Function to redirect to the Log In Window
    def redirectToLoginWindow():
        messagebox.showwarning('Warning', 'Are you sure you want to logout?')
        window.destroy()
        from logInWindow.main import logInWindow
        logInWindow()


    # When user is typing remove placeholder
    def searchbarFocus(event):
        print(event)
        searchInputTextBox.delete('0.0', "end")
        searchInputTextBox.configure(text_color='black')
            

    # When user is does not type or left halfway while typing,
    # then replace placeholder
    def searchbarOutFocus(event):
        print(event)
        searchInputTextBox.delete('0.0', "end")
        searchInputTextBox.insert('0.0', "Search Appointments by Date, Clinic Name or Doctor Name")
        searchInputTextBox.configure(text_color='gray')

    
    def bookAppointment():
        toplevel = ctk.CTkToplevel(window)
        toplevel.title("Book Appointment")
        toplevel.geometry("800x600+460+100")
        toplevel.resizable(False, False)
        toplevel.attributes("-topmost",True)
        toplevel.configure(fg_color = "#fff")

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PARENT FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        parentFrame = ctk.CTkScrollableFrame(toplevel, width=800, height=600, fg_color="#fff",)
        parentFrame.place(x=0, y=0)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TOP SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        topFrame = ctk.CTkFrame(parentFrame, width=650, height=500, fg_color="#FFFDFD",)
        topFrame.pack(side='top', fill='x', expand=False, padx=65, pady=(20,0))
        
        # Select Clinic Dropdown Menu
        clinicNameLabel = ctk.CTkLabel(topFrame, text="Select Clinic", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        clinicNameLabel.pack(side='top', fill='x', expand=False)
        clinicNameDropdown = ctk.CTkComboBox(
            topFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=['Clinic Name', 'Panmedic', 'Health Sync', 'Clinic Sungai Ara'], border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        clinicNameDropdown.pack(side='top', fill='x', expand=False,)
        

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TOP SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", )
        leftFrame.pack(side='left', fill='both', expand=False, padx=65, pady=30)

        
        clinicNameLabel = ctk.CTkLabel(leftFrame, text="Select Clinic", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        clinicNameLabel.pack(side='top', fill='x', expand=False)
        clinicNameDropdown = ctk.CTkComboBox(
            leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=['Clinic Name', 'Panmedic', 'Health Sync', 'Clinic Sungai Ara'], border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        clinicNameDropdown.pack(side='top', fill='x', expand=False,)
        # First name field
        # firstNameLabel = ctk.CTkLabel(leftFrame, text="First Name", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        # firstNameLabel.pack(side='top', fill='x', expand=False)
        # firstNameTextBox = ctk.CTkTextbox(
        #     leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
        #     border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
        #     scrollbar_button_color="#1AFF75", border_width=1
        # )
        # firstNameTextBox.pack(side='top', fill='x', expand=False,)

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
        rightFrame.pack(side='left', fill='both', expand=False, padx=(0,0), pady=30)

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
        )
        roleDropdown.pack(side='top', fill='x', expand=False,)


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Patient Window)")
    window.configure(fg_color="black")
    window.geometry("1350x800+115+5")
    window.update_idletasks()
    window.resizable(False, False)
    window.focus_set()
    window.lift()
    

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<< SIDEBAR FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    sidebarFrame = ctk.CTkFrame(window, width=310, height=800, fg_color="#000", border_color="#000", )
    sidebarFrame.place(x=0, y=0)

    # Logo Image
    logoImgPath = relative_to_assets("image_1.png")
    logoImg = ctk.CTkImage(light_image=Image.open(logoImgPath), size=(213,74))
    logoImgLabel = ctk.CTkLabel(sidebarFrame, image=logoImg, text_color='#000',text='', anchor=ctk.W,)
    logoImgLabel.pack(side="top", fill='none', expand=False, padx=(30, 0), pady=25)

    # Dashboard Button with Icon
    dashboardIconPath = relative_to_assets("dashboard-icon.png")
    dashboardIcon = ctk.CTkImage(light_image=Image.open(dashboardIconPath), size=(33,33))
    dashboardButton = ctk.CTkButton(
        sidebarFrame, text=" Dashboard", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#37D8B7", hover_color="#37D8B7", image=dashboardIcon,
        # anchor=ctk.W
    )
    dashboardButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=25)

    # Profile Button with Icon
    profileIconPath = relative_to_assets("profile-icon.png")
    profileIcon = ctk.CTkImage(light_image=Image.open(profileIconPath), size=(33,33),)
    profileButton = ctk.CTkButton(
        sidebarFrame, text=" Profile       ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=profileIcon,
        # anchor=ctk.W
    )
    profileButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=(0, 25))

    # Line that seperates Logout Button from others 
    lineFrame = ctk.CTkFrame(window, width=310, height=2, fg_color="#37D8B7" )
    lineFrame.place(x=0, y=686)

    # Logout Button with Icon
    logoutIconPath = relative_to_assets("logout-icon.png")
    logoutIcon = ctk.CTkImage(light_image=Image.open(logoutIconPath), size=(33,33),)
    logoutButton = ctk.CTkButton(
        sidebarFrame, text=" Logout      ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=logoutIcon,
        command=redirectToLoginWindow # anchor=ctk.W 
    )
    logoutButton.pack(side="bottom", fill='y', expand=True, padx=(35, 0), pady=(395, 0))


    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<< WHITE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    whiteFrame = ctk.CTkFrame(window, width=1040, height=800, fg_color="#fff", bg_color='#fff' )
    whiteFrame.place(x=310, y=0)


    # Label with Greeting Message & User's Full Name 

    now = datetime.now()  # Get the current date and time
    formatted_date = now.strftime("%B %d, %Y") # Format the date as 'Month Day, Year'
    current_hour = now.hour # Get the current hour
    current_time = now.strftime("%H:%M:%S") # Get the current time

    # Generate greeting message based on the current time
    if current_hour < 12:
        greeting = "Good Morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good Afternoon!"
    else:
        greeting = "Good Evening!" 


    greetingLabel1 = ctk.CTkLabel(whiteFrame, text="Welcome, {username}", font=("Inter", 36, "bold",), text_color="#000000")
    greetingLabel1.place(x=25, y=25)
    greetingLabel2 = ctk.CTkLabel(whiteFrame, text=f"{greeting}  ({formatted_date})", font=("Inter", 22,), text_color="#000000")
    greetingLabel2.place(x=25, y=72)
    roleLabel = ctk.CTkLabel(whiteFrame, text="(Patient)", font=("Inter", 36, "bold",), text_color="#000000")
    roleLabel.place(x=872, y=25)

    # Line that seperates Greeting Message from others
    lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
    lineFrame2.place(x=310, y=115)

    # Book Appointment Header & Description
    h1Label = ctk.CTkLabel(whiteFrame, text="Book Appointments", font=("Inter", 30, "bold", 'underline'), text_color="#000000")
    h1Label.place(x=25, y=135)
    descLabel = ctk.CTkLabel(
            whiteFrame, font=("Inter", 22,), text_color="#000000",
            text="Select available doctors from any clinic and make an appointment with a few clicks ", 
        )
    descLabel.place(x=25, y=182)

    # Select Clinic Dropdown Menu
    clinicDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=360, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Select Clinic', 'Panmedic', 'Health Sync', 'Clinic Sungai Ara'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    clinicDropdown.place(x=25, y=225)

    # Select Doctor Dropdown Menu
    doctorDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=615, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Select Doctor', 'Maisarah Majdi (Cardiologist)', 'Someshwar Rao (Neurosurgeon)', 'Karen Khor Siew Li (Psychologist)'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    doctorDropdown.place(x=400, y=225)

    # Select Consultation Time Dropdown Menu
    consultationTimeDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=360, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Select Consultation Time', '9am', '10am', '11am'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    consultationTimeDropdown.place(x=25, y=290)
    
    # Select Consultation Duration Dropdown Menu
    consultationDurationDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=320, height=48, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Select Consultation Duration', '30 Minutes', '1 hour', '1 hour 30 Minutes'], border_color="#b5b3b3", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    consultationDurationDropdown.place(x=400, y=290)

    # Book Appointment Button with Icon
    appointmentIconPath = relative_to_assets("add-icon.png")
    appointmentIcon = ctk.CTkImage(light_image=Image.open(appointmentIconPath), size=(28,28),)
    bookButton = ctk.CTkButton(
        whiteFrame, text=" Book Appointment", width=280, height=48, 
        font=("Inter", 22, "bold",), fg_color="#17D463", hover_color="#009B2B", image=appointmentIcon,
        command=bookAppointment # anchor=ctk.W 
    )
    bookButton.place(x=735, y=290)

    
    # <<<<<<<<<<<<<<<<<<<< TABLE FRAME STORING TREEVIEW >>>>>>>>>>>>>>>>>>>>> 
    tableFrame = ctk.CTkFrame(whiteFrame, fg_color="transparent",) #width=900
    tableFrame.place(x=25, y=355)

    # Initializing Treeview Scrollbar
    tableScrollbar1 = Scrollbar(tableFrame, orient=VERTICAL)
    # tableScrollbar2 = Scrollbar(tableFrame, orient="horizontal")

    # Treeview that stores User Data
    table = ttk.Treeview(tableFrame, yscrollcommand=tableScrollbar1.set,height=9)
    table.pack(side='left', fill='both')
    table['columns'] = (
        'No', 'Clinic ID', 'Clinic Name', 'Clinic Contact',
        "Clinic Admin", "Admin Email"
    )

    # Placing and Configuring Treeview Scrollbar
    tableScrollbar1.pack(side='left', fill='y')
    tableScrollbar1.config(command=table.yview)
    # tableScrollbar2.pack(side='bottom', fill='x')
    # tableScrollbar2.config(command=table.xview)

    # Styling the Treeview Heading and Rows 
    style = ttk.Style(tableFrame)
    style.theme_use('clam')
    style.configure(
        'Treeview.Heading', font=('Inter', 16, 'bold'), 
        foreground='#fff', background='#000', hover=False,
    )
    style.configure('Treeview', font=('Inter', 16), rowheight=45, fieldbackground="#DAFFF7")
    style.map(
        'Treeview', 
        background=[('selected', '#00BE97',)], 
        font=[('selected', ('Inter', 16, 'bold'))],
    )


    # Treeview Table Headings Details
    table.heading('No', text='No')
    table.heading('Clinic ID', text='Clinic ID',)
    table.heading('Clinic Name', text='Clinic Name')
    table.heading('Clinic Contact', text='Clinic Contact')
    table.heading('Clinic Admin', text='Clinic Admin')
    table.heading('Admin Email', text='Admin Email')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("No", width=43, anchor=ctk.CENTER)
    table.column("Clinic ID", anchor=ctk.CENTER)
    table.column("Clinic Name", width=220, anchor=ctk.CENTER)
    table.column("Clinic Contact", anchor=ctk.CENTER)
    table.column("Clinic Admin", width=250, anchor=ctk.CENTER)
    table.column("Admin Email", width=315, anchor=ctk.CENTER,)

    # Setting alternating colours for the rows in Treeview
    table.tag_configure("oddrow", background="#F2F5F8")
    table.tag_configure("evenrow", background="#B4EFF7")


    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
            whiteFrame, fg_color="#ffffff", text_color="gray", width=620, height=48, 
            border_color="#000", font=("Inter", 21), border_spacing=8,
            scrollbar_button_color="#1AFF75", border_width=2,
        )
    searchInputTextBox.insert('insert', "Search Appointments by Date, Clinic Name or Doctor Name")
    searchInputTextBox.place(x=25, y=726)
    searchInputTextBox.bind("<FocusIn>", searchbarFocus)
    searchInputTextBox.bind("<FocusOut>", searchbarOutFocus)

    # Update Appointment Details Button with Icon
    updateIconPath = relative_to_assets("update-icon.png")
    updateIcon = ctk.CTkImage(light_image=Image.open(updateIconPath), size=(33,33),)
    updateButton = ctk.CTkButton(
        whiteFrame, text=" Update  ", height=48, width=172,
        font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=updateIcon,
        # anchor=ctk.W 
    )
    updateButton.place(x=660, y=726)

    # Delete Appointment Button with Icon
    deleteIconPath = relative_to_assets("delete-icon.png")
    deleteIcon = ctk.CTkImage(light_image=Image.open(deleteIconPath), size=(26,26),)
    deleteButton = ctk.CTkButton(
        whiteFrame, text=" Delete ", height=48, width=172,
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=deleteIcon,
        # anchor=ctk.W 
    )
    deleteButton.place(x=847, y=726)




    # <<<<<<<<<<<<<<<<<<<< AUTOMATED TESTING >>>>>>>>>>>>>>>>>>>>>
    # global count
    # count = 0
    # #     if count % 2 == 0:
    # #         table.insert(parent='', index=0, values=data, tags=("evenrow",))
    # #     else:
    # #         table.insert(parent='', index=0, values=data, tags=("oddrow",))

    # clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
    # adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']



    # for i in range(15):
    #     num = (i+1)
    #     clinicID = ''.join(random.choices('0123456789', k=12))
    #     clinicName = choice(clinicNames)
    #     clinicContact = ''.join(random.choices('0123456789', k=8))
    #     clinicContact = f'+01{clinicContact}'
    #     adminName = choice(adminNames)
    #     adminEmail = f'{(adminName.replace(" ", "")).lower()}@email.com'

    #     data = (num, clinicID, clinicName, clinicContact, adminName, adminEmail)
    #     if count % 2 == 0:
    #         table.insert(parent='', index='end', values=data, tags=("evenrow",))
    #     else:
    #         table.insert(parent='', index='end', values=data, tags=("oddrow",))

    #     count += 1

    # # Test the insertion in table
    # def testTableInsertion():
    #     clinicNames = ["Health First Clinic", "Wellness Center", "Care Plus Clinic", "Family Health Clinic", "City Medical Center", "Sunrise Clinic", "Harmony Health", "Downtown Clinic", "Healing Hands Clinic", "Prime Care Clinic"]
    #     clinicAddress = ["Kuala Lumpur", "George Town", "Ipoh", "Johor Bahru", "Kota Kinabalu", "Shah Alam", "Malacca City", "Alor Setar", "Kuantan", "Kuching"]
    #     adminNames = ['James Smith', 'Mary Johnson', 'John Williams', 'Patricia Brown', 'Robert Jones', 'Jennifer Garcia', 'Michael Miller', 'Linda Davis', 'William Rodriguez', 'Elizabeth Martinez']

    #     for name in adminNames:
    #         email = name.replace(" ", "")

    #     for i in range(10):
    #         num = i
    #         clinicID = ''.join(random.choices('0123456789', k=12))
    #         clinicName = choice(clinicNames)
    #         clinicContact = ''.join(random.choices('0123456789', k=8))
    #         clinicAddress = choice(clinicAddress)
    #         adminName = choice(adminNames)
    #         adminEmail = f'{email}@email.com'

    #         data = (num, clinicID, clinicName, clinicContact, clinicAddress, adminName, adminEmail)
    #         if count % 2 == 0:
    #             table.insert(parent='', index=0, values=data, tags=("evenrow",))
    #         else:
    #             table.insert(parent='', index=0, values=data, tags=("oddrow",))

    #         count += 1
    


    window.mainloop()


# Only execute the Patient Dashboard Window if this script is run directly
if __name__ == "__main__":
    patientDashboardWindow(email=None)