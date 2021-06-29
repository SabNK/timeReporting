import client_1c_timesheet.models as m1c
import clockifyclient.models as mc
from datetime import datetime

from trsetup import *
from trutils import *
import calendar

TAGS = ["_Я", "_К"]


class Worker:
    def __init__(self, user: mc.User, employee: m1c.Employee):
        self.user = user
        self.employee = employee


def main_work():
    # Collect general data from Clockify
    users = api_session.get_users(workspace=WORKSPACE)
    tags = api_session.get_tags(workspace=WORKSPACE)
    users = [user for user in users if user.name == "SabNK"]
    start, end = month_start_end_datetime(month_in_RP)
    time_group_dict = {k: v for k in TAGS for v in api_session_1C.get_time_groups() if k[1:] == v.letter}
    employees = api_session_1C.get_employees()
    employees = [employee for employee in employees if employee.name.startswith("Боширов")]
    workers = [Worker(user, employee) for user, employee in zip(users, employees)]
    #workers = [Worker(user, employee) for user in users for employee in employees if user.name == employee.name]
    time_sheet = m1c.TimeSheet(uuid_str(), start.date(), m1c.APIObjectID("a2edb898-b4db-11eb-7297-000c298d5e5b"),
                               start.date(), end.date(), [])
    time_sheet_line_number = 0
    for worker in workers:
        time_entries = api_session.get_time_entries(WORKSPACE, worker.user, start, end)
        time_entries = api_session.api.substitute_api_id_entities(time_entries=time_entries, tags=tags)
        print(tags[0].name)
        print(time_entries[0].tags[0])
        end_of_month = calendar.monthrange(2021, month_in_RP)[1]
        for tag_str in TAGS:
            time_sheet_line_number += 1
            ts_line = m1c.TimeSheetLine(uuid_str(), time_sheet_line_number, worker.employee, [])
            for day in range(1, end_of_month + 1):

                elapsed_timedelta = sum(
                    [time_entry.end - time_entry.start for time_entry in time_entries
                     if time_entry.start.day == day and tag_str in [tag.name for tag in time_entry.tags]],
                    timedelta())
                hours = format_timedelta_hh(elapsed_timedelta)
                if hours > 0.1:
                    ts_record = m1c.TimeSheetRecord(day=day,
                                                    hours=hours,
                                                    time_group=time_group_dict[tag_str],
                                                    territory=m1c.APIObjectID("00000000-0000-0000-0000-000000000000"),
                                                    working_conditions=m1c.APIObjectID("00000000-0000-0000-0000-000000000000"),
                                                    work_shift=False)
                    ts_line.time_sheet_records.append(ts_record)
            time_sheet.time_sheet_lines.append(ts_line)
    new_time_sheet = api_session_1C.add_time_sheet(time_sheet)
    with open("../res/output_filename", 'w', encoding='utf-8') as outfile:
        json.dump(time_sheet.to_dict(),
                  outfile,
                  ensure_ascii=False,
                  sort_keys=False,
                  indent=4,
                  separators=(',', ': ')
                  )
main_work()


