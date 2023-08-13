from tkinter import *
import tkinter.ttk
import pandas

category = {'home': ['utilities','rent','cable'],
    'car': ['gas','oil','repairs'],
    'rv':['parks','maintenance','payment']}

class Application(Frame):

    def __init__(self, master=None, Frame=None):
        Frame.__init__(self, master)
        super(Application,self).__init__()
        self.grid(column = 5,row = 20,padx = 50,pady = 50)
        self.createWidgets()

    def getUpdateData(self,  event):
        self.AccountCombo['values'] = category[self.CategoryCombo.get()]

    def createWidgets(self):
        Label(text = 'Combo Box #1:').grid(row = 2,column = 1,padx = 10)
        Label(text = 'Combo Box #2:').grid(row = 4,column = 1,padx = 10)
        self.AccountCombo = tkinter.ttk.Combobox( width = 15)
        self.AccountCombo.grid(row = 5,column = 1,pady = 25,padx = 10)

        self.CategoryCombo = tkinter.ttk.Combobox(width = 15,  values = list(category.keys()))
        self.CategoryCombo.bind('<<ComboboxSelected>>', self.getUpdateData)
        self.CategoryCombo.grid(row = 3,column = 1,padx = 10,pady = 25)

app = Application()
app.mainloop()