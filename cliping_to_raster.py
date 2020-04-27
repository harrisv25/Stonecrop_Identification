import os
import rasterio
import fiona
from shapely.geometry import mapping, shape
from osgeo import ogr, osr, gdal

os.chdir(r"C:\Users\harri_000\Documents\Mongolia\harris_package\harris_package")

shp48=r'GPS_Points\points_48.shp'
shp49=r'GPS_Points\points_49.shp'

r1=r"images\Index of 011315448020_01\011315448020_01_P001_MUL\19SEP25034353-M2AS-011315448020_01_P001.tif"
r2=r"images\Index of 011315448030_01\011315448030_01_P001_MUL\19SEP08040927-M2AS-011315448030_01_P001.tif"
r3=r"images\Index of 011315448040_01\011315448040_01_P001_MUL\19SEP08040926-M2AS-011315448040_01_P001.tif"

rasters=[r1,r2,r3]



def clip_v_to_r(shp, rast):
    
# First we will open our raster image, to understand how we will want to rasterize our vector
    src=rasterio.open(rast)
    ext=src.bounds

    xmin = ext[0]
    xmax = ext[2]
    ymin = ext[1]
    ymax = ext[3]
    src.close()
    poly = []
    with fiona.open(shp) as c:
        for pol in c:
            geom = shape(pol['geometry'])
            if geom.coords[0][0] >= xmin and geom.coords[0][0] <= xmax:
                if geom.coords[0][1] >= ymin and geom.coords[0][1] <= ymax:
                    poly.append([geom, pol])
        
    print(ext,len(poly))
# Here's an example Shapely geometry
    myschema =  {'geometry': 'Point',
                 'properties': {'Location': 'str',
                                'Type': 'str',
                                'ident': 'str',
                                'lat': 'float',
                                'long': 'float',
                                'comment': 'str', 
                                'altitude': 'float'}}

    proj=fiona.open(shp).crs
    name="test.shp"
# Write a new Shapefile
    with fiona.open(name, 'w', crs=proj, driver='ESRI Shapefile', schema=myschema) as c:
    ## If there are multiple geometries, put the "for" loop here
        for i in poly:
            c.write({
                    'geometry': mapping(i[0]),
                    'properties': {'Location': i[1]['properties']['Location'],
                                   'Type': i[1]['properties']['Type'],
                                   'ident': i[1]['properties']['ident'],
                                   'lat': i[1]['properties']['lat'],
                                   'long': i[1]['properties']['long'],
                                   'comment': i[1]['properties']['comment'], 
                                   'altitude': i[1]['properties']['altitude']}
                    })


clip_v_to_r(shp49, r3)
