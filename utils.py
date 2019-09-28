client_id = '1063016171261-3m0ntr3asvduesaail3o4qh35kq8dc5e.apps.googleusercontent.com'
client_secret= '1Iq9izwrNSrH3ASq5zAQmBPt'
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
access_code = '4/igElgTbVX0AEwotwcMC-3jB0haCNjAeIrNgSZxWpv6DXVk21ziI_C8Q'
access_token = 'ya29.GltJB_64t5BuEef6aL25xprUf8Za7DXIIBAKBWvd5fQvI6AVkiYDQo6ZFrl7A_MEPCgn3S3R5tcpJXifAvPDNYOMYA6iUITKY5fEBb6CiIuX1Do3oBsya7W-Fp1B'
refresh_token = '1/a3fH-ISLUlVyz115g7Kp2REoPt0s-KqHUoxKv0vr18g'

from .models import Langing
from oauth2client.client import OAuth2WebServerFlow, GoogleCredentials
import httplib2
from googleapiclient.discovery import build
import datetime
import pandas as pd



def return_ga_data(start_date, end_date, view_id, metrics, dimensions,service):
    return print_response(get_report(service, start_date, end_date, view_id, metrics, dimensions))

def get_report(analytics, start_date, end_date, view_id, metrics, dimensions):
    return analytics.reports().batchGet(
        body={
            'reportRequests': [
                {'viewId': '129196190', "pageSize": "1000000000",
                 'dateRanges': [{'startDate': start_date, 'endDate': end_date}], 'metrics': metrics,
                 'dimensions': dimensions}]
        },
    ).execute()

def print_response(response):
    list = []
    # get report data
    for report in response.get('reports', []):
        # set column headers
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])
        rows = report.get('data', {}).get('rows', [])

        for row in rows:
            # create dict for each row
            dict = {}
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            # fill dict with dimension header (key) and dimension value (value)
            for header, dimension in zip(dimensionHeaders, dimensions):
                dict[header] = dimension

            # fill dict with metric header (key) and metric value (value)
            for i, values in enumerate(dateRangeValues):
                for metric, value in zip(metricHeaders, values.get('values')):
                    # set int as int, float a float
                    if ',' in value or '.' in value:
                        dict[metric.get('name')] = float(value)
                    else:
                        dict[metric.get('name')] = int(value)
            list.append(dict)
    df = pd.DataFrame(list)
    return df
def main():
    landing = Langing.objects.all()



    credentials = GoogleCredentials(access_token, client_id, client_secret, refresh_token, 3920,
                                    'https://accounts.google.com/o/oauth2/token', 'test')
    http = httplib2.Http()
    http = credentials.authorize(http)
    service = build('analytics', 'v4', http=http, cache_discovery=False,
                    discoveryServiceUrl='https://analyticsreporting.googleapis.com/$discovery/rest?version=v4')
    print(service)
    start = str(landing[0].start)
    stop = str(landing[0].end)
    if datetime.date(int(stop[:4]), int(stop[5:7]), int(stop[8:10]))>datetime.datetime.now().date():
        stop=str(datetime.datetime.now().date())
    else:
        pass
    print('!!!!!!')
    print(start)
    print(type(start))
    print(stop)
    print(type(stop))
    df = return_ga_data(
        start_date=start,
        end_date=stop,
        view_id='129196190',
        metrics=[{"expression": "ga:uniquePageviews"}, ],
        dimensions=[{'name': 'ga:pagePath'}, {'name': 'ga:sourceMedium'}, ],
        service=service,
    )
