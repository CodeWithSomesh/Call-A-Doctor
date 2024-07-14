import sys
from pathlib import Path
from PIL import Image
import sqlite3
from datetime import datetime
import random
from random import choice

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Tk, Scrollbar, VERTICAL, messagebox
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\doctor\assets\frame0")

def doctorDashboardWindow(email):

    # Connecting to Doctor DB
    doctorConn = sqlite3.connect('doctors.db')
    doctorCursor = doctorConn.cursor()
    doctorCursor.execute('SELECT * FROM doctors WHERE Email=?', [email])
    result = doctorCursor.fetchone()
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
        searchInputTextBox.insert('0.0', "Search")
        searchInputTextBox.configure(text_color='gray')

    global count
    count = 0
    def insertTreeview(array=None):
        global count

        # Connecting to Doctors DB
        doctorConn = sqlite3.connect('doctors.db')
        doctorCursor = doctorConn.cursor()
        doctorCursor.execute('SELECT * FROM doctors WHERE Email=?', [email])
        result = doctorCursor.fetchone()
        doctorName = f"{result[1]} {result[2]}" # Getting Doctor's Name
        clinicName = result[7]
        
        # Connecting to Appointments DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        appointmentCursor.execute('SELECT * FROM appointments WHERE DoctorName=? AND ClinicName=? AND IsConfirmed=?', [doctorName, clinicName, 1])
        appointments = appointmentCursor.fetchall()

        table.delete(*table.get_children())

        # Executed when searchbar is entered
        if array is None:
            for num, appointment in enumerate(appointments, start=1):
                appointmentID = appointment[0]
                patientName = appointment[1]
                date = appointment[9]
                time = appointment[10]
                dateAndTime = f'{date} ({time})'
                duration = appointment[11]
                painDetails = appointment[13]
                if appointment[15] == 'Empty':
                    prescriptions = 'Not Given'
                    completionStatus = "Waiting"
                else:
                    prescriptions = 'Given'
                    completionStatus = "Completed"
                 

                data = (num, patientName, dateAndTime, duration, painDetails, prescriptions, completionStatus, appointmentID)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
                else:
                    table.insert(parent='', index='end', values=data, tags=("oddrow",))

                count += 1
        
        # Executed when Approve Button is clicked
        else:
            for num, appointment in enumerate(array, start=1):
                appointmentID = appointment[0]
                patientName = appointment[1]
                date = appointment[9]
                time = appointment[10]
                dateAndTime = f'{date} ({time})'
                duration = appointment[11]
                painDetails = appointment[13]
                if appointment[15] == 'Empty':
                    prescriptions = 'Not Given'
                else:
                    prescriptions = 'Given'
                

                data = (num, patientName, dateAndTime, duration, painDetails, prescriptions, appointmentID)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
                else:
                    table.insert(parent='', index='end', values=data, tags=("oddrow",))

                count += 1

    def searchBy():
        # Connecting to Doctor DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()

        searchTerm = searchInputTextBox.get('0.0', 'end').strip()
        searchOption = searchByDropdown.get()

        # Connecting to Doctors DB
        doctorConn = sqlite3.connect('doctors.db')
        doctorCursor = doctorConn.cursor()
        doctorCursor.execute('SELECT * FROM doctors WHERE Email=?', [email])
        result = doctorCursor.fetchone()
        doctorName = f"{result[1]} {result[2]}" # Getting Doctor's Name
        clinicName = result[7]
        
        
        if searchOption == 'Patient Name':
            searchOption = "PatientName"
        elif searchOption == 'Date & Time':
            searchOption = "AppointmentDate"
        elif searchOption == 'Duration':
            searchOption = "AppointmentDuration"
        elif searchOption == 'Pain Details':
            searchOption = "PainDetails"
        elif searchOption == 'Prescriptions':
            searchOption = "Prescriptions"

            if searchTerm == 'Not Given':
                searchTerm = 'Empty'



        if searchTerm == "":
            messagebox.showerror('Error', 'Enter value to search.')
        elif searchOption == 'Search By Option':
            messagebox.showerror('Error', 'Please select an option.')
        else:
            appointmentCursor.execute(f'SELECT * FROM appointments WHERE {searchOption}=? AND DoctorName=? AND ClinicName=? AND IsConfirmed=?', (searchTerm, doctorName, clinicName, 1))
            result = appointmentCursor.fetchall()
            insertTreeview(result)
    
    def changeOnlineStatus():
       # Connecting to Doctors DB
        doctorConn = sqlite3.connect('doctors.db')
        doctorCursor = doctorConn.cursor()
        doctorCursor.execute('SELECT * FROM doctors WHERE Email=?', [email])
        result = doctorCursor.fetchone() 
        doctorID = result[0]
        onlineStatus = result[12]

        
        # If the Status is Offline, make it Online
        if onlineStatus == 0:
            doctorCursor.execute('UPDATE doctors SET IsOffline=? WHERE DoctorID=?', (1, doctorID))
            doctorConn.commit()
            doctorConn.close()
            goOfflineButton.configure(text=" Go Offline ", fg_color="#E00000", hover_color="#AE0000", image=onlineIcon)
            messagebox.showinfo('Success', f'You have made yourself online and available, now you will be able to receive new appointments!')

        

        # If the Status is Online, make it Offline
        if onlineStatus == 1:
            msg = messagebox.askokcancel('Warning', "You are about to go offline. When you go offline, you will not receive any new appointments.\nAre you sure you want to proceed?")

            if msg:
                goOfflineButton.configure(text=" Go Online ", fg_color="#1BC5DC", hover_color="#1695A7", image=onlineIcon)
                messagebox.showinfo('Success', f'You have made yourself offline successfully. Note that when you are offline, you will not receive any new appointments.')

                doctorCursor.execute('UPDATE doctors SET IsOffline=? WHERE DoctorID=?', (0, doctorID))
                doctorConn.commit()
                doctorConn.close()

            


    def topLevel():

        def handleSubmit():
            newPrescriptions = prescriptionsTextBox.get(0.0, 'end').strip()

            # , IsCompleted = ? {Need to update before Viva}
            if (newPrescriptions != ''):
                updateQuery = '''
                    UPDATE appointments
                    SET Prescriptions = ?
                    WHERE AppointmentID = ? '''

                appointmentCursor.execute(
                    updateQuery, (newPrescriptions, appointmentID))
                appointmentConn.commit()

                toplevel.attributes("-topmost",False)
                if prescriptions != "Empty":
                    messagebox.showinfo('Success', f'Prescriptions for Patient {patientName} updated successfully.')
                else:
                    messagebox.showinfo('Success', f'Prescriptions for Patient {patientName} added successfully.')

                toplevel.destroy()
                insertTreeview()
                 
            else:
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please fill up the Prescription Input Field.")
                if messagebox:
                    toplevel.attributes("-topmost",True)

        

        # <<<<<<<<<<<<<<<<<<<<<<<<<<< RETRIEVING APPOINTMENT DETAILS FROM TREEVIEW >>>>>>>>>>>>>>>>>
        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select an Appointment first.')
            return
        
        appointmentData = table.item(selectedItem)["values"]
        print(appointmentData)
        appointmentID = appointmentData[7]
        tablePrescriptions = appointmentData[5]

        if tablePrescriptions == "Given":
            msg = messagebox.askokcancel('Info', 'You have already given this patient their prescriptions, do you want to update it now?')

            if msg:
                pass
            else:
                return

        # <<<<<<<<<<<<<<<<<<<<<<<<<<< RETRIEVING APPOINTMENT DETAILS FROM DATABASE >>>>>>>>>>>>>>>>>
        # Connecting to Appointment DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        appointmentCursor.execute('SELECT * FROM appointments WHERE AppointmentID=?', [appointmentID])
        result = appointmentCursor.fetchone()
        patientName = result[1]
        patientID = result[2] 
        doctorName = result[3] 
        doctorID = result[4] 
        doctorType = result[5] 
        clinicName = result[7] 
        clinicID = result[8] 
        appointmentDate = result[9] 
        appointmentTime = result[10] 
        appointmentDuration = result[11] 
        appointmentCreatedTime = result[12]
        painDetails = result[13]
        prescriptions = result[15]  
        print(prescriptions)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<< TOPLEVEL >>>>>>>>>>>>>>>>>>>>>>>>>
        toplevel = ctk.CTkToplevel(window)
        toplevel.title("View Appointment Details & Give Prescriptions")
        toplevel.geometry("780x650+450+80")
        toplevel.resizable(False, False)
        toplevel.attributes("-topmost",True)
        toplevel.configure(fg_color = "#fff")

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        topLevelFrame = ctk.CTkScrollableFrame(toplevel, width=780, height=650, fg_color="#fff", scrollbar_fg_color="#000", scrollbar_button_color="#000",)
        topLevelFrame.place(x=0, y=0)


        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PARENT FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        parentFrame = ctk.CTkFrame(topLevelFrame, width=780, height=575, fg_color="#fff",)
        parentFrame.pack(side='top', fill='both', expand=False)


        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT FRAME INSDIE PARENT FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", )
        leftFrame.pack(side='left', fill='both', expand=False, padx=(75, 85), pady=(30, 30))

        # Patient Name 
        patientNameLabel = ctk.CTkLabel(leftFrame, text="Patient Name", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        patientNameLabel.pack(side='top', fill='x', expand=False,)
        patientNameDisplay = ctk.CTkLabel(leftFrame, text=patientName, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        patientNameDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Doctor Name 
        doctorNameLabel = ctk.CTkLabel(leftFrame, text="Doctor Name", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorNameLabel.pack(side='top', fill='x', expand=False,)
        doctorNameDisplay = ctk.CTkLabel(leftFrame, text=f"{doctorName} ({doctorType})", font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        doctorNameDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Clinic Name 
        clinicNameLabel = ctk.CTkLabel(leftFrame, text="Clinic Name", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        clinicNameLabel.pack(side='top', fill='x', expand=False,)
        clinicNameDisplay = ctk.CTkLabel(leftFrame, text=clinicName, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        clinicNameDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Appointment Date
        appointmentDateLabel = ctk.CTkLabel(leftFrame, text="Appointment Date", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        appointmentDateLabel.pack(side='top', fill='x', expand=False,)
        appointmentDateDisplay = ctk.CTkLabel(leftFrame, text=appointmentDate, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        appointmentDateDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Appointment Duration
        appointmentDurationLabel = ctk.CTkLabel(leftFrame, text="Appointment Duration", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        appointmentDurationLabel.pack(side='top', fill='x', expand=False,)
        appointmentDurationDisplay = ctk.CTkLabel(leftFrame, text=appointmentDuration, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        appointmentDurationDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Appointment Created At Time
        appointmentCreatedTimeLabel = ctk.CTkLabel(leftFrame, text="Appointment Booked At", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        appointmentCreatedTimeLabel.pack(side='top', fill='x', expand=False,)
        appointmentCreatedTimeDisplay = ctk.CTkLabel(leftFrame, text=appointmentCreatedTime, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        appointmentCreatedTimeDisplay.pack(side='top', fill='x', expand=False, pady=(0, 0))

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< RIGHT FRAME INSIDE SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        rightFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD",)
        rightFrame.pack(side='left', fill='both', expand=False, padx=(0,0), pady=(30, 30))
        
        # Patient ID
        patientIDLabel = ctk.CTkLabel(rightFrame, text="Patient ID", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        patientIDLabel.pack(side='top', fill='x', expand=False,)
        patientIDDisplay = ctk.CTkLabel(rightFrame, text=patientID, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        patientIDDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Doctor ID 
        doctorIDLabel = ctk.CTkLabel(rightFrame, text="Doctor ID", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorIDLabel.pack(side='top', fill='x', expand=False,)
        doctorIDDisplay = ctk.CTkLabel(rightFrame, text=f"{doctorID} ({doctorType})", font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        doctorIDDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Clinic ID 
        clinicIDLabel = ctk.CTkLabel(rightFrame, text="Clinic ID", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        clinicIDLabel.pack(side='top', fill='x', expand=False,)
        clinicIDDisplay = ctk.CTkLabel(rightFrame, text=clinicID, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        clinicIDDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Appointment Time
        appointmentTimeLabel = ctk.CTkLabel(rightFrame, text="Appointment Time", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        appointmentTimeLabel.pack(side='top', fill='x', expand=False,)
        appointmentTimeDisplay = ctk.CTkLabel(rightFrame, text=appointmentTime, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        appointmentTimeDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Appointment ID
        appointmentIDLabel = ctk.CTkLabel(rightFrame, text="Appointment ID", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        appointmentIDLabel.pack(side='top', fill='x', expand=False,)
        appointmentIDDisplay = ctk.CTkLabel(rightFrame, text=appointmentID, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        appointmentIDDisplay.pack(side='top', fill='x', expand=False, pady=(0, 25))

        # Pain Details
        painDetailsLabel = ctk.CTkLabel(rightFrame, text="Pain Details", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        painDetailsLabel.pack(side='top', fill='x', expand=False,)
        painDetailsDisplay = ctk.CTkLabel(rightFrame, text=painDetails, font=("Inter", 20,), anchor=ctk.W, text_color="#000000",)
        painDetailsDisplay.pack(side='top', fill='x', expand=False, pady=(0, 0))

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< BOTTOM FRAME INSIDE SCROLLABLE TOPLEVEL FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        bottomFrame = ctk.CTkFrame(topLevelFrame, fg_color="#fff" )
        bottomFrame.pack(side='bottom', fill='x', expand=False, padx=(78, 80), pady=(0,0))

        # Prescription Textbox
        prescriptionsLabel = ctk.CTkLabel(bottomFrame, text="Prescriptions", font=("Inter", 22, "bold",), anchor=ctk.W, text_color="#000000",)
        prescriptionsLabel.pack(side='top', fill='x', expand=False, pady=(0,0))
        prescriptionsTextBox = ctk.CTkTextbox(
            bottomFrame, fg_color="#ffffff", text_color="#000000", width=648, height=88, 
            border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
            scrollbar_button_color="#1AFF75", border_width=1
        )
        prescriptionsTextBox.pack(side='top', fill='none', expand=False, pady=(0, 0), anchor="w")

        if prescriptions != "Empty":
            prescriptionsTextBox.insert(0.0, prescriptions)

        if prescriptions == "Empty":
            # Generate prescriptions Button with Icon
            pillIconPath = relative_to_assets("give-pill-icon.png")
            pillIcon = ctk.CTkImage(light_image=Image.open(pillIconPath), size=(33,33),)
            pillButton = ctk.CTkButton(
                bottomFrame, text=" Generate Prescriptions", height=60, width=378,
                font=("Inter", 22, "bold",), fg_color="#00C16A", hover_color="#009B2B", image=pillIcon,
                command=handleSubmit # anchor=ctk.W 
            )
            pillButton.pack(side='top', fill='x', expand=False,pady=(30,30))

        else:
            # Update Button with Icon
            updateIconPath = relative_to_assets("update-icon.png")
            updateIcon = ctk.CTkImage(light_image=Image.open(updateIconPath), size=(33,33),)
            updateButton = ctk.CTkButton(
                bottomFrame, text=" Update Prescriptions", height=60, width=378,
                font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=updateIcon,
                command=handleSubmit # anchor=ctk.W 
            )
            updateButton.pack(side='top', fill='x', expand=False,pady=(30,30))



    # <<<<<<<<<<<<<<<<<<<< MAIN WINDOW >>>>>>>>>>>>>>>>>>>>>
    window = ctk.CTk()
    window.title("CaD - Doctor Appointment Booking System (Doctor Window)")
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


    # <<<<<<<<<<<<<<<<<<<< WHITE FRAME >>>>>>>>>>>>>>>>>>>>>
    whiteFrame = ctk.CTkFrame(window, width=1040, height=800, fg_color="#fff", bg_color='#fff' )
    whiteFrame.place(x=310, y=0)


    # Label with Greeting Message & User's Full Name 

    now = datetime.now()  # Get the current date and time
    todayInt = now.day # Get the current date in integer
    thisMonth = now.month # Get the current month in integer
    thisYear = now.year # Get the current year in integer
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
    clinicName.place(x=372, y=72)

    roleLabel = ctk.CTkLabel(whiteFrame, text="(Doctor)", font=("Inter", 36, "bold",), text_color="#000000")
    roleLabel.place(x=875, y=25)

    # Line that seperates Greeting Message from others
    lineFrame2 = ctk.CTkFrame(window, width=1040, height=3, fg_color="#37D8B7", border_color="#37D8B7", bg_color='#37D8B7' )
    lineFrame2.place(x=310, y=115)

    # Manage Patient Header & Description
    h1Label = ctk.CTkLabel(whiteFrame, text="Manage Patients", font=("Inter", 30, "bold", 'underline'), text_color="#000000")
    h1Label.place(x=25, y=135)
    descLabel = ctk.CTkLabel(
            whiteFrame, font=("Inter", 22,), text_color="#000000",
            text="View patient appointments, their medical records and generate suitable prescriptions for them ", 
        )
    descLabel.place(x=25, y=182)

    
    # Search Box Dropdown Menu 
    searchOptions = [
        'Search By Option', 'Patient Name', 'Date & Time', 
        "Duration", "Pain Details", "Prescriptions"
    ]
    searchByDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=252, height=50, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=searchOptions, border_color="#000", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff',
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    searchByDropdown.place(x=25, y=225)

    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
        whiteFrame, fg_color="#ffffff", text_color="gray", width=240, height=50, 
        border_color="#000", font=("Inter", 21), border_spacing=8,
        scrollbar_button_color="#1AFF75", border_width=2,
    )
    searchInputTextBox.insert('insert', "Search")
    searchInputTextBox.place(x=293, y=225)
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
    searchButton.place(x=465, y=225)


    # Cancel Search Button with Icon
    cancelSearchIconPath = relative_to_assets("reject-icon.png")
    cancelSearchIcon = ctk.CTkImage(light_image=Image.open(cancelSearchIconPath), size=(33,33),)
    cancelSearchButton = ctk.CTkButton(
        whiteFrame, text="", width=50, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=cancelSearchIcon, corner_radius=2,
        command=insertTreeview # anchor=ctk.W 
    )
    cancelSearchButton.place(x=510, y=225)

     # Connecting to Doctors DB
    doctorConn = sqlite3.connect('doctors.db')
    doctorCursor = doctorConn.cursor()
    doctorCursor.execute('SELECT * FROM doctors WHERE Email=?', [email])
    result = doctorCursor.fetchone() 
    doctorID = result[0]
    onlineStatus = result[12]    
            

    # Go Offline Button with Icon {Need to update before Viva}
    offlineIconPath = relative_to_assets("offline-icon.png")
    onlineIconPath = relative_to_assets("online-icon.png")
    offlineIcon = ctk.CTkImage(light_image=Image.open(offlineIconPath), size=(33,33),)
    onlineIcon = ctk.CTkImage(light_image=Image.open(onlineIconPath), size=(33,33),)
    goOfflineButton = ctk.CTkButton(
        whiteFrame, width=200, height=50, 
        font=("Inter", 22, "bold",), 
        command=changeOnlineStatus # anchor=ctk.W 
    )
    goOfflineButton.place(x=571, y=225)

    if onlineStatus == 0:
        goOfflineButton.configure(text=" Go Online ", fg_color="#1BC5DC", hover_color="#1695A7", image=onlineIcon)
    else:
        goOfflineButton.configure(text=" Go Offline ", fg_color="#E00000", hover_color="#AE0000", image=onlineIcon)
                           


    # Generate Prescriptions Button with Icon
    pillIconPath = relative_to_assets("pill-icon.png")
    pillIcon = ctk.CTkImage(light_image=Image.open(pillIconPath), size=(33,33),)
    generateMedicineButton = ctk.CTkButton(
        whiteFrame, text=" Prescriptions ", width=240, height=50, 
        font=("Inter", 22, "bold",), fg_color="#00C16A", hover_color="#009B2B", image=pillIcon,
        command=topLevel # anchor=ctk.W 
    )
    generateMedicineButton.place(x=782, y=225)


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
        'No', 'Patient Name', 'Date & Time', 'Duration',
        "Pain Details", "Prescriptions", "Status", "Appointment ID"
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
    table.heading('No', text='No')
    table.heading('Patient Name', text='Patient Name',)
    table.heading('Date & Time', text='Date & Time')
    table.heading('Duration', text='Duration')
    table.heading('Pain Details', text='Pain Details')
    table.heading('Prescriptions', text='Prescriptions')
    table.heading('Status', text='Status')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("No", width=43, anchor=ctk.CENTER)
    table.column("Patient Name", width=250, anchor=ctk.CENTER)
    table.column("Date & Time", width=200, anchor=ctk.CENTER)
    table.column("Duration", width=200, anchor=ctk.CENTER)
    table.column("Pain Details", width=220, anchor=ctk.CENTER)
    table.column("Prescriptions", width=160, anchor=ctk.CENTER)
    table.column("Status", width=160, anchor=ctk.CENTER)
    table.column("Appointment ID", width=0, stretch=ctk.NO)

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


# Only execute the Doctor Dashboard Window if this script is run directly
if __name__ == "__main__":
    doctorDashboardWindow(email=None)