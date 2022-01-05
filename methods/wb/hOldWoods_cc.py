# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# name: hOldWoods_cc.py
# purpose: identify and visualize the current conditions of old forests in Middlebury

# author: Grayson Shanley Barr
# update: 11/29/2021

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


## import tools from WBT module

import sys
sys.path.insert(0, '/Users/jhowarth/tools')
from WBT.whitebox_tools import WhiteboxTools

## declare a name for the tools

wbt = WhiteboxTools()

# Set the Whitebox working directory
# You will need to change this to your local path name

wbt.work_dir = "/Volumes/LaCie/GEOG0310/data/hOldWoods"


#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Required datasets:
#  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

oldTrees = "/Volumes/LaCie/GEOG0310/data/midd/oldTreeCounts_12092021.tif"
landCover = "/Volumes/LaCie/GEOG0310/data/midd/iLandCover_midd_12152021.tif"


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Note: we implemented steps 1 - 2 with QGIS.
#   We implemented step 3 with Google Earth Engine.

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# STEP 4: Retain points of agreement
#   (where three observers identified tree canopy in 1942)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Covert nodata of old tree counts and tree cover binary to zero
wbt.convert_nodata_to_zero(
    i = oldTrees,
    output = "01_otCount_noDataZero.tif"
)

wbt.maximum_filter(
    i = "01_otCount_noDataZero.tif",
    output = "02_maxFilter.tif",
    filterx=9,
    filtery=9
)

# Reclassify old tree counts to only include areas where three students documented the presence of old trees from 1942 aerial imagery
wbt.reclass(
    i = "02_maxFilter.tif",
    output = "03_reclassify.tif",
    reclass_vals = "0;0;0;1;0;2;1;3",
    assign_mode=True
)

# Reclassify conifer trees to 10 and deciduous trees to 0
wbt.reclass(
    i = landCover,
    output = "04_trees_reclassify.tif",
    reclass_vals = "10;0;2;0;2;100",
    assign_mode=False
)

# Multiply reclassified old tree count with tree binary to remove sections of the old tree count that are not currently forested
# The output retains current forest cover that are over 80 years old

wbt.add(
    input1 = "03_reclassify.tif",
    input2 = "04_trees_reclassify.tif",
    output = "05_young_old_trees.tif"
)
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# # STEP 5: Convert point buffers into regions
# #   (remove spaces between original sample points)
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# # Buffer reclassified old tree raster of points of current forests to begin determining the extent of old forests by creating a continuous forest block
#
# wbt.buffer_raster(
#     i = "03_multiply_otCount_treeBinary.tif",
#     output = "04_buffer_otCount_currentForests.tif",
#     size = 9.5,
#     gridcells=False,
# )
#
# # Reclassify buffered old tree raster of current forests to invert raster. Trees become 0 and everything else is 1.
# # This step assists in converting the interior sections of buffered points to be considered tree cover by including them as a continuous forest block.
#
# wbt.reclass(
#     i = "04_buffer_otCount_currentForests.tif",
#     output = "05_reclassify_buffered_otCount.tif",
#     reclass_vals = "1;0;0;1",
#     assign_mode=True
# )
#
# # Clump buffered old trees into individual objects. This functions to get the interior regions of buffered areas to clumped togehter to then calucalte their area and convert it to be 1 (part of inverting raster).
# wbt.clump(
#     i = "05_reclassify_buffered_otCount.tif",
#     output = "06_clump_interior_otCountBuffer.tif",
#     diag=False,
#     zero_back=True
# )
#
# # Calculate raster area of clumps (interior of old tree count circles).
# wbt.raster_area(
#     i = "06_clump_interior_otCountBuffer.tif",
#     output= "07_area_interior_otCountBuffer.tif",
#     out_text=False,
#     units="map units",
#     zero_back=False, # True would turn buffered circles into noData
# )
#
# # Reclassify to keep interior circles as 1 and everything else as 0 based on area, thus regions classified as 1 are considered old forest.
# wbt.reclass(
#     i = "07_area_interior_otCountBuffer.tif",
#     output = "08_reclassify_interior_otCount.tif",
#     reclass_vals = "1;0;200;0;200;99999999999999999999",
#     assign_mode=False
# )
#
# # Add buffered raster to reclassified interior circles.
# wbt.add(
#     input1 = "04_buffer_otCount_currentForests.tif",
#     input2 = "08_reclassify_interior_otCount.tif",
#     output = "09_add_otCount_interiorBuffer.tif"
# )
#
# # Reclassify where the section of overlap is 2 so that regions of overlapped buffer are considered forest
# wbt.reclass(
#     i = "09_add_otCount_interiorBuffer.tif",
#     output = "10_reclassify_buffered_otCount.tif",
#     reclass_vals = "1;0;0;1;2;1",
#     assign_mode=True
# )
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# # STEP 6: Distinguish current tree canopy as old versus young
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
#
# # Multiply buffered old tree count with current forest (tree canopy binary) to distinguish young vs. old forest and have an output of three classes (Old, Young, and No forests)
# wbt.multiply(
#     input1 = "10_reclassify_buffered_otCount.tif",
#     input2 = "01_treeBinary_noDataZero.tif",
#     output = "11_multiply_Buffered_otCount_treeBinary.tif"
# )
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# # STEP 7: Distinguish age classes of coniferous and deciduous trees
#
# # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#
# # Covert nodata of old tree cover binary and conifer bianry to zero
#
# wbt.convert_nodata_to_zero(
#     i = treeBinary,
#     output = "01_treeBinary_noDataZero.tif"
# )
#
# wbt.convert_nodata_to_zero(
#     i = imageConifers,
#     output = "11_confiers_noDataZero.tif"
# )
#
# # Reclassify conifer trees to 10 and deciduous trees to 0
# wbt.reclass(
#     i = "11_confiers_noDataZero.tif",
#     output = "02_reclassify_confiers.tif",
#     reclass_vals = "0;0;10;1",
#     assign_mode=True
# )
#
# # Add old tree canopy to recliassified conifers (0=no tree, 1= deciduous, 11=conifer)
# wbt.add(
#     input1 = "02_reclassify_confiers.tif",
#     input2 = "11_multiply_Buffered_otCount_treeBinary.tif",
#     output = "04_add_buffered_otCount_conifers.tif"
# )
#
# # Reclassify conifer trees to 10 and deciduous trees to 0
# wbt.reclass(
#     i = "04_add_buffered_otCount_conifers.tif",
#     output = "_reclassify_confiers_young_old.tif",
#     reclass_vals = "0;0;1;1;2;2;0;3;0;4;0;5;0;6;0;10;11;11;12;12",
#     assign_mode=True
# )
#
# # Final output raster pixel value classification: (0=no tree canopy, 1= young deciduous, 2= old deciduous, 11= young coniferous, 12= old coniferous)
