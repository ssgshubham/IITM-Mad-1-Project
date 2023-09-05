import sqlite3

def create_tables():
    conn = sqlite3.connect('database.db')
    print("Connected to database successfully")


    conn.execute('''CREATE TABLE IF NOT EXISTS credentials (name TEXT, email TEXT, password TEXT)''')
    conn.execute('''CREATE TABLE IF NOT EXISTS category (cname TEXT, cename TEXT,unit TEXT,rate INTEGER CHECK (rate >= 0), cquantity INTEGER CHECK (cquantity >= 0),incart INTEGER CHECK (incart >= 0),orignalquantity INTEGER CHECK (cquantity >= 0) )''')

#    conn.execute('DROP TABLE credentials')
#    conn.execute('DROP TABLE category')

    print("Created table successfully!")

    conn.close()