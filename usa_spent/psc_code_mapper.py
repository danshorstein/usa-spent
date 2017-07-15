import os
import csv


def main():
    #TODO create or open mapping document - /data/psc_mapper.csv
    #TODO - fix the load and save to be NOT DictReader... instead port from pipe delimited to a dictionary
    fileloc = r'C:\Users\dshorstein\Python\Projects\usa-spent\data\mapper.csv'

    headers = ['psc', 'napcs_code']

    map_object = {'6515': '811', 'R499': '741010101'}

    save_mapper(fileloc, headers, map_object)



def save_mapper(fileloc, headers, mapper):
    rows = headers
    rows.extend([(key, val) for key, val in mapper.items()])
    with open(fileloc, 'w', newline='') as output_file:  # TODO - MAKE SEPARATOR PIPE DELIMITED
        writer = csv.writer(output_file, delimiter='|')
        writer.writerows(rows)


def load_mapper(fileloc):
    with open(fileloc, 'r', newline='') as input_file:
        reader = csv.reader(input_file, delimiter='|')
        headers = next(reader)
        mapper = dict(reader)

    return headers, mapper

if __name__ == '__main__':
    main()