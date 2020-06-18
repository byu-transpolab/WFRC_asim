from __future__ import print_function
import openmatrix as omx
import numpy as np
import fnmatch
import os
from pathlib import Path
import re

skimsdir = Path.cwd()

matches = [filename for filename in os.listdir(skimsdir)
          if fnmatch.fnmatch(filename, "*.omx")]

print (matches)

for x in matches:
    myfile = omx.open_file(x, 'a')
    init = myfile['INITWAIT']
    xfer = myfile['XFERWAIT']
    combowait = np.add(init, xfer)
    myfile['INITWAIT+XFERWAIT'] = combowait
    num = re.sub("\D", "", x)
    time = myfile['T' + str(num)]
    drive = myfile['DRIVETIME']
    combotime = np.add(time, drive)
    myfile['T' + str(num) + '+DRIVETIME'] = combotime
    myfile.close()
