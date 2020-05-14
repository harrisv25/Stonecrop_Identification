from osgeo import gdal
from osgeo import ogr
from osgeo import gdalconst
import os

os.chdir(r"E:\Spring2020\Mongolia\harris_package\harris_package")


shp1='classes20.shp'
shp2='classes30.shp'
shp3='classes40.shp'


r1=r"images\Index of 011315448020_01\011315448020_01_P001_MUL\19SEP25034353-M2AS-011315448020_01_P001.tif"
r2=r"images\Index of 011315448030_01\011315448030_01_P001_MUL\19SEP08040927-M2AS-011315448030_01_P001.tif"
r3=r"images\Index of 011315448040_01\011315448040_01_P001_MUL\19SEP08040926-M2AS-011315448040_01_P001.tif"




def rasterize_pts(shp, rast):
    ndsm = rast
    shp = shp
    #get the transform information from the image to contrsuct the dimensions of the new raster
    data = gdal.Open(ndsm, gdalconst.GA_ReadOnly)
    geo_transform = data.GetGeoTransform()

    x_min = geo_transform[0]
    y_max = geo_transform[3]
    x_max = x_min + geo_transform[1] * data.RasterXSize
    y_min = y_max + geo_transform[5] * data.RasterYSize
    x_res = data.RasterXSize
    y_res = data.RasterYSize
    mb_v = ogr.Open(shp)
    mb_l = mb_v.GetLayer()
    pixel_width = geo_transform[1]
    #you can define the name of the new file here
    output = shp[11:16]+rast[26:28]+"_rast.tif"
    target_ds = gdal.GetDriverByName('GTiff').Create(output, x_res, y_res, 1, gdal.GDT_Byte)
    target_ds.SetGeoTransform((x_min, pixel_width, 0, y_min, 0, pixel_width))
    band = target_ds.GetRasterBand(1)
    NoData_value = -999999
    band.SetNoDataValue(NoData_value)
    band.FlushCache()
    #The target field must be an integer value! this will be the code written into 
    #the cells which overlay the points.
    gdal.RasterizeLayer(target_ds, [1], mb_l, options=["ATTRIBUTE=class_id"])

    target_ds = None


rasterize_pts(shp3, r3)
rasterize_pts(shp1, r1)
rasterize_pts(shp2, r2)
#rasterize_pts(shp3, r3)
