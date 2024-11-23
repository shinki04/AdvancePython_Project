import psycopg2
from psycopg2 import sql
import base64 
import os

class Database:
    def __init__(self, db_name, user, password, host, port, table_name):
        # self.db_name = db_name
        # self.user = user
        # self.password = password
        # self.host = host
        # self.port = port
        # self.table_name = table_name
        
        self.db_url = os.getenv('DATABASE_URL')  # Lấy URL từ biến môi trường
        self.table_name = table_name

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(self.db_url)
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cur = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Connection error: {e}")
            return False

    def insert_data(self, mssv, ho, ten, image_path):
        try:
            with open(image_path, "rb") as image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')
            insert_query = sql.SQL("INSERT INTO {} (mssv, ho, ten, image) VALUES (%s, %s, %s, %s)").format(
                sql.Identifier(self.table_name))
            data_to_insert = (mssv, ho, ten, image_data)
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Insertion error: {e}")
            return False

    def load_data(self):
        try:
            query = sql.SQL("SELECT mssv, ho, ten, image FROM {}").format(sql.Identifier(self.table_name))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            return rows
        except Exception as e:
            print(f"Loading error: {e}")
            return False
        
    def get_student_by_mssv(self, mssv):
        try:
            query = sql.SQL("SELECT mssv, ho, ten, image FROM {} WHERE mssv = %s").format(
                sql.Identifier(self.table_name)
            )
            self.cur.execute(query, (mssv,))
            return self.cur.fetchone()
        except Exception as e:
            print(f"Error fetching student: {e}")
            return None

    def update_data(self, mssv, ho, ten, image_path=None):
        try:
            if image_path:
                with open(image_path, "rb") as image_file:
                    image_data = base64.b64encode(image_file.read()).decode('utf-8')
                update_query = sql.SQL("UPDATE {} SET ho = %s, ten = %s, image = %s WHERE mssv = %s").format(
                    sql.Identifier(self.table_name)
                )
                data_to_update = (ho, ten, image_data, mssv)
            else:
                update_query = sql.SQL("UPDATE {} SET ho = %s, ten = %s WHERE mssv = %s").format(
                    sql.Identifier(self.table_name)
                )
                data_to_update = (ho, ten, mssv)
            self.cur.execute(update_query, data_to_update)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Update error: {e}")
            return False
        
    
    def delete_data(self,mssv):
        try: 
            delete_query = sql.SQL("DELETE FROM {} WHERE mssv = %s").format(sql.Identifier(self.table_name))
            self.cur.execute(delete_query, (mssv,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Delete error: {e}")
            return False
    
    
    # def validate_user(self, username, password):
    #     try:
    #         query = sql.SQL("SELECT * FROM users WHERE username = %s AND password = %s")
    #         self.cur.execute(query, (username, password))
    #         user = self.cur.fetchone()
    #         return user is not None
    #     except Exception as e:
    #         print(f"Login error: {e}")
    #         return False
