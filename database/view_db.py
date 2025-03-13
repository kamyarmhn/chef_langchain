import sqlite3

def view_database():
    # Connect to the database
    conn = sqlite3.connect('food_orders.db')
    cursor = conn.cursor()
    
    print("\n=== All Foods ===")
    cursor.execute("""
        SELECT id, food_name, food_category, restaurant_name, price 
        FROM foods
        ORDER BY restaurant_name, price
    """)
    foods = cursor.fetchall()
    for food in foods:
        print(f"ID: {food[0]}, {food[1]} ({food[2]}) at {food[3]} - ${food[4]}")

    print("\n=== Foods by Category ===")
    cursor.execute("""
        SELECT food_category, COUNT(*) as count, GROUP_CONCAT(food_name) as foods
        FROM foods 
        GROUP BY food_category
    """)
    categories = cursor.fetchall()
    for category in categories:
        print(f"Category: {category[0]}, Count: {category[1]}")
        print(f"Foods: {category[2]}")

    print("\n=== All Orders ===")
    cursor.execute("""
        SELECT id, person_name, person_phone_number, status, comment
        FROM food_orders
        ORDER BY id
    """)
    orders = cursor.fetchall()
    for order in orders:
        print(f"Order #{order[0]} - Customer: {order[1]} ({order[2]})")
        print(f"Status: {order[3]}")
        if order[4]:
            print(f"Comment: {order[4]}")
        print("---")

    print("\n=== Orders by Status ===")
    cursor.execute("""
        SELECT status, COUNT(*) as count
        FROM food_orders
        GROUP BY status
    """)
    status_counts = cursor.fetchall()
    for status in status_counts:
        print(f"Status: {status[0]}, Count: {status[1]}")

    # Close the connection
    conn.close()

if __name__ == '__main__':
    view_database() 