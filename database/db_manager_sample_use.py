# Import the functions from db_manager.py
from db_manager import food_search, cancel_order, comment_order, check_order_status


# Example Search by food name
matching_foods = food_search(food_name="Pizza")
print("Search by food name:")
for food in matching_foods:
    print(food)

# Example Search by restaurant name
matching_foods = food_search(restaurant_name="Pizza")
print("\nSearch by restaurant name:")
for food in matching_foods:
    print(food)

# Example Search by both
matching_foods = food_search(food_name="Pizza", restaurant_name="Pizza Place")
print("\nSearch by both:")
for food in matching_foods:
    print(food)

# Example Cancel Order
order_id, phone_number = 1, "123-456-7890"
cancel_result = cancel_order(order_id, phone_number)
print(f"\nCancel Order Result: {cancel_result}")

# Example Comment on Order
order_id, person_name = 1, "Alice"
comment_result = comment_order(order_id, person_name, "New comment for this order.")
print(f"\nComment Order Result: {comment_result}")

# Example Check Order Status
order_id = 10
status_result = check_order_status(order_id)
print(f"\nCheck Order Status Result: {status_result}")

