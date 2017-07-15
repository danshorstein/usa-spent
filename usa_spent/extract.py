from usa_spent.usa_params import PostParams
from usa_spent.usaspending_api import UsaSpendingService


# TODO - add error reporting and handling when usaspending API has issues

def main():
    fields = ['contract_data', 'federal_action_obligation']

    usa = UsaSpendingService()

    filter_ = PostParams.filter_

    params = PostParams(
            # fields=fields,
            filters=[
                filter_('awarding_agency__toptier_agency__cgac_code',
                        'equals',
                        '070'),
                filter_('action_date',
                        'less_than_or_equal',
                        '2017-03-15'),
                filter_('action_date',
                        'greater_than_or_equal',
                        '2017-03-01')
            ],
        )

    endpoint = '/api/v1/transactions/'

    usa.search(endpoint=endpoint, params=params.params)

    usa.save_to_csv(r'C:\Users\dshorstein\Python\Projects\usa-spent\data\output.csv')

if __name__ == '__main__':
    main()