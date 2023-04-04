# Payroll Calculation

This repository contains an implementation of a simple payroll module as a console application.

## Description

The company Warner Bros offers their employees the flexibility to work the hours they want. They will pay for the hours worked based on the day of the week and time of day based on different payment schedules and time ranges. This application provides a flexible configuration approach that allows for different time ranges and payments. It uses a `config.json` file inside the payroll package to read the payment schedules.

The application is built in a modular way, providing modules for input string parsing, payment configuration parsing, and payment calculation.

## Console application

To run the console application, execute the following command:

```
python app.py
```
After some descriptive messages, you can enter the input string in the following format::
```
RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00
```
The output will be printed in the console as follows:
```
The payment for RENE is: 215 USD
```
You can continue entering new inputs or close the application.

## Tests

The tests require the pytest dependency. To install the dependency, execute the following command from the payroll directory of the project:

```
pip install -r requirements.txt
```

To execute the tests, run the `pytest` command from the same directory.

In the tests, we verify the behavior of the public methods of the modules used in the application, including the input string parser, payment calculator, and payment schedule handler. We also test for special cases, such as overlapping time ranges and non-working days, to ensure the application behaves correctly in all scenarios.