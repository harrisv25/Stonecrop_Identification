import os
os.chdir(ryour directory")

from osgeo import gdal
import numpy as np
import pandas as pd

from sklearn import svm
from sklearn.model_selection import train_test_split

#opn the mask raster and convert it to an array.
test_ds="hp40_rast.tif"
srcgdal=gdal.Open(test_ds)
arr = np.array(srcgdal.GetRasterBand(1).ReadAsArray())
#mask=np.where(arr==1, 1, np.where(arr==2, 0, np.where(arr==3, 3, 0)))

#0 is unlabeled data. Because we want the cells which have been labeled, 
#we create a new array containing the indexes of these classified cells.
result=np.where(arr>0)
len(result[0])



#rtest=r"images 1"
#rtest=r"image 2"
rtest=r"image 3"

#open each of the image's bands and convert them to arrays.
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
label=[]

#Because the dimensions of the bands are the same as the mask array, 
#we can use the array of indexes to select the spectral information 
#from each of the bands for those specifc cells.
for i in range(len(result[0])):
    if b1[result[0][i], result[1][i]] != 0:
        Coastal_Band.append(b1[result[0][i], result[1][i]])
    if b2[result[0][i], result[1][i]] != 0:
        Blue.append(b2[result[0][i], result[1][i]])
    if b3[result[0][i], result[1][i]] != 0:
        Green.append(b3[result[0][i], result[1][i]])
    if b4[result[0][i], result[1][i]] != 0:
        Yellow.append(b4[result[0][i], result[1][i]])
    if b5[result[0][i], result[1][i]] != 0:
        Red.append(b5[result[0][i], result[1][i]])
    if b6[result[0][i], result[1][i]] != 0:
        Red_Edge.append(b6[result[0][i], result[1][i]])
    if b7[result[0][i], result[1][i]] != 0:
        NIR1.append(b7[result[0][i], result[1][i]])
    if b8[result[0][i], result[1][i]] != 0:
        NIR2.append(b8[result[0][i], result[1][i]])
        label.append(arr[result[0][i], result[1][i]])

#we can create a dataframe of spectral information and the associated labels to train models. 
df = pd.DataFrame(list(zip(Coastal_Band,Blue,Green,Yellow,Red,Red_Edge,NIR1,NIR2,label)), 
               columns =['Coastal_Band','Blue','Green','Yellow','Red','Red_Edge','NIR1','NIR2', 'Label']) 

#df.to_csv("ROI_bands40.csv")

#a common band combination to isolate flora. 
var= df[['Green','Red','NIR1']]
label=df['Label']

x=var.to_numpy()
y=label.to_numpy()

#Split the data for a cross-validation accuracy assement of the model
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

clf = svm.SVC(decision_function_shape='ovo')
clf.fit(x_train, y_train)


pred=clf.predict(x_test)
x_test[0]

#Determine the accuracy of the model by having it predict the test data. The predictions can
#be compared to the actual labeled values. 
s=0
f=0

for i in range(len(pred)):
    if pred[i] == y_test[i]:
        s+=1
    else:
        f+=1
a=s/(s+f)
print(a)

x_test.shape

#create an empty array that emulate the demensions of the image. 
p_arr = np.empty(b1.shape)



for i in range(len(p_arr)):
    lst=[]
    for y in range(len(p_arr[0])):
        #create an array for each cell in the original image containing the green, red and NIR 1 info.
        ts=[]
        ts.append(b3[i, y])
        ts.append(b5[i, y])
        ts.append(b7[i, y])
        lst.append(np.asarray(ts))
    a=np.asarray(lst)
    a.shape
   #for each record in the array, predict its label and write the label to the new array.
    value=[clf.predict(a)]
    p_arr[i]=value[0]


p_arr[0][0]
value[0][1]

np.min(p_arr)


#convert an array to a raster.
def array_to_raster(array,reference, output_file):
    ref=gdal.Open(reference)
    srcgdal = np.array(ref.GetRasterBand(1).ReadAsArray())
    dst_filename = output_file
    x_pixels = srcgdal.shape[1]  # number of pixels in x
    y_pixels = srcgdal.shape[0]  # number of pixels in y
    driver = gdal.GetDriverByName('GTiff')
    dataset = driver.Create(dst_filename,x_pixels, y_pixels, 1,gdal.GDT_Float32)
    dataset.GetRasterBand(1).WriteArray(array)

    # follow code is adding GeoTranform and Projection
    geotrans=ref.GetGeoTransform()  #get GeoTranform from existed 'data0'
    proj=ref.GetProjection() #you can get from a exsited tif or import 
    dataset.SetGeoTransform(geotrans)
    dataset.SetProjection(proj)
    dataset.FlushCache()
    dataset=None



array_to_raster(p_arr, rtest, "test.tif")
