import requests
import time
import json


endpoints = {
    'transactions': '/api/v1/download/transactions/'
}

baseurl = 'https://api.usaspending.gov'


def post_params(**parameters):
    return parameters


def filter_(**filter_params):
    return filter_params


def request_full_csv(endpoint, payload=None):

    headers = {'content-type': 'application/json'}

    url = baseurl + endpoint

    r = requests.post(url, headers=headers, data=payload)
    return r




if __name__ == '__main__':
    params = post_params(
        verbose=True,
        filters=[
            filter_(field='awarding_agency__toptier_agency__cgac_code',
                   operation='equals',
                   value='070'),
            filter_(field='action_date',
                    operation='equals',
                    value='2017-02-13')
        ]
    )

    endpoint = endpoints['transactions']

    r = request_full_csv(endpoint, json.dumps(params))

    print('Requested file for {} endpoint with parameters = {}'.format(endpoint, params))

    retry_url = r.json()['retry_url']

    elapsed = 0

    while r.status_code == 202:
        elapsed += 1
        time.sleep(1)
        r = requests.get(retry_url)
        print('Time elapsed = {} seconds. Status is "{}". Trying {} again.'.format(elapsed, r.json()['status'], r.url))


    if r.status_code == 200:
        print('success! csv file is located at {}'.format(r.json()['location']))

    else:
        print(r.status_code)