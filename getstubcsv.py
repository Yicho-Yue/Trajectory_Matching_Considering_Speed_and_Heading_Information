import shapefile
import numpy

import matplotlib.pyplot as plt


stub = 'E:\Test\Stub\Stub6.csv'

def getstubcsv():
    f = open(stub, 'r')
    lines = f.readlines()
    l = []
    for i in range(1, len(lines)):
        line = lines[i]
        line = line.replace('\n', '')
        if line == '':
            continue
        content = line.split(',')
        sp = [float(content[-2]) , float(content[-1])]
        if sp == [0.0, 0.0]:
            continue
        if not l.__contains__(sp):
            l.append(sp)

    f.close()
    return l

# def writestublineshape(linklist):
#     wsf = shapefile.Writer(shapefile.POLYLINE)
#     wsf.autoBalance = 1
#     wsf.field('Longitude', 'C', '40')
#     wsf.field('Latitude', 'C', '40')
#     for i in range(len(linklist)):
#         link=linklist[i]
#         r = numpy.array([link[0], link[1]])
#         t = r.T
#         wsf.line(parts=[t])
#         wsf.record(link[0], link[1])
#     wsf.save('Result\\StubLineShapeFile')
#
# def writestubpointshape(linklist):
#     wsf = shapefile.Writer(shapefile.POINT)
#     wsf.autoBalance = 1
#     wsf.field('Longitude', 'C', '40')
#     wsf.field('Latitude', 'C', '40')
#     for i in range(len(linklist)):
#         link = linklist[i]
#         p = list(zip(*[link[0], link[1]]))
#         wsf.point(p[0][0], p[0][1])
#         wsf.record(p[0][0], p[0][1])
#     wsf.save('Result\\StubPointShapeFile')

track = getstubcsv()

x=[]
y=[]

for i in range(len(track)):
    x.append(track[i][0])
    y.append(track[i][1])





# writestublineshape(track)
# writestubpointshape(track)

print(track)
print(len(track))

print(x)
print(y)

r=numpy.array([x,y])
t=r.T

wsf1=shapefile.Writer(shapefile.POINT)
wsf1.autoBalance=1
wsf1.field('Longitude','C','40')
wsf1.field('Latitude','C','40')
for i,j in enumerate(x):
    wsf1.point(j,y[i])
    wsf1.record(j, y[i])
wsf1.save('Result\\StubPointShapeFile')

wsf2=shapefile.Writer(shapefile.POLYLINE)
wsf2.autoBalance=1
wsf2.field('Longitude','C','40')
wsf2.field('Latitude','C','40')
for ii,jj in enumerate(x):
    wsf2.line(parts=[t])
    wsf2.record(jj,t[ii])
wsf2.save('Result\\StubLineShapeFile')