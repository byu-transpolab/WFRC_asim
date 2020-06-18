
### Setup

This model uses ActivitySim, an open source activity-based model, skims and socioeconomic
data provided by the Wasatch Front Regional Council, and a synthetic population created
using PopulationSim, WFRC data, and US Census data. For more information, see the following
websites:

https://activitysim.github.io/

https://wfrc.org/

https://github.com/byu-transpolab/populationsim_wfrc

Some setup is required to get the skims and synthetic population in the format expected 
by ActivitySim. The necessary files to do this can be found in the /setup folder.

Configure skims:
1. Copy omx_convert.s into the WFRC 1a_Skims folder and run it using Cube
2. Move the transit skims and the add_matrices.py file into their own folder and run 
using Anaconda or Python
3. Put these updated transit skims and auto skims in the /example/scripts folder
4. Set the working directory as the /example folder, then run "python scripts/combine_omx.py"
using the asimtest conda environment created when installing ActivitySim
5. Copy the final skims_wfrc.omx file into /example/data

Configure synthetic population:
1. Copy the synthetic_persons.csv and synthetic_households.csv files produced by
PopulationSim into /example/data
2. Run /example/data_configs.r
