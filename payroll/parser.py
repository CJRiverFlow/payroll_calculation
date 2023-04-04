"""
This module contains the InputParser class which is used to parse 
the input string containing work hostories for employees.
"""

import re
from datetime import datetime

from .data_classes import WorkHistory, WorkDay
from .constants import DAYS_OF_WEEK
from .errors import (
    InvalidInputFormatError,
    InvalidDayIntervalFormatError,
    InvalidDayAbbreviationError,
    InvalidTimeIntervalError,
)


class InputParser:
    """
    A class that parses a string input containing an employee's name and
    their work data,and returns a WorkHistory object containing their
    name and a list of DaySchedule objects representing their work schedule.

    Raises:
        PayrollError: If the input string is not in the correct format,
            or if the day abbreviation or time format in the schedule is invalid.

    Returns:
        WorkHistory: A WorkHistory object containing the employee's name
        and a list of DaySchedule objects representing their work schedule.
    """

    def parse(self, input_str: str) -> WorkHistory:
        """
        Parses the input string and returns a WorkHistory object containing
        the employee's name and a list of DaySchedule objects representing
        their work schedule.

        Args:
            input_str: An string where the employee's work data for a single week
                is expressed following the expected format.

        Raises:
            ValueError: If the input string is not in the correct format,
                or if the day abbreviation or time format in the schedule is invalid.

        Returns:
            WorkHistory: A WorkHistory object containing the employee's name
                and a list of DaySchedule objects representing their work schedule.
        """
        username, _, input_str = input_str.partition("=")

        if not username or not input_str:
            raise InvalidInputFormatError(f"Invalid input format: {input_str}")

        day_intervals = input_str.split(",")

        schedule = []

        for day_interval_str in day_intervals:
            match = re.match(
                r"^([A-Z]{2})(\d{2}:\d{2})-(\d{2}:\d{2})$", day_interval_str
            )

            if not match:
                raise InvalidDayIntervalFormatError(
                    f"Invalid day interval format: {day_interval_str}. "
                    f"Day intervals must be in the format DAY:START-END"
                )

            day, start_time_str, end_time_str = match.groups()

            if day not in DAYS_OF_WEEK:
                raise InvalidDayAbbreviationError(f"Invalid day abbreviation: {day}")

            start_time = datetime.strptime(start_time_str, "%H:%M").time()
            end_time = datetime.strptime(end_time_str, "%H:%M").time()

            start_dt = datetime.combine(datetime.today(), start_time)
            end_dt = datetime.combine(datetime.today(), end_time)

            if end_dt <= start_dt:
                raise InvalidTimeIntervalError(
                    f"End time must be after start time for day interval {day_interval_str}"
                )

            schedule.append(WorkDay(day=day, start=start_time, end=end_time))

        return WorkHistory(name=username, schedule=schedule)

    def __str__(self) -> str:
        return str(self.__dict__)
