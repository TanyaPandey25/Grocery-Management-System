import pickle
from datetime import datetime

# Load data from binary file
def load_data(filename):
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except (FileNotFoundError, EOFError):
        return []

# Save data to binary file
def save_data(data, filename):
    with open(filename, 'wb') as f:
        pickle.dump(data, f)

def validate_date(date_str, is_mfg=False):
    try:
        # Ensure date is in DD/MM/YYYY format
        date = datetime.strptime(date_str, "%d/%m/%Y")
        current_date = datetime.now()
        
        if is_mfg:
            # For manufacturing date, don't allow future dates
            if date > current_date:
                print("Manufacturing date cannot be in the future.")
                return False
        else:
            # For expiry date, only allow future dates
            if date < current_date:
                print("Expiry date must be in the future.")
                return False
                
        return True
    except ValueError:
        print("Invalid date format. Please enter the date as DD/MM/YYYY.")
        return False

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- Grocery Management Functions -x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
def add_item(grocery_list):
    print("\n--- Add New Grocery Item ---")
    ans=True
    while ans:
        name = input("Enter item name: ")
        category = input("Enter category(eg- chocolates, biscuits, cereals etc): ")
        
        try:
            price = float(input("Enter selling price of item: ₹"))
            cost_price = float(input("Enter cost price of item (for internal use): ₹"))
        except ValueError:
            print("Please enter valid numeric prices")
            continue

        # Check if the item already exists in the list
        existing_item = None
        for item in grocery_list:
            if item['name'].lower() == name.lower() and item['price']==price and item['cost_price']== cost_price: 
                existing_item = item
                break

        if existing_item:
            try:
                quantity = int(input("Enter additional quantity of " + existing_item['name']+ " to add: "))
                existing_item['quantity'] += quantity
                save_data(grocery_list, 'grocery_list.bin')
                print("Added", quantity, "more of", existing_item['name'],".")
            except ValueError:
                print("Please enter a valid quantity")
                continue
        else:
            try:
                quantity = int(input("Enter quantity: "))
            except ValueError:
                print("Please enter a valid quantity")
                continue

            while True:
                mfg_date = input("Enter manufacturing date (DD/MM/YYYY): ")
                if validate_date(mfg_date, is_mfg=True):
                    break
            while True:
                expiry_date = input("Enter expiry date (DD/MM/YYYY): ")
                if validate_date(expiry_date, is_mfg=False):
                    break 

            # Add new item to the list
            item = {
                "name": name,
                "category": category,
                "mfg_date": mfg_date,
                "expiry_date": expiry_date,
                "price": price,           # Selling price
                "quantity": quantity,
                "cost_price": cost_price   # Internal use
            }

            grocery_list.append(item)
            save_data(grocery_list, 'grocery_list.bin')
            print("Item", item['name'], "added successfully.")

        ans2=True
        while ans2:
            an1=input("Do you want to add another item?(yes/no): ")
            if an1.lower()=='yes':
                ans=True
                ans2= False
            elif an1.lower()== "no":
                ans= False
                ans2=False
            else:
                print("Enter a valid input ")
                ans2=True

#------------------------------------------------------------------------------------------
def display_items(grocery_list):
    if not grocery_list:
        print("No items in the grocery list.")
        return

    print("\n--- Grocery Items ---")
    for item in grocery_list:
        print( "Name:", item['name'],'\n',
               "Category:", item['category'],"\n", 
               "Mfg Date:" ,item['mfg_date'],"\n", 
               "Expiry Date:", item['expiry_date'],"\n", 
               "Price: ₹", item['price'],"\n" ,
               "Quantity:" ,item['quantity'],"\n")
        print("------------------------------------------------------------------------")

