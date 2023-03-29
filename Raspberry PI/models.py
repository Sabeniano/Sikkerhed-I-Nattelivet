import sqlite3
import os

db_path = db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'db', 'sinDB.db'))

class Bruger:
    def __init__(self, brugernavn, kode, produkt, bruger_id):
        self.brugernavn = brugernavn
        self.kode = kode
        self.produkt = produkt
        self.bruger_id = bruger_id

    def save(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        if self.id:
            cur.execute('UPDATE bruger SET brugernavn=?, kode=?, produkt=? WHERE bruger_id=?', (self.brugernavn, self.kode, self.produkt, self.bruger_id))
        else:
            cur.execute('INSERT INTO bruger (brugernavn, kode, produkt) VALUES (?, ?, ?)', (self.brugernavn, self.kode, self.produkt))
            self.id = cur.lastrowid
        conn.commit()
        conn.close()

    def insert(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('INSERT INTO bruger (brugernavn, kode, produkt) VALUES (?, ?, ?)', (self.brugernavn, self.kode, self.produkt))
        self.id = cur.lastrowid
        conn.commit()
        conn.close()

    def delete(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('DELETE FROM bruger WHERE bruger_id=?', (self.bruger_id,))
        conn.commit()
        conn.close()

    def koordinater(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT latitude, longitude FROM koordinater WHERE bruger_id=?', (self.bruger_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return row
        else:
            return None

    def telefon(self):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT telefonnummer FROM telefon WHERE bruger_id=?', (self.bruger_id,))
        row = cur.fetchone()
        conn.close()
        if row:
            return row[0]
        else:
            return None

    @staticmethod
    def find_by_username(brugernavn):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM bruger WHERE brugernavn=?', (brugernavn,))
        row = cur.fetchone()
        conn.close()
        if row:
            return Bruger(row[1], row[2], row[3], row[0])
        else:
            return None

    @staticmethod
    def get_all():
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute('SELECT * FROM bruger')
        rows = cur.fetchall()
        conn.close()
        users = []
        for row in rows:
            user = Bruger(row[1], row[2], row[3])
            user.id = row[0]
            users.append(user)
        return users