from datetime import datetime

from six.moves import zip

class Grabber(object):
    def __init__(self, authorized_service):
        """A ``Grabber`` object stores authetication information, and provides
        a convenient interface to query data from google analytics.
        
        :type authroized_service: service_account_auth.AuthorizedService
        :param authorized_service: An AuthorizedService object, 
             authorized for the 'analytics' service, version 'v3'.
        """
        self.project_id = authorized_service.project_id
        self.service = authorized_service.service

    def query(self, view, dimensions, metrics, start_date, end_date, **kwargs):
        """Run a query on the account's Google Analytics data.

        Required Arguments:

            view - the integer id representing the view to be
            queried. This can be found in the Google Analytics admin
            section "View Settings"

            dimensions - a list of dimensions to aggregate
            on. E.g. ['operatingSystem', 'dimension1']

            metrics - a list of the names ometrics to be included in
            the query. E.g. ['pageviews', 'timeOnPage']

            start_date - a datetime for the start of the query.

            end_date - a datetime for the end of the query.

        **kwargs:

            - Any additional query parameter can be passed in to the
            key word argument of this this function. These will not be
            automatically converted from python datatypes into
            appropriate google syntax. These should only be passed if
            you know what yo're doing.

        Returns:

            - data a list of dictionaries mapping the requested
            dimension/metric to its value for each row.

        """
        query_response = self._query_response(
            view, dimensions, metrics, start_date, end_date, **kwargs
        )
        data = data_from_query_response(query_response)
        return data

    def _query_response(self, view, dimensions, metrics, start_date, end_date, **kwargs):
        """Get the raw data for a query.
        """
        formatted_view = 'ga:' + str(view)
        formatted_dimensions = ','.join(['ga:' + dim for dim in dimensions])
        formatted_metrics = ','.join(['ga:' + metric for metric in metrics])
        formatted_start_date = datetime.strftime(start_date, '%Y-%m-%d')
        formatted_end_date = datetime.strftime(end_date, '%Y-%m-%d')
        query_response = self.service.data().ga().get(
            ids=formatted_view,
            dimensions=formatted_dimensions,
            metrics=formatted_metrics,
            start_date=formatted_start_date,
            end_date=formatted_end_date,
            **kwargs
        ).execute()
        return query_response


def data_from_query_response(query_response):
    """Format GA queries to a list of dicts.
    """
    convert = {
        'STRING': lambda x: x,
        'INTEGER': lambda x: int(x),
        'FLOAT': lambda x: float(x),
        'CURRENCY': lambda x: float(x),
        'TIME': lambda x: float(x),
        'PERCENT': lambda x: float(x)
    }
    headers = [h['name'].split(':')[1] for h in query_response['columnHeaders']]
    data_types = [h['dataType'] for h in query_response['columnHeaders']]
    rows = query_response['rows']
    data = []
    for row in rows:
        data_row = {}
        for header, data_type, value in zip(headers, data_types, row):
            data_row[header] = convert[data_type](value)
        data.append(data_row)
    return data
