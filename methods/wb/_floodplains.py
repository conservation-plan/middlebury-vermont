##  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
##  name:     floodplains.py
##  purpose:  Create a Relative Elevation Model (REM) for a town of Middlebury Conservation Plan
##  author:   Will Behm (From Jeff Howarth and Olson et al. [2014])
##  update:   12/27/2021
##  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

## import tools from WBT module

import sys
sys.path.insert(0, '/Users/jhowarth/tools')
from WBT.whitebox_tools import WhiteboxTools

## declare a name for the tools

wbt = WhiteboxTools()

## Define the Whitebox working directory
## You will need to change the path below to your local path name

wbt.work_dir = "/Volumes/LaCie/plans/methods/wb/data/bREM"

##After downloading layers (demHF, Flowlines, Flood Zones) from Earth Engine at ()
##All layers not in the NAD83/Vermont projection (ESPG 32145) were exported to a new layer (in QGIS) with ESPG 32145

dem = "/Volumes/LaCie/plans/methods/wb/data/midd/iDemHF_0p7_12222021.tif" #2017 Hydro-flattened DEM

#------------------------------------------------------------------------------------------------------------------------------------------------------------
##FIND CHANNEL CENTERLINES (QGIS)
#----------------------------------------------------------------------------------------------------------------------------------------------
##The flowlines dataset was clipped to the extent of the area of interest, and "articficial" flowlines were extracted to a new layer.

#----------------------------------------------------------------------------------------------------------------------------------------------
##CONSTRUCT POINTS ALONG CHANNEL CENTERLINES
#----------------------------------------------------------------------------------------------------------------------------------------------
##Channel points were then constructed along the flowlines using the points along geometries tool. Distance between Points
##was set to an estimated average width of the river channel (30m).
##Name this output channelPtsClipRep.shp


#----------------------------------------------------------------------------------------------------------------------------------------------
##EXTRACT ELEVATION TO CHANNEL POINTS (WBT)
#----------------------------------------------------------------------------------------------------------------------------------------------

#Extract elevation values from DEM, Adding them to the attribute table of the Channel Points layer just created in QGIS (VALUE1 column)

points = '/Volumes/LaCie/plans/methods/wb/data/bREM/starts/rivers/_fRiverPoints.shp'

wbt.extract_raster_values_at_points(
    inputs = dem,
    points = points,
    out_text = False
)

##Comment out after running

#----------------------------------------------------------------------------------------------------------------------------------------------
##GENERATE DETRENDED DEM (QGIS->WBT->QGIS)
#----------------------------------------------------------------------------------------------------------------------------------------------
##IN QGIS (Heatmap Tool) Create Point Density Raster
    #Input =  Channel Points layer(channelPtsClipRep)
    #search radius: 1000m
    #pixel size = 0.5
    #Output name: pointRaster.tif

##IN QGIS (Heatmap tool) Create Elevation Density Raster
    #Input =  Channel Points layer(channelPtsClipRep)
    #search radius: 1000m
    #weight from field: VALUE1
    #Output name: elevationRaster.tif

##Note: Test Radius may be varied to a value that produces the clearest result for a given study area

##Divide elevation density raster by point density raster to create Detrended Dem

# wbt.divide(
#     input1 = "elevationRaster.tif",
#     input2 = "pointRaster.tif",
#     output = "_detrendedDEM.tif",
# )

##Comment out after running
##IN QGIS, CLIP OUTPUT BY EXTENT OF demHF.tif TO PRESERVE DIMENSIONS OF ORIGINAL RASTER
##(Clip Raster by Extent, output named detrendedClip.tif)

#----------------------------------------------------------------------------------------------------------------------------------------------
##SUBTRACT RAW DEM FROM DETRENDED DEM TO CREATE RELATIVE ELEVATION MODEL
#----------------------------------------------------------------------------------------------------------------------------------------------

# #Subtract
#
# wbt.subtract(
#     input1 = dem,
#     input2 = "detrendedClip.tif",
#     output = "_testREM1.tif",
# )
#
# #Convert REM from meters to feet
#
# wbt.multiply(
#     input1 = "_testREM1.tif",
#     input2 = 3.2084,
#     output = "_final_REM.tif"
# )

#Symbolize using singleband pseudocolor as the render type, and the "blues" color ramp (invert so that low values are darker)
#Set maximum value to 15 feet and minimum valute to 0 in order to limit the color ramp to floodplains,
#more accurately visualizing historic morphology
