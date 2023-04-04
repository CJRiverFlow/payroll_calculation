"""
This module contains all the data classes used in the Payroll package.
"""
from dataclasses import dataclass
from typing import List, Dict
from datetime import time


@dataclass
class WorkDay:
    """
    Represents a work schedule for a single day.

    Attributes:
    day(str): The abbreviated day of the week (e.g. 'MO', 'TU', etc.).
    start(time): The time the work shift starts.
    en(time): The time the work shift ends.
    """

    day: str
    start: time
    end: time


@dataclass
class WorkHistory:
    """
    Represents an employee's work history, including the name of the employee
    and their daily work schedule.

    Attributes:
    nam(str): The name of the employee.
    schedule(List[DaySchedule]: A list of `DaySchedule` objects representing
        the employee's daily work schedule.
    """

    name: str
    schedule: List[WorkDay]


@dataclass
class TimeSlot:
    """
    A time slot during which work was performed and the corresponding hourly rate.

    Attributes:
    start(time): The start time(HH:MM) of the time slot.
    end(time): The end time(HH:MM) of the time slot.
    rate(float): The hourly rate(USD) for work performed during the time slot.
    """

    start: time
    end: time
    rate: float


@dataclass
class Period:
    """
    Represents a period of time during which an employee works, consisting of one or
    more time slots on specific days of the week.

    Attributes:
    days(List[str]): A list of abbreviated weekdays on which the employee works,
        e.g. ["MO", "TU", "WE"].
    time_slots(List[TimeSlot]): A list of TimeSlot objects representing the start
        and end times of each work period.
    """

    days: List[str]
    time_slots: List[TimeSlot]


@dataclass
class PaymentSchedule:
    """
    A dataclass representing a payment schedule for employees.

    Attributes:
    name(str): A string representing the name of the payment schedule.
    periods(List[Period]): A list of Period dataclasses representing the periods of
        time during which the employee is expected to work.
    """

    name: str
    periods: List[Period]

    def to_time_slots(self) -> Dict[str, TimeSlot]:
        """
        Returns a dictionary where each key is a day of the week
        and the value is a list of TimeSlot dataclasses representing
        the time slots for that day.
        """
        day_to_time_dict = {}
        for period in self.periods:
            for day in period.days:
                time_slots = day_to_time_dict.setdefault(day, [])
                time_slots.extend(period.time_slots)
        return day_to_time_dict
