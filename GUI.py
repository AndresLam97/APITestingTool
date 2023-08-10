import tkinter as tk
import tkinter.font as tkFont
import tkinter.filedialog as tkDialog
import Controller

class GUI:
    def __init__(self):
        self.root = tk.Tk()

    def init_components(self):
        # Font component
        generalFont = tkFont.Font(family='Times',size=12)

        # Label components
        self.collectionFileLabel=tk.Label(self.root,font=generalFont,fg="#333333",justify="center",text="Collections File(s)")
        self.environmentFileLabel=tk.Label(self.root,font=generalFont,fg="#333333",justify="center",text="Environment File(s)")
        self.iterationRunLabel=tk.Label(self.root,font=generalFont,fg="#333333",justify="center", text="Iteration run")

        # Entry/Text field components
        self.collectionFileTextField=tk.Text(self.root,borderwidth="1px",font=generalFont,fg="#333333", state='disabled')
        self.environmentFileTextField=tk.Text(self.root,borderwidth="1px",font=generalFont,fg="#333333")
        self.iterationRunTextField=tk.Entry(self.root,borderwidth="1px",font=generalFont,fg="#333333",justify="center")
        
        # Button components
        self.collectionFileButton=tk.Button(self.root,bg="#f0f0f0",font=generalFont,fg="#000000",justify="center",text="Browse",command=self.select_collection_file)
        self.environmentFileButton=tk.Button(self.root,font=generalFont,bg="#f0f0f0",fg="#000000",justify="center",text="Browse",command=self.select_environment_file)
        self.runButton=tk.Button(self.root,font=generalFont,bg="#f0f0f0",fg="#000000",justify="center",text="Run",command=self.run_process)

        # Check button components
        self.runRequestParallelCheckButtonVariable = tk.IntVar()
        self.runRequestParallelCheckButton=tk.Checkbutton(self.root,font=generalFont,fg="#333333",justify="center",text="Run Request Parallel",variable=self.runRequestParallelCheckButtonVariable,onvalue=True,offvalue=False)

        # Scrollbar components
        self.collectionTextScrollbar = tk.Scrollbar(self.collectionFileTextField,orient='vertical')
        self.environmentTextScrollbar = tk.Scrollbar(self.environmentFileTextField,orient='vertical')
        
        # Set default value for text area
        self.iterationRunTextField.insert(tk.INSERT,"1")
        
    def components_line_up(self):
        # Window config
        self.root.title("API Testing Tool")
        # Setting window size
        width=699
        height=200
        screenwidth = self.root.winfo_screenwidth()
        screenheight = self.root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.root.geometry(alignstr)
        self.root.resizable(width=False, height=False)

        # Placing components
        # First row
        self.collectionFileLabel.place(x=10,y=10,width=132,height=36)
        self.collectionFileTextField.place(x=150,y=10,width=441,height=45)
        self.collectionFileButton.place(x=600,y=10,width=90,height=25)

        # Second row
        self.environmentFileLabel.place(x=10,y=50,width=134,height=100)
        self.environmentFileTextField.place(x=150,y=60,width=441,height=100)
        self.environmentFileButton.place(x=600,y=100,width=90,height=25)

        # Third row
        self.iterationRunLabel.place(x=10,y=165,width=132,height=25)
        self.iterationRunTextField.place(x=150,y=165,width=97,height=25)
        self.runRequestParallelCheckButton.place(x=280,y=165,width=178,height=25)
        self.runButton.place(x=600,y=165,width=90,height=25)

        # Scrollbar setup
        self.collectionTextScrollbar.pack(side="right",fill='y')
        self.environmentTextScrollbar.pack(side='right',fill='y')
        
        self.collectionTextScrollbar.config(command=self.collectionFileTextField.yview)
        self.environmentTextScrollbar.config(command= self.environmentFileTextField.yview)

    def start_up(self):
        self.init_components()
        self.components_line_up()
        self.root.mainloop()

    def select_collection_file(self):
        self.collectionFileTextField.config(state = 'normal')
        postmanCollectionPattern = r"*.postman_collection.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Collection File"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        if len(self.get_collection_files()) > 1:
            self.collectionFileTextField.insert(tk.INSERT,"\n")

        for index in range(len(fileNames)):
            if index == len(fileNames)-1:
                self.collectionFileTextField.insert(tk.INSERT,fileNames[index])
            else:
                self.collectionFileTextField.insert(tk.INSERT,fileNames[index] + "\n")
        self.collectionFileTextField.config(state = 'disable')

    def select_environment_file(self):
        postmanEnvironmentPattern = r"*.postman_environment.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Environment File"
                                                      ,filetypes=[("Postman Environment File",postmanEnvironmentPattern)])
        if len(self.get_environment_files()) > 1:
            self.environmentFileTextField.insert(tk.INSERT,"\n")
            
        for index in range(len(fileNames)):
            if index == len(fileNames)-1:
                self.environmentFileTextField.insert(tk.INSERT,fileNames[index])
            else:
                self.environmentFileTextField.insert(tk.INSERT,fileNames[index] + "\n")

    def run_process(self):
        self.controller = Controller.Controller(self)
        self.controller.run_process()

    def get_collection_files(self):
        return self.collectionFileTextField.get(1.0,tk.END)
    
    def get_environment_files(self):
        return self.environmentFileTextField.get(1.0,tk.END)
    
    def get_iteration_run(self):
        return self.iterationRunTextField.get()
    
    def get_run_parralel_check_button_value(self):
        return self.runRequestParallelCheckButtonVariable.get()
    
    def get_main_frame(self):
        return self.root
