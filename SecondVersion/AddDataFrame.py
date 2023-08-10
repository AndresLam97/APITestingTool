import tkinter as tk
import tkinter.font as tkFont
from tkinter import ttk
import tkinter.messagebox as messagebox

class App:
    def __init__(self, root,collectionList,environmentList,dataFileList,databaseList):
        self.main = root
        self.mainFrame = root.get_main_frame()
        self.frame = tk.Toplevel(master=self.mainFrame)
        self.collectionList = collectionList
        self.environmentList = environmentList
        self.databaseList = databaseList
        self.dataFileList = dataFileList

    def add_process(self):
        try:
            collection = self.collectionCombobox.get()
            environment = self.environmentCombobox.get()
            dataFile = self.dataFileCombobox.get()
            database = self.databaseCombobox.get()
            runParralel = self.runParallelCheckBoxVariable.get()
            runTime = self.runTimeEntry.get()
            self.runTime = int(self.runTimeEntry.get())
            if self.runTime <= 0:
                raise TypeError()
            table = self.main.get_table()
            table.insert(parent='', index=len(table.get_children())+1, iid=len(table.get_children())+1, values=(collection, environment, database,dataFile,runTime,runParralel))
            self.cancel_process()
        except TypeError:
            messagebox.showwarning("Iteration run time validation","The run time must be greater than 0, please retry!!!")
        except Exception:
            messagebox.showwarning("Iteration run time validation","The run time must be number, please retry!!!")
        
            
        


    def cancel_process(self):
        self.frame.grab_release()
        self.frame.destroy()

    def init_components(self):
        # General Font
        generalFont = tkFont.Font(family='Times',size=12)

        # Label Components
        self.collectionLabel=tk.Label(self.frame,font=generalFont,anchor='center',fg="#333333",justify="left",text="Collection")
        self.environmentLabel=tk.Label(self.frame,font=generalFont,anchor='center',fg="#333333",justify="left",text="Environment")
        self.databaseLabel=tk.Label(self.frame,font=generalFont,anchor='center',fg="#333333",justify="left",text="Database")
        self.dataFileLabel=tk.Label(self.frame,font=generalFont,anchor='center',fg="#333333",justify="left",text="Data File")
        self.runTimeLabel=tk.Label(self.frame,font=generalFont,anchor='center',fg="#333333",justify="left",text="Run Time")
        self.runParallelLabel=tk.Label(self.frame,font=generalFont,anchor='center',fg="#333333",justify="left",text="Run Parallel")
        
        # Button Components
        self.addButton=tk.Button(self.frame,font=generalFont,bg="#f0f0f0",fg="#000000",justify="center",text="Add",command=self.add_process)
        self.cancelButton=tk.Button(self.frame,font=generalFont,bg="#f0f0f0",fg="#000000",justify="center",text="Cancel",command=self.cancel_process)

        # Combo Box Components
        self.collectionCombobox=ttk.Combobox(self.frame,font=generalFont,justify="center",state='readonly')
        self.environmentCombobox=ttk.Combobox(self.frame,font=generalFont,justify="center",state='readonly')
        self.databaseCombobox=ttk.Combobox(self.frame,font=generalFont,justify="center",state='readonly')
        self.dataFileCombobox=ttk.Combobox(self.frame,font=generalFont,justify="center",state='readonly')

        # Entry Components
        self.runTimeEntry=tk.Entry(self.frame,font=generalFont,justify="center")

        # Check Box Components
        self.runParallelCheckBoxVariable = tk.BooleanVar()
        self.runParralelCheckBox=tk.Checkbutton(self.frame,font=generalFont,borderwidth="1px",fg="#333333",justify="center",variable=self.runParallelCheckBoxVariable,onvalue=True,offvalue=False)
        
    def components_line_up(self):
        #setting title
        self.frame.title("Add information")

        #setting window size
        width=292
        height=290
        screenwidth = self.mainFrame.winfo_x() + int(self.mainFrame.winfo_width()/2) - int(width/2)
        screenheight = self.mainFrame.winfo_y() + int(self.mainFrame.winfo_height()/2) - int(height/2)
        self.frame.geometry(f"{width}x{height}+{screenwidth}+{screenheight}")
        self.frame.resizable(width=False, height=False)

        # First row
        self.collectionLabel.place(x=20,y=10,width=80,height=25)
        self.collectionCombobox.place(x=100,y=10,width=180,height=25)

        # Second row
        self.environmentLabel.place(x=20,y=50,width=80,height=25)
        self.environmentCombobox.place(x=100,y=50,width=180,height=25)

        # Third row
        self.databaseLabel.place(x=20,y=90,width=80,height=25)
        self.databaseCombobox.place(x=100,y=90,width=180,height=25)

        # Fourth row
        self.dataFileLabel.place(x=20,y=130,width=80,height=25)
        self.dataFileCombobox.place(x=100,y=130,width=180,height=25)

        # Fifth row
        self.runTimeLabel.place(x=20,y=170,width=80,height=25)
        self.runTimeEntry.place(x=100,y=170,width=180,height=25)

        # Sixth row
        self.runParallelLabel.place(x=20,y=210,width=80,height=25)
        self.runParralelCheckBox.place(x=170,y=210,width=80,height=25)

        # Seventh row
        self.addButton.place(x=50,y=250,width=80,height=25)
        self.cancelButton.place(x=170,y=250,width=80,height=25)

    def add_element_to_list_box(self):
        self.collectionCombobox['values'] = self.collectionList
        self.environmentCombobox['values'] = self.environmentList
        self.databaseCombobox['values'] = self.databaseList
        self.dataFileCombobox['values'] = self.dataFileList

    def start_up(self):
        self.frame.grab_set()
        self.init_components()
        self.components_line_up()
        self.add_element_to_list_box()
        self.frame.mainloop()