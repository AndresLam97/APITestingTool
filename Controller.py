import GUI
import tkinter.messagebox
import os
import subprocess

class Controller():
    def __init__(self,collectionFileName,environmentFiles,iterationTime):
        self.collectionFileName = collectionFileName
        self.environmentFiles = environmentFiles
        self.iterationTime = iterationTime
        self.useableEnvironmentFile = []
        self.notUsableEnvironmentFile = []
    
    def run_process(self):
        try:
            self.verify_collection_file()
            self.verify_environment_file()
            self.verify_iteration_run_time()
            dialogType = "Info"
            title = "Confirm before start process"
            message = "The environment file that will be run on process:\n"
            for environment in self.useableEnvironmentFile:
                message = message + environment + "\n"
            if len(self.notUsableEnvironmentFile) > 0:
                message = message + "\nThe environment file that will not be run on process:\n"
                for environment in self.notUsableEnvironmentFile:
                    message = message + environment + "\n"
            result = self.display_information_dialog(dialogType,title,message)
            if result == True:
                processFile = os.getcwd() + "\\Process.js"
                environmentFileList = ",".join(self.useableEnvironmentFile)
                process = subprocess.Popen(["node", processFile, self.collectionFileName, environmentFileList, str(self.iterationTime)])
                process.wait()
                dialogType = "Success"
                title = "Process run result"
                message = "The process was run successfully and the run report saved into the report folder, please check the folder to get the run report !!!"
                self.display_information_dialog(dialogType,title,message)
            else:
                pass
            
        except Exception as ex:
            dialogType, title, message = ex.args
            self.display_information_dialog(dialogType,title,message)

        
    def verify_collection_file(self):
        if(len(self.collectionFileName) == 0):
            raise Exception("Error","Collection file validation", "The collection file could not be empty, please retry!!!")
        else:
            return
        
    def verify_environment_file(self):
        if(len(self.environmentFiles) == 1):
            pass
        else:
            splittedEnvironmentFileList = self.environmentFiles.split("\n")
            self.check_environment_files(splittedEnvironmentFileList)
            
    def check_environment_files(self, environmentFiles):
        for environmentFile in environmentFiles:
            if(environmentFile != "\n"):
                trimmedEnvironmentFile = environmentFile.strip()
                if(os.path.isfile(trimmedEnvironmentFile)):
                    print(trimmedEnvironmentFile)
                    self.useableEnvironmentFile.append(trimmedEnvironmentFile)
                else:
                    print(trimmedEnvironmentFile)
                    self.notUsableEnvironmentFile.append(trimmedEnvironmentFile)
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