def check_expired_items(grocery_list):
    print("\n--- Check Expired Items ---")
    try:
        current_date = datetime.now()
        expired_items = []

        for item in grocery_list:
            expiry_date = datetime.strptime(item['expiry_date'], "%d/%m/%Y")
            if expiry_date < current_date:
                expired_items.append(item)

        if not expired_items:
            print("No expired items.")
        else:
            print("\n--- Expired Items ---")
            for item in expired_items:
                print("Name:", item['name'], "Expired on:", item['expiry_date'])
    except ValueError:
        print("Error processing dates. Please ensure all dates are in DD/MM/YYYY format.")

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- New arrivals -x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
def new_arrivals(grocery_list):
    print("\n--- Check New Arrivals ---")
    
    try:
        current_date = datetime.now()
        recent_items = []

        for item in grocery_list:
            mfg_date = datetime.strptime(item['mfg_date'], "%d/%m/%Y")
            days_diff = (current_date - mfg_date).days
            
            if days_diff <= 30:
                recent_items.append(item)

        if not recent_items:
            print("No new arrivals.")
        else:
            print("\n--- New Arrivals ---")
            for item in recent_items:
                print("Name:", item['name'], "Mfg Date:", item['mfg_date'])
    except ValueError:
        print("Error processing dates. Please ensure all dates are in DD/MM/YYYY format.")

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- Store Management Functions -x-x-x-x-x-x-x-x-x-x-x-x-x-x
def new_store(stores_list):
    print("\n--- Add New Store ---")
    store_name = input("Enter store name: ")
    location = input("Enter location: ")

    store = {
        "store_name": store_name,
        "location": location,
        "sales": [],
        "profit_loss": {}
    }

    stores_list.append(store)
    save_data(stores_list, 'stores_list.bin')
    print("Store",store['store_name'],"added successfully.")

def display_stores(stores_list):
    if not stores_list:
        print("No stores in the list.")
        return

    print("\n--- Stores ---")
    for store in stores_list:
        print("Store:", store['store_name'], "Location:" , store['location'])

def profit_loss(store, cost_price, quantity, sales_amount):
    total_cost = cost_price * quantity
    profit_or_loss = sales_amount - total_cost

    current_month = datetime.now().strftime("%B %Y")
    if current_month not in store['profit_loss']:
        store['profit_loss'][current_month] = 0
    store['profit_loss'][current_month] += profit_or_loss

    save_data([store], 'stores_list.bin')

def display_profit_loss(stores_list):
    print("\n--- Profit/Loss Report ---")
    for store in stores_list:
        print("Store:", store['store_name'], "Location:", store['location'])
        for month, profit_or_loss in store['profit_loss'].items():
            status = "Profit" if profit_or_loss > 0 else "Loss"
            print(month + ": " + status + " of ₹" + str(abs(profit_or_loss)))

def record_sales(stores_list, item, customer_name, item_name, quantity, sales_amount):
    if not stores_list:
        print("No stores found to record sales")
        return
        
    store = stores_list[0]
    
    sale_record = {
        'customer': customer_name,
        'item': item_name,
        'quantity': quantity,
        'total_sales': sales_amount,
        'date': datetime.now().strftime("%d/%m/%Y")
    }
    
    store['sales'].append(sale_record)
    
    try:
        cost_price = item['cost_price']
        profit_loss(store, cost_price, quantity, sales_amount)
    except (KeyError, TypeError) as e:
        print(f"Error calculating profit/loss: {e}")
    
    save_data(stores_list, 'stores_list.bin')

def display_sales(stores_list):
    print("\n--- Sales Data ---")
    for store in stores_list:
        print("Store: " + store['store_name'] + ", Location: " + store['location'])
        if not store['sales']:
            print(" No sales recorded.")
            continue
        for sale in store['sales']:
            customer = sale.get('customer', 'Unknown Customer')
            item = sale.get('item', 'Unknown Item')
            quantity = sale.get('quantity', 0)
            total_sales = sale.get('total_sales', 0)
            date = sale.get('date', 'Unknown Date')
            
            print(f" Date: {date}, Customer: {customer}, Item: {item}, Quantity: {quantity}, Total Sales: ₹{total_sales}")

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- CUSTOMER MANAGEMENT FUNCTIONS -x-x-x-x-x-x-x-x-x-x-x-x-x-x
def add_customer(customer_list):
    print("\n--- Add New Customer ---")
    name = input("Enter customer name: ")
    
    while True:
        contact = input("Enter contact number: ")
        if len(contact) == 10 and contact.isdigit():
            break
        print("Invalid contact number. Please enter a 10-digit number.")

    customer = {
        "name": name,
        "contact": contact,
        "purchases": []
    }

    customer_list.append(customer)
    save_data(customer_list, 'customer_list.bin')
    print("Customer",name,"added successfully.")

