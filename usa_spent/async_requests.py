import asyncio

from aiohttp import ClientSession


class AsyncGet:
    def __init__(self, url):
        self.url = url
        self.request_type = 'GET'


class AsyncPost:
    def __init__(self, url, payload, headers):
        self.url = url
        self.payload = payload
        self.headers = headers
        self.request_type = 'POST'


class AsyncResponses:
    def __init__(self, request_items):
        self.response = None
        self.request_items = list(request_items)
        self.print_status = False

    def _reset(self):
        self.response = None

    async def _fetch(self, request_obj, session):
        if self.print_status:
            print('Request for {}'.format(request_obj.url))

        if request_obj.request_type == 'GET':
            async with session.get(request_obj.url) as response:
                return await response.text()
        else:
            async with session.post(url=request_obj.url, data=request_obj.payload,
                                    headers=request_obj.headers) as response:
                return await response.text()

    async def _run(self):

        tasks = []
        async with ClientSession() as session:

            for request_obj in self.request_items:
                task = asyncio.ensure_future(self._fetch(request_obj, session))
                tasks.append(task)

            request_resp = await asyncio.gather(*tasks)
            self.response = request_resp

    def async_run(self):
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(self._run())
        loop.run_until_complete(future)

if __name__ == '__main__':
    urls = ['https://api.usaspending.gov/api/v1/accounts/awards/?page={}',
            'https://api.usaspending.gov/api/v1/federal_accounts/?page={}',
            'https://api.usaspending.gov/api/v1/transactions/?page={}',
            'https://api.usaspending.gov/api/v1/tas/balances/?page={}',
            'https://api.usaspending.gov/api/v1/tas/categories/?page={}']

    urls = [url.format(n) for n in range(1, 5) for url in urls]

    urls_async = [AsyncGet(url) for url in urls]

    async_request = AsyncResponses(urls_async)
    async_request.async_run()

    results = zip(urls, async_request.response)

    for item in results:
        print(item[0])
        print(item[1][:500])