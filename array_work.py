import os
os.chdir(r"C:\Users\harri_000\Documents\Mongolia\harris_package\harris_package")

from osgeo import gdal
import numpy as np
import pandas as pd


test_ds="shp30_rast.tif"
srcgdal=gdal.Open(test_ds)
test = np.array(srcgdal.GetRasterBand(1).ReadAsArray())
mask=np.where(test>0, 1, 0)
np.sum(pixels)
result=np.where(mask==1)

#b1 Coastal Band
#b2 Blue
#b3 Green
#b4 Yellow
#b5 Red
#b6 Red Edge
#b7 Near Infrared 1
#b8 Near Infrared 2

rtest=r"images\Index of 011315448020_01\011315448020_01_P001_MUL\19SEP25034353-M2AS-011315448020_01_P001.tif"
testgdal=gdal.Open(rtest)
b1=np.array(testgdal.GetRasterBand(1).ReadAsArray())
b2=np.array(testgdal.GetRasterBand(2).ReadAsArray())
b3=np.array(testgdal.GetRasterBand(3).ReadAsArray())
b4=np.array(testgdal.GetRasterBand(4).ReadAsArray())
b5=np.array(testgdal.GetRasterBand(5).ReadAsArray())
b6=np.array(testgdal.GetRasterBand(6).ReadAsArray())
b7=np.array(testgdal.GetRasterBand(7).ReadAsArray())
b8=np.array(testgdal.GetRasterBand(8).ReadAsArray())

Coastal_Band=[]
Blue=[]
Green=[]
Yellow=[]
Red=[]
Red_Edge=[]
NIR1=[]
NIR2=[]

for i in range(len(result[0])):
    Coastal_Band.append(b1[result[0][i], result[1][i]])
    Blue.append(b2[result[0][i], result[1][i]])
    Green.append(b3[result[0][i], result[1][i]])
    Yellow.append(b4[result[0][i], result[1][i]])
    Red.append(b5[result[0][i], result[1][i]])
    Red_Edge.append(b6[result[0][i], result[1][i]])
    NIR1.append(b7[result[0][i], result[1][i]])
    NIR2.append(b8[result[0][i], result[1][i]])


df = pd.DataFrame(list(zip(Coastal_Band,Blue,Green,Yellow,Red,Red_Edge,NIR1,NIR2)), 
               columns =['Coastal_Band','Blue','Green','Yellow','Red','Red_Edge','NIR1','NIR2']) 
