import pandas
import numpy
import matplotlib.pyplot as plt

numpy.set_printoptions(threshold=numpy.inf)

df = pandas.read_csv('Stub.csv')
data=numpy.array(df.loc[:,:])
newDF = df.drop_duplicates(subset=['Longitude', 'Latitude'],keep='first')
column_headers=list(df.columns.values)
# print(df)
# print(column_headers)
# print(data)
# print(newDF)
m = numpy.array(newDF.loc[:,:])
# print(m)
w=numpy.delete(m,0,axis=0)
# print(w)
x1=w[:,18]
y1=w[:,19]
# print(x1)
# print(y1)

result=[]
with open('TrackLine.csv','r')as csvFile2:
    for line in csvFile2:
        linelist=line.split(',')
        for index,item in enumerate(linelist):
            result.append(float(item))
    # print(result)
x2=result[0:105]
y2=result[105:]
# print(x2)
# print(y2)

plt.figure(figsize=(8,8))
plt.scatter(x1,y1,label="$Point$",color="black",linewidth=2)
plt.plot(x2,y2,label="$Line$",color="green",linewidth=3)
plt.title("Track of Vehicle")
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.xlim(139.34,139.56)
plt.ylim(35.40,35.57)
# 或者plt.axis([139.3,139.6,35.3,35.6])
plt.xticks(numpy.linspace(139.34,139.56,6,endpoint=True))
plt.yticks(numpy.linspace(35.40, 35.57,8,endpoint=True))
ax=plt.gca()
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# ax.xaxis.set_ticks_position('bottom')
# ax.spines['bottom'].set_position(('data',0))
# ax.yaxis.set_ticks_position('left')
# ax.spines['left'].set_position(('data', 0))
# for label in ax.get_xticklabels()+ax.get_yticklabels():
#     label.set_fontsize(8)
    # label.set_bbox(dict(facecolor='black',edgecolor='black',alpha=0.2))
plt.legend()
plt.savefig("Result\\MapTrack.jpg")
plt.show()