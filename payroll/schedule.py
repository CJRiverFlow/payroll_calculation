"""
This module contains the payment schedule handler 
"""
import os
import json
from datetime import datetime, time

from .constants import DEFAULT_CONFIG_FILE
from .data_classes import PaymentSchedule, TimeSlot, Period
from .errors import PaymentScheduleNotFound


class ScheduleHandler:
    """
    A class that handles the configuration of payment schedules and provides
    methods to retrieve them as dataclasses.

    Returns:
        A PaymentSchedule dataclass representing the payment schedule.

    Raises:
        PaymentScheduleNotFound: If the payment schedule with the given name is not found.
    """

    def __init__(self):
        self.schedule_config = self._read_config()

    def _read_config(self):
        """
        Reads the payment schedules from the configuration file
        """
        module_path = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(module_path, DEFAULT_CONFIG_FILE)
        with open(json_path, "r", encoding="utf-8") as file:
            config_data = json.load(file)
            payment_schedules = config_data.get("payment_schedules")
            return payment_schedules

    def get_schedule(self, schedule_name: str) -> PaymentSchedule:
        """
        Retrieves a payment schedule as a PaymentSchedule dataclass.        
        """
        schedule_json = self.schedule_config.get(schedule_name)
        if not schedule_json:
            raise PaymentScheduleNotFound(f"Schedule '{schedule_name}' not found")

        periods = []
        for period_json in schedule_json.get("periods"):
            days = period_json.get("days")
            time_slots = []
            for time_slot_json in period_json.get("time_slots"):
                start = datetime.strptime(time_slot_json.get("start"), "%H:%M").time()
                end = datetime.strptime(time_slot_json.get("end"), "%H:%M").time()
                end = time(23, 59, 59) if end == time.min else end
                rate = time_slot_json.get("rate")
                time_slots.append(TimeSlot(start=start, end=end, rate=rate))
            periods.append(Period(days=days, time_slots=time_slots))

        return PaymentSchedule(name=schedule_name, periods=periods)

    def __str__(self):
        return str(self.__dict__)
