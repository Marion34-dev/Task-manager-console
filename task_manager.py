# Define colour codes
PINK = '\033[95m'
BLUE = '\033[94m'
CYAN = '\033[96m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
WHITE = '\033[0m'
BOLD = '\033[1m'


# Create menu function
def menu():
    # Menu for 'admin' users, containing main menu plus 3 options
    while True:
        print(f"{CYAN}══ MENU ══")

        if username == "admin":
            menu = input(f'''{WHITE}Please select one of the following options below:
♦ a - Add a Task
♦ va - View all Tasks
♦ vm - View my Tasks
♦ e - Exit
{BLUE}══ Admin section ══
{WHITE}♦ r - Register a User
♦ vs - View Statistics
♦ gr - Generate Reports
What would you like to do? ''').lower()

        # Menu for all the other users
        else:
            menu = input(f'''{WHITE}Please select one of the following options below:
♦ a - Add a Task
♦ va - View all Tasks
♦ vm - View my Tasks
♦ e - Exit
What would you like to do? ''').lower()

        # To register a new user: (for admin only)
        if menu == 'r':
            reg_user()

        # To add a new task
        elif menu == 'a':
            add_task()

        # Display all tasks to the user
        elif menu == 'va':
            view_all()

        # Display tasks only assigned to the user who is logged in
        elif menu == 'vm':
            view_mine()

        # Exit option
        elif menu == 'e':
            print(f"{BOLD}{YELLOW}Goodbye!!!")
            return (0)  # exit function

        # Display statistics (for admin only)
        elif menu == 'vs':
            view_stats()

        # Display reports (for admin only)
        elif menu == 'gr':
            gen_reports()

        # Fail-safe, error message in case the user enters something else than all the menu options
        else:
            print(f"{RED}\nYour input wasn't recognised, please try again")


# Create the reg_user function
def reg_user():
    user_read = open('user.txt', 'r')
    username_list = []

    for line in user_read:
        user, psw = line.strip("\n").split(", ")
        username_list.append(user)

    # Ask for user input, ensuring the new username does not already exist
    new_ID = input("\nPlease insert a new username: ")
    if new_ID in username_list:
        new_ID = input("The username you have entered already exists. Please enter another username: ")

    # Ask user to insert password and ask for password confirmation before registering new user
    while True:
        new_password = input(f"{WHITE}Please insert the new password: ")
        password_confirmation = input("Please retype the password: ")

        if password_confirmation == new_password:
            user_write = open('user.txt', 'a')
            user_write.write(f"\n{new_ID}, {new_password}")
            user_write.close()
            print(f"{YELLOW}{BOLD}The new user has been successfully added!\n")
            break

        # If passwords do not match, ask user to re-enter the password twice
        else:
            print(f"{RED}The passwords don't match. Please try again.")

    user_read.close()


# Create the add_task function
def add_task():
    f = open('tasks.txt', 'a+')

    # Check whether username exists
    user_read = open('user.txt', 'r')
    username_list = []

    for line in user_read:
        user, psw = line.strip("\n").split(", ")
        username_list.append(user)

    while True:
        assigned_to = input("\nPlease insert the username of the person whom the task is assigned to: ")

        # If username does not exist, ask admin to add it first
        if assigned_to not in username_list:
            print("The username does not exist, please register them first.")
            continue

        # If valid username, ask for title and description of task
        else:
            title = input("Insert task title: ")
            description = input("Insert a description of the task: ")

            # Ask user for due date and check whether their input is valid
            from datetime import datetime
            while True:
                day = int(input("Enter the day the task is due: "))
                if day > 31:
                    print("Incorrect input, try again.")
                    continue
                month = input("Please enter the month the task is due in the MMM format: ").capitalize()
                if len(month) < 3 or len(month) > 3:
                    print("Incorrect input, try again.")
                    continue
                year = int(input("Please enter the year the task is due: "))
                if year < datetime.now().year:
                    print("Incorrect input, try again.")
                    continue

                due_date = f"{day} {month} {year}"
                break

            print(f"{BOLD}{YELLOW}The task has been successfully added!\n")

            # Import date.today from datetime library in the 'DD MMM YYYY' format
            from datetime import date
            today = date.today()
            td = today.strftime("%d %b %Y")

            # By default, 'No' is inserted at the end (Task completeness)
            f.write(f"\n{assigned_to}, {title}, {description}, {td}, {due_date}, No")
            f.close()
            break


