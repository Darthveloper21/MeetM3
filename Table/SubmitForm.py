from Table.table import *
from tkinter import messagebox
from datetime import datetime
import re


def checkDateTime(date_time):
    try:
        datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False


def checkDate(date):
    try:
        datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def checkMail(email):
    if email == '':
        return True

    regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if re.search(regex, email):
        return True
    else:
        return False


def checkNumeric(numeric):
    regex = '^[0-9]+$'
    if re.search(regex, str(numeric)):
        return True
    else:
        return False


def checkPhone(pnum):
    if pnum == '':
        return True

    regex = '[a-zA-Z]'
    if re.search(regex, pnum):
        return False
    else:
        return True


class SubmitForm:
    window: Toplevel
    root: Frame
    width: int
    height: int
    table: Table
    table_type: str
    action: str
    attributes: []
    attEntries: []
    attvars: []
    updateKey: str
    statusBox: ttk.Combobox

    def __init__(self, root, width, height, table, action):
        self.root = root
        self.window = Toplevel(root)
        self.window.title(action)
        self.window.protocol('WM_DELETE_WINDOW', self.hide)
        self.width = width
        self.height = height
        SCREEN_WIDTH = self.window.winfo_screenwidth()
        SCREEN_HEIGHT = self.window.winfo_screenheight()
        POS_X = SCREEN_WIDTH / 2 - self.width / 2  # position x
        POS_Y = SCREEN_HEIGHT / 3 - self.height / 3  # position y
        self.window.configure(bg='#FFFFFF')
        self.window.resizable(False, False)
        self.window.geometry('%dx%d+%d+%d' % (self.width, self.height, POS_X, POS_Y))
        self.hide()
        self.table = table
        self.action = action

        self.attvars = []
        for i in range(0, 10):
            tmp = StringVar()
            self.attvars.append(tmp)
        self.attEntries = []
        self.statusBox = ttk.Combobox()

        if isinstance(table, AppointmentsTable):
            self.table_type = 'appointment'
            self.attributes = ['Expected date (*): ', 'Pet ID (*): ', 'Doctor ID (*): ', 'Status (*): ']
        elif isinstance(table, OwnersTable):
            self.table_type = 'owner'
            self.attributes = ['SSN (*): ', 'First name (*): ', 'Last name (*): ',
                               'Date of birth (*): ', 'Phone number: ', 'email: ']
        elif isinstance(table, PetsTable):
            self.table_type = 'pet'
            self.attributes = ['Pet ID (*): ', 'Pet name (*): ', 'Date of birth (*): ',
                               'pet_type (*): ', 'Owner SSN (*): ']
        else:
            self.table_type = 'doctor'
            self.attributes = ['Doctor ID (*): ', 'First name (*): ', 'Last name (*): ',
                               'Date of birth (*): ', 'Phone number: ', 'email: ']

    def placing(self):
        formFrame = Frame(self.window, bg='white')
        formFrame.pack(side=TOP)

        lenAtt = len(self.attributes)
        if self.table_type == 'appointment':
            lenAtt -= 1
            statuses = ['pending', 'canceled', 'finished']

            self.statusBox = ttk.Combobox(formFrame, values=statuses)
            self.statusBox.set(statuses[0])
            self.statusBox.config(state='readonly')
            self.statusBox.grid(row=lenAtt, column=1, padx=5, pady=5)

        for i in range(0, lenAtt):
            attLabel = Label(formFrame, text=self.attributes[i], width=15, bg='white', anchor='w')
            attLabel.grid(row=i, column=0, padx=5, pady=5)

            self.attEntries.append(Entry(formFrame, textvariable=self.attvars[i], font=('Arial', 10),
                                         width=20, bd=1, relief='solid'))
            self.attEntries[i].grid(row=i, column=1, padx=5, pady=5)

        noteLabel = Label(self.window, text='Fields with (*) require information', bg='white')
        noteLabel.pack(side=TOP, pady=5)

        submitStyle = ttk.Style()
        submitStyle.configure('Submit.TButton', font=('Arial', 10), background='#AFFEFF')
        submitButton = ttk.Button(self.window, text='submit', style='Submit.TButton', command=self.submit)
        submitButton.pack(side=BOTTOM, pady=5)

    def clearForm(self):
        for i in range(0, len(self.attEntries)):
            self.attEntries[i].delete(0, 'end')

    def getKeys(self):
        self.updateKey = self.table.getSelectedKeys()[0]
        print(self.updateKey)

        if self.table_type == 'appointment':
            appt = normalAppointment(self.updateKey)
            for i in range(0, len(appt) - 1):
                self.attEntries[i].delete(0, 'end')
                self.attEntries[i].insert(0, appt[i])
                # self.attvars[i] = StringVar().set(appt[0])
        elif self.table_type == 'owner':
            owner = normalOwner(self.updateKey)
            for i in range(0, len(owner)):
                self.attEntries[i].delete(0, 'end')
                self.attEntries[i].insert(0, owner[i])
                # self.attvars[i] = StringVar().set(owner[0])
        elif self.table_type == 'pet':
            pet = normalPet(self.updateKey)
            for i in range(0, len(pet)):
                self.attEntries[i].delete(0, 'end')
                self.attEntries[i].insert(0, pet[i])
                # self.attvars[i] = StringVar().set(pet[0])
        else:
            doctor = normalDoctor(self.updateKey)
            for i in range(0, len(doctor)):
                self.attEntries[i].delete(0, 'end')
                self.attEntries[i].insert(0, doctor[i])
                # self.attvars[i] = StringVar().set(doctor[0])

    def submit(self):
        key = self.table.getSelectedKeys()[0]

        lenAtt = len(self.attributes)
        if self.table_type == 'appointment':
            lenAtt -= 1

        for i in range(0, lenAtt):
            print(self.attvars[i].get())
            if '*' in self.attributes[i] and self.attvars[i].get() == '':
                messagebox.showerror('Error', 'Fields with (*) require information')
                return

        if self.table_type == 'appointment':
            if checkDateTime(self.attvars[0].get()) is False:
                messagebox.showerror('Error', 'Expected Date must be in year-month-date hour:minute:second format')
                return
            if normalPet(self.attvars[1].get()) is None:
                messagebox.showerror('Error', 'No pet found')
                return
            if normalDoctor(self.attvars[2].get()) is None:
                messagebox.showerror('Error', 'No doctor found')
                return
        elif self.table_type == 'owner' or self.table_type == 'doctor':
            if checkNumeric(self.attvars[0].get()) is False:
                messagebox.showerror('Error', 'SSN must be a numeric value')
                return
            if checkDate(self.attvars[3].get()) is False:
                messagebox.showerror('Error', 'Date of birth must be in year-month-date format')
                return
            if checkPhone(self.attvars[4].get()) is False:
                messagebox.showerror('Error', 'Phone number field must be a phone number')
                return
            if checkMail(self.attvars[5].get()) is False:
                messagebox.showerror('Error', 'Email field must follow email format')
                return
        else:
            if checkNumeric(self.attvars[0].get()) is None:
                messagebox.showerror('Error', 'Pet ID must be a numeric value')
                return
            if checkDate(self.attvars[2].get()) is False:
                messagebox.showerror('Error', 'Date of birth must be in year-month-date format')
                return
            if normalOwner(self.attvars[4].get()) is None:
                messagebox.showerror('Error', 'No Owner found')
                return

        if self.action == 'update':
            if self.table_type == 'appointment':
                updateAppointment(key, new_date=self.attvars[0].get(), new_pet_id=self.attvars[1].get(),
                                  new_doctor_id=self.attvars[2].get(), new_status=self.statusBox.get())
            elif self.table_type == 'owner':
                updateOwner(key, new_ssn=self.attvars[0].get(), fname=self.attvars[1].get(),
                            lname=self.attvars[2].get(), dob=self.attvars[3].get(),
                            pnum=self.attvars[4].get(), email=self.attvars[5].get())
            elif self.table_type == 'pet':
                updatePet(key, pet_id=self.attvars[0].get(), pet_name=self.attvars[1].get(), dob=self.attvars[2].get(),
                          self.attvars[3].get(), owner_ssn=self.attvars[4].get())
            else:
                updateDoctor(self.attvars[0].get(), self.attvars[1].get(), self.attvars[2].get(), self.attvars[3].get(),
                             pnum=self.attvars[4].get(), email=self.attvars[5].get())

        if self.action == 'add':
            if self.table_type == 'appointment':
                addAppointment(self.attvars[0].get(), self.attvars[1].get(),
                               self.attvars[2].get(), self.statusBox.get())
            elif self.table_type == 'owner':
                addOwner(self.attvars[0].get(), self.attvars[1].get(), self.attvars[2].get(), self.attvars[3].get(),
                         pnum=self.attvars[4].get(), email=self.attvars[5].get())
            elif self.table_type == 'pet':
                addPet(self.attvars[0].get(), self.attvars[1].get(), self.attvars[2].get(),
                       self.attvars[3].get(), self.attvars[4].get())
            else:
                addDoctor(self.attvars[0].get(), self.attvars[1].get(), self.attvars[2].get(), self.attvars[3].get(),
                          pnum=self.attvars[4].get(), email=self.attvars[5].get())
        messagebox.showinfo('Success', self.action + ' row successfully')
        self.hide()

    def show(self):
        self.window.grab_set()
        self.window.deiconify()

    def hide(self):
        self.window.grab_release()
        self.window.withdraw()
