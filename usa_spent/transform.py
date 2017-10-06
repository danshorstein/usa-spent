import pandas as pd
import re
import numpy as np

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


def get_transaction_type(row): # TODO - add one / two loan types
    if is_loan(row['type_description']):
        return 'loan'

    elif row.type.isalpha():
        return 'grant'
    elif row.type.isdigit():
        return 'contract'

def is_loan(decription):
    loan = 'loan'
    if loan in decription.lower():
        return True
    else:
        return False

def state_code(row):
    if row['place_of_performance__state_code'] != '':
        row['STATE_transform'] = row['place_of_performance__state_code']
    else:
        row['STATE_transform'] = row['place_of_performance__state_name']
    #row['STATE_transform'] = np.where(~row['place_of_performance__state_code'].isnull(), row['place_of_performance__state_code'],
     #                          row['place_of_performance__state_name'])
    if row['STATE_transform'] == row['place_of_performance__state_code']:
        return row['STATE_transform']
    elif row['STATE_transform'] == row['place_of_performance__state_name']:
        if 'alabama' in row['STATE_transform'].lower():
            return 'AL'
        elif 'alaska' in row['STATE_transform'].lower():
            return 'AK'
        elif 'arizona' in row['STATE_transform'].lower():
            return 'AZ'
        elif 'arkansas' in row['STATE_transform'].lower():
            return 'AR'
        elif 'california' in row['STATE_transform'].lower():
            return 'CA'
        elif 'colorado' in row['STATE_transform'].lower():
            return 'CO'
        elif 'connecticut' in row['STATE_transform'].lower():
            return 'CT'
        elif 'delaware' in row['STATE_transform'].lower():
            return 'DE'
        elif 'florida' in row['STATE_transform'].lower():
            return 'FL'
        elif 'georgia' in row['STATE_transform'].lower():
            return 'GA'
        elif 'hawaii' in row['STATE_transform'].lower():
            return 'HI'
        elif 'idaho' in row['STATE_transform'].lower():
            return 'ID'
        elif 'illinois' in row['STATE_transform'].lower():
            return 'IL'
        elif 'iowa' in row['STATE_transform'].lower():
            return 'IA'
        elif 'kansas' in row['STATE_transform'].lower():
            return 'KS'
        elif 'kentucky' in row['STATE_transform'].lower():
            return 'KY'
        elif 'louisiana' in row['STATE_transform'].lower():
            return 'LA'
        elif 'maine' in row['STATE_transform'].lower():
            return 'ME'
        elif 'maryland' in row['STATE_transform'].lower():
            return 'MD'
        elif 'massachusetts' in row['STATE_transform'].lower():
            return 'MA'
        elif 'michigan' in row['STATE_transform'].lower():
            return 'MI'
        elif 'minnesota' in row['STATE_transform'].lower():
            return 'MN'
        elif 'mississippi' in row['STATE_transform'].lower():
            return 'MS'
        elif 'missouri' in row['STATE_transform'].lower():
            return 'MO'
        elif 'montana' in row['STATE_transform'].lower():
            return 'MT'
        elif 'nebraska' in row['STATE_transform'].lower():
            return 'NE'
        elif 'nevada' in row['STATE_transform'].lower():
            return 'NV'
        elif 'new hampshire' in row['STATE_transform'].lower():
            return 'NH'
        elif 'new jersey' in row['STATE_transform'].lower():
            return 'NJ'
        elif 'new mexico' in row['STATE_transform'].lower():
            return 'NM'
        elif 'new york' in row['STATE_transform'].lower():
            return 'NY'
        elif 'north carolina' in row['STATE_transform'].lower():
            return 'NC'
        elif 'north dakota' in row['STATE_transform'].lower():
            return 'ND'
        elif 'ohio' in row['STATE_transform'].lower():
            return 'OH'
        elif 'oklahoma' in row['STATE_transform'].lower():
            return 'OK'
        elif 'oregon' in row['STATE_transform'].lower():
            return 'OR'
        elif 'pennsylvania' in row['STATE_transform'].lower():
            return 'PA'
        elif 'rhode island' in row['STATE_transform'].lower():
            return 'RI'
        elif 'south carolina' in row['STATE_transform'].lower():
            return 'SC'
        elif 'south dakota' in row['STATE_transform'].lower():
            return 'SD'
        elif 'tennessee' in row['STATE_transform'].lower():
            return 'TN'
        elif 'texas' in row['STATE_transform'].lower():
            return 'TX'
        elif 'utah' in row['STATE_transform'].lower():
            return 'UT'
        elif 'vermont' in row['STATE_transform'].lower():
            return 'VT'
        elif 'virginia' in row['STATE_transform'].lower():
            return 'VA'
        elif 'washington' in row['STATE_transform'].lower():
            return 'WA'
        elif 'west virginia' in row['STATE_transform'].lower():
            return 'WV'
        elif 'wisconsin' in row['STATE_transform'].lower():
            return 'WI'
        elif 'wyoming' in row['STATE_transform'].lower():
            return 'WY'
        elif 'guam' in row['STATE_transform'].lower():
            return 'GU'
        elif 'puerto rico' in row['STATE_transform'].lower():
            return 'PR'
        elif 'virgin islands' in row['STATE_transform'].lower():
            return 'VI'
    else:
        return row['STATE_transform']




def df_search(term, df):
    result = df.description.apply(lambda x: term in str(x).lower())
    return result


if __name__ == '__main__':
    main()
