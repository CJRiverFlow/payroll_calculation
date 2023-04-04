"""
This file contains the test cases for the payroll calculator class
"""

from payroll.parser import InputParser
from payroll.schedule import ScheduleHandler
from payroll.calculator import PayrollCalculator


class TestPayrollCalculator:
    """
    Test class for PayrollCalculator class
    """

    @classmethod
    def setup_class(cls):
        """
        Initialize module instances
        """
        cls.schedule_handler = ScheduleHandler()
        cls.payroll_calculator = PayrollCalculator("default")
        cls.input_parser = InputParser()

    def test_calculate_payment(self):
        """
        Test case for partial payment calculation
        """
        input_str = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        work_history = self.input_parser.parse(input_str)
        payment = self.payroll_calculator.calculate_payment(work_history)
        assert int(payment) == 85

    def test_calculate_payment_weekend_bonus(self):
        """
        Test case for weekend bonus payment calculation.
        """
        input_str = "ASTRID=SA08:00-20:00,SU10:00-22:00"
        work_history = self.input_parser.parse(input_str)
        payment = self.payroll_calculator.calculate_payment(work_history)
        assert int(payment) == 520

    def test_calculate_payment_overtime(self):
        """
        Test case for overtime payment calculation.
        """
        input_str = "ASTRID=MO08:00-19:35,TU08:00-19:35,WE08:00-19:35,TH08:00-19:35,FR08:00-19:35"
        work_history = self.input_parser.parse(input_str)
        payment = self.payroll_calculator.calculate_payment(work_history)
        assert int(payment) == 1000
