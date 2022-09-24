import VariableQuantity as vq
import os
import shapefile
import collections
import math
from shapely.ops import cascaded_union
from shapely.geometry import box, Polygon, LineString, Point, MultiLineString


def getstubdata():
    f = open(vq.stub, 'r')
    lines = f.readlines()
    x = []
    y = []
    for i in range(1, len(lines)):
        line = lines[i]
        line = line.replace('\n', '')
        if line == '':
            continue
        x.append(line.split(',')[0])
        y.append(line.split(',')[1])
    f.close()
    return [x, y]

def getmeshrect(filename):
    path = os.path.dirname(filename)
    file = path + '\\' + os.path.basename(filename)[:7] + '_CONTROL.txt'
    if os.path.exists(file):
        f = open(file, 'r', encoding=vq.charset)
        line = f.readline()
        f.close()
        lines = line.split('\t')
        bllon = int(lines[7])
        bllat = int(lines[8])
        trlon = int(lines[9])
        trlat = int(lines[10])
        b = box(bllon, bllat, trlon, trlat)
    return [b, lines[0]]

def getmeshcontrol(dir, dic):
    if os.path.isfile(dir):
        if dir.endswith("_CONTROL.txt"):
            result = getmeshrect(dir)
            dic[result[1]].append(result[0])
    elif os.path.isdir(dir):
        for s in os.listdir(dir):
            newDir = os.path.join(dir, s)
            getmeshcontrol(newDir, dic)
            if dir.endswith("_CONTROL.txt"):
                break

def readdata(filename):
    shapedata = []
    file = os.path.splitext(filename)[0]
    if file:
        shp = os.path.exists("%s.shp" % file)
        dbf = os.path.exists("%s.dbf" % file)
        if (shp and dbf):
            sf1 = shapefile.Reader(filename)
            shapedata.append(sf1.records())
            shapedata.append(sf1.shapes())
        elif (dbf):
            sf1 = shapefile.ReaderDbfOnly(filename)
            shapedata.append(sf1.records())
    return shapedata

def getxylist(shapedata):
    xylist = []
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
        xylist.append([x,y, rec, collections.defaultdict(int), 0])

    return xylist


def getlinkdic(shapedata, points):
    dic = collections.defaultdict(list)
    recs = shapedata[0]
    for i in range(len(recs)):
        rec = recs[i]
        dic[rec[2]].append([rec, points[i]])
    return dic

def getroaddata(file, mesh, linkdic, l):
    roadpath = file%(vq.path, mesh, mesh)
    roaddata = readdata(roadpath)
    roadlist = getxylist(roaddata)
    if roadlist is not None:
        linkdic[mesh].append(getlinkdic(roaddata, roadlist))
    l.append(roadlist)

def getlinkbymesh(mesh, linkdic):
    l = []
    getroaddata('%s//Z%d//Z%d_ROAD_HIWAY2.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_HIWAY1.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_CROAD.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_LOCAL1.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_LOCAL2.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_GENERAL1.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_GENERAL2.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_GENERAL3.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_THIN.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_FERRY.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_CARTRAIN.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_ETC.dbf', mesh, linkdic, l)
    getroaddata('%s//Z%d//Z%d_ROAD_YET.dbf', mesh,  linkdic, l)
    getroaddata('%s//Z%d//Z%d_LANE.dbf', mesh,  linkdic, l)
    return l

def getallmesh(lonlatinl, meshdic, lonlatmesh):
    meshl = []
    for i in range(len(lonlatinl)):
        point = lonlatinl[i]
        for key in sorted(meshdic.keys()):
            x = float(point[0]) * 1000 * 3600
            y = float(point[1]) * 1000 * 3600
            if meshdic[key][0].contains(Point(y, x)):
                if len(meshl) > 0 and int(key) in list(zip(*meshl))[0]:
                    pass
                else:
                    meshl.append([int(key), meshdic[key][0]])
                lonlatmesh.append([point, int(key)])
                break
    return meshl

def circle(center, bound, angle):
    (center_x, center_y) = center
    (bound_x, bound_y) = bound
    RR = (center_x - bound_x) * (center_x - bound_x) + (center_y - bound_y) * (center_y - bound_y)
    R = math.sqrt(RR)
    x = R * math.cos(angle * math.pi / 180)
    y = R * math.sin(angle * math.pi / 180)
    point = (x + center_x, y + center_y)
    return point

