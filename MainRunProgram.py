import collections
import MapMatching as mm
import VariableQuantity as vq
import time
import DrawResult as dr
import WriteShape as ws
import matplotlib.pyplot as plt
import numpy as np
np.set_printoptions(threshold=np.inf)


meshdic = collections.defaultdict(list)
linkdic = collections.defaultdict(list)

print('start read stub')
time_start = time.time()

xylist = mm.getstubdata()

lonlatinl = list(zip(*xylist))

stub_end=time.time()
stubtime=stub_end-time_start
print('stub read cost %.2f(s)' % stubtime)

print('start read mesh')
mm.getmeshcontrol(vq.path, meshdic)

lonlatmesh = []

meshlist = mm.getallmesh(lonlatinl, meshdic, lonlatmesh)

mesh_end = time.time()
meshtime = mesh_end - stub_end
print('mesh read cost %.2f(s)' % meshtime)

print('start read roaddata')
listmesh = []

for meshindex in range(len(meshlist)):
    meshc = meshlist[meshindex]
    listmesh.append(mm.getlinkbymesh(meshc[0], linkdic))

road_end = time.time()
roadtime = road_end - mesh_end
print('roaddata read cost %.2f(s)' % roadtime)

print('start stub rect')
rects = mm.stubtorect(xylist, vq.multi, vq.generamulti)

rect_end=time.time()
recttime=rect_end-road_end
print('stub rect cost %.2f(s)' % recttime)

print('start link rect intersects')
result = mm.linerectintersects(rects, listmesh)

search_end = time.time()
searchtime = search_end - rect_end
print('search link rect intersects cost %.2f(s)' % searchtime)

print('start link match')
linklist = mm.getmatchlink(result, rects)

match_end = time.time()
matchtime = match_end - search_end
print('link match cost %.2f(s)' % matchtime)

print('start draw result')

mmp = linklist[0]
dr.drawmesh(meshlist)

for i in range(len(rects)):
    dr.drawoutrect(rects[i])
if mmp != None:
    dr.drawmatchlink(mmp, 'r')

plt.savefig('Result\\DrawResult.jpg')
plt.show()

draw_end = time.time()
drawtime = draw_end - match_end
print('figure draw cost %.2f(s)' % drawtime)

print('start write shape')

ws.writemeshshape(meshlist)
ws.writematchlineshape(linklist[0])
ws.writematchpointshape(linklist[0])
ws.writerectshape(rects)
ws.writeintersectshape(result)
ws.writeintersectpointshape(result)


write_end = time.time()
writetime = write_end - draw_end
print('write data cost %.2f(s)' % writetime)



