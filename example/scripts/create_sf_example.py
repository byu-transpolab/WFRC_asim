# ActivitySim
# See full license in LICENSE.txt.

import os

import numpy as np
import pandas as pd
import openmatrix as omx

import sys

# currently hdf5 written with python3 works with both p2.7 and p3,
# but reading hdf5 built with p2.7 (tables==3.4.4) p3 throws a ValueError reading land_use_taz:
# ValueError: Buffer dtype mismatch, expected 'Python object' but got 'double'
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")


# input files, SF county is zones 1 to 190, output files
source_store = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/data/synth_plus_se.h5"
source_skims = 'C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/data/skims_wfrc.omx'

dest_data_dir = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/data/subset"


def create_subset(dest_store, dest_skims, maxZone, households_sample_size=0):

    dest_store_path = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/data/subset/smallse.h5"
    dest_skims_path = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/data/subset/smallskims.omx"

    print('land_use_taz')
    df = pd.read_hdf(source_store, 'land_use_taz')
    df = df[df.index <= maxZone]
    df.to_hdf(dest_store_path, 'land_use_taz')
    del df

    print('households')
    hh_df = pd.read_hdf(source_store, 'households')
    hh_df = hh_df[hh_df.TAZ <= maxZone]
    if households_sample_size:
        hh_df = hh_df.take(np.random.choice(len(hh_df), size=households_sample_size, replace=False))
    hh_df.to_hdf(dest_store_path, 'households')

    print('persons')
    per_df = pd.read_hdf(source_store, 'persons')
    per_df = per_df[per_df.household_id.isin(hh_df.index)]
    per_df.to_hdf(dest_store_path, 'persons')

    # process all skims
    skims = omx.open_file(source_skims)
    skims_out = omx.open_file(dest_skims_path, 'w')

    skimsToProcess = skims.list_matrices()
    for skimName in skimsToProcess:
        print(skimName)
        skims_out[skimName] = skims[skimName][0:maxZone, 0:maxZone]
        skims_out[skimName].attrs.TITLE = ''  # remove funny character for OMX viewer


create_subset(dest_store='smallse.h5',
              dest_skims='smallskims.omx',
              maxZone=2000
              )

create_subset(dest_store='smallse.h5',
              dest_skims='smallskims.omx',
              maxZone=2000,
              households_sample_size=5000
              )
