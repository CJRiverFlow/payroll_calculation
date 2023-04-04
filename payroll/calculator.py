"""
This module contains the class PayrollCalculator to calculate the payroll based on
the employee's work history and the payment schedule configuration.
"""
from datetime import datetime, time

from .schedule import ScheduleHandler
from .data_classes import WorkDay, WorkHistory


class PayrollCalculator:
    """
    This class calculates the payment for an employee based on their work history
    and payment schedule.

    Args:
        schedule_name (str): The name of the payment schedule to be used for the calculation.

    Attributes:
        schedule_handler (ScheduleHandler): A ScheduleHandler object that retrieves
            payment schedules.
        payment_schedule (Dict[str, List[TimeSlot]]): A dictionary where each key is a day of
            the week and the value is a list of TimeSlot dataclasses representing the
            time slots for that day.
    """

    def __init__(self, schedule_name: str):
        self.schedule_handler = ScheduleHandler()
        self.payment_schedule = self.schedule_handler.get_schedule(
            schedule_name
        ).to_time_slots()

    @staticmethod
    def _calculate_overlap(start1: time, end1: time, start2: time, end2: time) -> float:
        """
        Calculates the overlap between two time periods in hours.

        Args:
            start1 (time): The start time of the first time period.
            end1 (time): The end time of the first time period.
            start2 (time): The start time of the second time period.
            end2 (datetime): The end time of the second time period.

        Returns:
            float: The number of hours of overlap between the two time periods.
        """
        overlap_start = datetime.combine(datetime.min, max(start1, start2))
        overlap_end = datetime.combine(datetime.min, min(end1, end2))
        overlap = (overlap_end - overlap_start).total_seconds() / 3600.0
        return max(0, overlap)

    def _get_day_payments(self, day: WorkDay, time_slots: list) -> float:
        """
        Calculates the payment for a work day based on its time slots.

        Args:
            day (WorkDay): A WorkDay object representing the work day to be calculated.
            time_slots (List[TimeSlot]): A list of TimeSlot dataclasses representing
                the time slots for the day.

        Returns:
            float: The payment for the work day based on its time slots.
        """
        day_payment = 0.0
        for time_slot in time_slots:
            overlap = self._calculate_overlap(
                day.start, day.end, time_slot.start, time_slot.end
            )
            day_payment += round(overlap) * time_slot.rate
        return day_payment

    def calculate_payment(self, work_history: WorkHistory) -> float:
        """
        Calculates the payment for an employee based on their work history and payment schedule.

        Args:
            work_history (WorkHistory): A WorkHistory object with the work history of an employee.

        Returns:
            float: The payment for the employee based on their work history and payment schedule.
        """
        day_payments = []
        for work_day in work_history.schedule:
            time_slots = self.payment_schedule.get(work_day.day)
            if time_slots is None:
                raise ValueError(
                    f"Failed to get payement configuration for {work_day.day}"
                )
            day_payments.append(self._get_day_payments(work_day, time_slots))

        return sum(day_payments)

    def __str__(self):
        return str(self.__dict__)
