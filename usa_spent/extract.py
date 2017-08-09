import os
from usa_spent.usa_params import PostParams
from usa_spent.usaspending_api import UsaSpendingService


def extract(start_date, ending_date, file_loc):

    # fields = ['contract_data', 'federal_action_obligation']

    endpoint = '/api/v1/transactions/'

    usa = UsaSpendingService()

    filter_ = PostParams.filter_

    params = PostParams(
            # fields=fields,
            filters=[
                # filter_('awarding_agency__toptier_agency__cgac_code',
                #         'equals',
                #         '070'),
                filter_('action_date',
                        'less_than_or_equal',
                        ending_date),
                filter_('action_date',
                        'greater_than_or_equal',
                        start_date)
            ],
        )

    usa.search(endpoint=endpoint, fileloc=file_loc, params=params.params)


if __name__ == '__main__':



    data_path = os.path.abspath(os.path.join(os.getcwd(), '..', 'data'))

    if not os.path.exists(data_path):
        os.mkdir(data_path)

    file_loc = os.path.join(data_path, 'output.csv')


    extract('2017-03-30', '2017-03-31', file_loc)
