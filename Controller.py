import GUI
import tkinter.messagebox


class Controller():
    def __init__(self,collectionFileName,environmentFiles,iterationTime):
        self.collectionFileName = collectionFileName
        self.environmentFiles = environmentFiles
        self.iterationTime = iterationTime
        self.useableEnvironmentFile = {}
        self.notUsableEnvironmentFile = {}
    
    def run_process(self):
        self.verify_environment_file()
        
    def verify_environment_file(self):
        if(len(self.environmentFiles) == 1):
            pass
        else:
            pass            