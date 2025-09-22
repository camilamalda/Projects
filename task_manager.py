from datetime import datetime

# ===== Function Definitions ===========


def reg_user(current_user):
    '''This function handles user registration for admin users'''   
    if current_user == 'admin':     
        with open('user.txt', 'r') as file:
            existing_users = [line.strip().split(', ')[0] for line in file]

        new_username = input("Enter a new username: ")
        if new_username in existing_users:
            print("Username already exists. Please choose a different username.")
            return
        
        new_password = input("Enter a new password: ")
        confirm_password = input("Confirm the new password: ")
        if new_password == confirm_password:
            with open('user.txt', 'a') as file:
                file.write(f"{new_username}, {new_password}\n")
            print(f"User {new_username} registered successfully.")
        else:
            print("Passwords do not match. Please try again.")
    else:
        print("Only admin can register new users.")


def add_task(current_user):
    '''This function allows users to add a new task'''
    title = input("Enter the task title: ")
    description = input("Enter the task description: ")
    date_assigned = datetime.now().strftime("%d-%m-%Y")
    due_date = input("Enter the due date (DD-MM-YYYY: ")
    completed = 'No'

    with open('tasks.txt', 'a') as file:
        file.write(f"{current_user}, {title}, {description}, {date_assigned}, {due_date}, {completed}\n")
    
    print("Task added successfully.")


def view_all():
    with open('tasks.txt', 'r') as file:
        for line in file:
            task_details = line.strip().split(', ')
            print(f"Assigned to: {task_details[0]}")
            print(f"Title: {task_details[1]}")
            print(f"Description: {task_details[2]}")
            print(f"Date assigned: {task_details[3]}")
            print(f"Due date: {task_details[4]}")
            print(f"Completed: {task_details[5]}\n")
            print("-" * 40)


def view_mine(current_user):
    user_tasks = []
    with open('tasks.txt', 'r') as file:
        for line in file:
            task_details = line.strip().split(', ')
            if task_details[0] == current_user:
                user_tasks.append(task_details)

    if user_tasks:
        for index, task in enumerate(user_tasks):
            print(f"Task {index}:")
            print(f"Title: {task[1]}")
            print(f"Description: {task[2]}")
            print(f"Date assigned: {task[3]}")
            print(f"Due date: {task[4]}")
            print(f"Completed: {task[5]}\n")
            print("-" * 40)

        task_choice = input("Enter the task number to select it, or -1 to return: ")
        if task_choice == "-1":
            return

        if task_choice.isdigit():
            task_index = int(task_choice)
            if 0 <= task_index < len(user_tasks):
                selected_task = user_tasks[task_index]
                print(f"You selected Task {task_index}: {selected_task[1]}")
                choice = input("Do you want to mark this task as completed or edit it? (m/e): ").lower()

                if choice == 'm':
                    if selected_task[5].strip().lower() == 'yes':
                        print("This task is already completed.")
                    else:
                        selected_task[5] = 'Yes'
                        print("Task marked as completed.")
                        with open('tasks.txt', 'r') as file:
                            tasks = file.readlines()
                        for i, line in enumerate(tasks):
                            task = line.strip().split(', ')
                            if task == user_tasks[task_index]:
                                tasks[i] = ', '.join(selected_task) + '\n'
                                break
                        with open('tasks.txt', 'w') as file:
                            file.writelines(tasks)

                elif choice == 'e':
                    if selected_task[5].strip().lower() == 'yes':
                        print("You can't edit a completed task.")
                    else:
                        edit_username = input("Do you want to change the username the task is assigned to? (y/n): ").lower()
                        if edit_username == 'y':
                            new_username = input("Enter the new username: ")
                            selected_task[0] = new_username

                        edit_due_date = input("Do you want to change the due date? (y/n): ").lower()
                        if edit_due_date == 'y':
                            new_due_date = input("Enter the new due date (DD-MM-YYYY): ")
                            selected_task[4] = new_due_date

                        with open('tasks.txt', 'r') as file:
                            tasks = file.readlines()
                        for i, line in enumerate(tasks):
                            task = line.strip().split(', ')
                            if task == user_tasks[task_index]:
                                tasks[i] = ', '.join(selected_task) + '\n'
                                break
                        with open('tasks.txt', 'w') as file:
                            file.writelines(tasks)
                        print("Task updated successfully.")
                else:
                    print("Invalid choice.")
            else:
                print("Invalid task number. Please enter a number.")
        else:
            print("Invalid input. Please enter a valid number.")
    else:
        print("No tasks found for your username.")


def view_completed():
    with open('tasks.txt', 'r') as file:
        for line in file:
            task_details = line.strip().split(', ')
            if task_details[5].strip().lower() == 'yes':
                print(f"Assigned to: {task_details[0]}")
                print(f"Title: {task_details[1]}")
                print(f"Description: {task_details[2]}")
                print(f"Date assigned: {task_details[3]}")
                print(f"Due date: {task_details[4]}")
                print(f"Completed: {task_details[5]}\n")
                print("-" * 40)


