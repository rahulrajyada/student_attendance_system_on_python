import os
import json
from datetime import date

# File paths
USERS_FILE = "users.json"
STUDENTS_DIR = "students_data"

# Create student data folder if it doesn't exist
if not os.path.exists(STUDENTS_DIR):
    os.makedirs(STUDENTS_DIR)

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    return {}

def save_users(users):
    with open(USERS_FILE, "w") as file:
        json.dump(users, file, indent=4)

def register_user(users):
    print("\n-- Register --")
    username = input("Choose a username: ").strip()
    if username in users:
        print("Username already exists!\n")
        return
    password = input("Choose a password: ").strip()
    users[username] = {"password": password}
    save_users(users)
    print("Registered successfully!\n")

def login(users):
    print("\n-- Login --")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if users.get(username, {}).get("password") == password:
        print("Login successful!\n")
        return username
    print("Login failed!\n")
    return None

def edit_user(users):
    print("\n-- Edit User --")
    username = input("Enter username: ").strip()
    if username not in users:
        print("User not found!\n")
        return
    old_pass = input("Current password: ").strip()
    if users[username]["password"] != old_pass:
        print("Wrong password!\n")
        return
    new_pass = input("New password: ").strip()
    users[username]["password"] = new_pass
    save_users(users)
    print("Password changed!\n")

def delete_user(users):
    print("\n-- Delete User --")
    username = input("Enter username: ").strip()
    if username not in users:
        print("User not found!\n")
        return
    confirm = input("Type 'yes' to confirm: ").strip().lower()
    if confirm == "yes":
        del users[username]
        save_users(users)
        student_file = os.path.join(STUDENTS_DIR, f"{username}.json")
        if os.path.exists(student_file):
            os.remove(student_file)
        print("User and data deleted.\n")
    else:
        print("Cancelled.\n")

def list_registered_users(users):
    print("\n--- Registered Users ---")
    if not users:
        print("No users registered.\n")
        return
    print(f"Total Users: {len(users)}")
    for i, username in enumerate(users, start=1):
        print(f"{i}. {username}")
    print()

def load_student_data(username):
    file_path = os.path.join(STUDENTS_DIR, f"{username}.json")
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return []

def save_student_data(username, students):
    file_path = os.path.join(STUDENTS_DIR, f"{username}.json")
    with open(file_path, "w") as f:
        json.dump(students, f, indent=4)

def add_student(students):
    print("\n-- Add Student --")
    roll = input("Roll Number: ").strip()
    if any(s["roll"] == roll for s in students):
        print("Roll number already exists.\n")
        return
    name = input("Name: ")
    age = input("Age: ")
    gender = input("Gender: ")
    contact = input("Contact: ")
    email = input("Email: ")
    address = input("Address: ")
    student = {
        "roll": roll, "name": name, "age": age, "gender": gender,
        "contact": contact, "email": email, "address": address,
        "attendance": {}
    }
    students.append(student)
    print("Student added!\n")

def update_student(students):
    print("\n-- Update Student --")
    roll = input("Enter roll number: ").strip()
    for s in students:
        if s["roll"] == roll:
            s["name"] = input(f"Name ({s['name']}): ") or s["name"]
            s["age"] = input(f"Age ({s['age']}): ") or s["age"]
            s["gender"] = input(f"Gender ({s['gender']}): ") or s["gender"]
            s["contact"] = input(f"Contact ({s['contact']}): ") or s["contact"]
            s["email"] = input(f"Email ({s['email']}): ") or s["email"]
            s["address"] = input(f"Address ({s['address']}): ") or s["address"]
            print("Student updated.\n")
            return
    print("Student not found.\n")

def delete_student(students):
    print("\n-- Delete Student --")
    roll = input("Enter roll number: ").strip()
    for s in students:
        if s["roll"] == roll:
            students.remove(s)
            print("Student deleted.\n")
            return
    print("Student not found.\n")

def mark_attendance(students):
    print("\n-- Mark Attendance --")
    today = str(date.today())
    for s in students:
        status = input(f"{s['roll']} - {s['name']} (P/A): ").strip().upper()
        s["attendance"][today] = "Present" if status == 'P' else "Absent"
    print("Attendance marked.\n")

def view_attendance(students):
    print("\n-- Attendance Records --")
    for s in students:
        print(f"{s['roll']} - {s['name']}")
        if not s["attendance"]:
            print("  No attendance.")
        else:
            for day, status in s["attendance"].items():
                print(f"  {day}: {status}")
    print()

def view_students(students):
    print("\n-- Student List --")
    if not students:
        print("No students found.\n")
    for s in students:
        print(f"Roll: {s['roll']}, Name: {s['name']}, Age: {s['age']}, Gender: {s['gender']}, Contact: {s['contact']}, Email: {s['email']}, Address: {s['address']}")
    print()

def student_menu(username):
    students = load_student_data(username)
    while True:
        print(f"\n-- {username}'s Menu --")
        print("1. Add Student")
        print("2. Update Student")
        print("3. Delete Student")
        print("4. Mark Attendance")
        print("5. View Attendance")
        print("6. View Student List")
        print("7. Logout")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_student(students)
        elif choice == "2":
            update_student(students)
        elif choice == "3":
            delete_student(students)
        elif choice == "4":
            mark_attendance(students)
        elif choice == "5":
            view_attendance(students)
        elif choice == "6":
            view_students(students)
        elif choice == "7":
            save_student_data(username, students)
            print("Logged out.\n")
            break
        else:
            print("Invalid choice.\n")

def main():
    users = load_users()
    while True:
        print("\n=== Main Menu ===")
        print("1. Register")
        print("2. Login")
        print("3. Edit User")
        print("4. Delete User")
        print("5. Exit")
        print("6. View Registered Usernames")
        choice = input("Choose: ").strip()
        if choice == "1":
            register_user(users)
        elif choice == "2":
            username = login(users)
            if username:
                student_menu(username)
        elif choice == "3":
            edit_user(users)
        elif choice == "4":
            delete_user(users)
        elif choice == "5":
            print("Goodbye!")
            break
        elif choice == "6":
            list_registered_users(users)
        else:
            print("Invalid option.\n")

if __name__ == "__main__":
    main()
