import pandas
import json

class FileWorker:
    def __init__(self):
        self.databaseColumnList = ['user','password','server','port','database','trustServerCertificate', 'encrypt', 'max', 'min', 'idleTimeoutMillis']
        self.dataFileColumnList = ['sqlQuery']
        self.excelExtensionList = ["xlsx","xlsm","csv"]
    
    def verify_database_file(self,databaseFilePath):
        extension = self.detach_file_extension(databaseFilePath)
        if extension in self.excelExtensionList:
            message = self.verify_database_excel_file(databaseFilePath,extension)
            return message
        else:
            return self.verify_database_json_file(databaseFilePath)
        
    def verify_database_excel_file(self,path,extension):
        try:
            message = ""
            fileInformation = None
            if(extension == "xlsx" or extension == "xlsm"):
                fileInformation = pandas.read_excel(path)
            else:
                fileInformation = pandas.read_csv(path)
            fileName = self.detach_file_name(path,True)
            verify_excel_columns_message = self.verify_excel_columns(fileInformation,fileName)
            verify_excel_columns_value_message = self.verify_columns_value(fileInformation,fileName)
            if verify_excel_columns_message != None:
                return verify_excel_columns_message
            if verify_excel_columns_value_message != None:
                return verify_excel_columns_value_message
            return message
        except:
            return "Cannot open the file, please recheck the path !!!"

    def verify_database_json_file(self,databaseFilePath):
        try:
            message = ""
            fileName = self.detach_file_name(databaseFilePath,True)
            with open(databaseFilePath) as f:
                data = json.load(f)
                for item in data:
                    if(len(self.databaseColumnList) != len(item)):
                        message = "The file " + '"' + fileName + '"' + " does not contain enought columns, please refer to the template file to get all the columns information !!!"
                        return message
                    for key in item.keys():
                        if(key not in self.databaseColumnList):
                            message = "The "+ '"' + key +'"' + " key in the "+ '"' + fileName +'"' + " file is not allowed, please refer to the template file to get all the columns information !!!"
                            return message
                        else:
                            if(key in self.databaseColumnList[:5] and item[key] == ""):
                                message = "The "+ '"' + key +'"' + " key in the "+ '"' + fileName +'"' + " file must not be empty, please recheck !!!"
                                return message
                            elif(key in self.databaseColumnList[:5] and (item[key] == 0 or item[key] == '0')):
                                message = "The " + '"' + key +'"' + " key in the "+ '"' + fileName +'"' + " file must not be 0, please recheck !!!"
                                return message
                            elif(key in self.databaseColumnList[:5] and type(item[key]) == str and key == "port"):
                                message = "The " + '"' + key +'"' + " key in the "+ '"' + fileName +'"' + " file must be number type, please recheck !!!"
                                return message
        except Exception:
            return "Cannot open the file, please recheck the path !!!"
        return message

    def detach_file_name(self,filePath,withExtension = True):
        pathList = filePath.split("/")
        fileName = pathList[len(pathList)-1]
        if withExtension == True:
            return fileName
        else:
            return fileName.split(".")[0]
        
    def detach_file_extension(self,filePath):
        pathList = filePath.split("/")
        fileName = pathList[len(pathList)-1]
        splittedFileName = fileName.split(".")
        return splittedFileName[len(splittedFileName)-1]
    
    def verify_excel_columns(self,fileInformation,fileName):
        columnList = fileInformation.columns.values
        if(len(self.databaseColumnList) != len(columnList)):
            message = "The file " + '"' + fileName + '"' +" does not contain enought columns, please refer to the template file to get all the columns information !!!"
            return message
        else:
            for column in self.databaseColumnList:
                if  column in columnList:
                    pass
                else:
                    message = "The file " + fileName + " must not be contain the " + '"' + column +'"' + " column, please refer to the template file to get all the columns information !!!"
                    return message

    def verify_columns_value(self,fileInformation,fileName):
        fileColumns = fileInformation.columns.values
        columnIndexList = {
            "user": 0,
            "password": 0,
            "server": 0,
            "database":0,
            "port": 0
        }
        message = ""

        for i in range(len(fileColumns)):
            if(fileColumns[i] in self.databaseColumnList[:5]):
                columnIndexList[fileColumns[i]] = i
        
        for index,row in fileInformation.iterrows():
            rowList = row.tolist()
            for key in columnIndexList:
                data = rowList[columnIndexList[key]]
                if isinstance(data,float):
                    message = "The "+ '"' + key +'"' + " column cell in the "+ fileName + " must not be empty, please recheck !!!"
                    return message
                elif(data == 0 or data == '0'):
                    message = "The " + '"' + key +'"' + " column cell in the "+ fileName + " must not be 0, please recheck !!!"
                    return message
                elif(type(data) == str and key == "port"):
                    message = "The " + '"' + key +'"' + " column cell in the "+ fileName + " must be number type, please recheck !!!"
                    return message
                
        return message

    def get_database_information(self,filePath,informationDict):
        newInformationDict = informationDict
        fileExtension = self.detach_file_extension(filePath=filePath)
        if fileExtension in self.excelExtensionList:
            df = pandas.read_excel(filePath)
            dataFrame = pandas.DataFrame(df)
            dataFrameServerDictionary = dataFrame.to_dict()['server']
            dataFrameDatabaseDictionary = dataFrame.to_dict()['database']
            for key in dataFrameServerDictionary:
                if dataFrameServerDictionary[key] in newInformationDict.keys():
                    newInformationDict[dataFrameServerDictionary[key]].append(dataFrameDatabaseDictionary[key])
                else:
                    newInformationDict[dataFrameServerDictionary[key]] = [dataFrameDatabaseDictionary[key]]
            return newInformationDict
        else:
            df = pandas.read_json(filePath)
            dataFrame = pandas.DataFrame(df)
            dataFrameServerDictionary = dataFrame.to_dict()['server']
            dataFrameDatabaseDictionary = dataFrame.to_dict()['database']
            for key in dataFrameServerDictionary:
                if dataFrameServerDictionary[key] in newInformationDict.keys():
                    newInformationDict[dataFrameServerDictionary[key]].append(dataFrameDatabaseDictionary[key])
                else:
                    newInformationDict[dataFrameServerDictionary[key]] = [dataFrameDatabaseDictionary[key]]
            return newInformationDict

    def verify_data_file(self,dataFilePath):
        extension = self.detach_file_extension(dataFilePath)
        if extension in self.excelExtensionList:
            message = self.verify_data_file_excel_file(dataFilePath,extension)
            return message
        else:
            return self.verify_data_file_json_file(dataFilePath)
    
    def verify_data_file_excel_file(self,path,extension):
        try:
            message = ""
            fileInformation = None
            if(extension == "xlsx" or extension == "xlsm"):
                fileInformation = pandas.read_excel(path)
            else:
                fileInformation = pandas.read_csv(path)
            fileName = self.detach_file_name(path,withExtension=True)
            verify_excel_columns_message = self.verify_data_file_excel_columns(fileInformation,fileName)
            if verify_excel_columns_message != None:
                return verify_excel_columns_message
            return message
        except:
            return "Cannot open the file, please recheck the path !!!"

    def verify_data_file_excel_columns(self,fileInformation,fileName):
        columnList = fileInformation.columns.values
        message = ""
        for expectedColumn in self.dataFileColumnList:
            if (expectedColumn not in columnList):
                message = "The file " + '"' + fileName + '"' +" does not contain enought columns, please refer to the template file to get all the columns information !!!"
                return message
        return message

    def verify_data_file_json_file(self,dataFilePath):
        try:
            message = ""
            fileName = self.detach_file_name(dataFilePath,True)
            with open(dataFilePath) as f:
                data = json.load(f)
                for item in data:
                    for expectedColumn in self.dataFileColumnList:
                        if expectedColumn not in item.keys():
                            message = "The file " + '"' + fileName + '"' + " does not contain enought columns, please refer to the template file to get all the columns information !!!"
                            return message
        except Exception:
            return "Cannot open the file, please recheck the path !!!"
        return message