import pandas as pd
import re

def main():


    fileloc = r'C:\Users\dshorstein\Python\Projects\usa-spent\data\output.csv'

    df = pd.read_csv(fileloc)

    df['TRANSACTION_TYPE'] = df.type.apply(get_transaction_type)


    # grouped = df[['type_description', 'TRANSACTION_TYPE', 'federal_action_obligation']].groupby(['TRANSACTION_TYPE', 'type_description']).sum()
    #
    # print(grouped)
    #
    # small_cols = ['federal_action_obligation', 'TRANSACTION_TYPE', 'contract_data__piid', 'assistance_data__fain', 'type', 'type_description', 'awarding_agency__toptier_agency__abbreviation', 'awarding_agency__subtier_agency__name', 'assistance_data__cfda__website_address', 'place_of_performance__state_name', 'place_of_performance__zip5', 'place_of_performance__state_code', 'place_of_performance__city_name', 'action_date', 'action_type', 'action_type_description', 'period_of_performance_current_end_date', 'period_of_performance_start_date', 'contract_data__naics', 'contract_data__naics_description', 'contract_data__product_or_service_code', 'description']
    #
    # small_df = df[small_cols]
    #
    # tp = small_df[df_search('toilet paper', small_df)]
    # grant_dollars = small_df[df_search('grant', small_df)].federal_action_obligation.sum()
    #
    # print(tp)
    # print(grant_dollars)


def get_transaction_type(char): # TODO - add one / two loan types
    if char.isalpha():
        return 'grant'
    elif char.isdigit():
        return 'contract'


def df_search(term, df):
    result = df.description.apply(lambda x: term in str(x).lower())
    return result


if __name__ == '__main__':
    main()