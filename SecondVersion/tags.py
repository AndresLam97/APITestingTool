import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter.filedialog as tkDialog
import Controller
import AddDataFrame

class App:
    def __init__(self):
        self.root = tk.Tk()
        self.collectionList = []
        self.environmentList = []
        self.databaseList = []
        self.dataFileList = []
        self.controller = Controller.Controller(self.root)

    def init_components(self):
        # Font components
        generalFont = tkFont.Font(family='Times',size=12)

        # Button components
        self.addCollectionButton =tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add colllection",command=self.add_collection)
        self.addEnvironmentButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add environment",command=self.add_environment)
        self.addDataFileButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add data file",command=self.add_data_file)
        self.addDatabaseButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add database",command=self.add_database)
        self.addButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add",command=self.add_row)
        self.deleteButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Delete",command=self.delete_row)
        self.runButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Run",command=self.run)
       
        # Table components
        self.table = ttk.Treeview(self.root,height=10)
        self.tableScrollBar = tk.Scrollbar(master=self.table,orient="vertical")
        self.table_config()
        self.table.insert(parent='', index=0, iid=0, values=("My Test Collection", "My Test Environment", "My Test Database","My Test Data File","Yes","Yes"))

    def table_config(self):
        self.table['columns'] = ('collection','environment','database','dataFile','iteration','parallel')
        self.table.column("#0", width=0,  stretch='no')
        self.table.heading("collection",text="Collection",anchor="center")
        self.table.heading("environment",text="Environment",anchor="center")
        self.table.heading("database",text="Database",anchor="center")
        self.table.heading("dataFile",text="Data File",anchor="center")
        self.table.heading("iteration",text="Iteration run",anchor="center")
        self.table.heading("parallel",text="Run parallel",anchor="center")
        
        self.tableScrollBar.pack(side='right',fill='y')
        self.tableScrollBar.config(command=self.table.yview)

        self.table['yscrollcommand'] = self.tableScrollBar.set
        self.table.column("collection",width=23,anchor='center')
        self.table.column("environment",width=23,anchor='center')
        self.table.column("database",width=23,anchor='center')
        self.table.column("dataFile",width=23,anchor='center')
        self.table.column("iteration",width=14,anchor='center')
        self.table.column("parallel",width=14,anchor='center')

    def components_line_up(self):
        # Window config
        self.root.title("API Testing Tool")
        # Setting window size
        width=919
        height=308
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Placing components
        # First row
        self.addCollectionButton.place(x=20,y=20,width=170,height=25)
        self.addEnvironmentButton.place(x=220,y=20,width=170,height=25)
        self.addDataFileButton.place(x=420,y=20,width=170,height=25)
        self.addDatabaseButton.place(x=620,y=20,width=170,height=25)
        
        # Second row
        self.table.place(x=20,y=60,width=785,height=200)
        self.addButton.place(x=810,y=60,width=100,height=25)
        self.deleteButton.place(x=810,y=140,width=100,height=25)
        self.runButton.place(x=810,y=220,width=100,height=25)

    def start_up(self):
        self.init_components()
        self.components_line_up()
        self.root.mainloop()

    def add_collection(self):
        postmanCollectionPattern = r"*.postman_collection.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Collections File"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        for file in fileNames:
            if file in self.collectionList:
                print("Yes")
            else:
                self.collectionList.append(file)

    def add_environment(self):
        postmanCollectionPattern = r"*.postman_environment.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Environment Files"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        for file in fileNames:
            if file in self.environmentList:
                pass
            else:
                self.environmentList.append(file)

    def add_data_file(self):
        csvPattern = r"*.csv"
        jsonPattern = r"*.json"
        excelPattern = r"*.xlsx"
        marcoExcelPattern = r"*.xlsm"
        fileTypes = [
            ("Csv file",csvPattern),
            ("Json file",jsonPattern),
            ("Excel file",excelPattern),
            ("Marco Excel file",marcoExcelPattern)
        ]
        fileNames = tkDialog.askopenfilenames(title = "Select Data File",filetypes=fileTypes)
        for file in fileNames:
            if file in self.dataFileList:
                pass
            else:
                self.dataFileList.append(file)

    def add_database(self):
        csvPattern = r"*.csv"
        jsonPattern = r"*.json"
        excelPattern = r"*.xlsx"
        marcoExcelPattern = r"*.xlsm"
        fileTypes = [
            ("Csv file",csvPattern),
            ("Json file",jsonPattern),
            ("Excel file",excelPattern),
            ("Marco Excel file",marcoExcelPattern)
        ]
        fileNames = tkDialog.askopenfilenames(title = "Select Database File",filetypes=fileTypes)
        for file in fileNames:
            if file in self.databaseList:
                pass
            else:
                self.databaseList.append(file)


    def add_row(self):
        self.addDataFrame = AddDataFrame.App(self,self.collectionList,self.environmentList,self.dataFileList,self.databaseList)
        self.addDataFrame.start_up()


    def delete_row(self):
        x = self.table.selection()
        if(len(x) == 0):
            pass
        else:
            self.table.delete(x)
        
    def run(self):
        print("run")

    def get_main_frame(self):
        return self.root
    
    def get_table(self):
        return self.table
    