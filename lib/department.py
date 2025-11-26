from __init__ import CURSOR, CONN

class Department:

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
                id INTEGER PRIMARY KEY,
                name TEXT,
                location TEXT
            );
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS departments;"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?);
        """
        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid

    @classmethod
    def create(cls, name, location):
        department = cls(name, location)
        department.save()
        return department

    @classmethod
    def get_all(cls):
        sql = "SELECT id, name, location FROM departments;"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()

        return [cls(id=row[0], name=row[1], location=row[2]) for row in rows]

    @classmethod
    def get_by_id(cls, department_id):
        sql = "SELECT id, name, location FROM departments WHERE id = ?;"
        CURSOR.execute(sql, (department_id,))
        row = CURSOR.fetchone()

        if row:
            return cls(id=row[0], name=row[1], location=row[2])

        return None

    def update(self):
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?;
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM departments WHERE id = ?;"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
