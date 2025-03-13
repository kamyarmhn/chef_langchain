import sqlite3
import os

def init_db():
    # Remove existing database if it exists
    if os.path.exists('food_orders.db'):
        os.remove('food_orders.db')

    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect('food_orders.db')
    cursor = conn.cursor()

    # Create foods table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS foods (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        food_name TEXT NOT NULL,
        food_category TEXT,
        restaurant_name TEXT NOT NULL,
        price REAL NOT NULL
    )
    ''')

    # Create food_orders table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS food_orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_name TEXT NOT NULL,
        person_phone_number TEXT NOT NULL,
        status TEXT DEFAULT 'preparation',
        comment TEXT
    )
    ''')

    # Insert sample foods
    sample_foods = [
        ('Pizza Margherita', 'Italian', 'Pizza Place', 12.99),
        ('Pepperoni Pizza', 'Italian', 'Pizza Place', 14.99),
        ('Sushi Roll', 'Japanese', 'Sushi Bar', 18.99),
        ('Burger', 'American', 'Burger Joint', 9.99),
        ('Pasta Carbonara', 'Italian', 'Italian Restaurant', 15.99),
    ]

    cursor.executemany('INSERT OR IGNORE INTO foods (food_name, food_category, restaurant_name, price) VALUES (?, ?, ?, ?)', sample_foods)

    # Insert sample orders
    sample_orders = [
        ('John Doe', '123-456-7890', 'preparation', None),
        ('Jane Smith', '098-765-4321', 'delivered', 'Great service!'),
    ]

    cursor.executemany('INSERT OR IGNORE INTO food_orders (person_name, person_phone_number, status, comment) VALUES (?, ?, ?, ?)', sample_orders)

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully!") 