from tkinter import *
from tkinter import ttk

from Database.database import *


class Table:
    root: Frame
    tableFrame: Frame
    selectButtons: list
    checkState: list
    df: pd.DataFrame
    widths: list
    justifies: list
    px: int
    py: int
    tableWidth: int
    tableHeight: int
    row_len: int
    col_len: int
    full_size: int
    offset: int

    def __init__(self, root, df: pd.DataFrame, widths, justifies, px=None, py=None):
        self.root = root
        self.px = px
        self.py = py
        self.df = df
        self.widths = widths
        self.justifies = justifies
        self.createFrame()
        self.tableWidth = 0
        self.row_len = len(self.df.index)
        self.col_len = len(self.df.columns)

        for i in widths:
            self.tableWidth += i + 50
        self.tableHeight = 300

        self.selectButtons = [None] * 1000
        self.checkState = [None] * 1000

        for i in range(0, self.row_len + 1):
            self.checkState[i] = IntVar()
            self.checkState[i].set(0)

    def createFrame(self):
        # self.tableFrame = Frame(self.root, highlightbackground="black", highlightcolor="black", highlightthickness=1)
        self.tableFrame = Frame(self.root)
        if self.px is not None or self.py is not None:
            self.tableFrame.place(x=self.px, y=self.py)
        else:
            self.tableFrame.pack(anchor='center')

    def create(self):
        self.createFrame()
        columns = self.df.columns

        font_col = ("Arial Bold", 10)
        font_row = ("Arial", 10)

        noEntry = Entry(self.tableFrame, font=font_col, bd=1, justify=CENTER, width=3, relief="flat")
        noEntry.insert(0, 'No.')
        noEntry.config(state="readonly", readonlybackground="#AFFEFF")
        noEntry.grid(column=1, row=0)
        for i in range(0, self.col_len):
            col_name = columns[i]
            col_justify = self.justifies[i]
            col_width = self.widths[i]
            col_entry = Entry(self.tableFrame, font=font_col, bd=1,
                              justify=col_justify, width=col_width, relief="flat")
            col_entry.insert(0, col_name)
            col_entry.config(state="readonly", readonlybackground="#AFFEFF")
            col_entry.grid(column=i + 2, row=0)

        for i in range(0, 10):
            noRowEntry = Entry(self.tableFrame, font=font_col, bd=1, justify=CENTER, width=3, relief="flat")
            numberOrdered = i + 1 + self.offset
            if numberOrdered > 0:
                noRowEntry.insert(0, str(numberOrdered))
            noRowEntry.config(state="readonly", readonlybackground="white")
            noRowEntry.grid(column=1, row=i + 1)
            for j in range(0, self.col_len):
                col_justify = self.justifies[j]
                col_width = self.widths[j]
                row_entry = Entry(self.tableFrame, font=font_row, bd=1,
                                  justify=col_justify, width=col_width, relief="flat")

                if i < self.row_len:
                    value = str(self.df.iloc[i, j])
                    row_entry.insert(0, value)

                row_entry.config(state="readonly", readonlybackground="white")
                row_entry.grid(column=j + 2, row=i + 1)

        for i in range(0, 11):
            self.selectButtons[i] = ttk.Checkbutton(self.tableFrame, variable=self.checkState[i],
                                                    takefocus=0, command=self.antiSelectAll)
            if i > self.row_len:
                self.selectButtons[i].config(state='disabled')
            self.selectButtons[i].grid(column=0, row=i)
        self.selectButtons[0].config(command=self.selectAll)

    def antiSelectAll(self):
        getSelects = self.getCheckList()
        cnt = 0
        for i in getSelects:
            if i == 1:
                cnt += 1
        if cnt < self.row_len:
            self.checkState[0].set(0)
        else:
            self.checkState[0].set(1)

    def deSelectAll(self):
        for i in range(0, self.row_len + 1):
            self.checkState[i].set(0)

    def selectAll(self):
        if self.row_len == 1:
            self.checkState[1].set(1 - self.checkState[1].get())
            return

        getSelects = self.getCheckList()
        cnt = 0
        for i in getSelects:
            if i == 1:
                cnt += 1

        for i in range(1, self.row_len + 1):
            if cnt == self.row_len or cnt == 0:
                self.checkState[i].set(1 - self.checkState[i].get())
            else:
                self.checkState[i].set(1)

    def getCheckList(self):
        checklist = []
        for i in range(1, self.row_len + 1):
            checklist.append(self.checkState[i].get())
        return checklist

    def getSelectedKeys(self):
        checklist = self.getCheckList()
        selectedKeys = []
        for i in range(0, len(checklist)):
            if checklist[i] == 1:
                selectedKeys.append(self.df.iloc[i, 0])
        return selectedKeys

    def delete(self):
        pass
        # selected = self.getSelectedKeys()
        # print(selected)
        # interface

    def update(self, offset, limit, name=None, key=None):
        if offset < 0:
            offset = 0

        if offset > self.full_size - 10:
            offset = max(0, self.full_size - 10)
        self.offset = offset

    def destroy(self):
        if self.tableFrame is not None:
            self.tableFrame.destroy()


