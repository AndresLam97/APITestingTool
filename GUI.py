import tkinter, tkinter.filedialog
import Controller

class GUI():
    def __init__(self):
        self.tk = tkinter.Tk()

    def init_components(self):
        # Label components
        self.collectionFileLabel = tkinter.Label(self.tk,text="Collection file")
        self.environmentUrlFileLabel = tkinter.Label(self.tk,text="Environment url file")
        self.environmentFileLabel = tkinter.Label(self.tk,text="Environment file(s)")
        self.iterationRunLabel = tkinter.Label(self.tk,text="Iteration")

        # Button components
        self.collectionFileButton = tkinter.Button(self.tk,text="Browse", command=self.select_collection_file)
        self.environmentUrlFileButton = tkinter.Button(self.tk,text="Browse", command=self.select_environment_url_file)
        self.environmentFileButton = tkinter.Button(self.tk,text="Browse",command=self.select_environment_file)
        self.runButton = tkinter.Button(self.tk,text="Run",command="")

        # Text field/area components
        self.collectionFileTextField = tkinter.Entry(self.tk,state="disabled")
        self.environmentUrlFileTextField = tkinter.Entry(self.tk,state="disabled")
        self.environmentFileTextField = tkinter.Text(self.tk,state="normal")
        self.iterationRunTextField = tkinter.Entry()

    def components_line_up(self):
        # Window config
        self.tk.title("Api Test Tool")
        self.tk.resizable(False,False)
        self.tk.minsize(640,480)
        
        # Grid config
        self.tk.grid_rowconfigure(0,weight=0)
        self.tk.grid_rowconfigure(1,weight=0)
        self.tk.grid_rowconfigure(2,weight=0)
        self.tk.grid_rowconfigure(3,weight=1)
        self.tk.grid_rowconfigure(4,weight=0)
        self.tk.grid_rowconfigure(5,weight=0)
        self.tk.grid_rowconfigure(6,weight=0)
        self.tk.grid_columnconfigure(0,weight=1)
        self.tk.grid_columnconfigure(1,weight=1)
        self.tk.grid_columnconfigure(2,weight=1)
        self.tk.grid_columnconfigure(3,weight=1)
        self.tk.grid_columnconfigure(4,weight=1)
        self.tk.grid_columnconfigure(5,weight=1)
        self.tk.grid_columnconfigure(6,weight=1)

        # Label components line up
        self.collectionFileLabel.grid(row = 0,column = 0,pady=5)
        self.environmentUrlFileLabel.grid(row = 2,column = 0)
        self.environmentFileLabel.grid(row = 3, column = 0,pady=5)
        self.iterationRunLabel.grid(row = 5, column = 0,pady = 5)

        # Text field components line up
        self.collectionFileTextField.grid(row = 0, column = 1 , columnspan= 5,sticky='nsew',pady=5)
        self.environmentUrlFileTextField.grid(row = 2, column = 1 , columnspan= 5,sticky='nsew')
        self.environmentFileTextField.grid(row = 3, column = 1 , columnspan= 5,sticky='nsew',pady=5)
        self.iterationRunTextField.grid(row = 5, column = 1,sticky='nsew',pady = 5)

        # Button components line up
        self.collectionFileButton.grid(row = 0, column = 6,pady=5,sticky='nsew', padx = 5)
        self.environmentUrlFileButton.grid(row = 2, column = 6,sticky='nsew', padx = 5)
        self.environmentFileButton.grid(row = 3, column = 6,pady=5,sticky='ew', padx = 5)
        self.runButton.grid(row = 5, column=6,sticky='nsew',pady = 5, padx = 5)

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

    def select_environment_url_file(self):
        csvPattern = r"*.csv"
        xlsxPattern = r"*.xlsx"
        fileName = tkinter.filedialog.askopenfilename(title = "Select Environment Url File"
                                                      ,filetypes=[("Csv File",csvPattern), ("Xlsx File", xlsxPattern)])
        self.environmentUrlFileTextField.configure(state="normal")
        self.environmentUrlFileTextField.insert(tkinter.INSERT,fileName)
        self.environmentUrlFileTextField.configure(state="disabled")

    def select_environment_file(self):
        postmanEnvironmentPattern = r"*.postman_environment.json"
        fileNames = tkinter.filedialog.askopenfilenames(title = "Select Environment File"
                                                      ,filetypes=[("Postman Environment File",postmanEnvironmentPattern)])
        for file in fileNames:
            self.environmentFileTextField.insert(tkinter.INSERT,file + "\n")

    def get_collection_file(self):
        return self.collectionFileTextField.get()
    
    def get_environment_url_file(self):
        return self.environmentUrlFileTextField.get()
    
    def get_environment_file(self):
        return self.environmentFileTextField.get(1.0,tkinter.END)
    
    def get_iteration_run(self):
        return self.iterationRunTextField.get()