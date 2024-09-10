from tkinter import *
import os
import PIL
import pandas
from datetime import *
from PIL import ImageTk, Image


# main screen
master = Tk()
master.title('MSLN Online Banking App')


# functions
def finish_registration():
    name = temp_name.get()
    age = temp_age.get()
    gender = temp_gender.get()
    password = temp_password.get()
    all_accounts = os.listdir()

    # if any field isn't filled
    if name == "" or age == "" or gender == "" or password == "":
        notif.config(fg="red", text="* All fields are required *")
        return

    for name_check in all_accounts:
        if name == name_check:
            notif.config(fg="red", text="This account already exists")
            return
        else:
            new_file = open(name, "w")
            new_file.write(name + '\n')
            new_file.write(password + '\n')
            new_file.write(age + '\n')
            new_file.write(gender + '\n')
            new_file.write('0')
            new_file.close()
            notif.config(fg="green", text="Account has been created successfully")


def register():
    # variables
    global temp_name
    global temp_age
    global temp_gender
    global temp_password
    global notif
    temp_name = StringVar()
    temp_age = StringVar()
    temp_gender = StringVar()
    temp_password = StringVar()

    # register screen
    register_screen = Toplevel(master)
    register_screen.title("Register")

    # labels
    Label(register_screen, text="Please enter your details below to register", font=("Calibri", 12)). \
        grid(row=0, sticky=N, pady=10)
    Label(register_screen, text="Name", font=("Calibri", 10)). \
        grid(row=1, sticky=W)
    Label(register_screen, text="Age", font=("Calibri", 10)). \
        grid(row=2, sticky=W)
    Label(register_screen, text="Gender", font=("Calibri", 10)). \
        grid(row=3, sticky=W)
    Label(register_screen, text="Password", font=("Calibri", 10)). \
        grid(row=4, sticky=W)
    notif = Label(register_screen, font=("Calibri", 12))
    notif.grid(row=6, sticky=N, pady=10)

    # entries
    Entry(register_screen, textvariable=temp_name).grid(row=1, column=0)
    Entry(register_screen, textvariable=temp_age).grid(row=2, column=0)
    Entry(register_screen, textvariable=temp_gender).grid(row=3, column=0)
    Entry(register_screen, textvariable=temp_password, show="*").grid(row=4, column=0)

    # buttons
    Button(register_screen, text="Register", command=finish_registration, font=("Calibri", 12)). \
        grid(row=5, sticky=N, pady=10)


def login_session():
    global login_name
    all_accounts = os.listdir()
    login_name = temp_login_name.get()
    login_password = temp_login_password.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split('\n')
            password = file_data[1]
            # account dashboard
            if login_password == password:
                login_screen.destroy()
                account_dashboard = Toplevel(master)
                account_dashboard.title("Dashboard")

                # labels
                Label(account_dashboard, text="Account Dashboard", font=("Calibri", 12)). \
                    grid(row=0, sticky=N, pady=10)
                Label(account_dashboard, text="Welcome, " + name, font=("Calibri", 12)). \
                    grid(row=1, sticky=N, pady=5)

                # buttons
                Button(account_dashboard, text="Personal Details", font=("Calibri", 12), width=30,
                       command=personal_details).grid(row=2, sticky=N, padx=10)
                Button(account_dashboard, text="Deposit", font=("Calibri", 12), width=30,
                       command=deposit).grid(row=3, sticky=N, padx=10)
                Button(account_dashboard, text="Withdraw", font=("Calibri", 12), width=30,
                       command=withdraw).grid(row=4, sticky=N, padx=10)
                Button(account_dashboard, text="E-Transfer", font=("Calibri", 12), width=30,
                       command=e_transfer).grid(row=5, sticky=N, padx=10)
                Button(account_dashboard, text="Transaction History", font=("Calibri", 12), width=30,
                       command=transaction_history).grid(row=6, sticky=N, padx=10)
                Label(account_dashboard).grid(row=7, sticky=N, pady=10)
                return
            else:
                login_notif.config(fg="red", text="Password is incorrect. Please Try again.")
                return
    login_notif.config(fg="red", text="Account not found")


