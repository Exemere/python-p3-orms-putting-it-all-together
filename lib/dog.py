import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None  

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS dogs')
        CONN.commit()

    def save(self):
            CURSOR.execute('INSERT INTO dogs (name, breed) VALUES (?, ?)', (self.name, self.breed))
            CONN.commit()
            self.id = CURSOR.lastrowid
      

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        id, name, breed = data
        dog = cls(name, breed)
        dog.id = id
        return dog

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM dogs')
        return [cls.new_from_db(row) for row in CURSOR.fetchall()]

    @classmethod
    def find_by_name(cls, name):
        CURSOR.execute('SELECT * FROM dogs WHERE name = ?', (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_by_id(cls, id):
        CURSOR.execute('SELECT * FROM dogs WHERE id = ?', (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        else:
            return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        else:
            return cls.create(name, breed)

    def update(self):
        if self.id:
            CURSOR.execute('UPDATE dogs SET name=?, breed=? WHERE id=?', (self.name, self.breed, self.id))
            CONN.commit()

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

if __name__ == '__main__':
    Dog.create_table()
    
    
    
