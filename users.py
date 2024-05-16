import psycopg2
from colorama import Fore

db_name = 'n47'
user = 'postgres'
host = 'localhost'
password = '123'
port = 5432

conn = psycopg2.connect(database=db_name, user=user,
                        host=host, password=password, port=port)

cur = conn.cursor()


def create_table():
    create_table_query = """CREATE TABLE IF NOT EXISTS "user"(
                            id SERIAL PRIMARY KEY,
                            username VARCHAR(50) UNIQUE NOT NULL,
                            password VARCHAR(50) UNIQUE NOT NULL,
                            email VARCHAR(50) UNIQUE NOT NULL,
                            age INT NOT NULL CHECK(age > 0)); """
    cur.execute(create_table_query)
    conn.commit()


class User:
    def __init__(self, username: str, password_: str,
                 email: str, age: int):
        self.username = username
        self.password = password_
        self.email = email
        self.age = age

    @staticmethod
    def save(self):
        insert_query = """INSERT INTO "user"(username,password,email,age)
                          VALUES(%s,%s,%s,%s)"""
        n = input('Enter username: ')
        p = input('Enter password: ')
        e = input('Enter email: ')
        a = int(input('Enter age: '))
        u = User(n, p, e, a)
        data = (self.username, self.password,
                self.email, self.age)
        print(Fore.GREEN, "Data added successfully", Fore.RESET)
        cur.execute(insert_query, data)
        conn.commit()

    @staticmethod
    def get_all():
        select_query = """SELECT * FROM "user";"""
        cur.execute(select_query)
        users = cur.fetchall()
        for u in users:
            print(u)


User.get_all()
# while input("Do you want to use database(y/n): ").startswith('y'):
#     print(' Insert data into user ==> 1\n', 'Show all user info ==> 2')
#     try:
#         ch = int(input('...'))
#         if ch == 1:
#             n = input('Enter username: ')
#             p = check_password()
#             e = input('Enter email: ')
#             a = int(input('Enter age: '))
#             user = User(n, p, e, a)
#             user.save()
#         elif ch == 2:
#             User.get_all()
#         else:
#             print(Fore.RED, 'Wrong input !', Fore.RESET)
#     except Exception as e:
#         print(Fore.RED, e, Fore.RESET)