class OwnersTable(Table):

    def __init__(self, root, offset, limit, px=None, py=None):
        self.offset = offset
        widths = [15, 15, 15, 15, 15, 25, 6]
        justifies = [CENTER, LEFT, LEFT, LEFT, LEFT, LEFT, LEFT]
        owners = getOwners(offset, limit)
        self.full_size = len(getOwners(0, 1000).index)
        super().__init__(root, owners, widths, justifies, px, py)

    def update(self, offset, limit, name=None, key=None):
        super().update(offset, limit)
        self.destroy()
        self.df = getOwners(self.offset, limit, name=name, ssn=key)
        self.row_len = len(self.df.index)
        self.create()

    def delete(self):
        super().delete()
        selectedKeys = super().getSelectedKeys()
        for key in selectedKeys:
            delOwner(key)
        self.update(0, 10)
        super().deSelectAll()


class AppointmentsTable(Table):

    def __init__(self, root, offset, limit, px=None, py=None):
        self.offset = offset
        widths = [10, 20, 10, 20, 15, 20, 10, 20, 8]
        justifies = [CENTER, LEFT, CENTER, LEFT, CENTER, LEFT, CENTER, LEFT, LEFT]
        appointments = getAppointments(offset, limit)
        self.full_size = len(getAppointments(0, 1000).index)
        super().__init__(root, appointments, widths, justifies, px, py)

    def update(self, offset, limit, name=None, key=None):
        super().update(offset, limit)
        self.destroy()
        self.df = getAppointments(self.offset, limit, name=name, appt_id=key)
        self.row_len = len(self.df.index)
        self.create()

    def delete(self):
        super().delete()
        selectedKeys = super().getSelectedKeys()
        for key in selectedKeys:
            delAppointment(key)
        self.update(0, 10)
        super().deSelectAll()


class PetsTable(Table):

    def __init__(self, root, offset, limit, px=None, py=None):
        self.offset = offset
        widths = [10, 20, 15, 10, 20, 20]
        justifies = [CENTER, LEFT, LEFT, LEFT, CENTER, LEFT]
        pets = getPets(offset, limit)
        self.full_size = len(getPets(0, 1000).index)
        super().__init__(root, pets, widths, justifies, px, py)

    def update(self, offset, limit, name=None, key=None):
        super().update(offset, limit)
        self.destroy()
        self.df = getPets(self.offset, limit, name=name, pet_id=key)
        self.row_len = len(self.df.index)
        self.create()

    def delete(self):
        super().delete()
        selectedKeys = super().getSelectedKeys()
        for key in selectedKeys:
            delPet(key)
        self.update(0, 10)
        super().deSelectAll()


class DoctorsTable(Table):

    def __init__(self, root, offset, limit, px=None, py=None):
        self.offset = offset
        widths = [10, 15, 15, 15, 15, 30, 10]
        justifies = [CENTER, LEFT, LEFT, LEFT, LEFT, LEFT, LEFT]
        doctors = getDoctors(offset, limit)
        self.full_size = len(getDoctors(0, 1000).index)
        super().__init__(root, doctors, widths, justifies, px, py)

    def update(self, offset, limit, name=None, key=None):
        super().update(offset, limit)
        self.destroy()
        self.df = getDoctors(self.offset, limit, name=name, doctor_id=key)
        self.row_len = len(self.df.index)
        self.create()

    def delete(self):
        super().delete()
        selectedKeys = super().getSelectedKeys()
        for key in selectedKeys:
            delDoctor(key)
        self.update(0, 10)
        super().deSelectAll()
