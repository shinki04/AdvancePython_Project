import psycopg2
from psycopg2 import sql
from tkinter import messagebox
class Database:
    def __init__(self,db_name, user, password, host, port,table_name) :
            self.db_name = db_name
            self.user = user
            self.password = password
            self.host = host
            self.port = port
            self.table_name = table_name
    
    def connect_db(self):
        """Kết nối tới cơ sở dữ liệu PostgreSQL"""
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),  # Lấy giá trị chuỗi từ tk.StringVar
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get(),  # Lấy giá trị cổng từ tk.StringVar
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            return False
        
    def insert_data(self,mssv,ho,ten):
            """Chèn dữ liệu sinh viên vào cơ sở dữ liệu"""
            try:
                insert_query = sql.SQL("INSERT INTO {} (mssv, ho,ten) VALUES (%s, %s,%s)").format(
                    sql.Identifier(self.table_name.get()))
                data_to_insert = (mssv, ho, ten)
                self.cur.execute(insert_query, data_to_insert)
                self.conn.commit()
                return True
            except Exception as e:
                self.conn.rollback()
                return False
    
    def load_data(self):
        """Tải dữ liệu từ cơ sở dữ liệu và hiển thị trong bảng Treeview"""
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query) 
            rows = self.cur.fetchall()
            return rows
        except Exception :
            return False

            
    def update_data(self,mssv,ho,ten):
        try:
            update_query = sql.SQL("UPDATE {} SET ho = %s, ten = %s WHERE mssv = %s").format(
                sql.Identifier(self.table_name.get()))
            data_to_update = (ho, ten, mssv)
            self.cur.execute(update_query, data_to_update)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False 
        
        
    def delete_data(self, mssv):
        """Xóa dữ liệu sinh viên khỏi cơ sở dữ liệu theo MSSV"""
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(
                sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (mssv,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            return False 