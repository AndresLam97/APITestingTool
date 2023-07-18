import GUI
import tkinter,tkinter.ttk
import random
import time

class ProgressBar():
    def __init__(self,mainFrame):
        self.gui = mainFrame
        self.mainFrame = mainFrame.get_main_frame()
        self.subFrame = tkinter.Toplevel(master=mainFrame.get_main_frame())
        self.progress = tkinter.ttk.Progressbar(self.subFrame, orient='horizontal', mode='determinate')
        self.progressLabel = tkinter.ttk.Label(self.subFrame,text="Progress: 0%",anchor="center")

    def line_up_components(self):
        self.subFrame.title("Collection running")
        self.subFrame.resizable(False,False)
        subFrame_width = 280
        subFrame_height = 50
        subFrame_x_position = self.mainFrame.winfo_x() + int(self.mainFrame.winfo_width()/2) - int(subFrame_width/2)
        subFrame_y_position = self.mainFrame.winfo_y() + int(self.mainFrame.winfo_height()/2) - int(subFrame_height/2)

        self.progress['length'] = 220
        self.progressLabel['width'] = 50

        self.progress.pack(pady=5)
        self.progressLabel.pack()
        self.subFrame.geometry(f"{subFrame_width}x{subFrame_height}+{subFrame_x_position}+{subFrame_y_position}")
        
    def animated_run(self):
        self.line_up_components()
        try:
            self.subFrame.grab_set()
            self.progress['maximum'] = 100
            stopPoint = random.randint(50,90)
            index = 0
            while index < 101:
                if self.gui.get_progress_check_variable() == False and index < stopPoint:
                    self.progress['value'] = index
                    self.progressLabel['text'] = "Progress: " + str(index) + "%"
                    self.progress.update()
                    self.subFrame.after(100)
                    index = index + 1
                elif self.gui.get_progress_check_variable() == True:
                    self.progress['value'] = index
                    self.progressLabel['text'] = "Progress: " + str(index) + "%"
                    self.progress.update()
                    self.subFrame.after(50)
                    index = index + 1
                else:
                    time.sleep(0.2)
            self.subFrame.grab_release()
        except Exception as ex:
            print(str(ex))