"""
This file contains the custo error classes for the payroll module
"""

class PayrollError(Exception):
    """Base class for payroll-related errors"""


class InvalidInputFormatError(PayrollError):
    """Raised when the input string is not in the expected format"""


class InvalidDayIntervalFormatError(PayrollError):
    """Raised when a day interval string is not in the expected format"""


class InvalidDayAbbreviationError(PayrollError):
    """Raised when a day abbreviation is not valid"""


class InvalidTimeIntervalError(PayrollError):
    """Raised when the end time is not after the start time"""


class PaymentScheduleNotFound(PayrollError):
    """Raised when the required payment schedule is not configured"""
