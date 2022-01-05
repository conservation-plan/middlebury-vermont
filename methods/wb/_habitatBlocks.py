#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  name:     habitatBlocks.py
#  purpose:  to identify habitat blocks for conservation planning
#
#  author:   Jeff Howarth
#  update:   12/09/2021
#  license:  Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# import tools from WBT module

import sys
sys.path.insert(0, '/Users/jhowarth/tools')
from WBT.whitebox_tools import WhiteboxTools

# declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

# Full data
wbt.work_dir = "/Volumes/LaCie/GEOG0310/data/lForestBlocks"

# Test data
# wbt.work_dir = "/Users/jhowarth/projects/GEOG0310/wbt_pySpace/hb_test"

#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Full datasets

rds = "/Volumes/LaCie/GEOG0310/data/midd/rdsFragmenting_12092021.tif"        # Highways and Class 3 roads
lc = "/Volumes/LaCie/GEOG0310/data/midd/iLandCover_midd_12092021.tif"        # 2016 Vermont base land cover


# Test datasets

# rds = "rds_fragmenting.tif"       # Highways and Class 3 roads
# bb = "buildingsBuffer100ft.tif"   # 2016 building footprints with 100 ft buffer
# lc = "lc_5m.tif"                  # 2016 Vermont base land cover

hbb = 12.192      # 40 foot buffer to contain powerlines cuts and islands.
cr = False        # Clump rule (no diagonals)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 1:
# Create fragmentation layer from buildings and roads
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# buffer roads by 3 meters

wbt.buffer_raster(
    i = rds,
    output = "00_rds_buff3m.tif",
    size = 3,
    gridcells=False
)

# # Reclass impervious land cover (roads, buildings, bare ground, other pavement)
# # 5,6,7,8 --> 1
# # 0,1,2,3,4,9 --> 0
#
# wbt.reclass(
#     i = lc,
#     output = "00_lcImp.tif",
#     reclass_vals = "0;0;0;1;0;2;0;3;0;4;1;5;1;6;1;7;1;8;0;9",
#     assign_mode=True
# )
#
# wbt.add(
#     input1 = "00_rds_buff3m.tif",
#     input2 = "00_lcImp.tif",
#     output = "01_constraints.tif"
# )

# Make all constraints 0 and non constraints 1

wbt.reclass(
    i = "00_rds_buff3m.tif",
    output = "02_constraintsInverted.tif",
    reclass_vals = "1;0;0;1",
    assign_mode=True
)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 2:
# Isolate tree canopy and lump small strips (from powerlines)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Isolate tree canopy

wbt.reclass(
    i = lc,
    output = "11_treeCanopy.tif",
    reclass_vals = "1;0;1;1;0;2;0;3;0;4;0;5;0;6;0;7;0;8;0;9",
    assign_mode=True
)

wbt.majority_filter(
    i = "11_treeCanopy.tif",
    output = "12_treeCanopyFilter.tif",
    filterx=47,
    filtery=47
)

# # buffer out XX feet (to remove powerline cuts from forest)
#
# wbt.buffer_raster(
#     i = "11_treeCanopy.tif",
#     output = "12_treeCanopyBuffered.tif",
#     size = hbb,
#     gridcells=False
# )
#
# # invert the buffer
#
# wbt.reclass(
#     i = "12_treeCanopyBuffered.tif",
#     output = "13_tcbInvert.tif",
#     reclass_vals = "1;0;0;1",
#     assign_mode=True
# )
#
# # buffer back in
#
# wbt.buffer_raster(
#     i = "13_tcbInvert.tif",
#     output = "14_tcbInvertBuffered.tif",
#     size = hbb,
#     gridcells=False
# )
#
# # invert back
#
# wbt.reclass(
#     i = "14_tcbInvertBuffered.tif",
#     output = "15_treeCanopyGood.tif",
#     reclass_vals = "1;0;0;1",
#     assign_mode=True
# )

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# STEP 3:
# Fragment tree canopy and identify clumps > 10 acres
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Erase constraints from tree canopy clumps

