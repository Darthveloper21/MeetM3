from Table.SubmitForm import *


class TableWindow:
    window: Toplevel
    root: Frame
    width: int
    height: int
    table: Table
    updateForm: SubmitForm
    addForm: SubmitForm

    def __init__(self, root, title, width, height):
        self.root = root
        self.window = Toplevel(root)
        self.window.title(title)
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
        self.window.withdraw()

        self.nameVar = StringVar()
        self.keyVar = StringVar()

    def placing(self, table):
        self.table = table
        self.table.create()

        # navigate bar

        navigateFrame = Frame(self.window, bg='white')
        navigateFrame.pack(side='bottom', ipady=2)

        pageStyle = ttk.Style()
        pageStyle.configure('No.TButton', font=('Open Sans Regular', 8))

        navigateLen = self.table.full_size

        leftButton = ttk.Button(navigateFrame, text='|<', width=10, style='No.TButton')
        leftButton.config(command=lambda: self.table.update(0, 10))
        leftButton.grid(row=0, column=0)
        rightButton = ttk.Button(navigateFrame, text='>|', width=10, style='No.TButton')
        rightButton.config(command=lambda: self.table.update(navigateLen - 10, 10))
        rightButton.grid(row=0, column=4)

        prevButton = ttk.Button(navigateFrame, text='<<', width=10, style='No.TButton')
        prevButton.config(command=lambda: self.table.update(self.table.offset - 10, 10))
        prevButton.grid(row=0, column=1)
        nextButton = ttk.Button(navigateFrame, text='>>', width=10, style='No.TButton')
        nextButton.config(command=lambda: self.table.update(self.table.offset + 10, 10))
        nextButton.grid(row=0, column=3)

        # tool bar

        toolBar = Frame(self.window, bg='white')
        toolBar.place(x=10, y=10)

        nameLabel = Label(toolBar, text='Name: ', width=5, bg='white')
        nameLabel.grid(row=0, column=0)
        nameEntry = Entry(toolBar, textvariable=self.nameVar, font=('Arial', 10), width=15, bd=1, relief='solid')
        nameEntry.grid(row=0, column=1)
        keyLabel = Label(toolBar, text='Key: ', width=5, bg='white')
        keyLabel.grid(row=0, column=2)
        keyEntry = Entry(toolBar, textvariable=self.keyVar, font=('Arial', 10), width=10, bd=1, relief='solid')
        keyEntry.grid(row=0, column=3)

        searchStyle = ttk.Style()
        searchStyle.configure('Search.TButton', font=('Arial', 8), background='#AFFEFF')

        searchButton = ttk.Button(toolBar, text='Search!', style='Search.TButton')
        searchButton.config(command=self.searchCommand)
        searchButton.grid(row=0, column=4, padx=5)

        delButton = ttk.Button(toolBar, text='Delete', style='Search.TButton')
        delButton.config(command=self.deleteCommand)
        delButton.grid(row=0, column=5)

        updateButton = ttk.Button(toolBar, text='Update', style='Search.TButton')
        updateButton.config(command=self.updateCommand)
        updateButton.grid(row=0, column=6, padx=5)

        if isinstance(self.table, AppointmentsTable):
            formHeight = 200
        elif isinstance(self.table, OwnersTable):
            formHeight = 260
        elif isinstance(self.table, PetsTable):
            formHeight = 220
        else:
            formHeight = 260

        self.updateForm = SubmitForm(self.window, 300, formHeight, self.table, 'update')
        self.updateForm.placing()

        addButton = ttk.Button(toolBar, text='Add row', style='Search.TButton')
        addButton.config(command=self.addCommand)
        addButton.grid(row=0, column=7)

        self.addForm = SubmitForm(self.window, 300, formHeight, self.table, 'add')
        self.addForm.placing()

    def addCommand(self):
        self.addForm.clearForm()
        self.addForm.show()

    def updateCommand(self):
        key = self.table.getSelectedKeys()

        if len(key) > 1:
            messagebox.showerror('Error', 'Can only update one row at a time !')
            self.window.focus()
        elif len(key) == 0:
            messagebox.showerror('Error', 'You must select one row to update !')
            self.window.focus()
        else:
            self.updateForm.clearForm()
            self.updateForm.getKeys()
            self.updateForm.show()

    def deleteCommand(self):
        checkList = self.table.getCheckList()
        cnt = 0
        for x in checkList:
            if x != 0:
                cnt += 1

        if len(self.table.df.index) == 0 or cnt == 0:
            messagebox.showerror('Error', 'Select one or multiple rows to delete')
            self.window.focus()
            return
        else:
            res = messagebox.askyesno('Confirmation', 'This action will delete all the related information '
                                                      'with the selected rows (Example: delete owners will '
                                                      'delete all information about their pets but delete a '
                                                      'meetings do not affect others) and cannot be undone, proceed ?')
            if res is True:
                self.table.delete()
        self.window.focus()

    def searchCommand(self):
        name = self.nameVar.get()
        key = self.keyVar.get()
        self.table.update(0, 10, name=name, key=key)

    def navigateCommand(self, offset):
        self.table.update(offset, 10)

    def show(self):
        self.window.deiconify()

    def hide(self):
        self.updateForm.hide()
        self.addForm.hide()
        self.window.withdraw()
