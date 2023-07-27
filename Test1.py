import Test

GUI = Test.GUI()
GUI.start_up()



# import tkinter as tk
# from tkinter import ttk

# def simulate_progress():
#     progress['maximum'] = 100
#     for i in range(101):
#         progress['value'] = i
#         progress.update()
#         progress_label['text'] = f"Tiến trình: {i}%"
#         root.update()
#         # Tạm dừng để mô phỏng quá trình
#         root.after(100)  # 100 milliseconds

# root = tk.Tk()

# progress_frame = ttk.Frame(root, padding=20)
# progress_frame.pack()

# progress = ttk.Progressbar(progress_frame, orient='horizontal', mode='determinate')
# progress.pack()

# progress_label = ttk.Label(progress_frame, text="Tiến trình: 0%")
# progress_label.pack()

# start_button = ttk.Button(root, text="Bắt đầu", command=simulate_progress)
# start_button.pack()

# root.mainloop()







