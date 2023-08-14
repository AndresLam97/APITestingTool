import tags
import tkinter,tkinter.ttk
import time

class ProgressBar():
    def __init__(self,mainFrame):
        self.gui = mainFrame
        self.mainFrame = mainFrame.get_main_frame()
        self.subFrame = tkinter.Toplevel(master=self.mainFrame)
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
        self.subFrame.grab_set()

    def animated_run(self,stopPoint,runspeed):
        try:
            self.progress['maximum'] = 100
            index = self.progress['value']
            while index <= stopPoint:
                self.progress['value'] = index
                self.progressLabel['text'] = "Progress: " + str(index) + "%"
                self.progress.update()
                self.subFrame.after(runspeed)
                index = index + 1
            if self.progress['value'] == 100:
                self.subFrame.grab_release()
                self.subFrame.destroy()
        except Exception as ex:
            print(str(ex))