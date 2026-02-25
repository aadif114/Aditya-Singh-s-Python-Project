import sqlite3

def init_db():
    conn = sqlite3.connect("travel_app.db")
    cursor = conn.cursor()
    # User Table: Stores logins
    cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                      (username TEXT PRIMARY KEY, password TEXT, role TEXT)''')
    # Travel Data Table: Stores admin entries
    cursor.execute('''CREATE TABLE IF NOT EXISTS travel_spots 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, budget_range TEXT, name TEXT, 
                       place_img TEXT, rest_name TEXT, rest_img TEXT, 
                       hotel_name TEXT, hotel_img TEXT)''')
    
    # Default Admin
    cursor.execute("SELECT * FROM users WHERE username='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users VALUES ('admin', 'admin123', 'admin')")
    
    conn.commit()
    conn.close()

def get_db_connection():
    return sqlite3.connect("travel_app.db")
