import sys
from pathlib import Path
from PIL import Image
import sqlite3
from datetime import datetime
from tkintermapview import TkinterMapView
from tkcalendar import *

# Add the parent directory to the system path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from tkinter import ttk, Tk, Scrollbar, VERTICAL, messagebox
import customtkinter as ctk


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"C:\Users\Somesh\Documents\Desktop App (Software Engineering Module)\Call-A-Doctor\patient\assets\frame0")

def patientDashboardWindow(email):

    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CONNECTING TO SQLITE3 DATABASE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

    # Creating Appointments DB
    appointmentConn = sqlite3.connect('appointments.db')
    appointmentCursor = appointmentConn.cursor()
    appointmentCursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            AppointmentID INTEGER PRIMARY KEY AUTOINCREMENT,
            PatientName TEXT NOT NULL,
            PatientID TEXT NOT NULL,
            DoctorName TEXT NOT NULL,
            DoctorID TEXT NOT NULL,
            DoctorType TEXT NOT NULL,
            DoctorAvailability INTEGER DEFAULT 0,
            ClinicName TEXT NOT NULL,
            ClinicID TEXT NOT NULL,
            AppointmentDate TEXT NOT NULL,
            AppointmentTime TEXT NOT NULL,
            AppointmentDuration TEXT NOT NULL,
            AppointmentCreatedTime TEXT NOT NULL,
            PainDetails TEXT NOT NULL,
            IsConfirmed INTEGER DEFAULT 0
        )          
    """)

    # Connecting to Patient Admin DB
    patientConn = sqlite3.connect('patients.db')
    patientCursor = patientConn.cursor()
    patientCursor.execute('SELECT * FROM patients WHERE Email=?', [email])
    result = patientCursor.fetchone()
    username = f"{result[1]} {result[2]}" # Getting user's full name to display on top 


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
        searchInputTextBox.insert('0.0', "Search by Appointment Details")
        searchInputTextBox.configure(text_color='gray')

    def updateAppointmentTopLevel():

        def updateAppointment():  
            clinicName = clinicNameDropdown.get()
            doctorType = doctorTypeDropdown.get()
            painDetails = painDetailsTextBox.get(0.0, 'end').strip()
            doctorName = doctorDropdown.get()
            date = calendar.get_date()
            time = consultationTimeDropdown.get()
            duration = consultationDurationDropdown.get()

            if (clinicName != '' and doctorType != '' and painDetails != '' and doctorName != '' and date != '' and 
                time != '' and duration != ''):

                if clinicName == 'Clinic Name':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select a Clinic.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if doctorType == 'Select Type':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select the Type of Doctor.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if doctorName == 'Select Doctor':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select a Doctor.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if time == 'Select Time':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select the Consultaion Time.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if duration == 'Select Duration':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select the Consultaion Duration.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                

                updateQuery = '''
                    UPDATE appointments
                    SET DoctorName = ?, DoctorType = ?, ClinicName = ?, AppointmentDate = ?, AppointmentTime = ?, AppointmentDuration = ?, PainDetails = ?
                    WHERE AppointmentID = ? '''

                appointmentCursor.execute(
                    updateQuery, (doctorName, doctorType, clinicName, date, time, duration, painDetails, appointmentID))
                appointmentConn.commit()

                toplevel.attributes("-topmost",False)
                messagebox.showinfo('Success', 'Appointment updated successfully.')
                toplevel.destroy()
                insertTreeview()
                
            
            else:
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please fill up all the fields.")
                if messagebox:
                    toplevel.attributes("-topmost",True)



        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select an Appointment first.')
            return
        
        appointmentData = table.item(selectedItem)["values"]
        print(appointmentData)
        appointmentID = appointmentData[6]
        print(appointmentID)


        toplevel = ctk.CTkToplevel(window)
        toplevel.title("Update Appointment")
        toplevel.geometry("800x600+460+100")
        toplevel.resizable(False, False)
        toplevel.attributes("-topmost",True)
        toplevel.configure(fg_color = "#fff")

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        parentFrame = ctk.CTkScrollableFrame(toplevel, width=800, height=600, fg_color="#fff", scrollbar_fg_color="#000", scrollbar_button_color="#000",)
        parentFrame.place(x=0, y=0)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TOP FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        topFrame = ctk.CTkFrame(parentFrame, width=650, height=500, fg_color="#FFFDFD" )
        topFrame.pack(side='top', fill='x', expand=False, padx=(65, 80), pady=(20,0))
        
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

        gMapsWidget = TkinterMapView(topFrame, width=650, height=400)
        gMapsWidget.pack(side='top', fill='x', expand=True, pady=(10,0), padx=(0,5))
        gMapsWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        gMapsWidget.set_address("Bayan Lepas, Penang, Malaysia", marker=True)
        gMapsWidget.set_zoom(12)

        # gMapsWidget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
        # gMapsWidget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=e...{x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        # gMapsWidget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style
        # marker.set_text("Select A Clinic")
        

        doctorTypeLabel = ctk.CTkLabel(topFrame, text="Select Type Of Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorTypeLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
        doctorTypes = [
            "Select Type","Allergist", "Cardiologist", "Dermatologist", "Endocrinologist", 
            "Gastroenterologist", "Geriatrician", "Internist", "Nephrologist", "Neurologist", 
            "Obstetrician/Gynecologist", "Oncologist", "Ophthalmologist", "Orthopedic Surgeon", 
            "Pediatrician", "Podiatrist", "Psychiatrist", "Pulmonologist", "Rheumatologist", 
            "General Practitioner", "Family Medicine Doctor", "Home Health Care Doctor", 
            "Emergency Medicine Specialist"]
        doctorTypeDropdown = ctk.CTkComboBox(
            topFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=doctorTypes, border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        doctorTypeDropdown.pack(side='top', fill='x', expand=False, pady=(0,0), padx=(0,5))

        painDetailsLabel = ctk.CTkLabel(topFrame, text="Explain Pain Details", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        painDetailsLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
        painDetailsTextBox = ctk.CTkTextbox(
            topFrame, fg_color="#ffffff", text_color="#000000", width=648, height=88, 
            border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
            scrollbar_button_color="#1AFF75", border_width=1
        )
        painDetailsTextBox.pack(side='top', fill='none', expand=False, pady=(0, 10), anchor="w")


        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT FRAME INSDIE PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", )
        leftFrame.pack(side='left', fill='both', expand=False, padx=65, pady=30)

        doctorDropdownLabel = ctk.CTkLabel(leftFrame, text="Select Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorDropdownLabel.pack(side='top', fill='x', expand=False,)
        doctorDropdown = ctk.CTkComboBox(
            leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=['Select Doctor', 'Maisarah Majdi', 'Someshwar Rao', 'Karen Khor Siew Li'], border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        doctorDropdown.pack(side='top', fill='x', expand=False,)

        times = [
            "Select Time",'9:00 AM', '10:00 AM', '11:00 AM', 
            '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
            '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
            '12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
            '6:00 AM', '7:00 AM', '8:00 AM'
        ]
        consultationTimeDropdownLabel = ctk.CTkLabel(leftFrame, text="Select Consultation Time", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        consultationTimeDropdownLabel.pack(side='top', fill='x', expand=False, pady=(150,0))
        consultationTimeDropdown = ctk.CTkComboBox(
            leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=times, border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        consultationTimeDropdown.pack(side='top', fill='x', expand=False,)

        # Cancel Button with Icon
        cancelIconPath = relative_to_assets("reject-icon.png")
        cancelIcon = ctk.CTkImage(light_image=Image.open(cancelIconPath), size=(33,33),)
        cancelButton = ctk.CTkButton(
            leftFrame, text=" Cancel ", width=280, height=60, 
            font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=cancelIcon,
            command=toplevel.destroy # anchor=ctk.W 
        )
        cancelButton.pack(side='top', fill='x', expand=False,pady=(40,15))


        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< RIGHT FRAME INSIDE PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        rightFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD",)
        rightFrame.pack(side='left', fill='both', expand=False, padx=(0,0), pady=30)
        

        # Select Consultation Date Widget
        consultationDateLabel = ctk.CTkLabel(rightFrame, text="Select Consultation Date", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        consultationDateLabel.pack(side='top', fill='x', expand=False,)
        calendar = Calendar(
            rightFrame, selectmode="day", year=thisYear, font=("Inter", 12),
            month=thisMonth, day=todayInt, background="#1AFF75", 
            selectbackground="#36D8B7", foreground="black"
        )
        calendar.pack(side='top', fill='x', expand=False,)

        # Select Consultation Duration Dropdown Menu
        durationArray = [
            'Select Duration', '1 hour', '1 hour 30 Minutes',
            '2 hours', '2 hours 30 Minutes', '3 hours', '3 hour 30 Minutes', '4 hours', 
            '4 hours 30 Minutes', '5 hours'
        ]
        consultationDurationDropdownLabel = ctk.CTkLabel(rightFrame, text="Select Consultation Duration", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        consultationDurationDropdownLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
        consultationDurationDropdown = ctk.CTkComboBox(
            rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=durationArray, border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        consultationDurationDropdown.pack(side='top', fill='x', expand=False,)

        # Book Button 2 with Icon
        updateIconPath = relative_to_assets("update-icon.png")
        updateIcon = ctk.CTkImage(light_image=Image.open(updateIconPath), size=(33,33),)
        updateButton = ctk.CTkButton(
            rightFrame, text=" Update Appointment Details", height=48, width=378,
            font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=updateIcon,
            command=updateAppointment # anchor=ctk.W 
        )
        updateButton.pack(side='top', fill='x', expand=False,pady=(40,15))

        # Connecting to Appointment DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()

        appointmentCursor.execute('SELECT * FROM appointments WHERE AppointmentID=?', [appointmentID])
        result = appointmentCursor.fetchone()
        print(result)

        clinicName = clinicNameDropdown.set(result[7])
        doctorType = doctorTypeDropdown.set(result[6])
        painDetails = painDetailsTextBox.insert('insert', result[13])
        doctorName = doctorDropdown.set(result[3])
        date = calendar.selection_set(result[9])
        time = consultationTimeDropdown.set(result[10])
        duration = consultationDurationDropdown.set(result[11])

      

    
    def bookAppointmentTopLevel():

        def bookAppointment():
            clinicName = clinicNameDropdown.get()
            doctorType = doctorTypeDropdown.get()
            painDetails = painDetailsTextBox.get(0.0, 'end').strip()
            doctorName = doctorDropdown.get()
            date = calendar.get_date()
            time = consultationTimeDropdown.get()
            duration = consultationDurationDropdown.get()
            
            # Connecting to Patient DB to get Patient Name & ID
            patientConn = sqlite3.connect('patients.db')
            patientCursor = patientConn.cursor()
            patientCursor.execute('SELECT * FROM patients WHERE Email=?', [email])
            patientResult = patientCursor.fetchone()
            patientName = f"{patientResult[1]} {patientResult[2]}"
            patientID = patientResult[0]

            # Connecting to Doctor DB to get Doctor ID
            doctorID = 1
            # doctorConn = sqlite3.connect('doctors.db')
            # doctorCursor = doctorConn.cursor()
            # doctorCursor.execute('SELECT * FROM doctors WHERE FirstName=?', [doctorFirstName])
            # doctorResult = doctorCursor.fetchone()
            # doctorID = doctorResult[0]
            doctorAvailability = 0

            # Connecting to Doctor DB to get Doctor ID
            # clinicAdminConn = sqlite3.connect('clinicAdmins.db')
            # clinicAdminCursor = clinicAdminConn.cursor()
            # clinicAdminCursor.execute('SELECT * FROM clinicAdmins WHERE ClinicName=?', [clinicName])
            # clinicAdminResult = clinicAdminCursor.fetchone()
            # clinicAdminID = clinicAdminResult[0]
            clinicAdminID = 1

            currentDateTime = datetime.now()
            appointmentCreatedAt = currentDateTime.strftime('%Y-%m-%d %H:%M:%S')

            if (clinicName != '' and doctorType != '' and painDetails != '' and doctorName != '' and date != '' and 
                time != '' and duration != ''):

                if clinicName == 'Clinic Name':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select a Clinic.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if doctorType == 'Select Type':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select the Type of Doctor.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if doctorName == 'Select Doctor':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select a Doctor.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if time == 'Select Time':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select the Consultaion Time.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return
                
                if duration == 'Select Duration':
                    toplevel.attributes("-topmost",False)
                    messagebox.showerror('Error',"Please select the Consultaion Duration.")
                    if messagebox:
                        toplevel.attributes("-topmost",True)
                    return

                # Connecting to Patients DB to retrieve Number Of Appointments
                patientConn = sqlite3.connect('patients.db')
                patientCursor = patientConn.cursor()
                patientCursor.execute('SELECT NumberOfAppointments FROM patients WHERE Email=?', [email])
                result = patientCursor.fetchone()
                currentAppointments = result[0]

                appointmentCursor.execute(
                    'INSERT INTO appointments (PatientName, PatientID, DoctorName, DoctorID, DoctorType, DoctorAvailability, ClinicName, ClinicID, AppointmentDate, AppointmentTime, AppointmentDuration, AppointmentCreatedTime, PainDetails, IsConfirmed) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)', 
                    [patientName, patientID, doctorName, doctorID, doctorType, doctorAvailability, clinicName, clinicAdminID, date, time, duration, appointmentCreatedAt, painDetails, 0])
                appointmentConn.commit()

                if result:
                    newAppointments = currentAppointments + 1

                    # Update the number of appointments
                    patientCursor.execute('UPDATE patients SET NumberOfAppointments = ? WHERE Email= ?', (newAppointments, email))
                    patientConn.commit()

                patientConn.close()
                

                toplevel.attributes("-topmost",False)
                messagebox.showinfo('Success', 'Appointment successfully added.')
                toplevel.destroy()
                insertTreeview()
                
            
            else:
                toplevel.attributes("-topmost",False)
                messagebox.showerror('Error',"Please fill up all the fields.")
                if messagebox:
                    toplevel.attributes("-topmost",True)

        




        toplevel = ctk.CTkToplevel(window)
        toplevel.title("Book Appointment")
        toplevel.geometry("800x600+460+100")
        toplevel.resizable(False, False)
        toplevel.attributes("-topmost",True)
        toplevel.configure(fg_color = "#fff")

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        parentFrame = ctk.CTkScrollableFrame(toplevel, width=800, height=600, fg_color="#fff", scrollbar_fg_color="#000", scrollbar_button_color="#000",)
        parentFrame.place(x=0, y=0)

        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< TOP FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        topFrame = ctk.CTkFrame(parentFrame, width=650, height=500, fg_color="#FFFDFD" )
        topFrame.pack(side='top', fill='x', expand=False, padx=(65, 80), pady=(20,0))
        
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

        gMapsWidget = TkinterMapView(topFrame, width=650, height=400)
        gMapsWidget.pack(side='top', fill='x', expand=True, pady=(10,0), padx=(0,5))
        gMapsWidget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google normal
        gMapsWidget.set_address("Bayan Lepas, Penang, Malaysia", marker=True)
        gMapsWidget.set_zoom(12)

        # gMapsWidget.set_tile_server("https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")  # OpenStreetMap (default)
        # gMapsWidget.set_tile_server("https://mt0.google.com/vt/lyrs=s&hl=e...{x}&y={y}&z={z}&s=Ga", max_zoom=22)  # google satellite
        # gMapsWidget.set_tile_server("http://c.tile.stamen.com/watercolor/{z}/{x}/{y}.png")  # painting style
        # marker.set_text("Select A Clinic")
        

        doctorTypeLabel = ctk.CTkLabel(topFrame, text="Select Type Of Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorTypeLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
        doctorTypes = [
            "Select Type","Allergist", "Cardiologist", "Dermatologist", "Endocrinologist", 
            "Gastroenterologist", "Geriatrician", "Internist", "Nephrologist", "Neurologist", 
            "Obstetrician/Gynecologist", "Oncologist", "Ophthalmologist", "Orthopedic Surgeon", 
            "Pediatrician", "Podiatrist", "Psychiatrist", "Pulmonologist", "Rheumatologist", 
            "General Practitioner", "Family Medicine Doctor", "Home Health Care Doctor", 
            "Emergency Medicine Specialist"]
        doctorTypeDropdown = ctk.CTkComboBox(
            topFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=doctorTypes, border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        doctorTypeDropdown.pack(side='top', fill='x', expand=False, pady=(0,0), padx=(0,5))

        painDetailsLabel = ctk.CTkLabel(topFrame, text="Explain Pain Details", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        painDetailsLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
        painDetailsTextBox = ctk.CTkTextbox(
            topFrame, fg_color="#ffffff", text_color="#000000", width=648, height=88, 
            border_color="#b5b3b3", font=("Inter", 20), border_spacing=10,
            scrollbar_button_color="#1AFF75", border_width=1
        )
        painDetailsTextBox.pack(side='top', fill='none', expand=False, pady=(0, 10), anchor="w")


        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< LEFT FRAME INSDIE PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        leftFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD", )
        leftFrame.pack(side='left', fill='both', expand=False, padx=65, pady=30)

        doctorDropdownLabel = ctk.CTkLabel(leftFrame, text="Select Doctor", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        doctorDropdownLabel.pack(side='top', fill='x', expand=False,)
        doctorDropdown = ctk.CTkComboBox(
            leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=['Select Doctor', 'Maisarah Majdi', 'Someshwar Rao', 'Karen Khor Siew Li'], border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        doctorDropdown.pack(side='top', fill='x', expand=False,)

        times = [
            "Select Time",'9:00 AM', '10:00 AM', '11:00 AM', 
            '12:00 PM', '1:00 PM', '2:00 PM', '3:00 PM', '4:00 PM', '5:00 PM', 
            '6:00 PM', '7:00 PM', '8:00 PM', '9:00 PM', '10:00 PM', '11:00 PM',
            '12:00 AM', '1:00 AM', '2:00 AM', '3:00 AM', '4:00 AM', '5:00 AM', 
            '6:00 AM', '7:00 AM', '8:00 AM'
        ]
        consultationTimeDropdownLabel = ctk.CTkLabel(leftFrame, text="Select Consultation Time", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        consultationTimeDropdownLabel.pack(side='top', fill='x', expand=False, pady=(150,0))
        consultationTimeDropdown = ctk.CTkComboBox(
            leftFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=times, border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        consultationTimeDropdown.pack(side='top', fill='x', expand=False,)

        # Cancel Button with Icon
        cancelIconPath = relative_to_assets("reject-icon.png")
        cancelIcon = ctk.CTkImage(light_image=Image.open(cancelIconPath), size=(33,33),)
        cancelButton = ctk.CTkButton(
            leftFrame, text=" Cancel ", width=280, height=60, 
            font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=cancelIcon,
            command=toplevel.destroy # anchor=ctk.W 
        )
        cancelButton.pack(side='top', fill='x', expand=False,pady=(40,15))


        # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< RIGHT FRAME INSIDE PARENT SCROLLABLE FRAME >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        rightFrame = ctk.CTkFrame(parentFrame, width=341, height=500, fg_color="#FFFDFD",)
        rightFrame.pack(side='left', fill='both', expand=False, padx=(0,0), pady=30)
        

        # Select Consultation Date Widget
        consultationDateLabel = ctk.CTkLabel(rightFrame, text="Select Consultation Date", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        consultationDateLabel.pack(side='top', fill='x', expand=False,)
        calendar = Calendar(
            rightFrame, selectmode="day", year=thisYear, font=("Inter", 12),
            month=thisMonth, day=todayInt, background="#1AFF75", 
            selectbackground="#36D8B7", foreground="black"
        )
        calendar.pack(side='top', fill='x', expand=False,)

         # Select Consultation Duration Dropdown Menu
        durationArray = [
            'Select Duration', '1 hour', '1 hour 30 Minutes',
            '2 hours', '2 hours 30 Minutes', '3 hours', '3 hour 30 Minutes', '4 hours', 
            '4 hours 30 Minutes', '5 hours'
        ]
        consultationDurationDropdownLabel = ctk.CTkLabel(rightFrame, text="Select Consultation Duration", font=("Inter", 16, "bold",), anchor=ctk.W, text_color="#000000",)
        consultationDurationDropdownLabel.pack(side='top', fill='x', expand=False, pady=(30,0))
        consultationDurationDropdown = ctk.CTkComboBox(
            rightFrame, fg_color="#ffffff", text_color="#000000", width=295, height=48, 
            font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
            values=durationArray, border_color="#b5b3b3", border_width=1,
            dropdown_font=("Inter", 20), dropdown_fg_color='#fff', 
            dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
        )
        consultationDurationDropdown.pack(side='top', fill='x', expand=False,)

        # Book Button 2 with Icon
        approveIconPath = relative_to_assets("approve-icon.png")
        approveIcon = ctk.CTkImage(light_image=Image.open(approveIconPath), size=(33,33),)
        bookButton2 = ctk.CTkButton(
            rightFrame, text=" Book Appointment", width=280, height=60, 
            font=("Inter", 22, "bold",), fg_color="#17D463", hover_color="#009B2B", image=approveIcon,
            command=bookAppointment # anchor=ctk.W 
        )
        bookButton2.pack(side='top', fill='x', expand=False,pady=(40,15))
        # bookButton2.bind("<Button-1>", command=bookAppointment)


    global count
    count = 0
    def insertTreeview(array=None):
        global count

        # Connecting to Patients DB
        patientConn = sqlite3.connect('patients.db')
        patientCursor = patientConn.cursor()
        patientCursor.execute('SELECT * FROM patients WHERE Email=?', [email])
        result = patientCursor.fetchone()
        patientID = result[0] # Getting Patient's ID
        numOfAppointments = result[8] # Getting Patient's number of appointments
        

        # Connecting to Appointments DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        appointmentCursor.execute('SELECT * FROM appointments WHERE PatientID=?', [patientID])
        appointments = appointmentCursor.fetchall()
        table.delete(*table.get_children())


        # Executed when searchbar is entered
        if array is None:
            for appointment in appointments:
                appointmentID = appointment[0]
                clinicName = appointment[7]
                doctorType = appointment[5]
                doctorName = appointment[3]
                date = appointment[9]
                time = appointment[10]
                dateAndTime = f'{date} ({time})'
                duration = appointment[11]
                if appointment[14] == 0:
                    isConfirmed = 'Waiting For Confirmation'
                elif appointment[14] == 1:
                    isConfirmed = 'Confirmed'
                elif appointment[14] == 2:
                    isConfirmed = 'Rejected'
                else:
                    isConfirmed = 'Doctor Replaced'
                

                data = (numOfAppointments, clinicName, doctorName, dateAndTime, duration, isConfirmed, appointmentID)


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
                clinicName = appointment[7]
                doctorType = appointment[5]
                doctorName = appointment[3]
                date = appointment[9]
                time = appointment[10]
                dateAndTime = f'{date} {time}'
                duration = appointment[11]
                if appointment[14] == 0:
                    isConfirmed = 'Waiting For Confirmation'
                elif appointment[14] == 1:
                    isConfirmed = 'Confirmed'
                elif appointment[14] == 2:
                    isConfirmed = 'Rejected'
                else:
                    isConfirmed = 'Doctor Replaced'
                

                data = (numOfAppointments, clinicName, doctorName, dateAndTime, duration, isConfirmed, appointmentID)


                if count % 2 == 0:
                    table.insert(parent='', index='end', values=data, tags=("evenrow",))
                    print(appointment)
                else:
                    table.insert(parent='', index='end', values=data, tags=("oddrow",))


                count += 1


    def searchBy():
        # Connecting to Appointment DB
        appointmentConn = sqlite3.connect('appointments.db')
        appointmentCursor = appointmentConn.cursor()
        searchTerm = searchInputTextBox.get('0.0', 'end').strip()
        print(searchTerm)
        searchOption = searchByDropdown.get()

        if searchOption == 'Clinic Name':
            searchOption = "ClinicName"
        elif searchOption == 'Doctor Name':
            searchOption = "DoctorName"
        elif searchOption == 'Date & Time':
            searchOption = "AppointmentDate"
        elif searchOption == 'Duration':
            searchOption = "AppointmentDuration"
        elif searchOption == 'Confirmation Status':
            searchOption = "IsConfirmed"

            if searchTerm == 'Waiting For Confirmation':
                searchTerm = '0'
            elif searchTerm == 'Confirmed':
                searchTerm = '1'
            elif searchTerm == 'Rejected':
                searchTerm = '2'
            else:
                searchTerm = '3'


        if searchTerm == "":
            messagebox.showerror('Error', 'Enter value to search.')
        elif searchOption == 'Search By Option':
            messagebox.showerror('Error', 'Please select an option.')
        else:
            appointmentCursor.execute(f'SELECT * FROM appointments WHERE {searchOption}=?', (searchTerm,))
            result = appointmentCursor.fetchall()
            insertTreeview(result)    


    def deleteAppointment():  
        
        selectedItem = table.focus()
        if not selectedItem:
            messagebox.showerror('Error', 'Select an Appointment first.')
            return
        
        appointmentData = table.item(selectedItem)["values"]
        print(appointmentData)
        appointmentID = appointmentData[6]
        print(appointmentID)

        msg = messagebox.askokcancel('Warning', 'Are you sure you want to delete your appointment?')
            

        if msg:
            appointmentCursor.execute('DELETE FROM appointments WHERE AppointmentID = ?', (appointmentID,))
            appointmentConn.commit()
            messagebox.showinfo('Success', 'Appointment deleted successfully.')
            insertTreeview()
        else:
            return
            
        


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


    # Search Box Dropdown Menu 
    searchByDropdown = ctk.CTkComboBox(
        whiteFrame, fg_color="#ffffff", text_color="#000000", width=252, height=50, 
        font=("Inter", 20), button_color='#1AFF75', button_hover_color='#36D8B7',
        values=['Search By Option', 'Clinic Name', 'Doctor Name', 'Date & Time', "Duration", 'Confirmation Status'], border_color="#000", border_width=1,
        dropdown_font=("Inter", 20), dropdown_fg_color='#fff',
        dropdown_text_color='#000', dropdown_hover_color='#1AFF75', hover=True,
    )
    searchByDropdown.place(x=25, y=290)

    # Search Box field 
    searchInputTextBox = ctk.CTkTextbox(
        whiteFrame, fg_color="#ffffff", text_color="gray", width=725, height=50, 
        border_color="#000", font=("Inter", 21), border_spacing=8,
        scrollbar_button_color="#1AFF75", border_width=2,
    )
    searchInputTextBox.insert('insert', "Search by Appointment Details")
    searchInputTextBox.place(x=293, y=290)
    searchInputTextBox.bind("<FocusIn>", searchbarFocus)
    searchInputTextBox.bind("<FocusOut>", searchbarOutFocus)


    # Search Button with Icon
    searchIconPath = relative_to_assets("search-icon-1.png")
    searchIcon = ctk.CTkImage(light_image=Image.open(searchIconPath), size=(25,25),)
    searchButton = ctk.CTkButton(
        whiteFrame, text="", width=50, height=50, 
        font=("Inter", 22, "bold",), fg_color="#000", hover_color="#333333", image=searchIcon, 
        corner_radius=0, command=searchBy # anchor=ctk.W 
    )
    searchButton.place(x=918, y=290)


    # Cancel Search Button with Icon
    cancelSearchIconPath = relative_to_assets("reject-icon.png")
    cancelSearchIcon = ctk.CTkImage(light_image=Image.open(cancelSearchIconPath), size=(30,30),)
    cancelSearchButton = ctk.CTkButton(
        whiteFrame, text="", width=51, height=50, 
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=cancelSearchIcon, corner_radius=0,
        command=insertTreeview # anchor=ctk.W 
    )
    cancelSearchButton.place(x=966, y=290)

    # Book Appointment Button with Icon
    appointmentIconPath = relative_to_assets("add-icon.png")
    appointmentIcon = ctk.CTkImage(light_image=Image.open(appointmentIconPath), size=(28,28),)
    bookButton = ctk.CTkButton(
        whiteFrame, text=" Book Appointment", width=290, height=48, 
        font=("Inter", 22, "bold",), fg_color="#17D463", hover_color="#009B2B", image=appointmentIcon,
        command=bookAppointmentTopLevel # anchor=ctk.W 
    )
    bookButton.place(x=25, y=225)

    # Update Appointment Details Button with Icon
    updateIconPath = relative_to_assets("update-icon.png")
    updateIcon = ctk.CTkImage(light_image=Image.open(updateIconPath), size=(33,33),)
    updateButton = ctk.CTkButton(
        whiteFrame, text=" Update Appointment Details", height=48, width=378,
        font=("Inter", 22, "bold",), fg_color="#1BC5DC", hover_color="#1695A7", image=updateIcon,
        command=updateAppointmentTopLevel # anchor=ctk.W 
    )
    updateButton.place(x=333, y=225)

    # Delete Appointment Button with Icon
    deleteIconPath = relative_to_assets("delete-icon.png")
    deleteIcon = ctk.CTkImage(light_image=Image.open(deleteIconPath), size=(26,26),)
    deleteButton = ctk.CTkButton(
        whiteFrame, text=" Delete Appointment", height=48, width=290,
        font=("Inter", 22, "bold",), fg_color="#E00000", hover_color="#AE0000", image=deleteIcon,
        command=deleteAppointment # anchor=ctk.W 
    )
    deleteButton.place(x=728, y=225)

    
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
        'No', 'Clinic Name',"Doctor Name", "Date & Time", 
        "Duration", "Confirmation Status", "Appointment ID"
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
    table.heading('Clinic Name', text='Clinic Name')
    #table.heading('Doctor Type', text='Doctor Type')
    table.heading('Doctor Name', text='Doctor Name')
    table.heading('Date & Time', text='Date & Time')
    table.heading('Duration', text='Duration')
    table.heading('Confirmation Status', text='Confirmation Status')

    # Treeview Table Columns Details
    table.column("#0", width=0, stretch=ctk.NO)
    table.column("No", width=43, anchor=ctk.CENTER)
    table.column("Clinic Name",width=250, anchor=ctk.CENTER)
    #table.column("Doctor Type", anchor=ctk.CENTER)
    table.column("Doctor Name", width=265, anchor=ctk.CENTER)
    table.column("Date & Time", width=200, anchor=ctk.CENTER,)
    table.column("Duration",anchor=ctk.CENTER,)
    table.column("Confirmation Status", width=260, anchor=ctk.CENTER)
    table.column("Appointment ID", width=0, stretch=ctk.NO)

    # Setting alternating colours for the rows in Treeview
    table.tag_configure("oddrow", background="#F2F5F8")
    table.tag_configure("evenrow", background="#B4EFF7")


    
    insertTreeview()

    window.mainloop()


# Only execute the Patient Dashboard Window if this script is run directly
if __name__ == "__main__":
    patientDashboardWindow(email=None)