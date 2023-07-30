import tkinter, tkinter.filedialog, tkinter.ttk
import Controller

class GUI():
    def __init__(self):
        self.tk = tkinter.Tk()

    def init_components(self):
        # Panel components
        self.leftFrame = tkinter.Frame(self.tk,width=100,height=640)
        self.leftFrame.pack(side="left")


        # Label components
        self.collectionFileLabel = tkinter.Label(self.leftFrame,text="Collection file")
        self.environmentFileLabel = tkinter.Label(self.leftFrame,text="Environment file(s)")
        self.iterationRunLabel = tkinter.Label(self.leftFrame,text="Iteration")

        # Button components
        self.collectionFileButton = tkinter.Button(self.tk,text="Browse", command=self.select_collection_file)
        self.environmentFileButton = tkinter.Button(self.tk,text="Browse",command=self.select_environment_file)
        self.runButton = tkinter.Button(self.tk,text="Run",command=self.run_process)

        # Text field/area components
        self.collectionFileTextField = tkinter.Entry(self.tk,state="disabled")
        self.environmentFileTextField = tkinter.Text(self.tk,state="normal")
        self.iterationRunTextField = tkinter.Entry()
        self.iterationRunTextField.insert(0,"1")

        # Check box components
        self.runRequestParallelVariable = tkinter.IntVar()
        self.runRequestParallelCheckButton = tkinter.Checkbutton(self.tk,text= "Run request parallel",variable=self.runRequestParallelVariable)

    def components_line_up(self):
        # Window config
        self.tk.title("Api Test Tool")
        self.tk.resizable(False,False)
        self.tk.minsize(640,480)

        # Label components line up
        self.collectionFileLabel.grid(row = 0,pady=5, padx=5)
        self.environmentFileLabel.grid(row = 1,rowspan= 2,pady=5,padx=5)
        self.iterationRunLabel.grid(row = 3,pady = 5,padx=5)

        # # Text field components line up
        # self.collectionFileTextField.grid(row = 0, column = 1 , columnspan= 5,sticky='nsew',pady=5)
        # self.environmentFileTextField.grid(row = 1, column = 1, columnspan= 5,sticky='nsew',pady=5)
        # self.iterationRunTextField.grid(row = 3, column = 1,sticky='nsew',pady = 5)

        # # Button components line up
        # self.collectionFileButton.grid(row = 0, column = 6,pady=5,sticky='nsew', padx = 5)
        # self.environmentFileButton.grid(row = 1, column = 6,pady=5,sticky='ew', padx = 5)
        # self.runButton.grid(row = 3, column=6,sticky='nsew',pady = 5, padx = 5)

        # # Check button components line up
        # self.runRequestParallelCheckButton.grid(row=3, column = 3, sticky='nsew')


    def start_up(self):
        self.init_components()
        self.components_line_up()
        self.tk.mainloop()

    def select_collection_file(self):
        postmanCollectionPattern = r"*.postman_collection.json"
        fileName = tkinter.filedialog.askopenfilename(title = "Select Postman Collection File"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        self.collectionFileTextField.configure(state="normal")
        self.collectionFileTextField.insert(tkinter.INSERT,fileName)
        self.collectionFileTextField.configure(state="disabled")


    def select_environment_file(self):
        postmanEnvironmentPattern = r"*.postman_environment.json"
        fileNames = tkinter.filedialog.askopenfilenames(title = "Select Environment File"
                                                      ,filetypes=[("Postman Environment File",postmanEnvironmentPattern)])
        for file in fileNames:
            self.environmentFileTextField.insert(tkinter.INSERT,file + "\n")

    def run_process(self):
        self.progressCheckVar = False
        self.controller = Controller.Controller(self)
        self.controller.run_process()

    def get_collection_file(self):
        return self.collectionFileTextField.get()
    
    def get_environment_files(self):
        return self.environmentFileTextField.get(1.0,tkinter.END)
    
    def get_iteration_run(self):
        return self.iterationRunTextField.get()
    
    def get_progress_check_variable(self):
        return self.progressCheckVar
    
    def set_progress_check_variable(self,value):
        self.progressCheckVar = value
        
    def get_main_frame(self):
        return self.tk
    
