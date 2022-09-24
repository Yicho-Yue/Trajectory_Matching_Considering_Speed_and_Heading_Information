import pandas
import numpy
import shapefile

numpy.set_printoptions(threshold=numpy.inf)

df = pandas.read_csv('Stub.csv')
data=numpy.array(df.loc[:,:])
newDF = df.drop_duplicates(subset=['Longitude', 'Latitude'],keep='first')
column_headers=list(df.columns.values)
m = numpy.array(newDF.loc[:,:])
w=numpy.delete(m,0,axis=0)
n=w.tolist()
x1=w[:,18]*60*60*1000

y1=w[:,19]*60*60*1000
w1=w[:,18:]
w2=w1.T

result=[]
with open('TrackLine.csv','r')as csvFile2:
    for line in csvFile2:
        linelist=line.split(',')
        for index,item in enumerate(linelist):
            result.append(float(item))
x2=result[0:105]
y2=result[105:]
r=numpy.array([result[0:105],result[105:]])
t=r.T

t1=t*60*60*1000
# print(t1)



wsf1=shapefile.Writer(shapefile.POINT)
wsf1.autoBalance=1
wsf1.field('Longitude','C','40')
wsf1.field('Latitude','C','40')
for i,j in enumerate(x1):
    wsf1.point(j,y1[i])
    wsf1.record(j, y1[i])
wsf1.save('Result\\NewTrackPointShpFile')

wsf2=shapefile.Writer(shapefile.POLYLINE)
wsf2.autoBalance=1
wsf2.field('Longitude','C','40')
wsf2.field('Latitude','C','40')
for ii,jj in enumerate(x2):
    wsf2.line(parts=[t1])
    wsf2.record(jj,y2[ii])
wsf2.save('Result\\NewTrackLineShpFile')