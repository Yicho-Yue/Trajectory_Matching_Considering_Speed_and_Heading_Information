import shapefile
import numpy

def writemeshshape(meshl):
    wsf = shapefile.Writer(shapefile.POLYLINE)
    wsf.autoBalance = 1
    wsf.field('Longitude', 'C', '40')
    wsf.field('Latitude', 'C', '40')
    for i in range(len(meshl)):
        poly = meshl[i][1]
        b = poly.boundary
        x = []
        y = []
        for i in range(len(b.xy[0])):
            # y.append(b.xy[0][i] / 1000 / 3600)
            # x.append(b.xy[1][i] / 1000 / 3600)
            y.append(b.xy[0][i])
            x.append(b.xy[1][i])
            r = numpy.array([x, y])
            t = r.T
            wsf.line(parts=[t])
            wsf.record(x, y)
    wsf.save('Result\\MeshShapeFile')

def writematchlineshape(linklist):
    wsf = shapefile.Writer(shapefile.POLYLINE)
    wsf.autoBalance = 1
    wsf.field('Longitude', 'C', '40')
    wsf.field('Latitude', 'C', '40')
    for i in range(len(linklist)):
        link = linklist[i]
        r = numpy.array([link[0], link[1]])
        t = r.T
        wsf.line(parts=[t])
        wsf.record(link[0], link[1])
    wsf.save('Result\\MatchLineShapeFile')

def writematchpointshape(linklist):
    wsf = shapefile.Writer(shapefile.POINT)
    wsf.autoBalance = 1
    wsf.field('Longitude', 'C', '40')
    wsf.field('Latitude', 'C', '40')
    for i in range(len(linklist)):
        link = linklist[i]
        p = list(zip(*[link[0], link[1]]))

        wsf.point(p[0][0], p[0][1])
        wsf.record(p[0][0], p[0][1])
    wsf.save('Result\\MatchPointShapeFile')

def writerectshape(rect):
    wsf = shapefile.Writer(shapefile.POLYLINE)
    wsf.autoBalance = 1
    wsf.field('Longitude', 'C', '40')
    wsf.field('Latitude', 'C', '40')
    for i in range(len(rect)):
        re=rect[i]
        r = numpy.array([re[0][0][0], re[0][0][1]])
        t = r.T
        wsf.line(parts=[t])
        wsf.record(re[0][0][0], re[0][0][1])
    wsf.save('Result\\TrackShapeFile')

    wsf1 = shapefile.Writer(shapefile.POLYLINE)
    wsf1.autoBalance = 1
    wsf1.field('Longitude', 'C', '40')
    wsf1.field('Latitude', 'C', '40')
    for i in range(len(rect)):
        re=rect[i]
        p1 = list(zip(*re[0][1]))
        r1 = numpy.array([p1[0], p1[1]])
        t1 = r1.T
        wsf1.line(parts=[t1])
        wsf1.record(p1[0], p1[1])
    wsf1.save('Result\\Rect1ShapeFile')

    wsf2 = shapefile.Writer(shapefile.POLYLINE)
    wsf2.autoBalance = 1
    wsf2.field('Longitude', 'C', '40')
    wsf2.field('Latitude', 'C', '40')
    for i in range(len(rect)):
        re=rect[i]
        p2 = list(zip(*re[0][2]))
        r2 = numpy.array([p2[0], p2[1]])
        t2 = r2.T
        wsf2.line(parts=[t2])
        wsf2.record(p2[0], p2[1])
    wsf2.save('Result\\Rect2ShapeFile')


def writeintersectshape(result):
    wsf = shapefile.Writer(shapefile.POLYLINE)
    wsf.autoBalance = 1
    wsf.field('Longitude', 'C', '40')
    wsf.field('Latitude', 'C', '40')
    for i in range(len(result)):
        links = result[i]
        for j in range(len(links)):
            link=links[j]
            r = numpy.array([link[0], link[1]])
            t = r.T
            wsf.line(parts=[t])
            wsf.record(link[0], link[1])
    wsf.save('Result\\IntersectLinkShapeFile')


def writeintersectpointshape(result):
    wsf = shapefile.Writer(shapefile.POINT)
    wsf.autoBalance = 1
    wsf.field('Longitude', 'C', '40')
    wsf.field('Latitude', 'C', '40')
    for i in range(len(result)):
        links = result[i]
        for j in range(len(links)):
            link=links[j]
            p = list(zip(*[link[0], link[1]]))

            wsf.point(p[0][0], p[0][1])
            wsf.record(p[0][0], p[0][1])
    wsf.save('Result\\IntersectPointShapeFile')