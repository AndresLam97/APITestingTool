import tkinter.messagebox
import os
import subprocess
import random
import tkinter.filedialog as tkDialog
import FileWorker
import tkinter.messagebox as messagebox

class Controller():
    def __init__(self,gui):
        # Controller variables
        self.fileWorker = FileWorker.FileWorker()
        self.collectionPathList = []
        self.environmentPathList = []
        self.databasePathList = []
        self.dataFilePathList = []
        self.detachedCollectionFileNameList = []
        self.detachedEnvironmentFileNameList = [""]
        self.detachedDatabaseUrlDict = {"":""}
        self.detachedDataFileNameList =[""]

        # Get the main frame components
        self.mainFrame = gui
        self.mainFrameTable = self.mainFrame.get_main_frame_table()
        self.mainFrameAddCollectionButton = self.mainFrame.get_main_frame_add_collection_button()
        self.mainFrameAddEnvironmentButton = self.mainFrame.get_main_frame_add_environment_button()
        self.mainFrameAddDatabaseButton = self.mainFrame.get_main_frame_add_database_button()
        self.mainFrameAddDataFileButton = self.mainFrame.get_main_frame_add_data_file_button()
        self.mainFrameAddRowButton = self.mainFrame.get_main_frame_add_row_button()
        self.mainFrameDeleteButton = self.mainFrame.get_main_frame_delete_button()
        self.mainFrameRunButton = self.mainFrame.get_main_frame_run_button()

        # Get the sub frame components
        self.subFrame = self.mainFrame.get_sub_frame()
        self.subFrameAddButton = self.mainFrame.get_sub_frame_add_button()
        self.subFrameCancelButton = self.mainFrame.get_sub_frame_cancel_button()
        self.subFrameCollectionCombobox = self.mainFrame.get_sub_frame_collection_combo_box()
        self.subFrameEnvironmentCombobox = self.mainFrame.get_sub_frame_environment_combo_box()
        self.subFrameDataFileCombobox = self.mainFrame.get_sub_frame_data_file_combo_box()
        self.subFrameDatabaseUrlCombobox = self.mainFrame.get_sub_frame_database_url_combo_box()
        self.subFrameDatabaseCombobox = self.mainFrame.get_sub_frame_database_combo_box()
        self.subFrameRunTimeEntry = self.mainFrame.get_sub_frame_run_time_entry()
        self.subFrameRunParallelCheckBoxVariable = self.mainFrame.get_sub_frame_run_parallel_check_box_variable()
        self.subFrameRunParallelCheckBox = self.mainFrame.get_sub_frame_run_parallel_check_box()
        self.subFrameDatabaseUrlCombobox.bind('<<ComboboxSelected>>',self.get_database_url_update_data)

    def config_button_command(self):
        # Main Frame button components
        self.mainFrameAddCollectionButton['command'] = self.main_frame_add_collection
        self.mainFrameAddEnvironmentButton['command'] = self.main_frame_add_environment
        self.mainFrameAddDatabaseButton['command'] = self.main_frame_add_database
        self.mainFrameAddDataFileButton['command'] = self.main_frame_add_data_file
        self.mainFrameAddRowButton['command'] = self.main_frame_add_row
        self.mainFrameDeleteButton['command'] = self.main_frame_delete_row
        self.mainFrameRunButton['command'] = self.main_frame_run

        # Sub Frame button components
        self.subFrameAddButton['command'] = self.sub_frame_add
        self.subFrameCancelButton['command'] = self.sub_frame_cancel
        self.subFrame.protocol('WM_DELETE_WINDOW',self.sub_frame_cancel)

    def main_frame_add_collection(self):
        postmanCollectionPattern = r"*.postman_collection.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Collections File"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        for file in fileNames:
            if file in self.collectionPathList:
                pass
            else:
                detachedCollectionFileName = self.fileWorker.detach_file_name(file,withExtension=False)
                self.collectionPathList.append(file)
                self.detachedCollectionFileNameList.append(detachedCollectionFileName)
        if(len(fileNames) > 0):
            self.display_information_dialog("Success","Add collection file", "Add collection file(s) successfully !!!")
        else: 
            pass

    def main_frame_add_environment(self):
        postmanCollectionPattern = r"*.postman_environment.json"
        fileNames = tkDialog.askopenfilenames(title = "Select Postman Environment Files"
                                                      ,filetypes=[("Postman Collection File",postmanCollectionPattern)])
        for file in fileNames:
            if file in self.environmentPathList:
                pass
            else:
                detachedEnvironmentFileName = self.fileWorker.detach_file_name(file,withExtension=False)
                self.environmentPathList.append(file)
                self.detachedEnvironmentFileNameList.append(detachedEnvironmentFileName)
        if(len(fileNames) > 0):
            self.display_information_dialog("Success","Add environment file", "Add environment file(s) successfully !!!")        
        else: 
            pass

    def main_frame_add_data_file(self):
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
            if file in self.dataFilePathList:
                pass
            else:
                detachedDataFileName = self.fileWorker.detach_file_name(file,withExtension=False)
                self.dataFilePathList.append(file)
                self.detachedDataFileNameList.append(detachedDataFileName)
        if(len(fileNames) > 0):
            self.display_information_dialog("Success","Add data file", "Add data file(s) successfully !!!")
        else: 
            pass
    
    def main_frame_add_database(self):
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
        fileName = tkDialog.askopenfilename(title = "Select Database File",filetypes=fileTypes)
        if fileName in self.databasePathList or fileName == "":
            pass
        else:
            message = self.fileWorker.verify_database_file(fileName)
            if  message == "":
                detachedDatabaseFileName = self.fileWorker.detach_file_name(fileName,withExtension=False)
                self.databasePathList.append(fileName)
                self.detachedDatabaseUrlDict = self.fileWorker.get_database_information(filePath=fileName,informationDict=self.detachedDatabaseUrlDict)
                self.display_information_dialog("Success","Add database file", "Add database file(s) successfully !!!")
            else:
                self.display_information_dialog("Error","Add database file",message)
        
    def main_frame_add_row(self):
        self.reload_combobox_items_for_sub_frame()
        self.refresh_combobox_selection()
        self.subFrame.grab_set()
        self.subFrame.deiconify()
        
    def main_frame_delete_row(self):
        x = self.mainFrameTable.selection()
        if(len(x) == 0):
            self.display_information_dialog("Error","Delete table row","Must select a row before delete, please retry !!!")
        else:
            self.mainFrameTable.delete(x)
        
    def main_frame_run(self):
        print(self.get_table_rows())

    def sub_frame_add(self):
        try:
            collection = self.subFrameCollectionCombobox.get()
            environment = self.subFrameEnvironmentCombobox.get()
            dataFile = self.subFrameDataFileCombobox.get()
            databaseUrl = self.subFrameDatabaseUrlCombobox.get()
            database = self.subFrameDatabaseCombobox.get()
            runParralel = self.subFrameRunParallelCheckBoxVariable.get()
            runTime = int(self.subFrameRunTimeEntry.get())
            if runTime <= 0:
                raise TypeError()
            if collection == '':
                raise KeyError()
            if databaseUrl != '' and database == "":
                raise NameError()
            nextRowIndex = len(self.mainFrameTable.get_children())+1
            self.mainFrameTable.insert(parent='', index=nextRowIndex, iid=nextRowIndex, values=(collection, environment, databaseUrl,database,dataFile,runTime,runParralel))
            self.sub_frame_cancel()
        except TypeError:
            self.display_information_dialog("Error","Iteration run time validation","The run time must be greater than 0, please retry !!!")
        except ValueError:
            self.display_information_dialog("Error","Iteration run time validation","The run time must have a number type, please retry !!!")
        except KeyError:
            self.display_information_dialog("Error","Collection validation","Must choose a collection, please retry !!!")
        except NameError:
            self.display_information_dialog("Error","Database validation","Must choose a database when the database url is selected, please retry !!!")
            
    def sub_frame_cancel(self):
        self.subFrame.grab_release()
        self.subFrame.withdraw()

    def start_up(self):
        self.mainFrame.components_line_up()
        self.config_button_command()
        self.mainFrame.mainFrame.mainloop()

    def display_information_dialog(self,type,title,message):
        if(type == "Error"):
            return tkinter.messagebox.showerror(title=title,message=message)
        elif(type == "Success"):
            return tkinter.messagebox.showinfo(title=title, message=message)
        elif(type == "Info"):
            return tkinter.messagebox.askokcancel(title=title,message=message)
        else:
            pass
 
    def reload_combobox_items_for_sub_frame(self):
        self.subFrameCollectionCombobox['values'] = self.detachedCollectionFileNameList
        self.subFrameEnvironmentCombobox['values'] = self.detachedEnvironmentFileNameList
        if len(self.detachedDatabaseUrlDict) == 0: 
            pass
        else:
            keyList = []
            for key in self.detachedDatabaseUrlDict.keys():
                keyList.append(key)
            self.subFrameDatabaseUrlCombobox['values'] = keyList       
        self.subFrameDataFileCombobox['values'] = self.detachedDataFileNameList

    def refresh_combobox_selection(self):
        self.subFrameCollectionCombobox.set("")
        self.subFrameEnvironmentCombobox.set("")
        self.subFrameDatabaseUrlCombobox.set("")
        self.subFrameDatabaseCombobox.set("")
        self.subFrameDataFileCombobox.set("")
        self.subFrameRunTimeEntry.delete(0,"end")
        self.subFrameRunTimeEntry.insert(0,"1")
        self.subFrameRunParallelCheckBoxVariable.set(False)

    def get_database_url_update_data(self,  event):
        self.subFrameDatabaseCombobox.set("")
        self.subFrameDatabaseCombobox['values'] = self.detachedDatabaseUrlDict[self.subFrameDatabaseUrlCombobox.get()]

    def get_table_rows(self):
        rows = []
        for line in self.mainFrameTable.get_children():
            row = []
            for value in self.mainFrameTable.item(line)['values']:
                row.append(value)
            rows.append(row)
        return rows