def display_customers(customer_list):
    if not customer_list:
        print("No customers found.")
        return

    print("\n--- Customers ---")
    for customer in customer_list:
        print("Name:", customer['name'], "Contact:", customer['contact'])       

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- BUY GROCERIES -x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x 
def buy_groceries(grocery_list, customer_list, stores_list, feedback_list):
    if not grocery_list:
        print("No items available in store.")
        return

    customer_name = input("Enter customer name: ")
    customer_found = None
    for customer in customer_list:
        if customer['name'].lower() == customer_name.lower():
            customer_found = customer
            break

    if not customer_found:
        print("Customer not found. Adding new customer details.")
        while True:
            contact = input("Enter contact number: ")
            if len(contact) != 10 or not contact.isdigit():
                print("Invalid contact number. Please enter a 10-digit number.")
                continue
                
            Rcontact = input("Re-enter contact number: ")
            if contact != Rcontact:
                print("Contact numbers don't match. Please try again.")
                continue
            break

        customer_found = {"name": customer_name, "contact": contact, "purchases": []}
        customer_list.append(customer_found)
        save_data(customer_list, 'customer_list.bin')
        print("Customer", customer_name, "added successfully.")

    ch = "y"
    while ch.lower() == "y":
        print("\n--- Available Groceries ---")
        for i, item in enumerate(grocery_list, 1):
            print(f"{i}. {item['name']} - Price: ₹{item['price']}, Available: {item['quantity']}")

        try:
            item_choice = int(input("Select item number to purchase: ")) - 1
            if item_choice < 0 or item_choice >= len(grocery_list):
                print("Invalid item number.")
                continue

            item = grocery_list[item_choice]
            quantity = int(input(f"Enter quantity of '{item['name']}' to purchase: "))

            if quantity <= 0:
                print("Please enter a valid quantity.")
                continue

            if item['quantity'] >= quantity:
                item['quantity'] -= quantity
                sales_amount = item['price'] * quantity
                
                customer_found['purchases'].append({
                    'name': item['name'],
                    'quantity': quantity,
                    'date': datetime.now().strftime("%d/%m/%Y")
                })

                print(f"Purchased {quantity} of {item['name']} successfully!")
                print(f"Total amount: ₹{sales_amount}")
                
                save_data(grocery_list, 'grocery_list.bin')
                save_data(customer_list, 'customer_list.bin')
                
                record_sales(stores_list, item, customer_name, item['name'], quantity, sales_amount)

                if input("Would you like to leave feedback for this item? (yes/no): ").strip().lower() == "yes":
                    add_feedback(feedback_list, customer_name, item['name'])
            else:
                print("Not enough stock available.")

        except ValueError:
            print("Please enter valid numbers.")
            continue
        except IndexError:
            print("Invalid selection.")
            continue

        ch = input("Do you want to buy more? (yes/no): ").strip().lower()
        if ch not in ['y', 'yes', 'n', 'no']:
            print("Invalid input. Assuming 'no'.")
            break

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- FEEDBACK -x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
def add_feedback(feedback_list, customer_name, item_name):
    print("\n--- Leave Feedback ---")
    print(f"Customer: {customer_name}, Item: {item_name}")

    while True:
        try:
            rating = int(input("Rate the item (1-5): "))
            if 1 <= rating <= 5:
                break
            print("Please enter a rating between 1 and 5.")
        except ValueError:
            print("Please enter a valid number.")
    
    comment = input("Any comments? (optional): ")

    feedback = {
        "customer_name": customer_name,
        "item_name": item_name,
        "rating": rating,
        "comment": comment,
        "date": datetime.now().strftime("%d/%m/%Y")
    }

    feedback_list.append(feedback)
    save_data(feedback_list, 'feedback_list.bin')
    print("Thank you for your feedback!")
    
def view_feedback(feedback_list, item_name):
    print(f"\n--- Feedback for {item_name} ---")

    item_feedback = [f for f in feedback_list if f['item_name'].lower() == item_name.lower()]
    
    if not item_feedback:
        print("No feedback available for this item.")
        return

    # Calculate average rating
    avg_rating = sum(f['rating'] for f in item_feedback) / len(item_feedback)
    print(f"Average Rating: {avg_rating:.1f}/5.0")
    
    for feedback in item_feedback:
        print(f"\nDate: {feedback.get('date', 'Unknown')}")
        print(f"Customer: {feedback['customer_name']}")
        print(f"Rating: {feedback['rating']}/5")
        if feedback['comment']:
            print(f"Comment: {feedback['comment']}")
        print("-------------------")

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- PASSWORD -x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
def password_admin():
    try:
        with open('password.txt', 'r') as f:
            current_password = f.read().strip()
            
        entered_password = input("Enter Current Password: ")
        
        if entered_password == current_password:
            new_password = input("Enter New Password: ")
            if len(new_password) < 4:
                print("Password must be at least 4 characters long.")
                return
                
            with open('password.txt', 'w') as f:
                f.write(new_password)
            print("Password has been changed successfully")
        else:
            print("Current Password Incorrect")
    except FileNotFoundError:
        print("Password file not found. Creating new password file...")
        new_password = input("Enter New Password: ")
        with open('password.txt', 'w') as f:
            f.write(new_password)
        print("Password has been set successfully")