def delete_task(): 
    tasks = []
    with open('tasks.txt', 'r') as file:
        tasks = [line.strip() for line in file]
        for i, task in enumerate(tasks):
            task_details = task.split(', ')
            print(f"{i}: {task_details[1]} | (Assigned to: {task_details[0]})")

    try:
        task_index = int(input("Enter the index of the task to delete: "))
        if 0 <= task_index < len(tasks):
            tasks.pop(task_index)
            with open('tasks.txt', 'w') as file:
                for task in tasks:
                    file.write(task + '\n')
            print("Task deleted successfully.")
        else:
            print("Invalid task index. Please try again.")
    except ValueError:
        print("Invalid input. Please enter a number.")


def generate_reports():
    with open('tasks.txt', 'r') as file:
        task_lines = [line.strip().split(', ') for line in file]

    total_tasks = len(task_lines)
    completed = 0 
    incomplete = 0   
    overdue = 0

    for task in task_lines:
        if task[5].strip().lower() == 'yes':
            completed += 1
        else:
            incomplete += 1
            due_date = datetime.strptime(task[4], "%d %b %Y")
            if due_date < datetime.now():
                overdue += 1

    with open('task_overview.txt', 'w') as file:
        file.write(f"Total tasks: {total_tasks}\n")
        file.write(f"Completed tasks: {completed}\n")
        file.write(f"Incomplete tasks: {incomplete}\n")
        file.write(f"Overdue tasks: {overdue}\n")
        file.write(f"Percentage incomplete: {incomplete / total_tasks * 100:.2f}%\n")
        file.write(f"Percentage overdue: {overdue / total_tasks * 100:.2f}%\n")

    with open('user.txt', 'r') as file:
        user_lines = [line.strip().split(', ') for line in file]
    total_users = len(user_lines)

    user_stats = {user: {'total': 0, 'completed': 0, 'incomplete': 0, 'overdue': 0} for user, _ in user_lines}

    for task in task_lines:
        user = task[0]
        if user in user_stats:
            user_stats[user]['total'] += 1
            if task[5].strip().lower() == 'yes':
                user_stats[user]['completed'] += 1
            else:
                user_stats[user]['incomplete'] += 1
                due_date = datetime.strptime(task[4], "%d %b %Y")
                if due_date < datetime.now():
                    user_stats[user]['overdue'] += 1

    with open('user_overview.txt', 'w') as file:
        file.write(f"Total users: {total_users}\n")
        file.write(f"Total tasks: {total_tasks}\n")
        for user, stats in user_stats.items():
            if stats['total'] > 0:
                pct_assigned = (stats['total'] / total_tasks) * 100
                pct_completed = (stats['completed'] / stats['total']) * 100
                pct_incomplete = (stats['incomplete'] / stats['total']) * 100
                pct_overdue = (stats['overdue'] / stats['total']) * 100
            else:
                pct_assigned = pct_completed = pct_incomplete = pct_overdue = 0.0

            file.write(f"\nUser: {user}\n")
            file.write(f"  Tasks assigned: {stats['total']}\n")
            file.write(f"  % of total tasks: {pct_assigned:.2f}%\n")
            file.write(f"  % completed: {pct_completed:.2f}%\n")
            file.write(f"  % incomplete: {pct_incomplete:.2f}%\n")
            file.write(f"  % overdue: {pct_overdue:.2f}%\n")


def display_statistics():
    generate_reports()
    print("\n=== Task Overview ===")
    with open('task_overview.txt', 'r') as file:
        print(file.read())
    print("\n=== User Overview ===")
    with open('user_overview.txt', 'r') as file:
        print(file.read())

# ==== Login Section ====


users = {}
with open('user.txt', 'r') as file:
    for line in file:
        username, password = line.strip().split(', ')
        users[username] = password

while True:
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if username in users and users[username] == password:
        print(f"Welcome {username}!")
        break
    else:
        print("Invalid username or password. Please try again.")

# ==== Main Menu Section ====
while True:
    if username == 'admin':
        menu = input(
        '''Select one of the following options:
r  - register a user
a  - add task
va - view all tasks
vm - view my tasks
vc - view completed tasks
del - delete tasks
gr - generate reports
ds - display statistics
e  - exit
: ''').lower()
    else:
        menu = input(
        '''Select one of the following options:
a  - add task
va - view all tasks
vm - view my tasks
e  - exit
: ''').lower()

    if menu == 'r':
        reg_user(username)
    elif menu == 'a':
        add_task(username)
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine(username)
    elif menu == 'vc':
        view_completed()
    elif menu == 'del':
        delete_task()
    elif menu == 'gr':
        generate_reports()
        print("Reports generated")
    elif menu == 'ds':
        display_statistics()
    elif menu == 'e':
        print('Goodbye!!!')
        break
    else:
        print("You have entered an invalid input. Please try again.")
