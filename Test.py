import tkinter as tk
from tkinter import messagebox

def show_error_detail():
    # Tạo một cửa sổ dialog mới
    error_detail_dialog = tk.Toplevel(root)
    error_detail_dialog.title("Chi tiết lỗi")

    # Đặt biểu tượng cho cửa sổ dialog
    icon_path = './cross.png'
    error_detail_dialog.iconbitmap(icon_path)

    # Tạo khung Frame để chứa biểu tượng và nội dung chi tiết lỗi
    frame = tk.Frame(error_detail_dialog)
    frame.pack(padx=10, pady=10, anchor='w')  # 'anchor' là để căn giữa theo trục ngang (west)

    # Tạo widget Label để hiển thị biểu tượng
    icon_label = tk.Label(frame)
    icon_label.grid(row=0, column=0, padx=10, pady=10)  # Đặt vào hàng 0, cột 0 và canh lề

    # Tạo nội dung chi tiết lỗi (đây chỉ là ví dụ, bạn có thể thay thế bằng thông tin lỗi thực tế)
    error_detail_text = "Lỗi không xác định\nMã lỗi: 123456\nNgày: 2023-07-11"

    # Tạo widget Label để hiển thị nội dung chi tiết lỗi
    error_detail_label = tk.Label(frame, text=error_detail_text, padx=10, pady=10)
    error_detail_label.grid(row=0, column=1, padx=10, pady=10)  # Đặt vào hàng 0, cột 1 và canh lề

    # Đặt vị trí hiển thị của cửa sổ dialog
    x_offset = 100
    y_offset = 100
    error_detail_dialog.geometry(f"+{x_offset}+{y_offset}")

# Tạo một cửa sổ gốc
root = tk.Tk()
root.title("Tkinter Dialog")

# Tạo nút để mở dialog hiển thị chi tiết lỗi
error_button = tk.Button(root, text="Xem chi tiết lỗi", command=show_error_detail)
error_button.pack(padx=20, pady=20)

# Bắt đầu vòng lặp mainloop để hiển thị cửa sổ gốc
root.mainloop()

