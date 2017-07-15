import json
import csv

from usa_spent.async_requests import AsyncPost, AsyncResponses


#TODO - write outputs in chunks to file, to reduce memory impact
#TODO - add error checks

class UsaSpendingService:
    def __init__(self):
        self.endpoints = None
        self.base_url = 'https://api.usaspending.gov'
        self.endpoint_fields = {}
        self.results = []
        self.result_keys = set([])

    def search(self, endpoint, params={}):
        url = self.base_url + endpoint

        chunk = 10
        start_page = 1

        headers = {'content-type': 'application/json'}

        print('Searching params: {}'.format(params))

        params['page'] = start_page
        params = json.dumps(params)

        while True:

            url_searches = []

            for page in range(start_page, start_page + chunk):
                params = json.loads(params)
                params['page'] = page
                params = json.dumps(params)
                url_searches.append(AsyncPost(url, payload=params, headers=headers))

            resp = AsyncResponses(url_searches)
            resp.async_run()
            for item in resp.response:
                item = json.loads(item)
                if item.get('message'):
                    print(item.get('message'))
                    continue

                print('Page {} | {}'.format(item['page_metadata']['page'], item['page_metadata']['current']))

            self.results.extend(self._flatten_json(json.loads(item)) for item in resp.response)

            try:
                if json.loads(resp.response[-1]).get('page_metadata').get('has_next_page'):
                    start_page += chunk
                else:
                    break

            except:
                print('error!', resp.response[-1])
                break

        flat_results = [result for page in self.results if page for result in page]

        self.results = flat_results

        print('Completed data pull! {} records found'.format(len(self.results)))

    def _flatten_json(self, json_data):
        data = []
        results = json_data.get('results')
        if not results:
            return None

        for record in results:
            record_data = {}
            for key, val in record.items():
                if not isinstance(val, dict):
                    record_data[key] = val
                else:
                    for subkey, subval in val.items():
                        if not isinstance(subval, dict):
                            record_data['{}__{}'.format(key, subkey)] = subval
                        else:
                            for subsubkey, subsubval in subval.items():
                                record_data['{}__{}__{}'.format(key, subkey, subsubkey)] = subsubval
            data.append(record_data)
            [self.result_keys.add(key) for key in record_data.keys()]

        return data

    def save_to_csv(self, fileloc):
        keys = sorted(self.result_keys)
        with open(fileloc, 'w', newline='', encoding="utf-8", errors='replace') as output_file:  #TODO - SAVE AS CHUNKS INSTEAD OF ALL AT ONCE
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(self.results)


# if __name__ == '__main__':
#     usa = UsaSpendingService()
#
#     params = {
#         'order': ["-federal_action_obligation"],
#         'filters': [{
#             'field': 'action_date',
#             'operation': 'greater_than_or_equal',
#             'value': ''
#
#         ]
#     }}
#
#     endpoint = '/api/v1/transactions/'
#     usa.search(endpoint)