def getstartcicle(s, multi):
    l = []
    step = vq.step * multi / 1000 / 3600
    for i in range(36):
        l.append(circle(s, [s[0] + step, s[1]], i * 10))
    l.append(l[0])
    poly = Polygon(l)
    return poly

def gettowprec(s1, s2, multi):
    step = vq.step * multi / 1000 / 3600
    result = []
    x1 = float(s1[0])
    x2 = float(s2[0])
    y1 = float(s1[1])
    y2 = float(s2[1])
    if x1 == x2 and y1 == y2:
        result = ([x1 - step, y1 + step], [x1 + step, y1 + step], [x1 + step, y1 - step], [x1 - step, y1 - step], [x1 - step, y1 + step])
    if x1 < x2:
        if y1 < y2:
            result = ([x1 - step, y1 + step], [x1 + step, y1 - step], [x2 + step, y2 - step], [x2 - step, y2 + step], [x1 - step, y1 + step])
        else:
            result = ([x1 - step, y1 - step], [x1 + step, y1 + step], [x2 + step, y2 + step], [x2 - step, y2 - step], [x1 - step, y1 - step])
    else:
        if y1 < y2:
            result = ([x1 - step, y1 - step], [x1 + step, y1 + step], [x2 + step, y2 + step], [x2 - step, y2 - step], [x1 - step, y1 - step])
        else:
            result = ([x1 - step, y1 + step], [x1 + step, y1 - step], [x2 + step, y2 - step], [x2 - step, y2 + step], [x1 - step, y1 + step])
    poly = Polygon(result)
    return poly

def stubtorect(lt, highmulti, generamulti):
    if len(lt) < 2:
        return
    rects = []
    sx = lt[0]
    sy = lt[1]
    for i in range(1, len(sx)):
        result = []
        s1 = (float(sx[i-1]), float(sy[i-1]))
        s2 = (float(sx[i]), float(sy[i]))
        p1 = getstartcicle(s1, highmulti)
        p2 = gettowprec(s1, s2, highmulti)
        p3 = getstartcicle(s2, highmulti)
        p4 = cascaded_union([p1,p2,p3])
        result.append(list(zip(*[s1, s2])))
        result.append(list(zip(*p4.boundary.xy)))

        p1 = getstartcicle(s1, generamulti)
        p2 = gettowprec(s1, s2, generamulti)
        p3 = getstartcicle(s2, generamulti)
        p4 = cascaded_union([p1, p2, p3])
        result.append(list(zip(*p4.boundary.xy)))
        rects.append([result, i-1])
    return rects

def orderbyintersect(re):
    for key in sorted(re.keys()):
        links = re[key]
        for i in range(len(links)):
            link = links[i]
            link[4] = link[3][key]
        links.sort(key=lambda x:(x[4]), reverse=True)

def linerectintersects(rects, listmesh):
    result = collections.defaultdict(list)
    for i in range(len(rects)):
        rect1 = rects[i][0][1]
        rect2 = rects[i][0][2]
        poly1 = Polygon(rect1)
        poly2 = Polygon(rect2)
        for j in range(len(listmesh)):
            roadtype = listmesh[j]
            for k in range(len(roadtype)):
                links = roadtype[k]
                if links is None:
                    continue
                for m in range(len(links)):
                    link = links[m]
                    sp = [link[0][0], link[1][0]]
                    ep = [link[0][-1], link[1][-1]]
                    lines = list(zip(*[link[0], link[1]]))
                    path = LineString(lines)
                    if k < 4:
                        poly = poly1
                    else:
                        poly = poly2
                        c = poly.contains(Point(sp))
                        if c:
                            pass
                        else:
                            d = poly.contains(Point(ep))
                            if d:
                                pass
                            else:
                                continue
                    a = poly.intersects(path)
                    b = poly.contains(path)

                    if b:
                        link[3][i] = path.length
                        result[i].append(link)
                        link[2][-1].append(i)
                    elif a:
                        np = poly.intersection(path)
                        s = 0
                        if isinstance(np, LineString):
                            s = np.length
                        elif isinstance(np, MultiLineString):
                            for k in range(len(np)):
                                s = s + np[k].length
                        dic = link[3]
                        dic[i] = s
                        result[i].append(link)
                        link[2][-1].append(i)
    orderbyintersect(result)
    return result

