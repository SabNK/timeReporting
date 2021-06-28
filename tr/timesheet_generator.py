import client_1c_timesheet.models as c1c
import clockifyclient.models as cc
from datetime import datetime

from trsetup import *
from trutils import *
import calendar

TAGS = ["_Я", "_К"]


class Worker:
    def __init__(self, user: clockifyclient.models.User, employee: client_1c_timesheet.models.Employee):
        self.user = user
        self.employee = employee


def main_work():
    # Collect general data from Clockify
    users = api_session.get_users(workspace=WORKSPACE)
    users = [user for user in users if user.name == "SabNK"]
    start, end = month_start_end_datetime(month_in_RP)
    time_group_dict = {k: v for k in TAGS for v in api_session_1C.get_time_groups() if k == v.name}
    employees = api_session_1C.get_employees()
    employees = [employee for employee in employees if employee.name.startswith() == "Боширов"]
    workers = [Worker(user, employee) for user in users for employee in employees if user.name == employee.name]
    time_sheet = c1c.TimeSheet(uuid_str(), start, c1c.APIObjectID("a2edb898-b4db-11eb-7297-000c298d5e5b"), start.date(),
                               end.date(), [])
    time_sheet_line_number = 0
    for worker in workers:
        time_sheet_line_number += 1
        time_entries = api_session.get_time_entries(WORKSPACE, worker.user, start, end)
        end_of_month = calendar.monthrange(2021, month_in_RP)[1]
        for tag in TAGS:
            ts_line = c1c.TimeSheetLine(uuid_str(), time_sheet_line_number, worker.employee, [])
            for day in range(1, end_of_month + 1):

                elapsed_timedelta = sum(
                    [time_entry.end - time_entry.start for time_entry in time_entries
                     if time_entry.start.day == day and time_entry.tag == tag],
                    timedelta())
                hours = format_timedelta_hh(elapsed_timedelta)
                ts_record = c1c.TimeSheetRecord(hours, time_group_dict[tag], )



