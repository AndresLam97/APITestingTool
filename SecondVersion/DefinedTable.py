from tkinter import *
# Table class
class Table:
    # Initialize a constructor
    def __init__(self, gui):
        employee_list = [('Collection', 'Environment', 'Database', 'Data File','Run Time'),
                        ("My Collection", 'Gorge', 'California', 30,"Male"),
                        (2, 'Maria', 'New York', 19,"Male"),
                        (3, 'Albert', 'Berlin', 22,"Male"),
                        (4, 'Harry', 'Chicago', 19,"Male"),
                        (5, 'Vanessa', 'Boston', 31,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (6, 'Ali', 'Karachi', 30,"Male"),
                        (2, 'Maria', 'New York', 19,"Male"),
                        (2, 'Maria', 'New York', 19,"Male"),
                        (2, 'Maria', 'New York', 19,"Male"),
                        (2, 'Maria', 'New York', 19,"Male"),
                        (2, 'Maria', 'New York', 19,"Male")]
        total_rows = len(employee_list)
        total_columns = len(employee_list[0])
        # An approach for creating the table
        for i in range(total_rows):
            for j in range(total_columns):
                if i ==0:
                    self.entry = Entry(gui, width=18, bg='LightSteelBlue',fg='Black',
                                       font=('Arial', 11, 'bold'))
                else:
                    self.entry = Entry(gui, width=18, fg='blue',
                               font=('Arial', 11, ''))

                self.entry.grid(row=i, column=j)
                self.entry.insert(END, employee_list[i][j])
                