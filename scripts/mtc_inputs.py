
# create mtc tm1 asim example data
# Ben Stabler, ben.stabler@rsginc.com, 01/24/19
# run from the mtc tm1 skims folder

import sys
import os
import pandas as pd

# currently hdf5 written with python3 works with both p2.7 and p3,
# but reading hdf5 built with p2.7 (tables==3.4.4) p3 throws a ValueError reading land_use_taz:
# ValueError: Buffer dtype mismatch, expected 'Python object' but got 'double'
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

col_map = {
    "HHID": "household_id",
    #"AGE": "age",
    #"SEX": "sex",
    "hworkers": "WIF",
    "HINC": "HHINCADJ",
    "AREATYPE": "area_type",
    "PERID": "per_num"
}

source_data_dir = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/data"
store_path = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/data/syth_plus_se.h5"

input_files = {
    "land_use_taz": {'filename': "SE_Data.csv", 'index_col': 'ZONE'},
    "households": {'filename': "synthetic_households.csv", 'index_col': 'household_id'},
    "persons": {'filename': "synthetic_persons.csv", 'index_col': 'perid'}
    }

print("writing store {}".format(store_path))

store = pd.HDFStore(store_path, "w")

for table_name, info in input_files.items():

    file_path = os.path.join(source_data_dir, info['filename'])
    print("reading {}".format(file_path))
    df = pd.read_csv(file_path, dtype={info['index_col']: int})

    print("df.dtypes", df.dtypes)
    print(df[info['index_col']].head())
    print(df[info['index_col']].tail())
    df.set_index(info['index_col'], inplace=True, verify_integrity=True, drop=True)
    df.columns = [col_map.get(s, s) for s in df.columns]
    store[table_name] = df
