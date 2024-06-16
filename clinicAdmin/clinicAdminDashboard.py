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
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\clinicAdmin\assets\frame0")

def clinicAdminDashboardWindow(email):
    # Connecting to Clinic Admin DB
    clinicAdminConn = sqlite3.connect('clinicAdmins.db')
    clinicAdminCursor = clinicAdminConn.cursor()
    clinicAdminCursor.execute('SELECT * FROM clinicAdmins WHERE Email=?', [email])
    result = clinicAdminCursor.fetchone()
    username = f"{result[1]} {result[2]}" # Getting user's full name to display on top 
    clinicName = result[7]


    # Helper function to get the full path of assets
    def relative_to_assets(path: str) -> Path:
        return ASSETS_PATH / Path(path)


    # Function to redirect to the Log In Window
    def redirectToLoginWindow():
        msg = messagebox.askokcancel('Warning', 'Are you sure you want to logout?')

        if msg:
            window.destroy()
            from logInWindow.main import logInWindow
            logInWindow()


    # Redirect to the Clinic Admin Doctor Window
    def redirectToClinicAdminDoctorWindow():
        window.destroy()
        from clinicAdmin.clinicAdminDoctors import clinicAdminDoctorWindow
        clinicAdminDoctorWindow(email)


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
        searchInputTextBox.insert('0.0', "Search by")
        searchInputTextBox.configure(text_color='gray')


    global count
    count = 0
    def insertTreeview(array=None):
        global count

        # Connecting to Appointments DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        appointmentCursor.execute('SELECT * FROM appointments')
        appointments = appointmentCursor.fetchall()
        table.delete(*table.get_children())

        # Executed when searchbar is entered
        if array is None:
            for appointment in appointments:
                appointmentID = appointment[0]
                patientName = appointment[1]
                doctorType = appointment[5]
                doctorName = appointment[3]
                  
                if appointment[14] == 0:
                    isConfirmed = 'Waiting'
                elif appointment[14] == 1:
                    isConfirmed = 'Confirmed'
                elif appointment[14] == 2:
                    isConfirmed = 'Rejected'
                elif appointment[14] == 3:
                    isConfirmed = 'Doctor Replaced'

                if appointment[6] == 0:
                    availability = 'Available'
                elif appointment[6] == 1:
                    availability = 'Busy'


                data = (appointmentID, patientName, doctorType, doctorName, availability, isConfirmed)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
                else:
                    table.insert(parent='', index='end', values=data, tags=("oddrow",))

                count += 1
        
        # Executed when Approve Button is clicked
        else:
            for appointment in array:
                appointmentID = appointment[0]
                patientName = appointment[1]
                doctorType = appointment[5]
                doctorName = appointment[3]
                  
                if appointment[14] == 0:
                    isConfirmed = 'Waiting'
                elif appointment[14] == 1:
                    isConfirmed = 'Confirmed'
                elif appointment[14] == 2:
                    isConfirmed = 'Rejected'
                elif appointment[14] == 3:
                    isConfirmed = 'Doctor Replaced'

                if appointment[6] == 0:
                    availability = 'Available'
                elif appointment[6] == 1:
                    availability = 'Busy'


                data = (appointmentID, patientName, doctorType, doctorName, availability, isConfirmed)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
                else:
                    table.insert(parent='', index='end', values=data, tags=("oddrow",))

                count += 1


    def approveAppointment():
        # Connecting to Appointments DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()

        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select an Appointment first.')
            return


        appointmentData = table.item(selectedItem)["values"]
        appointmentID = appointmentData[0]
        isConfirmedStatus = appointmentData[5]
        

        if isConfirmedStatus == 'Approved':
            messagebox.showinfo('Info', f'This Appointment (ID: {appointmentID}) is already approved.')
        else:
            
            appointmentCursor.execute('UPDATE appointments SET IsConfirmed=? WHERE AppointmentID=?', (1, appointmentID))
            appointmentConn.commit()
            appointmentConn.close()
            insertTreeview()
            messagebox.showinfo('Success', f'This Appointment (ID: {appointmentID}) has just been approved successfully. \nThe Patient will be notified.')

    
    def rejectAppointment():
        # Connecting to Appointments DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()

        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select an Appointment first.')
            return


        appointmentData = table.item(selectedItem)["values"]
        appointmentID = appointmentData[0]
        isConfirmedStatus = appointmentData[5]
        

        if isConfirmedStatus == 'Rejected':
            messagebox.showinfo('Info', f'This Appointment (ID: {appointmentID}) is already rejected.')
        else:
            
            appointmentCursor.execute('UPDATE appointments SET IsConfirmed=? WHERE AppointmentID=?', (2, appointmentID))
            appointmentConn.commit()
            appointmentConn.close()
            insertTreeview()
            messagebox.showinfo('Success', f'This Appointment (ID: {appointmentID}) has just been rejected. \nThe Patient will be notified.')


    
    def reassignToplevel():

        def reassignDoctor():
            # Validate dropdown option 
            newDoctorName = doctorDropdown.get()
            if newDoctorName == 'Select Doctor':
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please select a Doctor.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return
            
            # Validate new Doctor Name is not same as old Doctor Name 
            if newDoctorName == doctorName:
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',f"Please select another Doctor.\nDoctor {doctorName} is busy with another appointment at this Consultation Time.")
                if messagebox:
                    toplevel.attributes("-topmost",True)
                return

            # Connecting to Appointments DB
            appointmentConn = sqlite3.connect('appointments.db')
            appointmentCursor = appointmentConn.cursor()
            
            appointmentCursor.execute('UPDATE appointments SET IsConfirmed=?, DoctorName=?, DoctorAvailability=? WHERE AppointmentID=?', (3, newDoctorName, 0, appointmentID))
            appointmentConn.commit()
            appointmentConn.close()
                  

            toplevel.attributes("-topmost",False)
            messagebox.showinfo('Success', f'Doctor {doctorName} for this Appointment (ID: {appointmentID}) has just been replaced by Doctor {newDoctorName}. \nThe Patient will be notified.')  
            toplevel.destroy()
            insertTreeview()
        

        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select an Appointment first.')
            return

        appointmentData = table.item(selectedItem)["values"]
        appointmentID = appointmentData[0]
        doctorName = appointmentData[3]
        doctorAvailability = appointmentData[4]
        

        if doctorAvailability == 'Available':
            messagebox.showerror('Error', f'Doctor {doctorName}) is Available for this appointment schedule.\nThis appointment cannot be reassigned.')
            return


        toplevel = ctk.CTkToplevel(window)
        toplevel.title("Reassign Appointment")
        toplevel.geometry("750x200+600+300")
        toplevel.resizable(False, False)
        toplevel.attributes("-topmost",True)
        toplevel.configure(fg_color = "#fff")

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TOP FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        topFrame = ctk.CTkFrame(toplevel, width=650, height=500, fg_color="#FFFDFD" )
        topFrame.pack(side='top', fill='x', expand=False, padx=(65, 65), pady=(50,0))

        # Select Doctor Dropdown
        doctorDropdownLabel = ctk.CTkLabel(topFrame, text="Select New Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorDropdownLabel.pack(side='top', fill='x', expand=False,)
        doctorDropdown = ctk.CTkComboBox(
            topFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=['Select Doctor', 'Maisarah Majdi', 'Someshwar Rao', 'Karen Khor Siew Li'], border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        doctorDropdown.pack(side='left', fill='x', expand=True,)

        # Reassign Button with Icon
        reassignIconPath = relative_to_assets("reassign-icon.png")
        reassignIcon = ctk.CTkImage(light_image=Image.open(reassignIconPath), size=(33,33),)
        reassignButton = ctk.CTkButton(
            topFrame, text=" Reassign  ", width=140, height=50, 
            font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=reassignIcon,
            command=reassignDoctor # anchor=ctk.W 
        )
        reassignButton.pack(side='left', fill='x', expand=False, padx=(15, 0))


    
    def searchBy():
        # Connecting to Appointments DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        searchTerm = searchInputTextBox.get('0.0', 'end').strip()
        searchOption = searchByDropdown.get()

        searchOptions = [
        'Search By Option', 'Appointment ID', 'Patient Name', 'Doctor Type', 
        "Doctor Name", "Doctor Availability","Confirmation Status",
        ]

        if searchOption == 'Appointment ID':
            searchOption = "AppointmentID"
        elif searchOption == 'Patient Name':
            searchOption = "PatientName"
        elif searchOption == 'Doctor Type':
            searchOption = "DoctorType"
        elif searchOption == 'Doctor Name':
            searchOption = "DoctorName"
        elif searchOption == 'Doctor Availability':
            searchOption = "DoctorAvailability"

            if searchTerm == 'Available':
                searchTerm = '0'
            elif searchTerm == 'Busy':
                searchTerm = '1'

        elif searchOption == 'Confirmation Status':
            searchOption = "IsConfirmed"

            if searchTerm == 'Waiting':
                searchTerm = '0'
            elif searchTerm == 'Confirmed':
                searchTerm = '1'
            elif searchTerm == 'Rejected':
                searchTerm = '2'
            elif searchTerm == 'Doctor Replaced':
                searchTerm = '3'



        if searchTerm == "":
            messagebox.showerror('Error', 'Enter value to search.')
        elif searchOption == 'Search By Option':
            messagebox.showerror('Error', 'Please select an option.')
        else:
            appointmentCursor.execute(f'SELECT * FROM appointments WHERE {searchOption}=?', (searchTerm,))
            result = appointmentCursor.fetchall()
            insertTreeview(result)



    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Clinic Admin Window)")
    window.configure(fg_color="black")
    window.geometry("1350x800+115+5")
    window.update_idletasks()
    window.resizable(False, False)
    window.focus_set()
    window.lift()
    

    # <<<<<<<<<<<<<<<<<<<< SIDEBAR FRAME >>>>>>>>>>>>>>>>>>>>>
    sidebarFrame = ctk.CTkFrame(window, width=310, height=800, fg_color="#000", border_color="#000", )
    sidebarFrame.place(x=0, y=0)

    # 3D Image
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

    # Doctor Button with Icon
    doctorIconPath = relative_to_assets("doctor-icon.png")
    doctorIcon = ctk.CTkImage(light_image=Image.open(doctorIconPath), size=(44,44),)
    doctorButton = ctk.CTkButton(
        sidebarFrame, text=" Doctors     ", width=240, height=60, 
        font=("Inter", 26, "bold",), fg_color="#000", hover_color="#333333", image=doctorIcon,
        command=redirectToClinicAdminDoctorWindow
        # anchor=ctk.W 
    )
    doctorButton.pack(side="top", fill='none', expand=False, padx=(35, 0), pady=(0, 25))

    # Profile Button with Icon
    profileIconPath = relative_to_assets("profile-icon.png")
    profileIcon = ctk.CTkImage(light_image=Image.open(profileIconPath), size=(44,44),)
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
    logoutButton.pack(side="bottom", fill='y', expand=True, padx=(35, 0), pady=(310, 0))


    # <<<<<<<<<<<<<<<<<<<< WHITE FRAME >>>>>>>>>>>>>>>>>>>>>
    whiteFrame = ctk.CTkFrame(window, width=1040, height=800, fg_color="#fff", bg_color='#fff' )
    whiteFrame.place(x=310, y=0)


    # Label with Greeting Message & User's First Name 

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

    greetingLabel1 = ctk.CTkLabel(whiteFrame, text=f"Welcome, {username}", font=("Inter", 36, "bold",), text_color="#000000")
    greetingLabel1.place(x=25, y=25)
    greetingLabel2 = ctk.CTkLabel(whiteFrame, text=f"{greeting}  ({formatted_date})", font=("Inter", 22,), text_color="#000000")
    greetingLabel2.place(x=25, y=72)
    clinicName = ctk.CTkLabel(whiteFrame, text=f"({clinicName})", font=("Inter", 22,), text_color="#000000")
    clinicName.place(x=350, y=72)

    roleLabel = ctk.CTkLabel(whiteFrame, text="(Clinic Admin)", font=("Inter", 36, "bold",), text_color="#000000")
    roleLabel.place(x=775, y=25)

    # Line that seperates Greeting Message from others
    lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
    lineFrame2.place(x=310, y=115)

    # Manage Appointment Header & Description
    h1Label = ctk.CTkLabel(whiteFrame, text="Manage Appointments", font=("Inter", 30, "bold", 'underline'), text_color="#000000")
    h1Label.place(x=25, y=135)
    descLabel = ctk.CTkLabel(
            whiteFrame, font=("Inter", 22,), text_color="#000000",
            text="Manage the patient appointments after verifying with the doctor availability  ", 
        )
    descLabel.place(x=25, y=182)

    # Search Box Dropdown Menu 
    searchOptions = [
        'Search By Option', 'Appointment ID', 'Patient Name', 'Doctor Type', 
        "Doctor Name", "Doctor Availability","Confirmation Status",
    ]
    searchByDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=235, height=50, 
        font=("Inter", 19), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=searchOptions, border_color="#000", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff',
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    searchByDropdown.place(x=25, y=225)

    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
        whiteFrame, fg_color="#ffffff", text_color="gray", width=232, height=50, 
        border_color="#000", font=("Inter", 21), border_spacing=8,
        scrollbar_button_color="#1AFF75", border_width=2,
    )
    searchInputTextBox.insert('insert', "Search by")
    searchInputTextBox.place(x=275, y=225)
    searchInputTextBox.bind("<FocusIn>", searchbarFocus)
    searchInputTextBox.bind("<FocusOut>", searchbarOutFocus)
    #searchInputTextBox.bind("<KeyRelease>", filterTree)


    # Search Button with Icon
    searchIconPath = relative_to_assets("search-icon-1.png")
    searchIcon = ctk.CTkImage(light_image=Image.open(searchIconPath), size=(25,25),)
    searchButton = ctk.CTkButton(
        whiteFrame, text="", width=49, height=50, 
        font=("Inter", 22, "bold",), fg_color="#000", hover_color="#333333", image=searchIcon, 
        corner_radius=4, command=searchBy # anchor=ctk.W 
    )
    searchButton.place(x=410, y=225)


    # Cancel Search Button with Icon
    cancelSearchIconPath = relative_to_assets("reject-icon.png")
    cancelSearchIcon = ctk.CTkImage(light_image=Image.open(cancelSearchIconPath), size=(33,33),)
    cancelSearchButton = ctk.CTkButton(
        whiteFrame, text="", width=50, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=cancelSearchIcon, corner_radius=0,
        command=insertTreeview # anchor=ctk.W 
    )
    cancelSearchButton.place(x=457, y=225)


    # Approve Button with Icon
    approveIconPath = relative_to_assets("approve-icon.png")
    approveIcon = ctk.CTkImage(light_image=Image.open(approveIconPath), size=(33,33),)
    approveButton = ctk.CTkButton(
        whiteFrame, text=" Approve ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#00C16A", hover_color="#009B2B", image=approveIcon,
        command=approveAppointment # anchor=ctk.W 
    )
    approveButton.place(x=525, y=225)

    # Reject Button with Icon
    rejectIconPath = relative_to_assets("reject-icon.png")
    rejectIcon = ctk.CTkImage(light_image=Image.open(rejectIconPath), size=(33,33),)
    rejectButton = ctk.CTkButton(
        whiteFrame, text=" Reject  ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=rejectIcon,
        command=rejectAppointment # anchor=ctk.W 
    )
    rejectButton.place(x=695, y=225)


    # Reassign Button with Icon
    reassignIconPath = relative_to_assets("reassign-icon.png")
    reassignIcon = ctk.CTkImage(light_image=Image.open(reassignIconPath), size=(33,33),)
    reassignButton = ctk.CTkButton(
        whiteFrame, text=" Reassign  ", width=140, height=50, 
        font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=reassignIcon,
        command=reassignToplevel # anchor=ctk.W 
    )
    reassignButton.place(x=850, y=225)


    # <<<<<<<<<<<<<<<<<<<< TABLE FRAME STORING TREEVIEW >>>>>>>>>>>>>>>>>>>>> 
    tableFrame = ctk.CTkFrame(whiteFrame, fg_color="transparent",)
    tableFrame.place(x=25, y=295)

    # Initializing Treeview Scrollbar
    tableScrollbar1 = Scrollbar(tableFrame, orient=VERTICAL)
    # tableScrollbar2 = Scrollbar(tableFrame, orient="horizontal")

    # Treeview that stores User Data
    table = ttk.Treeview(tableFrame, yscrollcommand=tableScrollbar1.set,height=12)
    table.pack(side='left', fill='both')
    table['columns'] = (
        'ID', 'Patient Name', 'Doctor Type',
        "Doctor Name", "Availability", "Status"
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
    style.configure('Treeview', font=('Inter', 16), rowheight=47, fieldbackground="#DAFFF7")
    style.map(
        'Treeview', 
        background=[('selected', '#00BE97',)], 
        font=[('selected', ('Inter', 16, 'bold'))],
    )

    # Treeview Table Headings Details
    table.heading('ID', text='ID')
    table.heading('Patient Name', text='Patient Name')
    table.heading('Doctor Type', text='Doctor Type')
    table.heading('Doctor Name', text='Doctor Name')
    table.heading('Availability', text='Availability')
    table.heading('Status', text='Status')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("ID", width=43, anchor=ctk.CENTER)
    table.column("Patient Name", width=235, anchor=ctk.CENTER)
    table.column("Doctor Type",width=280, anchor=ctk.CENTER)
    table.column("Doctor Name", width=280, anchor=ctk.CENTER)
    table.column("Availability", width=180, anchor=ctk.CENTER,)
    table.column("Status", width=210, anchor=ctk.CENTER)

    # Setting alternating colours for the rows in Treeview
    table.tag_configure("oddrow", background="#F2F5F8")
    table.tag_configure("evenrow", background="#B4EFF7")


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
    

    insertTreeview()
    window.mainloop()


# Only execute the Clinic Admin Dashboard Window if this script is run directly
if __name__ == "__main__":
    clinicAdminDashboardWindow(email=None)