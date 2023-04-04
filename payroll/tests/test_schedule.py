"""
This file contains the tests for the payment schedule handler module
"""
from datetime import time
import pytest

from payroll.schedule import ScheduleHandler, PaymentSchedule, TimeSlot, Period
from payroll.errors import PaymentScheduleNotFound


class TestScheduleHandler:
    """
    Tests for ScheduleHandler class
    """

    @classmethod
    def setup_class(cls):
        """
        Test class initialization
        """
        cls.schedule_handler = ScheduleHandler()

    def test_get_schedule_valid(self):
        """
        Test a valid payment schedule configuration parsing
        """
        schedule_name = "default"
        expected_schedule = PaymentSchedule(
            name="default",
            periods=[
                Period(
                    days=["MO", "TU", "WE", "TH", "FR"],
                    time_slots=[
                        TimeSlot(start=time(0, 1), end=time(9, 0), rate=25),
                        TimeSlot(start=time(9, 1), end=time(18, 0), rate=15),
                        TimeSlot(start=time(18, 1), end=time(23, 59, 59), rate=20),
                    ],
                ),
                Period(
                    days=["SA", "SU"],
                    time_slots=[
                        TimeSlot(start=time(0, 1), end=time(9, 0), rate=30),
                        TimeSlot(start=time(9, 1), end=time(18, 0), rate=20),
                        TimeSlot(start=time(18, 1), end=time(23, 59, 59), rate=25),
                    ],
                ),
            ],
        )
        actual_schedule = self.schedule_handler.get_schedule(schedule_name)
        assert actual_schedule == expected_schedule

    def test_get_schedule_invalid_name(self):
        """
        Test for invalid payment schedule config
        """
        schedule_name = "invalid_schedule"
        with pytest.raises(PaymentScheduleNotFound):
            self.schedule_handler.get_schedule(schedule_name)
