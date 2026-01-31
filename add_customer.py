import boto3

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('potential_customers_for_ford')

def take_user_input():
    customer_id =  input("Please enter your unique customer ID: ")
    first_name = input("Please enter your first name: ")
    last_name = input("Please enter your last name: ")
    interests = input("Please enter your interests seperated by commas (,): ")
    age = int(input("Please enter you age: "))

    return {'customer_id': customer_id, 'first_name': first_name, 'last_name': last_name, 'interests': interests, 'age': age}

def add_user_to_db():
    try:
        user = take_user_input()
        response = table.get_item(Key={'customer_id': user['customer_id']})

        while ('Item' in response):
            print("Customer ID already exists. Please enter a unique customer ID.")
            user = take_user_input()
            response = table.get_item(Key={'customer_id': user['customer_id']})

        table.put_item(Item=user)
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    add_user_to_db()
