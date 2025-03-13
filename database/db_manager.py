import sqlite3
import Levenshtein
import atexit


# atexit.register(lambda: connection.close())



def food_search(food_name=None, restaurant_name=None, max_distance=1):
    """
    Search for foods based on food_name, restaurant_name, or both using edit distance.
    :param connection: SQLite database connection
    :param food_name: Food name to search for (optional)
    :param restaurant_name: Restaurant name to search for (optional)
    :param max_distance: Maximum allowed edit distance for a match
    :return: List of matching foods
    """
    connection = sqlite3.connect('food_orders.db')

    cursor = connection.cursor()
    cursor.execute("SELECT id, food_name, food_category, restaurant_name, price FROM foods")
    results = cursor.fetchall()

    matches = []
    for food_id, db_food_name, food_category, db_restaurant_name, db_price in results:
        food_name_distance = float('inf')
        restaurant_name_distance = float('inf')

        if food_name:
            food_name_distance_1 = Levenshtein.distance(food_name.lower(), db_food_name.lower(), weights=(0, 1, 1))
            food_name_distance_2 = Levenshtein.distance(food_name.lower(), db_food_name.lower(), weights=(1, 0, 1))
            food_name_distance_3 = Levenshtein.distance(food_name.lower(), db_food_name.lower(), weights=(1, 1, 1))
            food_name_distance = min(food_name_distance_1, food_name_distance_2, food_name_distance_3)
            

        if restaurant_name:
            restaurant_name_distance_1 = Levenshtein.distance(restaurant_name.lower(), db_restaurant_name.lower(), weights=(0, 1, 1))
            restaurant_name_distance_2 = Levenshtein.distance(restaurant_name.lower(), db_restaurant_name.lower(), weights=(1, 0, 1))
            restaurant_name_distance_3 = Levenshtein.distance(restaurant_name.lower(), db_restaurant_name.lower(), weights=(1, 1, 1))
            
            restaurant_name_distance = min(restaurant_name_distance_1, restaurant_name_distance_2, restaurant_name_distance_3)
            
        if food_name and restaurant_name:
            if food_name_distance <= max_distance and restaurant_name_distance <= max_distance:
                matches.append({
                    'id': food_id,
                    'food_name': db_food_name,
                    'food_category': food_category,
                    'restaurant_name': db_restaurant_name,
                    'price': db_price,
                    'edit_distance': min(food_name_distance, restaurant_name_distance)
                })
        elif food_name:
            if food_name_distance <= max_distance:
                matches.append({
                    'id': food_id,
                    'food_name': db_food_name,
                    'food_category': food_category,
                    'restaurant_name': db_restaurant_name,
                    'price': db_price,
                    'edit_distance': food_name_distance
                })
        elif restaurant_name:
            if restaurant_name_distance <= max_distance:
                matches.append({
                    'id': food_id,
                    'food_name': db_food_name,
                    'food_category': food_category,
                    'restaurant_name': db_restaurant_name,
                    'price': db_price,
                    'edit_distance': restaurant_name_distance
                })

    matches.sort(key=lambda x: x['edit_distance'])
    connection.close()
    return matches


def cancel_order(order_id, phone_number):
    """
    Cancel an order if its status is 'preparation'.
    :param connection: SQLite database connection
    :param order_id: ID of the order to cancel
    :return: Result message
    """
    connection = sqlite3.connect('food_orders.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT status FROM food_orders WHERE id = ? AND person_phone_number = ?", (order_id,phone_number))
    result = cursor.fetchone()
    
    if result is None:
        return f"Order ID {order_id} from {phone_number} does not exist."
    
    current_status = result[0]
    
    if current_status == "preparation":
        cursor.execute("UPDATE food_orders SET status = 'canceled' WHERE id = ?", (order_id,))
        connection.commit()
        connection.close()
        return f"Order ID {order_id} from {phone_number} has been successfully canceled."
    else:
        connection.close()
        return f"Order ID {order_id} from {phone_number} cannot be canceled as it is in '{current_status}' status."


def comment_order(order_id, person_name ,comment):
    """
    Add or overwrite a comment for an order.
    :param connection: SQLite database connection
    :param order_id: ID of the order to comment on
    :param comment: The comment to add or overwrite
    :return: Result message
    """
    connection = sqlite3.connect('food_orders.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT id FROM food_orders WHERE id = ?", (order_id,))
    result = cursor.fetchone()
    
    if result is None:
        return f"Order ID {order_id} does not exist."
    
    cursor.execute("UPDATE food_orders SET comment = ? WHERE id = ?", (comment, order_id))
    connection.commit()
    connection.close()
    return f"Comment for Order ID {order_id} from {person_name} has been updated."


def check_order_status(order_id):
    """
    Check the status of an order.
    :param connection: SQLite database connection
    :param order_id: ID of the order to check
    :return: Order status or an error message
    """
    connection = sqlite3.connect('food_orders.db')
    cursor = connection.cursor()
    
    cursor.execute("SELECT status FROM food_orders WHERE id = ?", (order_id,))
    result = cursor.fetchone()
    connection.close()
    if result is None:
        return f"Order ID {order_id} does not exist."
    
    return f"Order ID {order_id} from is currently in '{result[0]}' status."