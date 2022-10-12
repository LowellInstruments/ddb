import glob
from populate_db import *
from datetime import datetime


FOLDER_VALUES = 'Bottom_Temperature'
MASK_FILES_VALUES = 'BT*.csv'
OUTPUT_DATABASE_FILE = 'bt.db'
OUTPUT_DATABASE_TABLE = 'BT'
db = OUTPUT_DATABASE_FILE
t = OUTPUT_DATABASE_TABLE


def main_erase():
    print('\nrunning main_erase()')
    table_delete(db, t)


def main_write():
    print('\nrunning main_write()')

    # so we don't create duplicates
    main_erase()

    # get today's number of day in year
    ndy = datetime.now().timetuple().tm_yday
    print('today is day # {} of the year'.format(ndy))

    table_create(db, t)

    wildcard = '{}/{}'.format(FOLDER_VALUES, MASK_FILES_VALUES)
    all_data_files = glob.glob(wildcard)
    s = 'found {} files in folder {}'
    print(s.format(len(all_data_files), FOLDER_VALUES))
    for every_df in all_data_files:
        put_data_file_to_table(db, t, every_df)

    # displays (index, day, lat, lon, value)
    # table_display(db, t)


def main_read():
    print('\nrunning main_read()')
    day = 37
    lat = 36.8
    lon = -74.9

    # ex: retrieve day #37 (36.8,-74.9) value 8.8211
    table_query(db, t, day, lat, lon)


if __name__ == '__main__':
    main_write()
    main_read()
