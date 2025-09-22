# You have been approached by a financial company to create a program 
# They want two different financial calculators: an investment calculator and a home loan repayment calculator 

import math 

# Print investment or bond for user to choose
print("Investment - to calculate the amount of interest you'll earn on your investment")
print("Bond - to calculate the amount you'll have to pay on a home loan")

# Prompt user to choose, use input to use what user inputs 
user_choice = (input("Enter either 'investment' or 'bond' to proceed:")).lower() # Using lower turns whatever user inputs into lowercase

# If user choses investment we begin here 
if user_choice == "investment": 
    amount = float(input("Enter amount of money you will deposit"))
    interest_rate = float(input("Enter interest rate"))  
    years = int(input("Enter number of years you plan on investing"))
    interest_type = input("Do you want 'simple' or 'compund' interest?").lower()

    r = interest_rate / 100 # Convert percentage to decimal 
# If user chooses simple interest here is the calculation 
    if interest_type == "simple": #Don't forget : when using if 
        total = amount * (1+ r * years)
        print(f"Your simple interest total is {total: .2f} dollars") # .2f means two decimal points 
 # If user chooses compound interest here is the calculation        
    elif interest_type == "compound": 
        r = interest_rate / 100 # Convert percentage to decimal 
        total = amount * math.pow ((1+ r ),years) # Formula for compound 
        print(f"Your compound interest total is {total:.2f} dollars")
# For it to work you have to add an else at the end 
    else: 
        print("Invalid interest type entered")

# If user chooses bond we start here 
if user_choice == "bond": 
    present_value = float(input("Enter present value of the house"))
    interest_rate = float(input("Enter interest rate"))
    number_of_months = float(input("Enter number of months you plan to take to repay the bond"))
    r = interest_rate / 100 # Convert percentage to decimal 
    i = r / 12 # Divide interest by 12 since we're looking at monthly payments 
    repayment = (i * present_value) /( 1 - (1+ i)**(-number_of_months)) # Formula for bond 
    print(f"You will have to pay{repayment:.2f} dollars each month to repay the bond")
else : 
    print("Invalid, please enter either 'investment' or 'bond'")
