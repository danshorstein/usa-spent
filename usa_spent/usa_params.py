import requests


class PostParams:

    def __init__(self, **kwargs):
        self.params = {}
        for key, val in kwargs.items():
            self.params.update({key: val})

    @staticmethod
    def filter_(field, operation, value):
        return {'field': field, 'operation': operation, 'value': value}


if __name__=='__main__':
    filter_ = PostParams.filter_

    params = PostParams(
            page=1,
            filters=[
                filter_('awarding_agency__toptier_agency__cgac_code',
                        'equals',
                        '070'),
                filter_('action_date',
                        'equals',
                        '2017-02-13')
            ],
        )

    print(params.params)