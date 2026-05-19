import pandas as pd
import os
# the function use for verify the user
def verify_user(user_id, ic_number,password):
    user_id = str(user_id).strip()
    ic_number = str(ic_number).strip()
    password = str(password).strip()

    if not user_id or not ic_number or not password:
        return False
    if not ic_number.isdigit() or len(ic_number)!=12:
        return False
    last_four = ic_number[-4:]
    return password == last_four

def calculate_tax(income, tax_relief):
    net_income = max(0,income -tax_relief)
    if net_income <=5000:
        tax = 0
    elif net_income <=20000:
        tax = 150+(net_income-5000)*0.01
    elif net_income <=35000:
        tax = 450+(net_income-20000)*0.03
    elif net_income <=50000:
        tax = 600+(net_income-35000)*0.06
    elif net_income <=70000:
        tax = 1500+(net_income-50000)*0.11
    elif net_income <=100000:
        tax = 3700+(net_income-100000)*0.19
    elif net_income <=400000:
        tax = 9400+(net_income-100000)*0.25
    elif net_income <=600000:
        tax = 84400+(net_income-400000)*0.26
    elif net_income <=2000000:
        tax = 136400+(net_income-600000)*0.28
    else:
        tax = 528400+(net_income-2000000)*0.30
    return round(tax,2)

def save_user_data(data,filename = 'user data.csv'):
    newfile1 = pd.DataFrame([data])
    if not os.path.exists(filename):
        newfile1.to_csv(filename, index=False)
    else:
        newfile1.to_csv(filename, mode = 'a', header = False, index =False)

def save_tax_record(data,filename ="tax record.csv"):
    newfile2 = pd.DataFrame([data])
    if not os.path.exists(filename):
        newfile2.to_csv(filename, index=False)
    else:
        newfile2.to_csv(filename, mode = "a", header = False, index =False)

def read_from_csv1(filename='user data.csv'):
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename, dtype={"User ID": str, "IC Number": str})
        except (IOError, pd.errors.EmptyDataError):
            return None
    return None
def read_from_csv2(filename="tax record.csv"):
    if os.path.exists(filename):
        try:
            return pd.read_csv(filename, dtype={"User ID": str, "IC Number": str})
        except (IOError, pd.errors.EmptyDataError):
            return None
    return None