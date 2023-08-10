import tkinter as tk
import tkinter.font as tkFont
import DefinedTable as t
from tkinter import ttk

class App:
    def __init__(self):
        self.root = tk.Tk()

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

        # Label components
        self.iterationRunLabel=tk.Label(self.root,font=generalFont,anchor="center",fg="#333333",justify="center",text="Iteration run")
        
        # Entry components
        self.iterationRunEntry=tk.Entry(self.root,font=generalFont,fg="#333333",justify="center",borderwidth="1px")
        
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
        self.addButton.place(x=810,y=100,width=100,height=25)
        self.deleteButton.place(x=810,y=160,width=100,height=25)
        
        # Third row
        self.iterationRunLabel.place(x=20,y=270,width=90,height=25)
        self.iterationRunEntry.place(x=110,y=270,width=97,height=25)
        self.runButton.place(x=810,y=270,width=100,height=25)

    def start_up(self):
        self.init_components()
        self.components_line_up()
        self.root.mainloop()

    def add_collection(self):
        print("add_collection")


    def add_environment(self):
        print("add_environment")


    def add_data_file(self):
        print("add_data_file")


    def add_database(self):
        print("add_database")


    def add_row(self):
        print("add_row")


    def delete_row(self):
        print("delete_row")


    def run(self):
        print("run")

if __name__ == "__main__":
    app = App()
    app.start_up()
