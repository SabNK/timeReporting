import os
import json
from clockifyclient.client import APISession
from clockifyclient.api import APIServer
import client_1c_timesheet.client as c1c
import client_1c_timesheet.api as a1c

def credentials():
    CREDENTIALS_FILE_1С = os.path.abspath('../res/1c.json')
    with open(CREDENTIALS_FILE_1С, 'r', encoding='utf-8') as task:
        setup_dict = json.load(task)
    return setup_dict


CLOCKIFY_SETUP_FILE = os.path.abspath('../res/report_setup.json')
with open(CLOCKIFY_SETUP_FILE, 'r', encoding='utf-8') as task:
    setup_dict = json.load(task)
api_key = setup_dict['api_key']
url = "https://api.clockify.me/api/v1/"
api_session = APISession(APIServer(url), api_key)
WORKSPACE = [ws for ws in api_session.get_workspaces() if ws.name == setup_dict['workspace_name']][0]
# TODO practice generator
CREDENTIALS_FILE = os.path.abspath('../res/' + setup_dict['google_credentials_file'])  # имя файла с закрытым ключом
REPORT_SPREADSHEET_ID = setup_dict['report_spreadsheet_id']
REPORT_SHEET_ID = setup_dict['report_sheet_id']
DATA_LINE = 4
PROJECT_COLUMN = 1
weeks_in_RP = [15]
month_in_RP = 7

api_session_1C = c1c.APISession(a1c.APIServer(credentials()['url']), (credentials()['user'], credentials()['password']))

