import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk

class GUI:
    def __init__(self):
        # Main Frame components init
        self.mainFrame = tk.Tk()

        # Font components
        generalFont = tkFont.Font(family='Times',size=12)
        subFrameFont = tkFont.Font(family='Times',size = 11)

        # Main Frame button components
        self.mainFrameAddCollectionButton =tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add Colllection")
        self.mainFrameAddEnvironmentButton=tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add Environment")
        self.mainFrameAddDataFileButton=tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add Data File")
        self.mainFrameAddDatabaseButton=tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add Database")
        self.mainFrameAddRowButton=tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Add")
        self.mainFrameDeleteButton=tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Delete")
        self.mainFrameRunButton=tk.Button(self.mainFrame,font=generalFont,anchor="center",bg="#f0f0f0",fg="#000000",justify="center",text="Run")
       
        # Main Frame table components
        self.mainFrameTable = ttk.Treeview(self.mainFrame,height=10)
        self.mainFrameTableScrollBar = tk.Scrollbar(master=self.mainFrameTable,orient="vertical")
        self.table_config()
        
        # Sub Frame components init
        self.subFrame = tk.Toplevel(master=self.mainFrame)

        # Sub Frame label Components
        self.subFrameCollectionLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Collection")
        self.subFrameEnvironmentLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Environment")
        self.subFrameDatabaseUrlLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Database Url")
        self.subFrameDatabaseLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Database")
        self.subFrameDataFileLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Data File")
        self.subFrameRunTimeLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Run Time")
        self.subFrameRunParallelLabel=tk.Label(self.subFrame,font=subFrameFont,anchor='center',fg="#333333",justify="left",text="Run Parallel")
        
        # Sub Frame button components
        self.subFrameAddRowButton=tk.Button(self.subFrame,font=subFrameFont,bg="#f0f0f0",fg="#000000",justify="center",text="Add")
        self.subFrameCancelButton=tk.Button(self.subFrame,font=subFrameFont,bg="#f0f0f0",fg="#000000",justify="center",text="Cancel")

        # Sub Frame combo box components
        self.subFrameCollectionCombobox=ttk.Combobox(self.subFrame,font=subFrameFont,justify="center",state='readonly')
        self.subFrameEnvironmentCombobox=ttk.Combobox(self.subFrame,font=subFrameFont,justify="center",state='readonly')
        self.subFrameDatabaseUrlCombobox=ttk.Combobox(self.subFrame,font=subFrameFont,justify="center",state='readonly')
        self.subFrameDatabaseCombobox=ttk.Combobox(self.subFrame,font=subFrameFont,justify="center",state='readonly')
        self.subFrameDataFileCombobox=ttk.Combobox(self.subFrame,font=generalFont,justify="center",state='readonly')

        # Sub Frame entry components
        self.subFrameRunTimeEntry=tk.Entry(self.subFrame,font=subFrameFont,justify="center")

        # Sub Frame check box components
        self.subFrameRunParallelCheckBoxVariable = tk.BooleanVar()
        self.subFrameRunParallelCheckBox=tk.Checkbutton(self.subFrame,font=subFrameFont,borderwidth="1px",fg="#333333",justify="center",variable=self.subFrameRunParallelCheckBoxVariable,onvalue=True,offvalue=False)
        
    def table_config(self):
        self.mainFrameTable['columns'] = ('collection','environment','databaseUrl','database','dataFile','iteration','parallel')
        self.mainFrameTable.column("#0", width=0,  stretch='no')
        self.mainFrameTable.heading("collection",text="Collection",anchor="center")
        self.mainFrameTable.heading("environment",text="Environment",anchor="center")
        self.mainFrameTable.heading("databaseUrl",text="Database Url",anchor="center")
        self.mainFrameTable.heading("database",text="Database",anchor="center")
        self.mainFrameTable.heading("dataFile",text="Data File",anchor="center")
        self.mainFrameTable.heading("iteration",text="Iteration Run",anchor="center")
        self.mainFrameTable.heading("parallel",text="Run Parallel",anchor="center")
        
        self.mainFrameTableScrollBar.pack(side='right',fill='y')
        self.mainFrameTableScrollBar.config(command=self.mainFrameTable.yview)

        self.mainFrameTable['yscrollcommand'] = self.mainFrameTableScrollBar.set
        self.mainFrameTable.column("collection",width=23,anchor='center', stretch=tk.YES)
        self.mainFrameTable.column("environment",width=23,anchor='center', stretch=tk.YES)
        self.mainFrameTable.column("databaseUrl",width=50,anchor='center', stretch=tk.YES)
        self.mainFrameTable.column("database",width=23,anchor='center', stretch=tk.YES)
        self.mainFrameTable.column("dataFile",width=23,anchor='center', stretch=tk.YES)
        self.mainFrameTable.column("iteration",width=14,anchor='center', stretch=tk.YES)
        self.mainFrameTable.column("parallel",width=14,anchor='center', stretch=tk.YES)

    def components_line_up(self):
        # Window config
        self.mainFrame.title("API Testing Tool")
        self.subFrame.title("Add information")

        self.subFrame.withdraw()

        # Setting main frame size and position
        mainFrameWidth=970
        mainFrameHeight=290
        mainFrameScreenwidth = self.mainFrame.winfo_screenwidth()
        mainFrameScreenHeight = self.mainFrame.winfo_screenheight()
        mainFrameXPosition = int(mainFrameScreenwidth - mainFrameWidth) / 2
        mainFrameYPosition = int(mainFrameScreenHeight - mainFrameHeight) / 2
        mainFrameAlignStr = '%dx%d+%d+%d' % (mainFrameWidth, mainFrameHeight, mainFrameXPosition, mainFrameYPosition)

        # Setting sub frame size and position
        subFrameWidth=350
        subFrameHeight=325
        subFrameXPosition = int(mainFrameXPosition + int(mainFrameWidth/2) - int(subFrameWidth/2))
        subFrameYPosition = int(mainFrameYPosition + int(mainFrameHeight/2) - int(subFrameHeight/2))
        subFrameAlignStr = '%dx%d+%d+%d' % (subFrameWidth,subFrameHeight,subFrameXPosition,subFrameYPosition)
        
        self.mainFrame.geometry(mainFrameAlignStr)
        self.mainFrame.resizable(width=False, height=False)
        self.subFrame.geometry(subFrameAlignStr)
        self.subFrame.resizable(width=False, height=False)
        
        # Placing components
        # Main Frame first row
        self.mainFrameAddCollectionButton.place(x=20,y=20,width=170,height=25)
        self.mainFrameAddEnvironmentButton.place(x=220,y=20,width=170,height=25)
        self.mainFrameAddDataFileButton.place(x=420,y=20,width=170,height=25)
        self.mainFrameAddDatabaseButton.place(x=620,y=20,width=170,height=25)
        
        # Main Frame second row
        self.mainFrameTable.place(x=20,y=60,width=830,height=200)
        self.mainFrameAddRowButton.place(x=855,y=60,width=100,height=25)
        self.mainFrameDeleteButton.place(x=855,y=140,width=100,height=25)
        self.mainFrameRunButton.place(x=855,y=220,width=100,height=25)

        # Sub Frame first row
        self.subFrameCollectionLabel.place(x=20,y=10,width=80,height=25)
        self.subFrameCollectionCombobox.place(x=105,y=10,width=233,height=25)

        # Sub Frame second row
        self.subFrameEnvironmentLabel.place(x=20,y=50,width=80,height=25)
        self.subFrameEnvironmentCombobox.place(x=105,y=50,width=233,height=25)

        # Sub Frame third row
        self.subFrameDatabaseUrlLabel.place(x=20,y=90,width=80,height=25)
        self.subFrameDatabaseUrlCombobox.place(x=105,y=90,width=233,height=25)

        # Sub Frame fourth row
        self.subFrameDatabaseLabel.place(x=20,y=130,width=80,height=25)
        self.subFrameDatabaseCombobox.place(x=105,y=130,width=233,height=25)

        # Sub Frame fifth row
        self.subFrameDataFileLabel.place(x=20,y=170,width=80,height=25)
        self.subFrameDataFileCombobox.place(x=105,y=170,width=233,height=25)

        # Sub Frame sixth row
        self.subFrameRunTimeLabel.place(x=20,y=210,width=80,height=25)
        self.subFrameRunTimeEntry.place(x=105,y=210,width=233,height=25)

        # Sub Frame seventh row
        self.subFrameRunParallelLabel.place(x=20,y=250,width=80,height=25)
        self.subFrameRunParallelCheckBox.place(x=170,y=250,width=110,height=25)

        # Sub Frame eighth row
        self.subFrameAddRowButton.place(x=126,y=290,width=80,height=25)
        self.subFrameCancelButton.place(x=232,y=290,width=80,height=25)

    def get_main_frame(self):
        return self.mainFrame
    
    def get_main_frame_table(self):
        return self.mainFrameTable
    
    def get_main_frame_add_collection_button(self):
        return self.mainFrameAddCollectionButton
    
    def get_main_frame_add_environment_button(self):
        return self.mainFrameAddEnvironmentButton
    
    def get_main_frame_add_database_button(self):
        return self.mainFrameAddDatabaseButton
    
    def get_main_frame_add_data_file_button(self):
        return self.mainFrameAddDataFileButton
    
    def get_main_frame_add_row_button(self):
        return self.mainFrameAddRowButton
    
    def get_main_frame_delete_button(self):
        return self.mainFrameDeleteButton

    def get_main_frame_run_button(self):
        return self.mainFrameRunButton
    
    def get_sub_frame_add_button(self):
        return self.subFrameAddRowButton
    
    def get_sub_frame_cancel_button(self):
        return self.subFrameCancelButton
    
    def get_sub_frame_collection_combo_box(self):
        return self.subFrameCollectionCombobox
    
    def get_sub_frame_environment_combo_box(self):
        return self.subFrameEnvironmentCombobox
    
    def get_sub_frame_data_file_combo_box(self):
        return self.subFrameDataFileCombobox
    
    def get_sub_frame_database_combo_box(self):
        return self.subFrameDatabaseCombobox
    
    def get_sub_frame_run_time_entry(self):
        return self.subFrameRunTimeEntry
    
    def get_sub_frame_run_parallel_check_box_variable(self):
        return self.subFrameRunParallelCheckBoxVariable
    
    def get_sub_frame_run_parallel_check_box(self):
        return self.subFrameRunParallelCheckBox
    
    def get_sub_frame(self):
        return self.subFrame
    
    def get_sub_frame_database_url_combo_box(self):
        return self.subFrameDatabaseUrlCombobox