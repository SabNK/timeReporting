from datetime import *
# import pygsheets
from pygsheets import DataRange, Cell, Worksheet, authorize
from trsetup import *
from trutils import *
import calendar

def model_cell(wks: Worksheet, index: str) -> Cell:
    '''Prepare model_cell to apply to DataRange in main program'''
    cell = Cell(index)
    wks.unlink()
    cell.text_format['fontSize'] = 11
    cell.text_format['bold'] = True
    cell.borders = {'top': {'style': 'SOLID'}}
    wks.link()
    return cell


def main_work():
    client = authorize(service_file=CREDENTIALS_FILE)
    sh = client.open_by_key(REPORT_SPREADSHEET_ID)
    wks = sh.worksheet('id', '546411462')
    # ToDo year not today but the report target
    wks.update_value('A1', date.today().year)

    # Collect general data from Clockify
    users = api_session.get_users(workspace=WORKSPACE)
    users = [user for user in users if user.name == "AdyBB"]

    # TODO change using yield
    month_sunday = None  # for month in headers
    curr_line = DATA_LINE - 1
    date_column = 3 - 1
    lines_for_range_for_borders = []
    report_dict = {}
    m_cell = model_cell(wks, 'A1')

    start, end = month_start_end_datetime(month_in_RP)
    print ('start', start)
    print ('end', end)
    for day in datetime_range(start, end + timedelta(days=1)):
        wks.update_value((3, date_column+day.day), day.day)
    for user in users:
        curr_line += 1
        report_dict.update({user: []})
        report_dict[user] += [user.name, '']

        time_entries = api_session.get_time_entries(WORKSPACE, user, start, end)

        end_of_month = calendar.monthrange(2021, month_in_RP)[1]
        for day in range(1, end_of_month+1):
            date_column += 1
            elapsed_timedelta = sum(
                [time_entry.end - time_entry.start for time_entry in time_entries if time_entry.start.day == day],
                timedelta())
            report_dict[user] += [format_timedelta_hh(elapsed_timedelta)]

            #print(elapsed_timedelta)
    DataRange((DATA_LINE, PROJECT_COLUMN), (curr_line, date_column +1),
              wks).update_values([report_dict[x] for x in users])


main_work()
