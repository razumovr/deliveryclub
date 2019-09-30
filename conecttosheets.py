import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd
import os
import numpy as np
import re

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
    def __init__(self, service,sheetnumber):
        self.service = service
        self.sheetID = sheetnumber
        self.range = '{}!A1:AZ500000'
        self.names = []
        self.tables = []

    def getSheets(self):
        if self.service:
            sheets = self.service.spreadsheets().get(spreadsheetId=self.sheetID).execute()
            for sheet in sheets['sheets']:
                name = self.range.format(sheet['properties']['title'])
                table = self.service.spreadsheets().values().get(spreadsheetId=self.sheetID, range=name).execute()[
                    'values']
                self.names.append(sheet['properties']['title'])
                self.tables.append(table)

    def intoDF(self):
        data = []
        for table in self.tables:
            all_data = []
            for col_id, col_name in enumerate(table[0]):
                column_data = []
                for row in table[1:]:
                    column_data.append(row[col_id])
                ds = pd.Series(data=column_data, name=col_name)
                all_data.append(ds)
            df = pd.concat(all_data, axis=1)
            data.append(df)
        self.tables = data


def keyurl(sheetnumber):
    result = re.search(r'/{1}[^/].+/',sheetnumber)
    utm = result.group(0)
    indexslesh = []
    for i in range(len(utm)):
        if utm[i] == '/':
            indexslesh.append(i)
    utmforanalytics = utm[indexslesh[3] + 1:len(utm) - 1]
    return utmforanalytics


def connect(sheetnumber):
    gs = Connection()
    gs.connect()
    utm = UTMtable(gs.service,keyurl(sheetnumber))
    utm.getSheets()
    df = utm.tables
    for i in range(len(df[0])):
        if len(df[0][i]) < len(df[0][0]):
            while len(df[0][i]) != len(df[0][0]):
                df[0][i].append('')
        elif len(df[0][i]) > len(df[0][0]):
            df[0][i] = df[0][i][:len(df[0][0])]
        else:
            pass
    sheet = pd.DataFrame(np.array(df[0][1:]), columns=df[0][0])
    return sheet


def connectsheet(sheetnumber,datastart):
    gs = Connection()
    gs.connect()
    utm = UTMtable(gs.service,keyurl(sheetnumber))
    utm.getSheets()
    df = utm.tables[19]
    if datastart[:7] == '2019-05':
        df = utm.tables[16]
    elif datastart[:7] == '2019-06':
        df = utm.tables[17]
    elif datastart[:7]=='2019-07':
        df = utm.tables[18]
    elif datastart[:7]=='2019-08':
        pass
    elif datastart[:7]=='2019-09':
        df = utm.tables[20]
    elif datastart[:7]=='2019-10':
        df = utm.tables[21]
    elif datastart[:7]=='2019-11':
        df = utm.tables[22]
    elif datastart[:7]=='2019-12':
        df = utm.tables[23]
    elif datastart[:7]=='2020-01':
        df = utm.tables[24]
    elif datastart[:7]=='2020-02':
        df = utm.tables[25]
    elif datastart[:7]=='2020-03':
        df = utm.tables[26]
    #Poprevit nado so vremenem


    for i in range(len(df)):
        if len(df[i]) < len(df[0]):
            while len(df[i]) != len(df[0]):
                df[i].append('')
        elif len(df[i]) > len(df[0]):
            df[i] = df[i][:len(df[0])]
        else:
            pass
    sheet = pd.DataFrame(np.array(df[1:]), columns=df[0])
    return sheet





def connectIP(sheetnumber):
    gs = Connection()
    gs.connect()
    utm = UTMtable(gs.service,keyurl(sheetnumber))
    utm.getSheets()
    df = utm.tables[0]
    #Poprevit nado so vremenem

    for i in range(len(df)):
        if len(df[i]) < len(df[0]):
            while len(df[i]) != len(df[0]):
                df[i].append('')
        elif len(df[i]) > len(df[0]):
            df[i] = df[i][:len(df[0])]
        else:
            pass
    sheet = pd.DataFrame(np.array(df[1:]), columns=df[0])
    return sheet

if __name__ == '__main__':
    connect('https://docs.google.com/spreadsheets/d/1ION9tishR6WdGOqVHoWG_F9_iLc13YOndyCKtdnYoQo/edit#gid=1226535961')
