#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Author: Drew An-Pham, Jeff Howarth
# Last Edited: 3 December 2021
# Purpose: To visualize the present conditions of wetlands in Middlebury
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

## import tools from WBT module

import sys
sys.path.insert(0, '/Users/jhowarth/tools')
from WBT.whitebox_tools import WhiteboxTools

## declare a name for the tools

wbt = WhiteboxTools()

# This directory will change, based on where you run your Whitebox Tools from
wbt.work_dir = "/Volumes/LaCie/GEOG0310/data/hWetlands"

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Introducing Our Data & Distinguishing Each Wetlands Layers #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Pull in data used for this analysis
advisory = "/Volumes/LaCie/GEOG0310/data/midd/wetlands/iWetAdvisory_12272021.tif"
arrow = "/Volumes/LaCie/GEOG0310/data/midd/wetlands/iWetArrow_12272021.tif"
_class = "/Volumes/LaCie/GEOG0310/data/midd/wetlands/iWetClass_12272021.tif"
hydSoils = "/Volumes/LaCie/GEOG0310/data/midd/wetlands/iHydricSoils_12272021.tif"


'''
0: N
1: U - Uncertain?
2: Y
3: water
'''

# Reclass advisory layer to distinguish layer in final composite
wbt.reclass(
    i = advisory,
    output = "01_advisory_reclass.tif",
    reclass_vals = "0;0;10;1",
    assign_mode = True
)

# Reclass arrowwood layer to distinguish layer in final composite
wbt.reclass(
    i = arrow,
    output = "02_arrow_reclass.tif",
    reclass_vals = "0;0;100;1",
    assign_mode = True
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Creating Our Initial Wetlands Layer Composite #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Add the advisory and arrowwood layers together
wbt.add(
    input1 = "01_advisory_reclass.tif",
    input2 = "02_arrow_reclass.tif",
    output = "03_advisory_arrow.tif"
)

# Create a wetland composite of all 3 layers
wbt.add(
    input1 = _class,
    input2 = "03_advisory_arrow.tif",
    output = "04_allWetlands.tif"
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Using Hydric Soils to Increase Confidence #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Create a hydric soils binary
wbt.reclass(
    i = hydSoils,
    output = "05_hydSoils_reclass.tif",
    reclass_vals = "0;0;0;1;2;2;0;3",
    assign_mode = True
)

# Create a wetland composite of all 3 layers w/ hydric soils
wbt.add(
    input1 = "04_allWetlands.tif",
    input2 = "05_hydSoils_reclass.tif",
    output = "06_allWetlands_withHydric.tif"
)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
# Visualize Levels of Certainty #
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# Reclass wetland composite to form levels of certainty
wbt.reclass(
    i = "06_allWetlands_withHydric.tif",
    output = "07_allWetlands_reclassed.tif",
    reclass_vals = "0;0;4;1;0;2;4;3;1;10;4;11;2;12;4;13;1;100;4;101;2;102;4;103;3;110;4;111;3;112;4;113",
    assign_mode = True
)
