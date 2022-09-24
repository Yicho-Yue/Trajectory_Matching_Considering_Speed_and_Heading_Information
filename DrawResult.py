import random
import matplotlib.pyplot as plt


def drawmesh(meshl):
    c = ['m']
    for i in range(len(meshl)):
        k = random.randint(0, len(c)-1)
        col = c[k]
        poly = meshl[i][1]
        b = poly.boundary
        y1 = (b.xy[0][3]) / 1000 / 3600
        x1 = b.xy[1][3] / 1000 / 3600
        plt.text(x1, y1, meshl[i][0], color=col)
        x = []
        y = []
        for i in range(len(b.xy[0])):
            y.append(b.xy[0][i] / 1000 / 3600)
            x.append(b.xy[1][i] / 1000 / 3600)
        plt.plot(x, y, '-', color=col, linewidth=1)

def drawoutrect(rect):
    p = list(zip(*rect[0][1]))
    p1 = list(zip(*rect[0][2]))
    plt.plot(p[0], p[1], ':', color='g', linewidth=2)
    plt.plot(p1[0], p1[1], ':', color='r', linewidth=2)
    plt.plot(rect[0][0][0], rect[0][0][1], '-.', color='gray')

def drawmatchlink(linklist, c):
    for i in range(len(linklist)):
        links = linklist[i]
        plt.plot(links[0], links[1], '-', color=c, linewidth=4)
        p = list(zip(*[links[0], links[1]]))
        plt.plot(p[0][0], p[0][1], 'ro', color='b', markersize=5)
        plt.plot(p[-1][0], p[-1][1], 'ro', color='b', markersize=3)


