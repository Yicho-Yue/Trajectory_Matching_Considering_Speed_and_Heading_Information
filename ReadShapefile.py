import os
import shapefile
import collections

def GetFileList(dir):
    filelist=[]
    for root, dirs, files in os.walk(dir):
        for filename in files:
            pos = filename.split('_')
            # print(pos)
            if pos[1] == 'ROAD':
                filelist.append(os.path.join(root, filename))
    return filelist

def GetMesh(dir):
    mesh=[]
    filelist=[]
    for root, dirs, files in os.walk(dir):
        for filename in files:
            # pos=filename.find('_')
            # if pos >= 0 and filename[pos+1:]=='CONTROL.txt':
            pos = filename.split('_')
            if pos[1] == 'CONTROL.txt':
                filelist.append(os.path.join(root, filename))
    for i in range(len(filelist)):
        controlFile = open(filelist[i], 'r')
        lstcon = controlFile.readlines()
        for point in lstcon:
            lstvalue = point.split("\t")
            mesh_name = int(lstvalue[0])
            mesh.append(mesh_name)
    return mesh

def ReadData(filename):
    shapedata = []
    file = os.path.splitext(filename)[0]
    if file:
        shp = os.path.exists("%s.shp" % file)
        dbf = os.path.exists("%s.dbf" % file)
        if (shp and dbf):
            sf = shapefile.Reader(filename)
            shapedata.append(sf.records())
            shapedata.append(sf.shapes())
        elif (dbf):
            sf = shapefile.ReaderDbfOnly(filename)
            shapedata.append(sf.records())
    return shapedata

def GetPointsList(shapedata):
    list = []
    if len(shapedata) < 2:
        return
    shapes = shapedata[1]
    records = shapedata[0]
    for i in range(len(shapes)):
        line = shapes[i]
        rec = records[i]
        rec.append([])
        x = []
        y = []
        for j in range(len(line.points)):
            p = line.points[j]
            x.append(p[0] / 1000 / 3600)
            y.append(p[1] / 1000 / 3600)
        list.append([x,y, rec, collections.defaultdict(int), 0])
    return list






dir='D:\\YinJichong'
filelist=GetFileList(dir)
meshlist=GetMesh(dir)

shapedata1=[]
list1=[]
for i in range(len(filelist)):
    filename=filelist[i]
    shapedata=ReadData(filename)
    shapedata1.append(shapedata)
    list=GetPointsList(shapedata)
    list1.append(list)

print(shapedata)
print(list1)













