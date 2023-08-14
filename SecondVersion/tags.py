import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

class App:
    def __init__(self):
        self.root = tk.Tk()
        
        # Font components
        generalFont = tkFont.Font(family='Times',size=12)
        
        # Button components
        self.addCollectionButton =tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add colllection")
        self.addEnvironmentButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add environment")
        self.addDataFileButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add data file")
        self.addDatabaseButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add database")
        self.addButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add")
        self.deleteButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Delete")
        self.runButton=tk.Button(self.root,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Run")
        
        # Table components
        self.table = ttk.Treeview(self.root,height=10)
        self.tableScrollBar = tk.Scrollbar(master=self.table,orient="vertical")
        self.table_config()
        

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
        self.components_line_up()
        self.root.mainloop()

    def get_main_frame(self):
        return self.root
    
    def get_table(self):
        return self.table
    
    def get_add_collection_button(self):
        return self.addCollectionButton
    
    def get_add_environment_button(self):
        return self.addEnvironmentButton
    
    def get_add_database_button(self):
        return self.addDatabaseButton
    
    def get_add_data_file_button(self):
        return self.addDataFileButton
    
    def get_add_button(self):
        return self.addButton
    
    def get_delete_button(self):
        return self.deleteButton
    
    def get_run_button(self):
        return self.runButton