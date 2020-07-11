# ActivitySim
# Copyright (C) 2016 RSG Inc
# See full license in LICENSE.txt.
# run from the mtc tm1 skims folder

import os
import sys

import pandas as pd
import openmatrix as omx


def read_manifest(manifest_file_name):
    """
    Read CSV file with information on the type and location of skims.
    Parameters
    ----------
    manifest_file_name

    Returns
    -------
    manifest dictionary
    """

    column_map = {
        'Token': 'skim_key1',
        'TimePeriod': 'skim_key2',
        'File': 'source_file_name',
        'Matrix': 'source_key',
    }
    converters = {
        col: str for col in column_map.keys()
    }

    manifest = pd.read_csv(manifest_file_name, header=0, comment='#', converters=converters)

    manifest.rename(columns=column_map, inplace=True)

    return manifest


def omx_getMatrix(omx_file_name, omx_key):

    with omx.open_file(omx_file_name) as omx_file:

        #if omx_key not in omx_file.list_matrices():
        #    print "Source matrix with key '%s' not found in file  % (omx_key, omx_file)"
        #    print omx_file.list_matrices()
        #    raise RuntimeError("Source matrix with key '%s' not found in file '%s'
        #                       % (omx_key, omx_file))

        data = omx_file[omx_key]

    return data

def compile_omx_files(manifest, dest_file_name, source_data_dir):
    with omx.open_file(dest_file_name, 'a') as dest_omx:

        for row in manifest.itertuples(index=True):

            source_file_name = os.path.join(source_data_dir, row.source_file_name)

            if row.skim_key2:
                dest_key = row.skim_key1 + '__' + row.skim_key2
            else:
                dest_key = row.skim_key1

            print ("Reading '%s' from '%s' in %s' % (dest_key, row.source_key, source_file_name)")
            with omx.open_file(source_file_name, 'r') as source_omx:

                if row.source_key not in source_omx.list_matrices():
                    print("Source matrix with key '%s' not found in file '%s'" % (row.source_key, source_file_name,))
                    print(source_omx.list_matrices())
                    raise RuntimeError("Source matrix with key '%s' not found in file '%s'" % (row.source_key, dest_omx))

                data = source_omx[row.source_key]

                if dest_key in dest_omx.list_matrices():
                    print("deleting existing dest key '%s'" % (dest_key,))
                    dest_omx.removeNode(dest_omx.root.data, dest_key)

                data = np.delete(data, np.r_[135:140, 420:422, 1781:1788, 2873:2881], axis = 0)
                data = np.delete(data, np.r_[135:140, 420:422, 1781:1788, 2873:2881], axis = 1)
                dest_omx[dest_key] = data


if __name__ == '__main__':
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
    manifest_file_name = sys.argv[0]
    dest_file_name = sys.argv[1]

    manifest_file_name = 'C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/setup/skims_manifest.csv'
    manifest = read_manifest(manifest_file_name)

    dest_file_name = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/scripts/skims_wfrc.omx"
    source_data_dir = "C:/projects/ActivitySim/activitysim-master/activitysim-master/WFRC/example/scripts"
