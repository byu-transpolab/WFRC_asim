from __future__ import print_function
import openmatrix as omx
import numpy as np
import fnmatch
import os
from pathlib import Path
import re
myfile=omx.open_file('skims_wfrc.omx')
print('attributes:', myfile.list_matrices()) 