changelinks = []

def makematchlink(link, reverse):
    changelinks.append(link)
    x = link[0][0], link[0][-1]
    y = link[1][0], link[1][-1]
    if (reverse):
        x = link[0][-1], link[0][0]
        y = link[1][-1], link[1][0]
    mesh = link[2][0]
    id = link[2][2]
    return x, y, [mesh, 0, id], LineString(list(zip(*[link[0], link[1]]))), link[2][9], reverse

def getstartlink(result, rects):
    x = rects[0][0][0][0][0]
    y = rects[0][0][0][1][0]
    linklist = []
    key = min(result.keys())
    line = result[key]
    for i in range(len(line)):
        x1 = line[i][0][0]
        y1 = line[i][1][0]
        dis = Point(x1, y1).distance(Point(x, y))
        if dis < vq.deviation:
            linklist.append([makematchlink(line[i], False)])
        else:
            x1 = line[i][0][-1]
            y1 = line[i][1][-1]
            dis = Point(x1, y1).distance(Point(x, y))
            if dis < vq.deviation:
                linklist.append([makematchlink(line[i], True)])
    return linklist

def makecoordkey(x, y):
    return '%f,%f'%(x, y)

def addmap(po, dic, link):
    value = dic.get(po)
    if (value == None):
        dic.setdefault(po, [link])
    else:
        value.append(link)

def makemap(alllink):
    m = {}
    for link in alllink:
        sp = makecoordkey(link[0][0], link[1][0])
        ep = makecoordkey(link[0][-1], link[1][-1])
        addmap(sp, m, link)
        addmap(ep, m, link)
    return m

def pointtocircle(ep, multi):
    p1 = getstartcicle(ep, multi)
    return p1

def endlink(link, rect):
    ep = rect[0][0][0][-1], rect[0][0][1][-1]
    circlep = pointtocircle(ep, vq.semulti)
    line = link[3]
    return circlep.intersects(line)

def getmeshlinkid(links):
    l = []
    for link in links:
        l.append('%s,%s'%(link[2][0], link[2][2]))
    return l

def getangle(cen, first, second):
    dx1 = first[0] - cen[0]
    dy1 = first[1] - cen[1]
    dx2 = second[0] - cen[0]
    dy2 = second[1] - cen[1]
    cosfi = dx1 * dx2 + dy1 * dy2
    norm = (dx1 * dx1 + dy1 * dy1) * (dx2 * dx2 + dy2 * dy2)
    cosfi /= math.sqrt(norm)

    if (cosfi >= 1.0):
        return 0
    if (cosfi <= -1.0):
        return math.pi
    fi = math.acos(cosfi)

    if (180 * fi / math.pi < 180):
        return 180 * fi / math.pi
    else:
        return 360 - 180 * fi / math.pi

def calculateangle(startlink, link):
    lpl = list(zip(*[link[0],link[1]]))
    sspl = list(zip(*startlink[3].xy))
    if lpl[0] == sspl[0]:
        return getangle(lpl[0], lpl[1], sspl[1])
    elif lpl[0] == sspl[-1]:
        return getangle(lpl[0], lpl[1], sspl[-2])
    elif lpl[-1] == sspl[0]:
        return getangle(sspl[0], sspl[1], lpl[-2])
    elif lpl[-1] == sspl[-1]:
        return getangle(sspl[-1], sspl[-2], lpl[-2])
    else:
        return 100

