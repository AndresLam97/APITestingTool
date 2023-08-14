import tkinter.messagebox
import os
import subprocess
import ProgressBar as ProgressBar
import random
import tkinter.filedialog as tkDialog
import AddDataFrame

class Controller():
    def __init__(self,gui):
        self.gui = gui
        self.collectionList = []
        self.environmentList = []
        self.databaseList = []
        self.dataFileList = []
        
        self.trimmedCollectionList = []
        self.trimmedEnvironmentList = []
        self.trimmedDatabaseList = []
        self.trimmedDataFileList = []
        
        # Config Button Command
        self.gui.get_add_collection_button()['command'] = self.add_collection
        self.gui.get_add_environment_button()['command'] = self.add_environment
        self.gui.get_add_database_button()['command'] = self.add_database
        self.gui.get_add_data_file_button()['command'] = self.add_data_file
        self.gui.get_add_button()['command'] = self.add_row
        self.gui.get_delete_button()['command'] = self.delete_row
        self.gui.get_run_button()['command'] = self.run_process
        
    
    def run_process(self):
        try:
            self.verify_collection_file()
            self.verify_environment_file()
            self.verify_iteration_run_time()
            if len(self.environmentFiles) == 1:
                self.start()
            else:
                dialogType = "Info"
                title = "Confirm before start process"
                message = "The environment file that will be run on process:\n"
                for environment in self.usableEnvironmentFiles:
                    message = message + environment + "\n"
                if len(self.notUsableEnvironmentFiles) > 0:
                    message = message + "\nThe environment file that will not be run on process:\n"
                    for environment in self.notUsableEnvironmentFiles:
                        message = message + environment + "\n"
                result = self.display_information_dialog(dialogType,title,message)
                if result == True:
                    self.start()
                else:
                    pass
            
        except Exception as ex:
            dialogType, title, message = ex.args
            self.display_information_dialog(dialogType,title,message)

        
    def verify_collection_file(self):
        if(len(self.collectionFileName) == 1):
            raise Exception("Error","Collection file validation", "The collection file could not be empty, please retry!!!")
        else:
            self.collectionFileName = self.collectionFileName.split("\n")
        
    def verify_environment_file(self):
        if(len(self.environmentFiles) == 1):
            pass
        else:
            splittedEnvironmentFileList = self.environmentFiles.split("\n")
            self.check_environment_files(splittedEnvironmentFileList)
            
    def check_environment_files(self, environmentFiles):
        for environmentFile in environmentFiles:
            if(environmentFile != "\n" and environmentFile != ""):
                trimmedEnvironmentFile = environmentFile.strip()
                if(os.path.isfile(trimmedEnvironmentFile)):
                    self.usableEnvironmentFiles.append(trimmedEnvironmentFile)
                else:
                    self.notUsableEnvironmentFiles.append(trimmedEnvironmentFile)
            else:
                pass
            
    def verify_iteration_run_time(self):
        try:
            self.iterationTime = int(self.iterationTime)
        except Exception:
            raise Exception("Error","Iteration run time validation", "The iteration must be number, please retry!!!")            
    
    def display_information_dialog(self,type,title,message):
        if(type == "Error"):
            return tkinter.messagebox.showerror(title=title,message=message)
        elif(type == "Success"):
            return tkinter.messagebox.showinfo(title=title, message=message)
        elif(type == "Info"):
            return tkinter.messagebox.askokcancel(title=title,message=message)
        else:
            pass

    def start(self):
        progressBar = ProgressBar.ProgressBar(self.gui)
        progressBar.line_up_components()
        processFile = os.getcwd() + "\\Process.js"
        dialogType = "Success"
        title = "Process run result"
        message = "The process was run successfully and the run report saved into the report folder, please check the folder to get the run report !!!"
        command = self.get_command_base_on_inputted_data()
        process = subprocess.Popen(["node",processFile,command])
        progressBar.animated_run(random.randint(50,90),100)
        process.wait()
        progressBar.animated_run(100,50)
        self.display_information_dialog(dialogType,title,message)
        
    def get_command_base_on_inputted_data(self):
        collectionString = ""
        environmentString = ""
        iterationTime = str(self.iterationTime)
        command = " "
        if(len(self.collectionFileName)> 1):
            collectionString = ",".join(self.collectionFileName)
        else:
            collectionString = collectionString + self.collectionFileName[0]
            
        if(len(self.usableEnvironmentFiles)> 1):
            environmentString = ",".join(self.usableEnvironmentFiles)
        elif(len(self.usableEnvironmentFiles) == 1):
            environmentString = environmentString + self.usableEnvironmentFiles[0]
        else:
            pass
        
        if(environmentString == ""):
            command = command + "-c " + '"' + collectionString  + '"' + " -n " + iterationTime
        else:
            command = command + "-c " + '"' + collectionString + '"' + " -e " + '"' + environmentString + '"' + " -n " + iterationTime
            
        if(self.runParallel == True):
            command = command + " -p"
        else:
            pass
        
        print(command)
            
        return command
    
    
    def add_collection(self):
        postmanCollectionPattern = r"*.postman_collection.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Collections File"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        for file in fileNames:
            if file in self.collectionList:
                print("Yes")
            else:
                self.collectionList.append(file)
                self.trimmedCollectionList.append(self.detach_file_name(file))
    
    
    
    def add_environment(self):
        postmanCollectionPattern = r"*.postman_environment.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Environment Files"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        for file in fileNames:
            if file in self.environmentList:
                pass
            else:
                self.environmentList.append(file)
                self.trimmedEnvironmentList.append(self.detach_file_name(file))

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
                self.trimmedDataFileList.append(self.detach_file_name(file))

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
                self.trimmedDatabaseList.append(self.detach_file_name(file))

    def add_row(self):
        self.addDataFrame = AddDataFrame.App(self.gui,self.trimmedCollectionList,self.trimmedEnvironmentList,self.trimmedDataFileList,self.trimmedDatabaseList)
        self.addDataFrame.start_up()

    def delete_row(self):
        x = self.table.selection()
        if(len(x) == 0):
            pass
        else:
            self.table.delete(x)
            
    def detach_file_name(self,filePath):
        pathList = filePath.split("/")
        fileName = pathList[len(pathList) - 1]
        detachedFileName = fileName.split(".")[0]
        return detachedFileName