# Create the view_all function
def view_all():
    tasks_read = open('tasks.txt', 'r')
    data = tasks_read.readlines()

    # Create nice display to output
    for pos, line in enumerate(data, 1):
        split_data = line.split(", ")
        output = f'-----[{pos}]-----\n'
        output += '\n'
        output += f'Assigned to:\t\t\t\t\t\t{split_data[0]}\n'
        output += f'Title of the task:\t\t\t\t\t{split_data[1]}\n'
        output += f'Description of the task:\t\t\t{split_data[2]}\n'
        output += f'Assigned on:\t\t\t\t\t\t{split_data[3]}\n'
        output += f'Due date:\t\t\t\t\t\t\t{split_data[4]}\n'
        output += f'Task completed? Yes/No:\t\t\t\t{split_data[5]}\n'

        print(output)

    tasks_read.close()


# Create the view_mine function
def view_mine():
    data = ''  # clear buffer to avoid previous inputs
    f = open('tasks.txt', 'r')
    data = f.readlines()
    find_task = False

    # Display the user's tasks in nice output display
    for pos, line in enumerate(data, 1):
        split_data = line.split(", ")

        if username == split_data[0]:
            output = f'-----[{pos}]-----\n'
            output += '\n'
            output += f'Assigned to:\t\t\t\t\t\t{split_data[0]}\n'
            output += f'Title of the task:\t\t\t\t\t{split_data[1]}\n'
            output += f'Description of the task:\t\t\t{split_data[2]}\n'
            output += f'Assigned on:\t\t\t\t\t\t{split_data[3]}\n'
            output += f'Due date:\t\t\t\t\t\t\t{split_data[4]}\n'
            output += f'Task completed? Yes/No:\t\t\t\t{split_data[5]}\n'
            find_task = True
            print(output)

    # If the user has no tasks assigned to them, indicate it
    if find_task == False:
        print(f"{YELLOW}You have already completed all your tasks!\n")
        f.close()
        return (0)

    # Allowing the user to select a specific task or type -1 to return to menu
    complete_data = ""
    while find_task == True:

        xtask_choice = input(f"{WHITE}\nPlease select a specific task by entering its number "
                             "or type -1 to return to the main menu: ")
        if not xtask_choice:
            xtask_choice = -1
        task_choice = int(xtask_choice) - 1

        # Return to main menu if user enters -1
        if task_choice == -2:
            return (0)

        # Fail-safe in case user enters an invalid option
        elif task_choice < -2 or task_choice > len(data):
            print(f"{RED}You have selected a invalid option, try again.")
            continue

        complete_data = data[task_choice]
        split_data = complete_data.split(", ")

        # Check that task is attributed to the user
        if username != split_data[0]:
            print(f"{RED}You have selected an invalid option, try again.")
            continue

        break

    # Display the two options when user has inserted a valid input above
    while True:
        xchoice = input(f'''{WHITE}\n-----[SELECT AN OPTION]-----
1. Mark the Task as complete
2. Edit the task
Please type 1 or 2: ''')
        if not xchoice:
            xchoice = 0
        choice = int(xchoice)

        split_data = complete_data.split(", ")

        # Fail-safe if user inputs an invalid option
        if choice <= 0 or choice >= 3:
            print(f"{RED}You have selected an invalid option, try again.")
            continue

        # Making sure the edits are only possible if the task has not yet been completed
        if split_data[-1] == "Yes\n":
            print(f"{RED}The task is already completed, you cannot modified it")
            f.close()
            return (0)

        o = open('tasks.txt', 'w')

        # Mark the task as completed
        if choice == 1:
            split_data = complete_data.split(", ")
            split_data[-1] = "Yes\n"
            data_edited = ", ".join(split_data)
            data[task_choice] = data_edited

            print(f"{YELLOW}The task is now completed!\n")

        # Option to amend the task
        elif choice == 2:

            # Amend username option
            xuser_edit = input("\nWhat would you like to do?\n"
                               "1- Assign the task to another username\n"
                               "2- The due date\n"
                               "Please type 1 or 2: ")
            if not xuser_edit:
                xuser_edit = 0
            user_edit = int(xuser_edit)
            if user_edit == 1:
                while True:

                    # Check that the username already exists
                    user_read = open('user.txt', 'r')
                    username_list = []
                    for line in user_read:
                        user, psw = line.strip("\n").split(", ")
                        username_list.append(user)

                    # Ask user to insert the username
                    new_username = input("To whom (which username) would you like to assign the task to? or type -1 ")
                    if new_username in username_list:
                        split_data = complete_data.split(", ")
                        split_data[0] = new_username
                        new_data = ", ".join(split_data)
                        data[task_choice] = new_data
                        print(f"{YELLOW}You have successfully amended the username for this task.\n")
                        break

                    # If the username does not exist, ask user to register it first
                    else:
                        print("This username does not exist, please register them first")
                        continue

            # Amend due date option
            elif user_edit == 2:
                from datetime import datetime

                # Ask user to enter the date and check their input is valid
                while True:
                    xday = input("Enter the day the task is due: ")
                    if not xday:
                        xday = datetime.now().day
                    day = int(xday)
                    if day < 1 or day > 31:
                        print("Incorrect input, try again.")
                        continue
                    month = input("Please enter the month the task is due in the MMM format: ").capitalize()
                    if len(month) < 3 or len(month) > 3:
                        print("Incorrect input, try again.")
                        continue

                    year = int(input("Please enter the year the task is due: "))
                    if year < datetime.now().year:
                        print("Incorrect input, try again.")
                        continue

                    new_date = f"{day} {month} {year}"
                    split_data = complete_data.split(", ")
                    split_data[-2] = new_date
                    new_data = ", ".join(split_data)
                    data[task_choice] = new_data

                    print(f"{YELLOW}You have successfully amended the due date of the task.\n")
                    break

        for line in data:
            o.write(line)

        o.close()
        break
    f.close()


