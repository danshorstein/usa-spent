import json
import csv

from async_requests import AsyncPost, AsyncResponses


#TODO - write outputs in chunks to file, to reduce memory impact
#TODO - add error checks

class UsaSpendingService:
    def __init__(self):
        self.endpoints = None
        self.base_url = 'https://api.usaspending.gov'
        self.endpoint_fields = {}
        self.results = []
        self.record_count = 0
        self.result_keys = []
        self.first_line = True

    def search(self, endpoint, fileloc, params={}):
        url = self.base_url + endpoint

        chunk = 10
        start_page = 1
        page_index = start_page

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

            # self.results = [self._flatten_json(json.loads(item)) for item in resp.response]

            self.results = [json.loads(item).get('results') for item in resp.response]

            pages_dict = {}
            for page in self.results:
                transactions = {}
                if page:
                    for item in page:
                        transactions[item["id"]] = item
                    pages_dict[("page-" + str(page_index))] = transactions
                    page_index += 1

            flat_results = [result for page in self.results if page for result in page]

            self.results = pages_dict

            self.save_raw_json(fileloc)

            # self.save_dict_to_csv(fileloc)

            self.record_count += len(self.results)

            try:
                if json.loads(resp.response[-1]).get('page_metadata').get('has_next_page'):
                    start_page += chunk
                else:
                    break

            except:
                print('error!', resp.response[-1])
                start_page += chunk

        print('Completed data pull! {} records found'.format(self.record_count))

    # def _flatten_json(self, json_data):
    #     data = []
    #     results = json_data.get('results')
    #     if not results:
    #         return None
    #
    #     for record in results:
    #         record_data = {}
    #         for key, val in record.items():
    #             if not isinstance(val, dict):
    #                 record_data[key] = val
    #             else:
    #                 for subkey, subval in val.items():
    #                     if not isinstance(subval, dict):
    #                         record_data['{}__{}'.format(key, subkey)] = subval
    #                     else:
    #                         for subsubkey, subsubval in subval.items():
    #                             record_data['{}__{}__{}'.format(key, subkey, subsubkey)] = subsubval
    #         data.append(record_data)
    #         [self.result_keys.append(key) for key in record_data.keys() if key not in self.result_keys]
    #
    #     return data

    #
    # # TODO - MAKE HEADER ONLY WRITTEN ONCE or NONE... and tack on new fields to end using SET; write separate csv file
    # def save_dict_to_csv(self, fileloc):
    #     keys = self.result_keys
    #     with open(fileloc, 'a+', newline='', encoding="utf-8", errors='replace') as output_file:
    #         dict_writer = csv.DictWriter(output_file, keys)
    #         if self.first_line:
    #             dict_writer.writeheader()
    #             self.first_line = False
    #         dict_writer.writerows(self.results)

    def save_raw_json(self, fileloc):
        # This is a conventional way to append to json, but you could do a more hack-y approach if runtime suffers
        # Though realistically, network operations almost always dominate runtime
        with open(fileloc) as input_file:
            data = json.load(input_file)

        data.update(self.results)
        #for result in self.results:
        #    data.update(result)

        with open(fileloc, 'w') as output_file:
            json.dump(data, output_file)


            #print(self.results, output)
