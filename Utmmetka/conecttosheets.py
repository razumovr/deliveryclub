from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import re
from transliterate import translit
import datetime as dt


class Connection:
    def __init__(self):
        self.service = None

    def connect(self):
        scope = ['https://www.googleapis.com/auth/drive']
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', scope)
                creds = flow.run_local_server(port=0)
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        self.service = build('sheets', 'v4', credentials=creds)


class UTMtable:
    def __init__(self, service):
        self.service = service
        self.sheetID = '1irPfC1ZwRfW528NT-Tf9Zt-YuOMcdIZLZWGa17rs11c'
        self.range = '{}!A1:F50'
        self.names = []
        self.tables = dict()

    def getSheets(self):
        if self.service:
            sheets = self.service.spreadsheets().get(spreadsheetId=self.sheetID).execute()
            for sheet in sheets['sheets']:
                name = self.range.format(sheet['properties']['title'])
                table = self.service.spreadsheets().values().get(spreadsheetId=self.sheetID, range=name).execute()[
                    'values']
                self.names.append(sheet['properties']['title'])
                self.tables[sheet['properties']['title']] = table

    def intoDF(self):
        data = dict()
        for name, table in self.tables.items():
            all_data = []
            for col_id, col_name in enumerate(table[0]):
                column_data = []
                for row in table[1:]:
                    column_data.append(row[col_id])
                ds = pd.Series(data=column_data, name=col_name)
                all_data.append(ds)
            try:
                df = pd.concat(all_data, axis=1)
                data.update({name: df})
            except Exception:
                continue
        self.tables = data


class PSP:
    def __init__(self, service, url):
        self.service = service
        self.url = url
        self.sheetID = None
        self.makeID()

    def makeID(self):
        self.sheetID = re.findall(r'/d/\S+/', self.url)[0][3:-1]

    def appendData(self, name, utm):
        now = str(dt.datetime.now())
        if self.service:
            body = {
                'range': 'UTM!A4:C4',
                'majorDimension': 'ROWS',
                'values': [[name, utm, now]]
            }
            sheets = self.service.spreadsheets().values()
            inserted = sheets.append(spreadsheetId=self.sheetID, range='UTM!A4:C4',
                                     body=body, valueInputOption='USER_ENTERED').execute()


if __name__ == '__main__':
    gs = Connection()
    gs.connect()
    utm = UTMtable(gs.service)
    utm.getSheets()
    for i in utm.tables.keys():
        print(i)