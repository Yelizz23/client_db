import psycopg2


conn = psycopg2.connect(database="client_db", user="postgres", password="secret_password")

with conn.cursor() as cur:
    cur.execute('''
    DROP TABLE phone_number;
    DROP TABLE client
   ''')

    
#  Функция, создающая структуру БД (таблицы);
def create_table():
    with conn.cursor() as cur:
        cur.execute('''
        CREATE TABLE IF NOT EXISTS client(
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(60) NOT NULL,
        surname VARCHAR(60) NOT NULL,
        email VARCHAR(120)
        );
        ''')
        cur.execute('''
        CREATE TABLE IF NOT EXISTS phone_number(
        id SERIAL PRIMARY KEY,
        phone VARCHAR(50),
        client_id INTEGER NOT NULL REFERENCES client(id)
        );
        ''')

        
#  Функция, позволяющая добавить нового клиента;
def add_client(name_client, surname_client, email, phone):
    with conn.cursor() as cur:
        cur.execute('''
        INSERT INTO client(first_name, surname, email) VALUES(%s, %s, %s) RETURNING id;
        ''', (name_client, surname_client, email))
        res = cur.fetchone()
        cur.execute('''
        INSERT INTO phone_number(phone, client_id) VALUES (%s, %s);
        ''', (phone, res))

        
#  Функция, позволяющая добавить телефон для существующего клиента;
def add_phone(name, phone):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT id FROM client WHERE surname=%s;
        ''', (name,))
        res = cur.fetchone()[0]
        cur.execute('''
        INSERT INTO phone_number(phone, client_id) VALUES (%s, %s);
        ''', (phone, res))

        
#  Функция, позволяющая изменить данные о клиенте;
def update_client(name, last_name, new_name, new_surname, new_email):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT id FROM client WHERE first_name=%s AND surname=%s;
        ''', (name, last_name))
        res = cur.fetchone()[0]
        cur.execute('''
        UPDATE client SET first_name=%s, surname=%s, email=%s WHERE id=%s;
        ''', (new_name, new_surname, new_email, res))

        
#  Функция, позволяющая удалить телефон для существующего клиента;
def delete_phone(name, last_name):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT id FROM client WHERE first_name=%s AND surname=%s;
        ''', (name, last_name))
        res = cur.fetchone()[0]
        cur.execute('''
        DELETE FROM phone_number WHERE id=%s;
        ''', (res,))

        
#  Функция, позволяющая удалить существующего клиента;
def delete_client(name, last_name):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT id FROM client WHERE first_name=%s AND surname=%s;
        ''', (name, last_name))
        res = cur.fetchone()[0]
        print(res)
        cur.execute('''
        DELETE FROM phone_number WHERE client_id=%s;
        ''', (res,))
        cur.execute('''
        DELETE FROM client WHERE first_name=%s AND surname=%s
        ''', (name, last_name))

        
#  Функция, позволяющая найти клиента по его данным (имени, фамилии, email-у или телефону);
def find_client(name, last_name, e_mail, phone_num):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT first_name, surname, email, pn.phone FROM client c
        LEFT JOIN phone_number pn ON pn.client_id = c.id
        WHERE first_name=%s AND surname=%s AND email=%s AND pn.phone=%s;
        ''', (name, last_name, e_mail, phone_num))
        res = cur.fetchall()
        print(res)


create_table()

add_client('Audrey', 'Smith', 'smith.a@gmail.com', '+420608345177')
add_client('Alison', 'Dunlop', 'dun.al@hotmail.com', '+420775365145')
add_client('Melany', 'Cleo', 'cleo.melany@gmail.com', '+420721567544')
add_client('Thomas', 'Cook', 'cook.th@hotmail.com', '+420602252787')
add_client('Lesley', 'Ellers', 'miss.ellers@hotmail.com', '+420777187777')
add_client('Martin', 'Freeman', 'marty.free@gmail.com', '+42060660352')

add_phone('Smith', '+420602272666')
add_phone('Smith', '+420777875355')
add_phone('Smith', '+420606879456')
add_phone('Cleo', '+420773183478')
add_phone('Ellers', '+420773264355')
add_phone('Freeman', '+420774555178')

update_client('Melany', 'Cleo', 'Melany', 'Seeto', 'seeto.mel@gmail.com')
update_client('Martin', 'Freeman', 'Martin', 'Freeman', 'martin.freeman@hotmail.com')
update_client('Alison', 'Dunlop', 'Alison', 'Moore', 'moore.al@gmail.com')

delete_phone('Audrey', 'Smith')
delete_phone('Alison', 'Moore')
delete_phone('Melany', 'Seeto')
delete_client('Melany', 'Seeto')

find_client('Audrey', 'Smith', 'smith.a@gmail.com', '+420777875355')

conn.commit()