# Create the view_stats function
def view_stats():
    import os
    if os.path.exists('task_overview.txt') == False or os.path.exists('user_overview.txt') == False:
        gen_reports()

    print(f"{WHITE} ")
    print(f"{CYAN}======== STATISTICS =============")
    print(f"{GREEN} ")

    f = open('task_overview.txt', 'r')
    data = f.readlines()
    for line in data:
        print(f"{GREEN} {line}")
    f.close()
    print(f"{CYAN}=================================")
    print(f"{GREEN} ")

    f = open('user_overview.txt', 'r')
    data = f.readlines()
    for line in data:
        print(f"{GREEN} {line}")
    f.close()
    print(f"{WHITE} ")


# Create the gen_reports function
def gen_reports():
    data = ''
    # reference for selection
    my_selection = 'task_manager.py'

    # Creation of the 'task_overview' report
    f = open('tasks.txt', 'r')
    data = f.readlines()
    x = 0
    split_data = ''  # clear field
    # Calculate the total number of tasks that have been generated and tracked
    for line in data:
        split_data = line.split(", ")
        # the task must have been generated by task_manager.py
        # if split_data[1].count(my_selection) == 0 and split_data[2].count(my_selection) == 0:
        #     continue

        if split_data[-1] == "Yes\n" or split_data[-1] == "Yes":
            x += 1
    o = open('task_overview.txt', 'w+')

    total = len(data)
    o.write(f"The total number of tasks that have been generated and tracked by {my_selection}: {total}\n")

    # Calculate the total number of completed tasks per user
    o.write(f"The total number of completed tasks is: {x}\n")

    # Calculate the total number of incomplete tasks per user
    incomp_tasks = total - x
    o.write(f"The total number of uncompleted tasks is: {incomp_tasks}\n")

    # Calculate the percentage of incomplete tasks per user
    percentage = str(round((incomp_tasks / total) * 100, 0))
    o.write(f"The percentage of uncompleted tasks is: {percentage}%\n")

    # Calculate the number of tasks that are incomplete and overdue per user
    import datetime
    date_format = "%d %b %Y"
    x = 0
    y = 0
    overdue_percentage = 0

    for line in data:
        split_data = line.split(", ")
        date_obj = datetime.datetime.strptime(split_data[4], date_format)
        if date_obj < datetime.datetime.today():
            y += 1
            if split_data[-1] == "No\n" or split_data[-1] == "No":
                x += 1
                overdue_percentage = round((x / total) * 100, 0)

    o.write(f"The total number of tasks that are incomplete and overdue is: {x}\n")

    # Calculate the percentage of tasks that are overdue (and incomplete)
    o.write(f"The percentage of tasks that are overdue is: {overdue_percentage}%\n")

    o.close()
    f.close()

    # Creation of the 'user_overview' report
    user_read = open('user.txt', 'r')
    username_list = []
    user_count = 0

    # Calculate the total number of users registered
    for line in user_read:
        user, psw = line.strip("\n").split(", ")
        username_list.append(user)

        if split_data[0] in username_list:
            user_count += 1

    o = open('user_overview.txt', 'w+')
    o.write(f"The total number of users registered with task_manager.py is: {user_count}\n")

    data = ''
    # Creation of the 'user_overview' option
    f = open('tasks.txt', 'r')
    data = f.readlines()
    x = 0

    # Calculate the total number of tasks that have been generated and tracked
    for line in data:
        split_data = line.split(", ")
        if split_data[-1] == "Yes":
            x += 1

    total = len(data)
    o.write(f"The total number of tasks that have been generated and tracked using task_manager.py is: {total}\n")

    # Calculate the total numbers of tasks per user, using dictionaries
    dict_main = {}  # number of tasks assigned by user - checking for name in list
    dict_completed = {}  # number of completed tasks per user
    dict_overdue = {}  # number of tasks uncompleted and overdue per user

    import datetime
    date_format = "%d %b %Y"

    for line in data:
        split_data = line.strip().split(", ")
        name = split_data[0]

        if name not in dict_main:
            dict_main[name] = 1
            dict_completed[name] = 0
            dict_overdue[name] = 0
            if split_data[-1] == "Yes":
                dict_completed[name] += 1
        else:
            dict_main[name] += 1
            if split_data[-1] == "Yes":
                dict_completed[name] += 1
            else:
                # checking if incomplete task is overdue
                date_obj = datetime.datetime.strptime(split_data[4], date_format)
                if date_obj < datetime.datetime.today():
                    # if overdue, add 1 to dict_overdue name
                    dict_overdue[name] += 1

    o.write('The total number of tasks assigned by user is:')
    for item, amount in dict_main.items():
        o.write("\t{}: {} ".format(item, amount))

    # Calculate the percentage of the total number of tasks per user
    total = len(data)
    o.write("\nThe percentage of the total number of tasks assigned by user:")

    for key, val in dict_main.items():
        percent = str(round((val / total) * 100, 0)) + "%"
        o.write("\t{}: {} ".format(key, percent))

    # Calculate per user the percentage of tasks for this user that have been completed
    x = 0
    o.write(f"\nThe percentage per user of completed tasks for this user: ")
    for key, val_total in dict_main.items():
        val_completed = dict_completed.get(key, 0)
        percentage = round((val_completed / val_total) * 100, 0)
        my_percentage = f"{percentage}%"
        o.write("\t{}: {} ".format(key, my_percentage))

    # Calculate per user the percentage of tasks for this user that are incomplete
    o.write(f"\nThe percentage per user of uncompleted tasks for this user: ")

    for key, val_total in dict_main.items():
        val_completed = dict_completed.get(key, 0)
        percentage = round(((val_total - val_completed) / val_total) * 100, 0)
        my_percentage = f"{percentage}%"
        o.write("\t{}: {} ".format(key, my_percentage))

    # Calculate per user the percentage of tasks of user that are incomplete and overdue for this user
    o.write(f"\nThe percentage per user of tasks of user that are incomplete and overdue for this user: ")

    for key, val_total in dict_main.items():
        val_overdue = dict_overdue.get(key, 0)
        percentage = round((val_overdue / val_total) * 100, 0)
        my_percentage = f"{percentage}%"
        o.write("\t{}: {} ".format(key, my_percentage))

    o.close()
    print(f"{YELLOW}The reports have been generated!\n")


# LOG IN SECTION
user_read = open('user.txt', 'r')

# Create empty lists
username_list = []
pas_list = []

# For loop to create the two lists (usernames & passwords)
for line in user_read:
    user, psw = line.strip("\n").split(", ")
    username_list.append(user)
    pas_list.append(psw)

user_read.close()
user_read = open('user.txt', 'r')

print(f"{PINK} ╔═══════ MANAGE YOUR TASKS ══════╗\n")
print(f"{CYAN}══ Welcome! Log in area ══")

username = input(f"{WHITE}Please enter your username: ")

# While loop to recognise a valid username and error message in case of invalid input
while username not in username_list:
    print(f"{RED}Invalid username")
    username = input(f"{WHITE}Please enter your username: ")

# While loop to match the index of the username with the index of the password
post = username_list.index(username)
password = input("Please enter your password: ")
while password != pas_list[post]:
    print(f"{RED}Invalid password")
    password = input(f"{WHITE}Please enter your password: ")

username_cap = username.capitalize()
print(f"{YELLOW}{BOLD}Successful login. Welcome, {username_cap}!\n")

user_read.close()

# DISPLAYING MENU SECTION
menu()
