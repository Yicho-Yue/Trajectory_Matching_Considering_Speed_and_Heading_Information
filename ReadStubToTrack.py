import csv
import numpy
import pandas

numpy.set_printoptions(threshold=numpy.inf)
data = []
track=open("Result\\Track6.csv","w",newline='')
track_csv_writer=csv.writer(track,dialect="excel")
with open('Stub6.csv', 'r', newline='') as csvFile1:
    reader = csv.DictReader(csvFile1)
    for row in reader:
        PI = row['PathIndex']
        if PI == '14':
            data.append(row)
    df = pandas.DataFrame(data)
    #print(df)
    l = numpy.array(df.loc[:, :])
    #print(l)
    newDF = df.drop_duplicates(subset=['Longitude', 'Latitude'], keep='first')
    w = numpy.array(newDF.loc[:, :])
    #print(newDF)
    #print(m)
    # w=numpy.delete(m,7,axis=0)
    #print(w)
    print(len(w))
    x=w[:,-2]
    y=w[:,-1]
    #print(x)
    #print(y)
    #w1=w[:,18:]
    #w2 = w.take([18, 19], axis=1)
    #print(w1)
    #print(w2)
    track_csv_writer.writerow(x)
    track_csv_writer.writerow(y)
    #track_csv_writer.writerow(w1)
csvFile1.close()