wbt.multiply(
    input1 = "02_constraintsInverted.tif",
    input2 = "12_treeCanopyFilter.tif",
    output = "21_treesAfterConstraints.tif",
)

# Find contiguous regions of habitat

wbt.clump(
    i = "21_treesAfterConstraints.tif",
    output = "22_treeClumps.tif",
    diag=cr,
    zero_back=True
)

# Set zero as no data

wbt.set_nodata_value(
    i = "22_treeClumps.tif",
    output = "23_treeClumps_nd0.tif",
    back_value = 0,
)

# Compute area of each clump

wbt.raster_area(
    i = "23_treeClumps_nd0.tif",
    output= "24_treeClumpAreas.tif",
    out_text=False,
    units="map units",
    zero_back=True
)

wbt.divide(
    input1 = "24_treeClumpAreas.tif",
    input2 = 4046.86,
    output = "25_treeClumpAcres_47.tif"
)


#
# # threshold for habitat block > 20 acres
# # 10 acres = 40468.6 square meters
#
# wbt.reclass(
#     i = "23_treeClumpAreas.tif",
#     output = "24_treeGT20acres.tif",
#     reclass_vals = "0;0;80937;1;80937;999999999999999999999",
#     assign_mode=False
# )
#
# wbt.convert_nodata_to_zero(
#     i = "24_treeGT20acres.tif",
#     output = "25_bigTreeClumps_nd0.tif"
# )
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # STEP 4:
# # Fill holes within habitat blocks
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# # First invert big tree clump raster
#
# wbt.reclass(
#     i = "25_bigTreeClumps_nd0.tif",
#     output = "31_bigTreeClumps_invert.tif",
#     reclass_vals = "0;1;1;0",
#     assign_mode=True
# )
#
# # Identify clumps of unforested land
#
# wbt.clump(
#     i = "31_bigTreeClumps_invert.tif",
#     output = "32_holeClumps.tif",
#     diag=cr,
#     zero_back=True
# )
#
# # Compute area
#
# wbt.raster_area(
#     i = "32_holeClumps.tif",
#     output= "33_holeClumpAreas.tif",
#     out_text=False,
#     units="map units",
#     zero_back=True
# )
#
# # Reclass holes < 500 acres (2023428.2 square meters)
#
# wbt.reclass(
#     i = "33_holeClumpAreas.tif",
#     output = "34_holeLTacres.tif",
#     reclass_vals = "1;0;2023428.2;0;2023428.2;99999999999999999999999",
#     assign_mode=False
# )
#
# wbt.convert_nodata_to_zero(
#     i = "34_holeLTacres.tif",
#     output = "35_holeClumpAreas_nd0.tif"
# )
#
# # Reclass not fields
# # 0,1,2,3,5,6,7,8,9 --> not
# # 4 --> fields
#
# wbt.reclass(
#     i = lc,
#     output = "36_natLC.tif",
#     reclass_vals = "1;0;1;1;1;2;1;3;0;4;1;5;1;6;1;7;1;8;1;9",
#     assign_mode=True
# )
#
# ## Fill holes with natural cover
#
# wbt.multiply(
#     input1 = "35_holeClumpAreas_nd0.tif",
#     input2 = "36_natLC.tif",
#     output = "37_holesWithNatLC.tif",
# )
#
# ## Add filled holes to tree clumps
#
# wbt.add(
#     input1 = "25_bigTreeClumps_nd0.tif",
#     input2 = "37_holesWithNatLC.tif",
#     output = "38_block_holes_filled.tif"
# )
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# # STEP 5:
# # Identify discrete habitat blocks
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# ## Identify habitat blocks
#
# wbt.clump(
#     i = "38_block_holes_filled.tif",
#     output = "41_habitatBlocks.tif",
#     diag=cr,
#     zero_back=True
# )
#
# wbt.set_nodata_value(
#     i = "41_habitatBlocks.tif",
#     output = "_habitatBlocks_nd_15_20.tif",
#     back_value = 0,
# )
