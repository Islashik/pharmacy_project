class tabletSQL():
    def __init__(self, cursor):
        self.cursor = cursor

    def show_tables(self):
        query = """
        SHOW TABLES;
        """
        self.cursor.execute(query)

    def create_table_med(self):
        query = """
        CREATE TABLE tablets(
            id INTEGER PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(30) NOT NULL,
            price VARCHAR(100) NOT NULL,
            description TEXT NOT NULL);
        """
        self.cursor.execute(query)

    def add_new_medicine(self, name,price, description):
        query = f"""
         INSERT INTO tablets(name, price, description) 
         VALUES('{name}','{price}','{description}');
         """
        self.cursor.execute(query)
        print('Новое лекарство успешно добавлено!')

    def delete_table_tablets(self):
        self.cursor.execute("DROP TABLE tablets")

    def extract_data(self,id):
        self.cursor.execute(f"SELECT * FROM tablets WHERE id = {id}")
        return self.cursor.fetchone()

    def update_data_with_name(self,id,name):
        self.cursor.execute(f"""
        UPDATE tablets
        SET name='{name}' WHERE id = {id};""")

    def update_data_with_price(self,id,price):
        self.cursor.execute(f"""
        UPDATE tablets
        SET price='{price}' WHERE id = {id};""")

    def update_data_with_desc(self,id,desc):
        self.cursor.execute(f"""
        UPDATE tablets
        SET description='{desc}' WHERE id = {id};""")

    def extract_all_data(self):
        self.cursor.execute(f"SELECT * FROM tablets")
        return self.cursor.fetchall()

    def extract_name(self):
        self.cursor.execute(f"SELECT name FROM tablets")
        return self.cursor.fetchall()

    def extract_one_tablet(self, id):
        self.cursor.execute(f"SELECT * FROM tablets WHERE id={id}")
        return self.cursor.fetchall()