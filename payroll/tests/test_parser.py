"""
This file contains the tests for the payroll parser module
"""
from datetime import time
import pytest

from payroll.parser import InputParser
from payroll.data_classes import WorkHistory, WorkDay
from payroll.errors import (
    InvalidInputFormatError,
    InvalidDayIntervalFormatError,
    InvalidDayAbbreviationError,
    InvalidTimeIntervalError,
)


class TestInputParser:
    """
    Tests for InputParse class
    """

    @classmethod
    def setup_class(cls):
        """
        Test class initialization
        """
        cls.parser = InputParser()

    def test_parse_valid_input(self):
        """
        Test for valid input work history
        """
        input_str = "ALICE=MO10:00-12:00,TU10:00-12:00,WE10:00-12:00,TH10:00-12:00,FR10:00-12:00"
        expected_output = WorkHistory(
            name="ALICE",
            schedule=[
                WorkDay(day="MO", start=time(hour=10), end=time(hour=12)),
                WorkDay(day="TU", start=time(hour=10), end=time(hour=12)),
                WorkDay(day="WE", start=time(hour=10), end=time(hour=12)),
                WorkDay(day="TH", start=time(hour=10), end=time(hour=12)),
                WorkDay(day="FR", start=time(hour=10), end=time(hour=12)),
            ],
        )
        assert self.parser.parse(input_str) == expected_output

    def test_parse_invalid_input_format(self):
        """
        Test fo incomplete input case
        """
        input_str = "ALICE="
        with pytest.raises(InvalidInputFormatError):
            self.parser.parse(input_str)

    def test_parse_invalid_day_interval_format(self):
        """
        Test for incorrect day interval
        """
        input_str = "ALICE=MO10:00-12:00,WRONGFORMAT,TU10:00-12:00"
        with pytest.raises(InvalidDayIntervalFormatError):
            self.parser.parse(input_str)

    def test_parse_invalid_day_abbreviation(self):
        """
        Test for invalid day abbreviation
        """
        input_str = "ALICE=MO10:00-12:00,XX10:00-12:00"
        with pytest.raises(InvalidDayAbbreviationError):
            self.parser.parse(input_str)

    def test_parse_invalid_time_interval(self):
        """
        Test for incorrect time range or interval
        """
        input_str = "ALICE=MO10:00-09:00"
        with pytest.raises(InvalidTimeIntervalError):
            self.parser.parse(input_str)
