import os
import rasterio
import fiona
from shapely.geometry import mapping, shape
from osgeo import ogr, osr, gdal

os.chdir("your directory")

#my images cover two seperate projections, so the a shapefile was created for each projection. 
shp48=r'points_48.shp'
shp49=r'points_49.shp'

r1=r"image 1"
r2=r"image 2"
r3=r"image 3"

rasters=[r1,r2,r3]

#the intent is to just use points and a raster.Everything else will be automated in the function

def clip_v_to_r(shp, rast):
    
# First we will open our raster image, to understand how we will want to rasterize our vector
    src=rasterio.open(rast)
    ext=src.bounds
#the left, right, top bottom coordinates will be used to draw a bounding box around the points
    xmin = ext[0]
    xmax = ext[2]
    ymin = ext[1]
    ymax = ext[3]
    src.close()
    #create an empty list that the points within the box will be written into
    poly = []
    with fiona.open(shp) as c:
        for pol in c:
            geom = shape(pol['geometry'])
            #check to see if the geometry opened is within the box. If so it is appended to the list.
            if geom.coords[0][0] >= xmin and geom.coords[0][0] <= xmax:
                if geom.coords[0][1] >= ymin and geom.coords[0][1] <= ymax:
                    poly.append([geom, pol])
        
    print(ext,len(poly))
# The schema is based ioff the original shapefile's attribute table. NOthing needs
    #to be altered, simplpy copied to a new shapefile
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
