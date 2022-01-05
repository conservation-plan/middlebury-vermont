# -----------------------------------------------------------------------------
# TITLE:            ncCurrentConditions.py
# AUTHOR:           Will Ebby, Jeff Howarth
# LAST UPDATE:      12/22/21
# -----------------------------------------------------------------------------

## import tools from WBT module

import sys
sys.path.insert(0, '/Users/jhowarth/tools')
from WBT.whitebox_tools import WhiteboxTools

## declare a name for the tools

wbt = WhiteboxTools()

# Define the Whitebox working directory
#test Region
wbt.work_dir = "/Volumes/LaCie/GEOG0310/data/ncCurrent"

#total study site (Middlebury)
#wbt.work_dir = "/Volumes/EbbyEHD/GEOG310/wbt_pySpace-master/midd"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ncSoils = "/Volumes/LaCie/GEOG0310/data/midd/iNatCom_12222021.tif"
lc = "/Volumes/LaCie/GEOG0310/data/midd/iLandCover_midd_12152021.tif"


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 1: Distinguish agriculture and human landscaping from natural land cover
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wbt.reclass(
    i = lc,
    output = "01_lc_reclass.tif",
    reclass_vals = '1;0;1;1;2;2;3;3;4;4;6;5;6;6;5;7;6;8;6;9;6;10',   #new value;oldvalue
    assign_mode=True
)

# Result:
# 1 = tree canopy
# 2 = grass/shrublands
# 3 = water
# 4 = ag fields
# 5 = bare ground
# 6 = developed

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 2: Combine updated land cover with clayplain soils
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# distinguish natural communities

# Result:
# 0 : water
# 10: swamp forests
# 20: floodplain forests
# 30: wet valley clayplain forests
# 40: valley clayplain forests
# 50: northern hardwood forests
# 60: oak-pine northern hardwood forests
# 70: rocky
# 80: quarry

wbt.multiply(
    input1 = ncSoils,
    input2 = 10,
    output = "02_nc_multiply10.tif"
)


# add land cover and nc classes

wbt.add(
    input1 = "01_lc_reclass.tif",
    input2 = "02_nc_multiply10.tif",
    output = "03_lc_nc_classes.tif"
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 3: Compute area of historic soils and current land cover
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

wbt.raster_area(
    i = "02_nc_multiply10.tif",
    output="11_nc_area.tif",
    out_text=False,
    units="map units",
    zero_back=False
)

wbt.raster_area(
    i = "03_lc_nc_classes.tif",
    output="12_lc_nc_area.tif",
    out_text=False,
    units="map units",
    zero_back=False
)

wbt.divide(
    input1 = "12_lc_nc_area.tif",
    input2 = "11_nc_area.tif",
    output = "13_lc_nc_percents.tif"
)

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Part 4: Calculate amount of change (total number of pixels)
#   from historic clayplain forest (based on soils)
#   to current land cover classes
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


wbt.zonal_statistics(
    i = "13_lc_nc_percents.tif",
    features = "03_lc_nc_classes.tif",
    out_table= "_NC_table.html"
)
