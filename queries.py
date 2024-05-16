import psycopg2
from colorama import Fore
from datetime import datetime

db_name = 'n47'
password = '123'
host = 'localhost'
user = 'postgres'
port = 5432

conn = psycopg2.connect(dbname=db_name,
                        user=user,
                        password=password,
                        host=host,
                        port=port)

cur = conn.cursor()


def create_table():
    create_t_q = (""" CREATE TABLE IF NOT EXISTS products(
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(50) NOT NULL,
                        image VARCHAR(50),
                        is_liked BOOL DEFAULT FALSE,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                  );""")
    cur.execute(create_t_q)
    conn.commit()
    print(Fore.GREEN, "Table created successfully", Fore.RESET)


def insert_product_data():
    name = str(input('Enter product name: '))
    image = str(input('Enter product\'s image: '))
    is_liked = str(input('Is product liked(true/false): '))
    created_at = datetime.now()
    updated_at = datetime.now()
    insert_p_q = ("""INSERT INTO products (name, image,is_liked,created_at,updated_at)
                     VALUES (%s, %s,%s,%s,%s);""")
    params = (name, image, is_liked, created_at, updated_at)
    cur.execute(insert_p_q, params)
    conn.commit()
    print(Fore.GREEN, "Data added successfully", Fore.RESET)


def select_data():
    select_d_q = " SELECT * FROM products;"
    cur.execute(select_d_q)
    rows = cur.fetchall()
    for row in rows:
        print(row)


def update_product():
    choice = str(input('What do you want to update(id/name): '))
    _id = input('Enter id of product to update: ')
    try:
        if choice == 'id':
            new_id = input('Enter new id: ')
            update_p_q = "UPDATE products SET id = %s WHERE id = %s;"
            params = (_id, new_id)
            cur.execute(update_p_q, params)
            conn.commit()
        elif choice == 'name':
            new_name = input('Enter new product name: ')
            update_p_q = "UPDATE products SET name = %s WHERE id = %s;"
            params = (new_name, _id)
            cur.execute(update_p_q, params)
            conn.commit()
        else:
            print(Fore.RED, 'Wrong input !', Fore.RESET)
    except Exception as ex:
        print(Fore.RED, ex, Fore.RESET)
    finally:
        print(Fore.GREEN, "Data updated successfully", Fore.RESET)


def delete_product():
    _id = input('Enter id of product to delete: ')
    data = (_id,)
    delete_p_q = "DELETE FROM products WHERE id = %s;"
    cur.execute(delete_p_q, data)
    conn.commit()
    print(Fore.GREEN, "Data deleted successfully", Fore.RESET)


while input('Do you want to use db:(y/n): ').startswith('y'):
    print(" insert data => 1\n", "select data => 2\n", "update data => 3\n", "delete data => 4")
    try:
        ch = input("...")
        if ch == '1':
            insert_product_data()
        elif ch == '2':
            select_data()
        elif ch == '3':
            update_product()
        elif ch == '4':
            delete_product()
        else:
            print(Fore.RED, 'Wrong input !', Fore.RESET)
    except Exception as e:
        print(Fore.RED, e, Fore.RESET)
