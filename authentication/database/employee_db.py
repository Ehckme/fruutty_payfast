import mysql.connector

class CreateDb:
    def __init__(self, db_name, host, username, password):
        self.db_name = db_name
        self.host = host
        self.username = username
        self.password = password

    def connect(self):
        conn = mysql.connector.connect(host=self.host, user=self.username, password=self.password, )
        if conn.is_connected():
            success_message = 'Connection Established'
            print(success_message)
        else:
            success_message = 'No Connection Established'
            print(success_message)

        my_cursor = conn.cursor()
        my_cursor.execute(f'CREATE DATABASE {self.db_name}')
        my_cursor.execute('SHOW DATABASES')
        for db in my_cursor:
            print(db)

    def __repr__(self,):
        return f'CreateDb("{self.db_name!r}", "{self.host!r}", "{self.username!r}", "{self.password!r}", )'
        # my_cursor.close()
        # conn.close()
if __name__ == '__main__':
    fruutty_employees = CreateDb('Fruutty_employees', 'localhost', 'root', '#FruuttydbPassword123')
    fruutty_employees.connect()

