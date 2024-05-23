import requests

session = requests.Session()

def register(username, password):
    url = 'http://localhost:5001/register'
    data = {'username': username, 'password': password}
    try:
        response = session.post(url, json=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def login(username, password):
    url = 'http://localhost:5001/login'
    data = {'username': username, 'password': password}
    try:
        response = session.post(url, json=data)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def logout():
    url = 'http://localhost:5001/logout'
    try:
        response = session.post(url)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def mark_attendance():
    url = 'http://localhost:5001/mark_attendance'
    try:
        response = session.post(url)
        response.raise_for_status()
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

def get_attendance():
    url = 'http://localhost:5001/attendance'
    try:
        response = session.get(url)
        response.raise_for_status()
        attendance = response.json()
        for record in attendance:
            print(f"ID: {record['id']}, Username: {record['username']}, Timestamp: {record['timestamp']}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    while True:
        choice = input("1. Register\n2. Login\n3. Logout\n4. Mark Attendance\n5. Get Attendance\n6. Exit\nChoose an option: ")
        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            register(username, password)
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login(username, password)
        elif choice == '3':
            logout()
        elif choice == '4':
            mark_attendance()
        elif choice == '5':
            get_attendance()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")
