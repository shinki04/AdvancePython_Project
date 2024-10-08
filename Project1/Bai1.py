# Dựa trên bài combox - button nhập 2 dòng A B , click me lấy giá trị a , b + , hoặc giải phương trình 1 2 , xuất kq ra button
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as mbox
# from tkinter import *

win = tk.Tk()
win.title("Simple Math")

tabControl = ttk.Notebook(win)
# Add the tab to tabControl:
tab1 = ttk.Frame(tabControl)  # Create a tab

tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
# Add a second tab
# * Thêm tab phải theo thứ tự 1 2 3 , chứ không nó loạn
tabControl.add(tab1, text='Ptrinh Bac 1')  # Add the tab

tabControl.add(tab2, text='Độ dài')
tabControl.add(tab3,text="Canvas")
tabControl.pack(expand=1, fill='both')  # Pack to make visible


main_label = ttk.Label(tab1, text="ax + b = 0")
main_label.grid(column=0, row=0 , padx=10 , pady=3)


a_label = ttk.Label(tab1, text="ax")
a_label.grid(column=0, row=2)
a = tk.IntVar()
a_entered = ttk.Entry(tab1, width=12, textvariable=a)
a_entered.grid(column=1, row=2 , padx=3)

b_label = ttk.Label(tab1, text="b")
b_label.grid(column=0, row=3)
b = tk.IntVar()
b_entered = ttk.Entry(tab1, width=12, textvariable=b)
b_entered.grid(column=1, row=3)

c = tk.IntVar()
c.set(0)

c_entered = ttk.Entry(tab1, width=12, textvariable=c, state="disable")
c_entered.grid(column=2, row=2)
# Click Event Handle Func


def click_me():
    try:
        if a.get() != 0:
            c.set(-b.get() / a.get())
        else:
            mbox.showerror("Error", "a phải khác 0")

    # Lỗi này là do sai giá trị
    except tk.TclError:
        mbox.showerror("Input Error", "Nhập số vào a và b")
    # ktra những lỗi khác, này dư thừa nhưng để cho bt
    except:
        mbox.showerror("Something wrong", "Check again")


# # Adding a button
action = ttk.Button(tab1, text="Giải", command=click_me)
action.grid(column=0, row=4, columnspan=3,pady=3)

# # Hàm chuyển đổi

def convert():
    try:
        input_value = float(entry.get())
        from_unit = from_combo.get()
        to_unit = to_combo.get()

    #     # Chuyển đổi từ km
    #     if from_unit == 'Kilometers (km)':
    #         if to_unit == 'Centimeters (cm)':
    #             result = input_value * 100000
    #         elif to_unit == 'Millimeters (mm)':
    #             result = input_value * 1000000
    #         else:
    #             result = input_value

    #     # Chuyển đổi từ cm
    #     elif from_unit == 'Centimeters (cm)':
    #         if to_unit == 'Kilometers (km)':
    #             result = input_value / 100000
    #         elif to_unit == 'Millimeters (mm)':
    #             result = input_value * 10
    #         else:
    #             result = input_value
    #     # Chuyển đổi từ mm
    #     elif from_unit == 'Millimeters (mm)':
    #         if to_unit == 'Kilometers (km)':
    #             result = input_value / 1000000
    #         elif to_unit == 'Centimeters (cm)':
    #             result = input_value / 10
    #         else:
    #             result = input_value
        # Hệ số chuyển đổi giữa các đơn vị
        conversion_factors = {
            'Kilometers (km)':
                {
                    'Kilometers (km)': 1,
                    'Centimeters (cm)': 100000,
                    'Millimeters (mm)': 1000000
                },
            'Centimeters (cm)': 
                {
                    'Kilometers (km)': 1/100000, 
                    'Centimeters (cm)': 1, 
                    'Millimeters (mm)': 10},
            'Millimeters (mm)': 
                {
                    'Kilometers (km)': 1/1000000, 
                    'Centimeters (cm)': 1/10, 
                    'Millimeters (mm)': 1
                }
        }

        # Tính kết quả dựa trên hệ số chuyển đổi
        result = input_value * conversion_factors[from_unit][to_unit]

        # Hiển thị kết quả
    #     .rstrip('0'): Xóa các số 0 ở cuối.
    #     .rstrip('.'): Xóa dấu chấm nếu không có phần thập phân nào sau dấu chấm.
        # result_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="N")
        # result_label.config(text=f"Result: {format(
        #     result, '.10f').rstrip('0').rstrip('.')} {to_unit}")
        re.set(format(result, '.10f').rstrip('0').rstrip('.'))
     # Lỗi này là do sai giá trị
    except tk.TclError:
        mbox.showerror("Input Error", "Nhập số vào a và b")
    # ktra những lỗi khác, này dư thừa nhưng để cho bt
    except ValueError:
        # Hiển thị thông báo lỗi nếu người dùng nhập không phải là số
        mbox.showerror("Lỗi nhập liệu", "Nhập số")
    except:
        mbox.showerror("Something wrong", "Check again")



# Tiêu đề
title_label = tk.Label(
    tab2, text="Convert Between Kilometers, Centimeters, and Millimeters")
title_label.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

# Nhập số liệu
entry_label = tk.Label(tab2, text="From:")
entry_label.grid(row=1, column=0)

entry = tk.Entry(tab2, width=10)
entry.grid(row=1, column=1)

# # Chọn đơn vị gốc
# from_label = tk.Label(tab2, text="From:")
# from_label.grid(row=1, column=0, padx=10, pady=5)

from_combo = ttk.Combobox(tab2, width=15, state='readonly')
from_combo['value'] = (
    'Kilometers (km)', 'Centimeters (cm)', 'Millimeters (mm)')

from_combo.current(0)
from_combo.grid(row=1, column=2)

# Chọn đơn vị đích
to_label = tk.Label(tab2, text="To:")
to_label.grid(row=2, column=0)

re = tk.DoubleVar()
entry_to = tk.Entry(tab2, width=10, state="disabled", textvariable=re)
entry_to.grid(row=2, column=1)

to_combo = ttk.Combobox(tab2, width=15, state='readonly')
to_combo['value'] = ('Kilometers (km)', 'Centimeters (cm)', 'Millimeters (mm)')
to_combo.current(0)
to_combo.grid(row=2, column=2, pady=3)

# Nút chuyển đổi
convert_button = tk.Button(tab2, text="Convert", command=convert)
convert_button.grid(row=4, column=0, columnspan=3, pady=10)

# # Nhãn hiển thị kết quả
# result_label = tk.Label(tab2, text="Result: ")
# result_label.grid(row=5, column=0, columnspan=2, pady=10, sticky="N")

tab3_frame = tk.Frame(tab3, bg='blue')  
tab3_frame.pack()

for orange_color in range(2):
        canvas = tk.Canvas(tab3_frame, width=150, height=80,  highlightthickness=0, bg='orange')
        canvas.grid(row=orange_color, column=orange_color)
win.mainloop()
