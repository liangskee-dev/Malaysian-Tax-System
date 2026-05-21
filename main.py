import function as ft
# Function to safely get validated non-negative float numbers from inputs
def get_input(prompt_message):
    while True:
        try:
            value = float(input(prompt_message))
            if value < 0:
                print("Value cannot be negative. Please try again.")
                continue
            return value
        except ValueError:
            print('Invalid input format. Please enter the positive value.')
#Function to drive the main execution menu loop dashboard interface
def menu():
    tax_file = "tax_record.csv"
    user_file = 'user_database.csv'
    print('============================================')
    print('    Malaysian Tax Input Program System    ')
    print('============================================')

    while True:
        print("\n---Main Menu---")
        print("1. Register (New User) ")
        print("2. Login & Calculate Tax (Registered User) ")
        print("3. View All Tax Records ")
        print("4. Exit")
# option 1: For user register in the system only
        option = input("Please select an option(1-4): ").strip()
        if option == '1':
            print('\n---User Registration Information---')
            user_id = input("Enter User ID: ")
            ic_num = input("Enter your ic number as a password(do not include '-'): ").strip()
            confirm_password = input("Confirm Password(Last 4 digit of IC): ").strip()
            if not ft.verify_user(user_id, ic_num, confirm_password):
                print('\n[ERROR] Registration failed!')
                print('Ensure User ID is not blank.')
                print('Ensure your IC has exactly 12 numeric digits.')
                print('Ensure your confirm password matches the last 4 digits of your IC.')
                continue
            user_database = ft.read_from_csv1(user_file)

            if user_database is not None and not user_database.empty:

                if 'User ID' not in user_database.columns or 'IC Number' not in user_database.columns:
                    user_database.columns = ['User ID', 'IC Number']

                duplicate_row = user_database[
                    (user_database['User ID'].astype(str)==user_id) &
                    (user_database['IC Number'].astype(str)==ic_num)
                ]
                if not duplicate_row.empty:
                    print('\n[ERROR] User already exists in our database!')
                    continue

                elif user_id in user_database['User ID'].astype(str).values:
                    print(f"\n[ERROR] The User ID '{user_id}' is already used. Please change to another.")
                    continue
                elif ic_num in user_database['IC Number'].astype(str).values:
                    print("\n[ERROR] The user is registered already with this IC number!")
                    continue
            account_data ={
                'User ID': user_id,
                'IC Number': ic_num,
            }
            ft.save_user_data(account_data, user_file)
            print('\n>>> User is successfully registered in our system <<<')
            print('You can now log in using Option 2 to process your tax assessments.')
# option 2:  Login and calculate tax
        elif option == '2':
            print('\n---User Login Authentication---')
            user_id = input("Enter User ID: ")
            ic_num = input("Enter your IC Number as a password(do not include '-'): ").strip()
            confirm_password = input("Confirm Password(Last 4 digit of IC): ").strip()

            if not ft.verify_user(user_id, ic_num, confirm_password):
                print('\n[ERROR] Authentication failed!Structural pattern rejected!')
                continue

            user_database = ft.read_from_csv1(user_file)

            if user_database is None or user_database.empty:
                print('\n[ERROR] Login failed! No registered accounts exists in the system yet')
                continue
            matched_user = user_database[
                (user_database['User ID'].astype(str) == user_id) &
                (user_database['IC Number'].astype(str) == ic_num)
            ]
            if matched_user.empty:
                print('\n[ERROR]Login failed! Incorrect User ID or IC Number combination!')
                continue
            print(f'\n>>>Login Successful! Welcome back, {user_id}.<<<')
            # Inner Loop: For Login User Sub Menu
            while True:
                print(f'\n---Sub Menu----')
                print("1. Calculate Tax ")
                print('2. View Personal Tax Records')
                print('3. Log Out')
                sub_option = input('Please select an sub option(1-3): ').strip()
                # Sub Option 1: Calculate Tax and save into the Excel File
                if sub_option == '1':
                    print('\n---Financial Data Entry---')
                    annual_income = get_input("Enter annual income(RM): ")
                    tax_relief = get_input("Enter tax relief(RM): ")
                    tax_payable = ft.calculate_tax(annual_income,tax_relief)

                    print('\n==============================')
                    print('     Tax Assessment Summary     ')
                    print('===============================')
                    print(f'User ID           : {user_id}')
                    print(f'IC Number         : {ic_num}')
                    print(f'Annual Income(RM) : RM {annual_income:,.2f}')
                    print(f'Tax Relief(RM)    : RM {tax_relief:,.2f}')
                    print('--------------------------------------')
                    print(f'Tax Payable(RM)   : RM {tax_payable:,.2f}')
                    print('=======================================')

                    tax_data = {
                        'User ID': user_id,
                        'IC Number': ic_num,
                        'Annual Income(RM)': annual_income,
                        'Tax Relief(RM)': tax_relief,
                        'Tax Payable(RM)': tax_payable,
                    }
                    ft.save_tax_record(tax_data, tax_file)
                    print('[SUCCESS] Tax Calculation Successfully generated and save into file')
                # The login user can view their own records only
                elif sub_option == '2':
                    print(f'\n---Personal Tax Records')
                    tax_database = ft.read_from_csv2(tax_file)
                    if tax_database is None or tax_database.empty:
                        print('[INFO] You do not have compute any records in the tax file yet. ')
                        continue
                    own_records = tax_database[
                        (tax_database['User ID'].astype(str) == user_id)&
                        (tax_database['IC Number'].astype(str) == ic_num)
                    ]

                    if own_records.empty:
                        print("[INFO] You do not have any records saved in the system yet.")
                    else:
                        print('\n',own_records.to_string(index=False))
                        print(f'\nTotal Personal Records Saved:{len(own_records)}')
                # Login out from the system
                elif sub_option == '3':
                    print(f'\nLogging Out from user account: {user_id}')
                    break
                else:
                    print('\nInvalid Sub Option! Please choose either 1,2, or 3')

        # option 3: View All the tax records that calculate by all user
        elif option == '3':
            print('\n---System Tax Record---')
            tax_database = ft.read_from_csv2(tax_file)
            if tax_database is None or tax_database.empty:
                print('\n[Info] No tax records found. The database is currently empty')
                continue
            display_df = tax_database.copy()
            display_df['User ID'] = display_df['User ID'].astype(str).apply(
                lambda x: x[0] + '*' * (len(x)-1) if len(x) >1 else x
            )
            display_df['IC Number'] = display_df['IC Number'].astype(str).apply(
                lambda x: x[:6] + '******' if len(x) >= 6 else '******'
            )
            display_df.columns = [
                "User ID", "IC Number", "Annual Income(RM)", 'Tax Relief(RM)', 'Tax Payable(RM)'
            ]
            print('\n', display_df.to_string(index=False))
            print(f'\nTotal Active Calculation Records: {len(tax_database)}')
        # option 4: Exit the system
        elif option=='4':
            print('\nThank you for using this system. Goodbye and have a nice day!')
            break
        else:
            print('\n[Invalid Option] Please choose the option between 1 to 4')
if __name__ == '__main__':
    menu()