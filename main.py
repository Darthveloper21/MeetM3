from Table.windowTable import *

window = Tk()

window.title("MeetM3")

''' window setup '''
SCREEN_WIDTH = window.winfo_screenwidth()
SCREEN_HEIGHT = window.winfo_screenheight()
WINDOW_WIDTH = 300
WINDOW_HEIGHT = 200

POS_X = SCREEN_WIDTH / 20 - WINDOW_WIDTH / 20     # position x
POS_Y = SCREEN_HEIGHT / 15 - WINDOW_HEIGHT / 15   # position y

window.configure(bg='#FFFFFF')
window.resizable(False, False)
window.geometry('%dx%d+%d+%d' % (WINDOW_WIDTH, WINDOW_HEIGHT, POS_X, POS_Y))
''' finish window setup'''


def showAppointmentWindow():
    global appointmentWindow
    appointmentWindow.show()


def showOwnerWindow():
    global ownerWindow
    ownerWindow.show()


def showPetWindow():
    global petWindow
    petWindow.show()


def showDoctorWindow():
    global doctorWindow
    doctorWindow.show()


# spreadsheet interface

helloLabel = Label(window, text="Hello hvn2001! how you doing ?", bg='white', font=('Arial Bold', 10))
helloLabel.pack(anchor='n')

buttonFrame = Frame(window, bg='WHITE')
buttonFrame.pack(anchor='center', pady=10)

style = ttk.Style()
style.configure('TButton', font=('Open Sans Regular', 12))

appointmentsButton = ttk.Button(buttonFrame, text="Appointments information",
                                width=30, style='TButton', command=showAppointmentWindow)
appointmentsButton.grid(row=0, column=0, pady=2)

ownerButton = ttk.Button(buttonFrame, text="Owners information",
                         width=30, style='TButton', command=showOwnerWindow)
ownerButton.grid(row=1, column=0, pady=2)

petsButton = ttk.Button(buttonFrame, text="Pets information",
                        width=30, style='TButton', command=showPetWindow)
petsButton.grid(row=2, column=0, pady=2)

doctorButton = ttk.Button(buttonFrame, text="Doctors information",
                          width=30, style='TButton', command=showDoctorWindow)
doctorButton.grid(row=3, column=0, pady=2)

appointmentWindow = TableWindow(window, "Appointments", 1040, 310)
ownerWindow = TableWindow(window, "Owners", 840, 310)
petWindow = TableWindow(window, "Pets", 760, 310)
doctorWindow = TableWindow(window, "Doctors", 860, 310)

appointmentTable = AppointmentsTable(appointmentWindow.window, 0, 10, 10, 40)
ownerTable = OwnersTable(ownerWindow.window, 0, 10, 10, 40)
petTable = PetsTable(petWindow.window, 0, 10, 10, 40)
doctorTable = DoctorsTable(doctorWindow.window, 0, 10, 10, 40)

appointmentWindow.placing(appointmentTable)
ownerWindow.placing(ownerTable)
petWindow.placing(petTable)
doctorWindow.placing(doctorTable)

window.mainloop()