def transaction_history():
    # variables
    global login_name
    global amount
    amount = StringVar()
    transactions = []
    for transaction in transactions:
        print(transaction)

    # transaction history screen
    transaction_history_screen = Toplevel(master)
    transaction_history_screen.title("Transaction History")

    # labels
    Label(transaction_history_screen, text="Transaction History", font=("Calibri", 12), width=25). \
        grid(row=0, sticky=N, pady=10)

    # Read transaction history from file
    file_name = login_name + "_transaction_history.txt"
    if not os.path.exists(file_name):
        Label(transaction_history_screen, text="No transaction history available.", font=("Calibri", 12)). \
            grid(row=1, sticky=N, padx=10)
        return

    with open(file_name, "r") as file:
        transactions = file.read().splitlines()

    # Display transaction history
    if not transactions:
        Label(transaction_history_screen, text="No transaction history available.", font=("Calibri", 12)). \
            grid(row=1, sticky=N, padx=10)
    else:
        for i, transaction in enumerate(transactions):
            Label(transaction_history_screen, text=transaction, font=("Calibri", 12)).grid(row=i + 1, sticky=N, padx=10)

        row_counter = + 1
        # Display amount
        Label(transaction_history_screen, text=amount, font=("Calibri", 10)).grid(row=row_counter, column=1, padx=10)


