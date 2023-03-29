import sqlite3

# Insert function
def insertIntoDB():
    conn = sqlite3.connect('sinDB.db')
    
    query = 'INSERT INTO bruger (brugernavn, kode, produkt) VALUES(?,?,?)'
    data = (brugernavn, kode, produkt)
    try:
        cur = conn.cursor()
        cur.execute(query, data)
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert into bruger ! {e} ')
    finally:
        conn.commit()
        conn.close()



brugernavn, kode, produkt = "test", "test", "1234"
insertIntoDB()