import tkinter

class MessageDialog():
    def __init__(self, root):
        self.gui = root
        self.mainFrame = self.gui.get_main_frame()
        self.subFrame = tkinter.Toplevel(master= self.mainFrame)
        self.messageDetail = tkinter.Label(self.subFrame,text="",wraplength=300)
        self.okButton = tkinter.Button(self.subFrame, text="Ok", command=())
        self.cancelButton = tkinter.Button(self.subFrame, text="Cancel", command=())
        
    def line_up_components(self,messageTitle,messageDetail):
        self.subFrame.title(messageTitle)
        self.subFrame.resizable(False,False)
        subFrame_width = 350
        subFrame_height = 100
        subFrame_x_position = self.mainFrame.winfo_x() + int(self.mainFrame.winfo_width()/2) - int(subFrame_width/2)
        subFrame_y_position = self.mainFrame.winfo_y() + int(self.mainFrame.winfo_height()/2) - int(subFrame_height/2)
        self.subFrame.geometry(f"{subFrame_width}x{subFrame_height}+{subFrame_x_position}+{subFrame_y_position}")
        self.subFrame.grid_rowconfigure(index=0,weight=1)
        self.subFrame.grid_rowconfigure(index=1, weight=1)
        self.subFrame.grid_columnconfigure(index = 0, weight=1)
        self.subFrame.grid_columnconfigure(index = 1, weight=1)
        self.subFrame.grid_columnconfigure(index = 2, weight=1)
        self.subFrame.grid_columnconfigure(index = 3, weight=1)
        self.messageDetail['text'] = messageDetail
        
        self.messageDetail.grid(row= 0 , column=0,columnspan=2)
        self.okButton.grid(row = 1, column = 1, sticky='nsew')
        self.cancelButton.grid(row = 1, column= 3, sticky='nsew')
        
        
    def display_message_dialog(self,messageType,messageTitle,messageDetail):
        if messageType == 'Error':
            self.line_up_components(messageTitle=messageTitle, messageDetail=messageDetail)
        elif messageType == 'Success':
            self.line_up_components(messageTitle=messageTitle, messageDetail=messageDetail)
        elif messageType == 'Info':
            self.line_up_components(messageTitle=messageTitle, messageDetail=messageDetail)
        else:
            pass