def deposit():
    # variables
    global amount
    global deposit_notif
    global current_balance_label
    today = date.today()
    datetime = today.strftime("%B %d, %Y")
    amount = StringVar()
    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    # deposit screen
    deposit_screen = Toplevel(master)
    deposit_screen.title("Deposit")

    # labels
    Label(deposit_screen, text="Deposit", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    current_balance_label = Label(deposit_screen, text="Current Balance: $" + details_balance, font=('Calibri', 12))
    current_balance_label.grid(row=1, sticky=W)
    Label(deposit_screen, text="Amount: ", font=('Calibri', 12)).grid(row=2, sticky=W)
    deposit_notif = Label(deposit_screen, font=('Calibri', 12))
    deposit_notif.grid(row=4, sticky=N, pady=5)
    Label(deposit_screen, text=datetime, font=('Calibri', 12)).grid(row=3,column=1, sticky=E, pady=5)

    # entries
    Entry(deposit_screen, textvariable=amount).grid(row=2, column=1)

    # buttons
    Button(deposit_screen, text="Finish", font=('Calibri', 12), command=finish_deposit).grid(row=3, sticky=W, pady=5)


def finish_deposit():
    if amount.get() == "":
        deposit_notif.config(fg="red", text="Amount is required")
        return
    if float(amount.get()) <= 0:
        deposit_notif.config(fg='red', text="A negative amount has been entered, please try again.")
        return
    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]
    updated_balance = current_balance
    updated_balance = float(updated_balance) + float(amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate(0)
    file.write(file_data)
    file.close()

    today = date.today()
    datetime = today.strftime("%B %d, %Y")

    # Update transaction history
    transaction_file_name = login_name + "_transaction_history.txt"
    transaction = "Deposit: +$" + amount.get() + " | Balance: $" + str(updated_balance) + " | " + datetime + "\n"
    with open(transaction_file_name, "a") as transaction_file:
        transaction_file.write(transaction)

    current_balance_label.config(fg='green', text='Current Balance: $' + str(updated_balance))
    deposit_notif.config(fg='green', text='Balance Updated')


def withdraw():
    # variables
    global withdraw_amount
    global withdraw_notif
    global current_balance_label
    today = date.today()
    datetime = today.strftime("%B %d, %Y")
    withdraw_amount = StringVar()
    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]

    # withdraw screen
    withdraw_screen = Toplevel(master)
    withdraw_screen.title("Withdraw")

    # labels
    Label(withdraw_screen, text="Withdraw", font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    current_balance_label = Label(withdraw_screen, text="Current Balance: $" + details_balance,
                                  font=('Calibri', 12))
    current_balance_label.grid(row=1, sticky=W)
    Label(withdraw_screen, text="Amount: ", font=('Calibri', 12)).grid(row=2, sticky=W)
    withdraw_notif = Label(withdraw_screen, font=('Calibri', 12))
    withdraw_notif.grid(row=4, sticky=N, pady=5)
    Label(withdraw_screen, text=datetime, font=('Calibri', 12)).grid(row=3, column=1, sticky=E, pady=5)

    # entries
    Entry(withdraw_screen, textvariable=withdraw_amount).grid(row=2, column=1)

    # buttons
    Button(withdraw_screen, text="Finish", font=('Calibri', 12), command=finish_withdraw).grid(row=3, sticky=W, pady=5)


def finish_withdraw():
    if withdraw_amount.get() == "":
        withdraw_notif.config(fg="red", text="Amount is required")
        return
    if float(withdraw_amount.get()) <= 0:
        withdraw_notif.config(fg='red', text="A negative amount has been entered, please try again.")
        return
    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]

    if float(withdraw_amount.get()) >= float(current_balance):
        withdraw_notif.config(fg='red', text='Insufficient Funds')
        return

    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(withdraw_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate()
    file.write(file_data)
    file.close()

    today = date.today()
    datetime = today.strftime("%B %d, %Y")

    # Update transaction history
    transaction_file_name = login_name + "_transaction_history.txt"
    transaction = "Withdraw: -$" + withdraw_amount.get() + " | Balance: $" + str(
        updated_balance) + " | " + datetime + "\n"
    with open(transaction_file_name, "a") as transaction_file:
        transaction_file.write(transaction)

    current_balance_label.config(fg='green', text='Current Balance: $' + str(updated_balance))
    withdraw_notif.config(fg='green', text='Balance Updated')


def personal_details():
    # variables
    file = open(login_name, 'r')
    file_data = file.read()
    user_details = file_data.split('\n')
    details_name = user_details[0]
    details_age = user_details[2]
    details_gender = user_details[3]
    details_balance = user_details[4]

    personal_details_screen = Toplevel(master)
    personal_details_screen.title("Personal Details")

    # labels
    Label(personal_details_screen, text="Personal Details", font=("Calibri", 12), width=25). \
        grid(row=0, sticky=N, pady=10)
    Label(personal_details_screen, text="Name: " + details_name, font=("Calibri", 12), width=25). \
        grid(row=1, sticky=W, pady=10)
    Label(personal_details_screen, text="Age: " + details_age, font=("Calibri", 12), width=25). \
        grid(row=2, sticky=W, pady=10)
    Label(personal_details_screen, text="Gender: " + details_gender, font=("Calibri", 12), width=25). \
        grid(row=3, sticky=W, pady=10)
    Label(personal_details_screen, text="Balance: $" + details_balance, font=("Calibri", 12), width=25). \
        grid(row=4, sticky=W, pady=10)


def e_transfer():
    # variables
    global e_transfer_amount
    global e_transfer_notif
    global login_name
    global current_balance_label
    today = date.today()
    datetime = today.strftime("%B %d, %Y")
    withdraw_amount = StringVar()
    file = open(login_name, "r")
    file_data = file.read()
    user_details = file_data.split('\n')
    details_balance = user_details[4]
    all_accounts = os.listdir()
    login_name = temp_login_name.get()

    for name in all_accounts:
        if name == login_name:
            file = open(name, "r")
            file_data = file.read()
            file_data = file_data.split('\n')
            name = file_data[0]

    # e-transfer screen
    e_transfer_screen = Toplevel(master)
    e_transfer_screen.title("E-Transfer")

    # labels
    Label(e_transfer_screen, text="E-Transfer", font=("Calibri", 12), width=25).grid(row=0, sticky=N, pady=10)
    current_balance_label = Label(e_transfer_screen, text="Current Balance: $" + details_balance,
                                  font=('Calibri', 12))
    current_balance_label.grid(row=1, sticky=W)
    Label(e_transfer_screen, text="Name of Recipient: ", font=("Calibri", 12)).grid(row=2, sticky=W)
    Label(e_transfer_screen, text="Amount: ", font=("Calibri", 12)).grid(row=3, sticky=W)
    e_transfer_notif = Label(e_transfer_screen, font=("Calibri", 12))
    e_transfer_notif.grid(row=5, sticky=N, pady=5)

    # entries
    e_transfer_amount = StringVar()
    Entry(e_transfer_screen, textvariable=temp_login_name).grid(row=2, column=1)
    Entry(e_transfer_screen, textvariable=e_transfer_amount).grid(row=3, column=1)

    # buttons
    Button(e_transfer_screen, text="Finish", font=("Calibri", 12), command=finish_e_transfer).grid(row=4, sticky=W,
                                                                                                   pady=5)


def finish_e_transfer():
    global current_balance_label
    if e_transfer_amount.get() == "":
        e_transfer_notif.config(fg="red", text="Amount is required")
        return
    if float(e_transfer_amount.get()) <= 0:
        e_transfer_notif.config(fg='red', text="A negative amount has been entered, please try again.")
        return
    file = open(login_name, 'r+')
    file_data = file.read()
    details = file_data.split('\n')
    current_balance = details[4]

    if float(e_transfer_amount.get()) >= float(current_balance):
        e_transfer_notif.config(fg='red', text='Insufficient Funds')
        return

    updated_balance = current_balance
    updated_balance = float(updated_balance) - float(e_transfer_amount.get())
    file_data = file_data.replace(current_balance, str(updated_balance))
    file.seek(0)
    file.truncate()
    file.write(file_data)
    file.close()

    current_balance_label.config(fg='green', text='Current Balance: $' + str(updated_balance))
    e_transfer_notif.config(fg='green', text='Balance Updated')


def login():
    # variable
    global temp_login_name
    global temp_login_password
    global login_notif
    global login_screen
    temp_login_name = StringVar()
    temp_login_password = StringVar()

    # login screen
    login_screen = Toplevel(master)
    login_screen.title('Login')

    # labels
    Label(login_screen, text='Login into your account', font=('Calibri', 12)).grid(row=0, sticky=N, pady=10)
    Label(login_screen, text='Name', font=('Calibri', 12)).grid(row=1, sticky=W)
    Label(login_screen, text='Password', font=('Calibri', 12)).grid(row=2, sticky=W)
    login_notif = Label(login_screen, font=("Calibri", 12))
    login_notif.grid(row=4, sticky=N)

    # entries
    Entry(login_screen, textvariable=temp_login_name).grid(row=1, column=1, padx=5)
    Entry(login_screen, textvariable=temp_login_password, show="*").grid(row=2, column=1, padx=5)

    # buttons
    Button(login_screen, text="Login", command=login_session, width=15, font=("Calibri", 12)). \
        grid(row=3, sticky=W, pady=5, padx=5)


# image import - under construction D:
'''
image = PIL.Image.open("bank pfp.png")
img = ImageTk.PhotoImage(image)
l = Label(image=img)
l.pack()


img = Image.open('bank pfp.png')
img = ImageTk.PhotoImage()
img = img.resize((150, 150))
imglabel = Label(image=img).grid(row=1, column=1)        
'''

# labels
Label(master, text="MLSN Bank App", font=('Calibri', 14)).grid(row=0, sticky=N, pady=10)
Label(master, text="The easy-to-use version for your service. ", font=('Calibri', 12)).grid(row=1, sticky=N)

# buttons
Button(master, text="Register", font=("Calibri", 12), width=20, command=register).grid(row=3, sticky=N)
Button(master, text="Login", font=("Calibri", 12), width=20, command=login).grid(row=4, sticky=N, pady=10)

master.mainloop()
