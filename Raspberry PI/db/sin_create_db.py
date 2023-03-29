import sqlite3

# Tilslutter til database
conn = sqlite3.connect('sinDB.db')

# Vi laver et curser object til at eksekvere SQL kommandoer
cur = conn.cursor()

try:
    cur.execute('''
                CREATE TABLE IF NOT EXISTS bruger (
                [bruger_id] INTEGER PRIMARY KEY,
                [brugernavn] TEXT NOT NULL,
                [kode] TEXT NOT NULL,
                [produkt] INTEGER NOT NULL
                )
                ''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS koordinater (
                [koordinat_id] INTEGER PRIMARY KEY,
                [bruger_id] INTEGER NOT NULL,
                [latitude] TEXT,
                [longitude] TEXT,
                FOREIGN KEY (bruger_id) REFERENCES bruger(bruger_id)
                )
                ''')

    cur.execute('''
                CREATE TABLE IF NOT EXISTS telefon (
                [telefon_id] INTEGER PRIMARY KEY,
                [bruger_id] INTEGER NOT NULL,
                [telefonnummer] TEXT,
                FOREIGN KEY (bruger_id) REFERENCES bruger(bruger_id)
                )
                ''')
except sqlite3.Error as e:
    print(f'Could not create ! {e} ')
finally:
    conn.commit()
    conn.close()