def getroute(dic, route):
    if (len(route)) == 0:
        print('route is zero')
    startlink = route[-1]
    l = []
    key = makecoordkey(startlink[0][-1], startlink[1][-1])
    links = dic.get(key)
    meshlinkidl = getmeshlinkid(route)
    ep = startlink[0][-1], startlink[1][-1]
    if (links != None):
        for link in links:
            ro = []
            sp = link[0][0], link[1][0]
            tep = link[0][-1], link[1][-1]
            if (link[2][0] == startlink[2][0] and link[2][2] == startlink[2][2]):
                continue
            if ep == sp and meshlinkidl.__contains__('%s,%s'%(link[2][0],link[2][2])):
                continue
            if ep == tep:
                llink = makematchlink(link, True)
            else:
                llink = makematchlink(link, False)
            if ro.__contains__(llink):
                pass
            else:
                angle = calculateangle(startlink, link)
                if angle < 70:
                    continue
                ro.extend(route)
                ro.append(llink)
                l.append(ro)
    if len(l) == 0:
        l = [route]
    return l

def gettempend(allroute, rect):
    l = []
    if len(allroute) == 0:
        return l
    ep = rect[0][0][0][-1], rect[0][0][1][-1]
    semulti = vq.semulti
    while True:
        if semulti > vq.maxmulti:
            break
        circlep = pointtocircle(ep, semulti)
        for route in allroute:
            find = False
            k = 0
            cnt = 0
            for link in route:
                if circlep.intersects(link[3]):
                    find = True
                    break
                k += 1
                cnt += 1
            if find:
                l.append(route)
        if len(l) > 0:
            break
        semulti += vq.semutlistep
    if len(l) == 0:
        l.extend(allroute)
        l = [l[0]]
    if len(l) > 100:
        l.sort(key=lambda x:(len(x)))
        l = [l[0]]
    return l

def getallroute(allroute, rects, k, lastroute, m):
    routechg = 1
    n = 0
    while routechg > 0:
        routechg = 0
        if n == len(allroute):
            n = 0
        i = n
        while i < len(allroute):
            if k == 13 and i == 0:
                dk = 0
            ro = allroute[i]
            t = ro
            if endlink(t[-1], rects[k]):
                i += 1
                continue
            cnt = len(t)
            re = getroute(m,t)
            if len(re) > 1:
                lastroute.append(t)
                allroute.remove(t)
                for r in sorted(re, reverse=True):
                    allroute.insert(i, r)
                continue
            elif len(re[-1]) > cnt:
                allroute[i] = re[0]
                continue
            else:
                i += 1
                pass
    allroute = gettempend(allroute, rects[k])
    return allroute

def routelinktostring(allroute):
    l = []
    for route in allroute:
        s = ''
        for link in route:
            s += '%s,%s,'%(link[2][0], link[2][2])
        l.append(s)
    return l

def deleteexists(allroute, lastroute):
    if len(lastroute) == 0:
        return
    lastroute.sort(key=lambda x:(len(x)), reverse=True)
    all = routelinktostring(allroute)
    last = routelinktostring(lastroute)
    dell = []
    for i in range(len(last)):
        for a in all:
            if a == last[i]:
                dell.append(lastroute[i])
                break
    for d in dell:
        lastroute.remove(d)
    dell.clear()
    last = routelinktostring(lastroute)
    for i in range(len(last)):
        prer = last[i]
        if i == len(last)-1:
            break
        for j in range(i+1, len(last)):
            r = last[j]
            if prer == r:
                dell.append(lastroute[i])
                break
    for d in dell:
        lastroute.remove(d)

def getlinkconnect(result, linklist, rects):
    allroute = linklist
    index = 0
    key = min(result.keys())
    lastroute = []
    for k in range(key, len(result)):
        index += 1
        alllink = result[k]
        m = makemap(alllink)
        if len(lastroute) > 0:
            temp = []
            lastroute = getallroute(lastroute, rects, k, temp, m)
            deleteexists(allroute, lastroute)
            allroute.extend(lastroute)
            lastroute.clear()
        allroute = getallroute(allroute, rects, k, lastroute, m)
    return allroute

def linkchange(allroute):
    m = {}
    for link in changelinks:
        key = '%s,%s'%(link[2][0], link[2][2])
        v = m.get(key)
        if v == None:
            m.setdefault(key, link)
    result = []
    for route in allroute:
        l = []
        for link in route:
            key = '%s,%s'%(link[2][0], link[2][2])
            v = m.get(key)
            if v == None:
                print('error link not find %s'%v)
            else:
                l.append(v)
        result.append(l)
    return result

