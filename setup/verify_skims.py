from __future__ import print_function
import openmatrix as omx
import numpy as np
import fnmatch
import os
from pathlib import Path
import re
import pandas as pd
pd.set_option('display.max_rows', 1000)

skims = pd.read_csv("setup/skims_manifest.csv")
for key in skims['name']:
    mode = omx.open_file("example/data/skims_wfrc.omx", 'r')[key]
    mode = pd.DataFrame(mode)
    num_na = mode.isnull().sum().sum()
    print(key + "..." + str(num_na))