#x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x- MAIN Program -x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x-x
def admin_interface(grocery_list, stores_list, customer_list, feedback_list):
    while True:
        print("\n--- Admin Interface ---")
        print("1. Add Grocery Item")
        print("2. Display Grocery Items")
        print("3. Check Expired Items")
        print("4. New Arrivals")
        print("5. Add Store")
        print("6. Display Stores")
        print("7. View Sales Data")
        print("8. View Profit/Loss Report")
        print("9. Change admin password")
        print("10. View feedback")
        print("11. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                add_item(grocery_list)
            elif choice == '2':
                display_items(grocery_list)
            elif choice == '3':
                check_expired_items(grocery_list)
            elif choice == '4':
                new_arrivals(grocery_list)
            elif choice == '5':
                new_store(stores_list)
            elif choice == '6':
                display_stores(stores_list)
            elif choice == '7':
                display_sales(stores_list)
            elif choice == '8':
                display_profit_loss(stores_list)
            elif choice == '9':
                password_admin()
            elif choice == '10':
                item_name = input("Enter the item name to view feedback: ")
                view_feedback(feedback_list, item_name)
            elif choice == '11':
                print("Exiting Admin Interface.")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

def customer_interface(grocery_list, customer_list, stores_list, feedback_list):
    while True:
        print("\n----WELCOME----")
        print("\n--- Customer Interface ---")
        print("1. View Grocery Items")
        print("2. Buy Groceries")
        print("3. Display Customers")
        print("4. Add Feedback")
        print("5. Exit")

        choice = input("Enter your choice: ")

        try:
            if choice == '1':
                display_items(grocery_list)
            elif choice == '2':
                buy_groceries(grocery_list, customer_list, stores_list, feedback_list)
            elif choice == '3':
                display_customers(customer_list)
            elif choice == '4':
                customer_name = input("Enter your name: ")
                item_name = input("Enter the item name you want to leave feedback for: ")
                add_feedback(feedback_list, customer_name, item_name)
            elif choice == '5':
                print("Exiting Customer Interface.")
                print("-----THANK YOU-----")
                break
            else:
                print("Invalid choice, please try again.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("Please try again.")

def main():
    # Initialize data files
    try:
        stores_list = load_data('stores_list.bin')
        if not stores_list:
            stores_list = [{
                "store_name": "Main Store",
                "location": "City Center",
                "sales": [],
                "profit_loss": {}
            }]
            save_data(stores_list, 'stores_list.bin')
    except Exception as e:
        print(f"Error loading stores data: {str(e)}")
        stores_list = [{
            "store_name": "Main Store",
            "location": "City Center",
            "sales": [],
            "profit_loss": {}
        }]
        save_data(stores_list, 'stores_list.bin')

    try:
        grocery_list = load_data('grocery_list.bin')
        customer_list = load_data('customer_list.bin')
        feedback_list = load_data('feedback_list.bin')
    except Exception as e:
        print(f"Error loading data: {str(e)}")
        grocery_list = []
        customer_list = []
        feedback_list = []

    while True:
        print("\n=== Grocery Store Management System ===")
        user_type = input("Are you an Admin or a Customer? (or 'exit' to quit): ").strip().lower()
        
        if user_type == 'exit':
            print("Thank you for using our system. Goodbye!")
            break
            
        elif user_type == 'admin':
            try:
                with open("password.txt", "r") as f:
                    password_current = f.read().strip()
                
                epassword = input("Enter admin password: ")
                if epassword == password_current:
                    admin_interface(grocery_list, stores_list, customer_list, feedback_list)
                else:
                    print("Incorrect Password\nAccess Denied")
                    
            except FileNotFoundError:
                print("Password file not found. Creating new password file...")
                new_password = input("Enter New Password: ")
                with open('password.txt', 'w') as f:
                    f.write(new_password)
                print("Password has been set successfully")
                admin_interface(grocery_list, stores_list, customer_list, feedback_list)
                
        elif user_type == 'customer':
            customer_interface(grocery_list, customer_list, stores_list, feedback_list)
            
        else:
            print("Invalid user type. Please enter 'admin' or 'customer' or 'exit'.")
while True:
    if __name__ == "__main__":
        main()