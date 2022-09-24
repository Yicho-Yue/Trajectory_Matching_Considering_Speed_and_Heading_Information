import os
import collections
from shapely.geometry import box


dic=collections.defaultdict(list)
filelist=[]
for root,dirs,files in os.walk('D:\\YinJichong'):
    for filename in files:
        # pos=filename.find('_')
        # if pos >= 0 and filename[pos+1:]=='CONTROL.txt':
        pos=filename.split('_')
        if pos[1]=='CONTROL.txt':
            filepath=os.path.join(root,filename)
            filelist.append(filepath)
            for i in range(len(filelist)):
                controlFile=open(filelist[i],'r')
                lstcon=controlFile.readlines()
                for point in lstcon:
                    lstvalue=point.split("\t")
                    mesh_name=int(lstvalue[0])
                    ltb=float(lstvalue[7])
                    lgb=float(lstvalue[8])
                    ltt=float(lstvalue[9])
                    lgt=float(lstvalue[10])
                    b = box(ltb,lgb,ltt,lgt)
                dic[mesh_name].append(b)

print(filelist)
print(b)
print(dic)


