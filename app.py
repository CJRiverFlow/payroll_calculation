"""
This script allows users to calculate the payment for an employee based on their work history. 
Simply enter the employee's work history and the script will calculate their payment. 
Users can choose to calculate payments for multiple employees in a row. 

Usage: 
python payroll.py
"""
from payroll.parser import InputParser
from payroll.calculator import PayrollCalculator

if __name__ == "__main__":
    payroll_calculator = PayrollCalculator("default")
    input_parser = InputParser()
    print("\033[1;33m" + "Welcome to the Employee Payment Software" + "\033[0m")
    CALCULATE_PAYMENT = True
    while CALCULATE_PAYMENT:
        work_data = input("Please enter the employee's work history: ")
        work_history = input_parser.parse(work_data)
        payment = payroll_calculator.calculate_payment(work_history)
        print(f"The payment for {work_history.name} is: {round(payment)} USD")
        while True:
            another_calculation = input(
                "Do you want to calculate another payment? [y/n]: "
            )
            if another_calculation.lower() == "y":
                break
            if another_calculation.lower() == "n":
                CALCULATE_PAYMENT = False
                break
            print("Please enter a valid option [y/n]")
    print(
        "\033[1;33m" + "Thank you for using the Employee Payment Software" + "\033[0m"
    )