def getendlink(result, rects):
    x = rects[0][0][0][-1]
    y = rects[0][0][1][-1]
    linklist = []
    key = min(result.keys())
    line = result[key]
    for i in range(len(line)):
        x1 = line[i][0][-1]
        y1 = line[i][1][-1]
        dis = Point(x1, y1).distance(Point(x, y))
        if dis < vq.deviation:
            linklist.append([makematchlink(line[i], False)])
    return linklist

def isendpoint(link, ep):
    x = ep[0]
    y = ep[1]
    x1 = link[0][-1]
    y1 = link[1][-1]
    dis = Point(x1, y1).distance(Point(x, y))
    if dis < vq.deviation:
        return True
    return False

def isendlink(elink, links):
    for l in links:
        link = l[0]
        if elink[2][0] == link[2][0] and elink[2][2] == link[2][2]:
            return True
    return False

def listadd(ls, a):
    if ls.__contains__(a):
        pass
    else:
        ls.append(a)

def linetorect(lt, multi):
    if len(lt) < 2:
        return
    rects = []
    sx = lt[0]
    sy = lt[1]
    for i in range(1, len(sx)):
        result = []
        s1 = (float(sx[i-1]), float(sy[i-1]))
        s2 = (float(sx[i]), float(sy[i]))
        p1 = getstartcicle(s1, multi)
        p2 = gettowprec(s1, s2, multi)
        p3 = getstartcicle(s2, multi)
        p4 = cascaded_union([p1, p2, p3])
        result.append(list(zip(*[s1, s2])))
        result.append(list(zip(*p4.boundary.xy)))
        rects.append([result, i-1])
    return rects

def getbestroute(allroute, end):
    l = []
    l.append(end)
    sl = end[0][2][0], end[0][2][2]
    el = end[-1][2][0], end[-1][2][2]
    for route in allroute:
        rsl = route[0][2][0], route[0][2][2]
        rel = route[-1][2][0], route[-1][2][2]
        if (sl == rsl and el == rel):
            l.append(route)
    l.sort(key=lambda x:(len(x)))
    return l[0]

def getendroute(allroute, result, rects):
    dell = []
    cnt = 1
    while True:
        if cnt > len(rects):
            break
        endlinklist = getendlink(result, rects[len(rects) - cnt])
        x = rects[len(rects) - cnt][0][0][0][-1]
        y = rects[len(rects) - cnt][0][0][1][-1]
        cnt += 1
        for route in allroute:
            if isendpoint(route[-1], (x, y)):
                pass
            elif isendlink(route[-1], endlinklist):
                pass
            else:
                dell.append(route)
        if len(dell) < len(allroute):
            for delt in dell:
                allroute.remove(delt)
            break
    l = []
    for rect in rects:
        tl = list(zip(*([rect[0][0][0],rect[0][0][1]])))
        listadd(l, tl[0])
        listadd(l, tl[1])
    ls = list(zip(*l))
    serect = linetorect(ls, vq.semulti)
    m = Polygon()
    for rect in serect:
        poly = Polygon(rect[0][1])
        m = cascaded_union([poly, m])
    re = []
    for i in range(0, len(allroute)):
        route = allroute[i]
        linkpoly = Polygon()
        ls = []
        for link in route:
            l = list(zip(*[link[0], link[1]]))
            for ll in l:
                listadd(ls, ll)
        l = list(zip(*ls))
        serect = linetorect(l, vq.semulti)
        for rect in serect:
            poly = Polygon(rect[0][1])
            linkpoly = cascaded_union([poly,linkpoly])
        sl = linkpoly.area
        inter = m.intersection(linkpoly)
        if (inter.area == 0):
            area = 0
        else:
            area = inter.area
        re.append([area, i, sl])
    re = sorted(re, key=lambda a:a[0], reverse=True)
    if len(re) > 0:
        end = allroute[re[0][1]]
        end = getbestroute(allroute, end)
    else:
        end = None
    return end

def getmatchlink(result, rects):
    exceptlink = []
    linklist = getstartlink(result, rects)
    allroute = getlinkconnect(result, linklist, rects)
    allroute = linkchange(allroute)
    linklist = getendroute(allroute, result, rects)
    return [linklist, exceptlink]

