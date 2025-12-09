import sqlite3
import pandas as pd

conn = sqlite3.connect("renting_rooms.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS ANIMAL (
    name TEXT,
    price TEXT,
    location TEXT,
    url_image TEXT,
    _type TEXT DEFAULT 'dog',
    UNIQUE(name, price, location,url_image,_type)
    
)
""")

conn.commit()
conn.close()


def insert_if_not_exists(name, price, location, url_image,_type='dog'):
   
    
    try:
        conn = sqlite3.connect('renting_rooms.db')
        c = conn.cursor()

        # Exécuter l'insertion
        c.execute("""
            INSERT OR IGNORE INTO ANIMAL (name, price, location, url_image,_type)
            VALUES (?, ?, ?, ?,?)
        """, (name, price, location, url_image, _type))

        rows_inserted = c.rowcount  # Nombre de lignes insérées
        conn.commit()
        conn.close()

        return (True, rows_inserted, "Success")

    except Exception as e:
        return (False, 0, str(e))


def load_data_from_database():
    try:
        conn = sqlite3.connect("renting_rooms.db")
        df = pd.read_sql_query("SELECT * FROM ANIMAL", conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Erreur lors du chargement: {e}")
        return pd.DataFrame()


def get_total_count():
    try:
        conn = sqlite3.connect("renting_rooms.db")
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM ANIMAL")
        count = c.fetchone()[0]
        conn.close()
        return count
    except Exception as e:
        print(f"Erreur: {e}")
        return 0
    
    
def get_count_by_category():
    try:
        conn = sqlite3.connect("renting_rooms.db")
        c = conn.cursor()

        c.execute("""
            SELECT _type, COUNT(*) 
            FROM ANIMAL 
            GROUP BY _type
        """)

        results = c.fetchall()
        conn.close()

        return dict(results)

    except Exception as e:
        print(f"Error: {e}")
        return {}

def get_dogs():
    return pd.read_sql_query(
        "SELECT * FROM ANIMAL WHERE _type = 'dog'",
        sqlite3.connect("renting_rooms.db")
    )


def get_sheep():
    return pd.read_sql_query(
        "SELECT * FROM ANIMAL WHERE _type = 'sheep'",
        sqlite3.connect("renting_rooms.db")
    )


def get_poultry_rabbit():
    return pd.read_sql_query(
        "SELECT * FROM ANIMAL WHERE _type = 'poultry-rabbit'",
        sqlite3.connect("renting_rooms.db")
    )


def get_other_animals():
    return pd.read_sql_query(
        "SELECT * FROM ANIMAL WHERE _type = 'other'",
        sqlite3.connect("renting_rooms.db")
    )


def get_count_by_type_df():
    conn = sqlite3.connect("renting_rooms.db")
    df = pd.read_sql_query(
        "SELECT _type, COUNT(*) AS total FROM ANIMAL GROUP BY _type",
        conn
    )
    conn.close()
    return df


def get_count_by_location_df():
    conn = sqlite3.connect("renting_rooms.db")
    df = pd.read_sql_query(
        """
        SELECT location, COUNT(*) AS total
        FROM ANIMAL
        GROUP BY location
        ORDER BY total DESC
        LIMIT 10
        """,
        conn
    )
    conn.close()
    return df
