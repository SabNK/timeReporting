# TODO move to utils update doc
from datetime import *
import datetime
from dateutil import tz
import uuid

# TODO move TIME_ZONE to main user attribute? to ClockifyClient
# TODO get the TimeZone from Google Spreadshhet settings?
# Use https://developers.google.com/apps-script/reference/spreadsheet/spreadsheet#getspreadsheettimezone
# Set special file to get this. Use credentials
#
TIME_ZONE = tz.tzoffset('MSK', 10800)  # ('Europe/Moscow') https://www.epochconverter.com/timezones


class DateOutOfRangeException(Exception):
    pass


# TODO update doc, change to ValueException
def week_start_end_datetime(week_number, year=date.today().year):
    '''???'''
    if week_number > 54 or week_number < 1:
        raise DateOutOfRangeException('Week must from 1 to 54, but', week_number)
    if year > 9999 or year < 1:
        raise DateOutOfRangeException('Year must from 1 to 9999, but', year)
    d = "%04d" % (year,) + '-W' + str(week_number)
    tdelta = datetime.timedelta(days=7, microseconds=-1)
    start_datetime = datetime.datetime.strptime(d + '-1', '%G-W%V-%u')
    end_datetime = start_datetime + tdelta
    week_number = datetime.date.isocalendar(end_datetime)
    return (start_datetime, end_datetime)


# TODO update doc how to make docs in line
def format_timedelta_hhmm(td: timedelta) -> str:
    '''shows timedelta in hours and minutes only
    e.g.: 192:13 - 192 hours and 13 minutes
    ===========
    Parameters:
        td = period of time
    Return:
        str in hh:mm format where hh might be as big as needed e.g. 6934:55'''
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60) #td.total_seconds()
    hours, minutes = divmod(minutes, 60)
    return '{:d}:{:02d}'.format(hours, minutes)

# TODO update doc how to make docs in line
def format_timedelta_hh(td: timedelta) -> float:
    '''shows timedelta in hours * 10 only
    e.g.: 1925 = 192 hours  and 30 minutes
    ===========
    Parameters:
        td = period of time
    Return:
        int in hh*10 format where hh might be as big as needed e.g. 6934'''
    minutes, seconds = divmod(td.seconds + td.days * 86400, 60)
    return minutes/60



def month_start_end_datetime(month_number, year=date.today().year):
    """???"""
    if month_number > 12 or month_number < 1:
        raise DateOutOfRangeException('Month must from 1 to 12, but', month_number)
    if year > 9999 or year < 1:
        raise DateOutOfRangeException('Year must from 1 to 9999, but', year)
    start_datetime = datetime.datetime(year, month_number, 1)
    end_datetime = datetime.datetime(year, month_number + 1, 1) - datetime.timedelta(milliseconds=1)
    # end_datetime = calendar.monthrange(year, month_number)[1]
    # start_datetime = end_datetime.replace(day=1)
    return (start_datetime, end_datetime)


def datetime_range(start_datetime, end_datetime):
    for n in range(int((end_datetime - start_datetime).days)):
        yield start_datetime + timedelta(days=n)


def uuid_str() -> str:
    return str(uuid.uuid4())

"""
print(month_start_end_datetime(2, 2021))
print(week_start_end_datetime(16))


start_date = date(2013, 1, 1)
end_date = date(2015, 6, 2)
for single_date in datetime_range(month_start_end_datetime(2, 2021)[0], month_start_end_datetime(2, 2021)[1]+timedelta(days=1)):
    print(single_date)
    #.strftime("%Y-%m-%d"))"""

