'''
GUI made by HieuTran 20/10/2024
'''

import tkinter as tk
from tkinter import Menu, ttk, messagebox, filedialog
from psycopg2 import sql
import pandas as pd
from PIL import Image, ImageTk
from database import Database

class TableApp(Database):
    def __init__(self, root, db_name, user, password, host, port,table_name):
        super().__init__(db_name, user, password, host, port,table_name)
        self.root = root
        self.root.iconbitmap('logo.ico')
        self.root.title("Kết nối database")
        # File menu
        self.menu_bar = Menu(self.root)
        file_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Xuất", command=self.export_to_excel)
        file_menu.add_command(label="Exit", command=self.quit_app)
        # Help_menux
        help_menu = Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.msg_box_info)
        self.root.config(menu=self.menu_bar)
        self.root.title("Quản lý sinh viên")
        self.db_name = tk.StringVar(value=db_name)
        self.user = tk.StringVar(value=user)
        self.password = tk.StringVar(value=password)
        self.host = tk.StringVar(value=host)
        self.port = tk.StringVar(value=port)
        self.table_name = tk.StringVar(value=table_name)
        

        
        
        original_image = Image.open("logovlu.png")
        resized_image = original_image.resize((100, 100))
        self.image = ImageTk.PhotoImage(resized_image)
        
        # width = 700
        # height = 700
        # self.root.geometry(f"{height}x{width}")
        # screen_width = self.root.winfo_screenwidth()
        # screen_height = self.root.winfo_screenheight()
        # x = (screen_width - width) // 2
        # y = (screen_height - height) // 2
        # self.root.geometry(f'{width}x{height}+{x}+{y}')

        self.widgets_connect()

    def widgets_connect(self):

        self.connection_frame = tk.Frame(self.root)
        self.connection_frame.pack(pady=10)

        image_label = tk.Label(self.connection_frame, image=self.image)
        image_label.grid(row=0, column=0, columnspan=3, pady=20)

        tk.Label(self.connection_frame, text="DB Name:").grid(
            row=1, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.db_name).grid(
            row=1, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="User:").grid(
            row=2, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.user).grid(
            row=2, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Password:").grid(
            row=3, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.password,
                 show="*").grid(row=3, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Host:").grid(
            row=4, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.host).grid(
            row=4, column=1, padx=5, pady=5)

        tk.Label(self.connection_frame, text="Port:").grid(
            row=5, column=0, padx=5, pady=5)
        tk.Entry(self.connection_frame, textvariable=self.port).grid(
            row=5, column=1, padx=5, pady=5)

        tk.Button(self.connection_frame, text="Connect",
                  command=self.connect_to_manage).grid(row=6, columnspan=2, pady=10)

    def widgets_manage(self):

        # Khung chứa bảng
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(pady=10)
        tk.Label(self.table_frame, text="Quản lý sinh viên VLU", border=2, font=(
            "Helvetica", 16, "bold")).grid(column=0, row=0, columnspan=3, pady=20)
        # Tạo bảng Treeview
        self.data_table = ttk.Treeview(self.table_frame, columns=(
            "MSSV", "Họ", "Tên"), show="headings", height=10)
        self.data_table.heading("MSSV", text="MSSV")
        self.data_table.heading("Họ", text="Họ")
        self.data_table.heading("Tên", text="Tên")

        self.data_table.column("MSSV", width=100)
        self.data_table.column("Họ", width=200)
        self.data_table.column("Tên", width=200)
        self.data_table.grid(column=0, row=2)
        self.data_table.bind("<ButtonRelease-1>", self.on_tree_select)
        self.load_data_tabletree()

        # Khung chứa các ô nhập liệu
        form_frame = ttk.LabelFrame(self.root, text="")
        form_frame.pack(pady=10)

        # Nhãn và ô nhập MSSV
        input_frame = ttk.LabelFrame(form_frame, text="Entry Frame")
        input_frame.grid(padx=10, row=0, column=0)
        ttk.Label(input_frame, text="MSSV : ").grid(
            row=0, column=0, padx=5, pady=5)
        self.mssv = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.mssv).grid(
            row=0, column=1, padx=5, pady=5)

        # Nhãn và ô nhập Họ Tên
        ttk.Label(input_frame, text="Họ : ").grid(
            row=1, column=0, padx=5, pady=5)
        self.ho = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.ho).grid(
            row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Tên : ").grid(
            row=2, column=0, padx=5, pady=5)
        self.ten = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.ten).grid(
            row=2, column=1, padx=5, pady=5)

        # Frame button
        button_frame = ttk.LabelFrame(form_frame, text="Button Frame")
        button_frame.grid(padx=10, row=0, column=1)
        # Nút để thêm hàng mới
        add_button = ttk.Button(
            button_frame, text="Thêm hàng mới", command=self.add_data_button)
        add_button.grid(column=0, row=0, padx=5, pady=10)

        # Nút để load data
        load_button = ttk.Button(
            button_frame, text="Load data", command=self.load_data_button)
        load_button.grid(column=1, row=0, padx=5, pady=10)
        # Nút để xóa data đang chọn
        delete_button = ttk.Button(
            button_frame, text="Xóa các hàng đang chọn", command=self.delete_selected_row)
        delete_button.grid(column=0, row=1, padx=5, pady=10)

        # Nút để xóa data trong ô
        delete_input_button = ttk.Button(
            button_frame, text="Xóa dữ liệu trong ô mssv", command=self.delete_data_button)
        delete_input_button.grid(column=1, row=1, padx=5, pady=10)

        # Nút clear input
        clear_button = ttk.Button(
            button_frame, text="Xóa nội dung trong ô", command=self.clear_inputs)
        clear_button.grid(column=0, row=2, padx=5, pady=10)
        # Nút update data
        update_button = ttk.Button(
            button_frame, text="Cập nhật nội dung trong ô", command=self.update_data_button)
        update_button.grid(column=1, row=2, padx=5, pady=10)

    def on_tree_select(self, event):
        """Xử lý khi người dùng chọn hàng trong Treeview"""
        selected_items = self.data_table.selection()
        if selected_items:
            item = selected_items[0]
            values = self.data_table.item(item, 'values')
            mssv = values[0]
            ho = values[1]
            ten = values[2]
            self.mssv.set(mssv)
            self.ho.set(ho)
            self.ten.set(ten)

    # def insert_data_button(self):
    #     mssv = self.mssv.get().strip()
    #     ho = self.ho.get().strip()
    #     ten = self.ten.get().strip()

    #     if self.check_exsit(self.mssv.get()):
    #         self.insert_data(mssv,ho,ten)
    #         self.add_table(mssv, ho, ten)
    #         self.clear_inputs()
    #         self.load_data_tabletree()
    #     else:
    #         messagebox.showerror("Error", "Mã sinh viên không tồn tại")

    def add_data_button(self):
        """Thêm sinh viên mới vào cơ sở dữ liệu và bảng Treeview"""
        mssv = self.mssv.get().strip()
        ho = self.ho.get().strip()
        ten = self.ten.get().strip()

        if self.validate_input(mssv, ho, ten):
            if self.check_exist(mssv):
                messagebox.showerror("Error", "Mã sinh viên đã tồn tại")
            else:
                if self.insert_data(mssv,ho,ten) :
                    self.add_table(mssv, ho, ten)
                    self.clear_inputs()
                    self.load_data_tabletree()
                else :
                    messagebox.showerror("Error", "Lỗi")

    def update_data_button(self):
        mssv = self.mssv.get().strip()
        ho = self.ho.get().strip()
        ten = self.ten.get().strip()
        
        if self.check_exist(mssv):
            result = self.update_data(mssv, ho, ten)  # Lấy cả result và error
            if result:
                self.clear_inputs()
                self.load_data_tabletree()
            else:
                # Hiển thị thông báo lỗi nếu có vấn đề xảy ra và hiển thị thông tin lỗi từ biến 'error'
                messagebox.showerror("Error", f"Đã xảy ra lỗi khi cập nhật dữ liệu")
        else:
            messagebox.showerror("Error", "Mã sinh viên không tồn tại")

    def delete_data_button(self):
        mssv = self.mssv.get().strip()
        if self.check_exist(mssv):
            result = self.delete_data(mssv)
            if result :
                self.clear_inputs()
                messagebox.showinfo("Done", "Đã xóa thành công   ")
                self.load_data_tabletree()

        else:
            messagebox.showerror("Error", "Mã sinh viên không tồn tại")

    def load_data_button(self):
        if self.check_load_data():
            messagebox.showinfo("Success", "Load data done")

    def validate_input(self, mssv, ho, ten):
        """Kiểm tra đầu vào không được để trống."""
        if not mssv or not ho or not ten:
            messagebox.showwarning(
                "Lỗi nhập liệu", "MSSV và Họ Tên không được để trống.")
            return False
        return True

    def add_table(self, mssv, ho, ten):
        """Thêm hàng mới vào bảng Treeview."""
        new_row = (mssv, ho, ten)
        self.data_table.insert("", tk.END, values=new_row)

    def clear_inputs(self):
        """Xóa các ô nhập liệu sau khi thêm dữ liệu thành công."""
        self.mssv.set("")
        self.ho.set("")
        self.ten.set("")

    
    def load_data_tabletree(self):
        result = self.load_data()  # Gọi load_data và lưu kết quả
        if result:  # Nếu result không phải False
            rows = result  # Gán rows là kết quả trả về của load_data
            self.data_table.delete(*self.data_table.get_children())  # Xóa dữ liệu cũ
            for row in rows:
                self.data_table.insert("", tk.END, values=row)  # Chèn dữ liệu vào bảng
            messagebox.showinfo("Done", "Dữ liệu đã được tải thành công")
        else:
            messagebox.showerror("Error", "Không thể tải dữ liệu từ cơ sở dữ liệu")
        

    def delete_selected_row(self):
        """Xóa hàng đang được chọn trong Treeview"""
        try:
            # Lấy tất cả các hàng đang được chọn
            selected_items = self.data_table.selection()
            if not selected_items:
                messagebox.showwarning("Lỗi", "Vui lòng chọn hàng để xóa.")
                

            for item in selected_items:
                values = self.data_table.item(item, 'values')
                mssv = values[0]
                result= self.delete_data(mssv)
                if result :
                    if item in self.data_table.get_children():
                        self.data_table.delete(item)
                    else:
                        messagebox.showwarning(
                            "Lỗi", f"Item {item} không tồn tại trong bảng.")

            self.clear_inputs()
            messagebox.showinfo("Thành công", "Đã xóa hàng thành công.")
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting selected row: {e}")

    def delete_data_input(self):
        try:
            self.delete_data(self.mssv.get())
            self.load_data_tabletree()
            self.clear_inputs()
            messagebox.showinfo("Success", "Đã xóa thành công")
        except Exception as e:
            messagebox.showerror("Error", f"{e}")

  

    def connect_to_manage(self):
        result = self.connect_db()
        if result is True:
            # Kết nối thành công
            # print("Kết nối cơ sở dữ liệu thành công!")
            self.connection_frame.pack_forget()
            self.widgets_manage()
        else:
            # Kết nối thất bại, xử lý lỗi
            result, error = result
            print(f"Không thể kết nối: {error}")
    def msg_box_info(self):
        messagebox.showinfo(
            "About", "This is a GUI made by Hieu Tran version 1.0\n Release in 10/13/2024\n")

    def quit_app(self):
        self.root.destroy()

    def check_exist(self, mssv):
        children = self.data_table.get_children()
        for child in children:
            values = self.data_table.item(child, 'values')
            if values[0] == mssv:
                return True
        return False

    def export_to_excel(self):
        try:
            rows = []
            for item in self.data_table.get_children():
                row_data = self.data_table.item(item)['values']
                rows.append(row_data)

            # Tạo DataFrame
            df = pd.DataFrame(rows, columns=["MSSV", "Họ", "Tên"])
            df.index = df.index + 1

            # Mở hộp thoại lưu tệp để chọn đường dẫn lưu
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[
                                                         ("Excel files", "*.xlsx"), ("All files", "*.*")],
                                                     title="Chọn nơi lưu file")
            if file_path:  # Nếu người dùng không hủy
                # Xuất ra file Excel
                df.to_excel(file_path, index=True)
                messagebox.showinfo(
                    "Xuất file", "Dữ liệu đã được xuất ra file Excel thành công!")
            else:
                messagebox.showwarning("Hủy", "Bạn đã hủy lưu file.")

        except Exception as e:
            messagebox.showwarning("Warning", f"Có lỗi xảy ra: {str(e)}")
            
    def check_load_data(self):
        result = self.load_data()
        if result is False:
            messagebox.showerror("Error", "Không thể load dữ liệu")
            return False
        else : 
            return True


if __name__ == "__main__":
    root = tk.Tk()
    db_name ="quanlysinhvien"
    user ="postgres"
    password ="123456"
    host ="localhost"
    port ="5432"
    table_name ="sinhvien"
    TableApp(root,db_name, user, password, host, port,table_name)
    root.mainloop()
