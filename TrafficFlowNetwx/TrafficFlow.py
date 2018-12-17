
#!/usr/bin/env python 3.6
# -*- coding: utf-8 -*-
# @Time    : 12/3/18 16:31
# @Author  : Yam
# @Site    : 
# @File    : TrafficFlow.py
# @Software: PyCharm

import networkx as nx
import random
import matplotlib.pyplot as plt


def gengraph(n, prob):
    g = nx.Graph()
    points = list(range(0, n))
    g.add_nodes_from(points)
    pointdic = genpoints(g, points)
    edgedic = genedges(g, points, prob)
    return g


def genpoints(graph, points):
    pointdic = dict()
    for p in points:
        x = random.uniform(280, 1050)
        y = random.uniform(220, 620)
        graph.nodes[p]['pos'] = tuple((x, y))
        pointdic[p] = tuple((x, y))
    return pointdic


def genedges(graph, points, prob):
    edgedic = dict()
    for p in points:
        for nextp in points:
            if p == nextp:
                continue
            else:
                iscon = connectprob(prob)
                if iscon:
                    graph.add_edge(p, nextp)
                    graph.add_edge(nextp, p)
                    if p in edgedic:
                        edges = edgedic.get(p)
                        edges.append(nextp)
                        edgedic[p] = edges
                    else:
                        edges = list()
                        edges.append(nextp)
                        edgedic[p] = edges
    return edgedic


def genposition(graph):
    for nodenum, attrs in graph.nodes.items():
        x = random.uniform(280, 1050)
        y = random.uniform(220, 620)
        graph.nodes[nodenum]['pos'] = tuple((x, y))


def connectprob(prob):
    c = random.random()
    if c <= prob:
        return True
    else:
        return False


def report(graph, path):
    zero = 0
    one = 0
    two = 0
    thr = 0
    thrp = 0
    sumdis = 0
    for point, edges in path.items():
        for connect, dis in edges.items():
            if dis == 0:
                zero = zero+1
            elif dis == 1:
                one = one+1
            elif dis == 2:
                two = two+1
            elif dis == 3:
                thr = thr+1
            elif dis > 3:
                thrp = thrp+1
                sumdis = sumdis+dis
    # one = one/2
    # two = two/2
    # thr = thr/2
    # thrp = thrp/2
    # sumdis = sumdis/2+one+two*2+thr*3
    # avgdis = sumdis/len(graph.edges)
    # print(len(graph.edges))
    # degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    # dmax = max(degree_sequence)
    # dmin = min(degree_sequence)
    # gb = len(graph.edges)/sumdis

    one = one
    two = two
    thr = thr
    thrp = thrp
    sumdis = sumdis + one + two * 2 + thr * 3
    avgdis = sumdis / (one+two+thr)
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    dmax = max(degree_sequence)
    dmin = min(degree_sequence)
    gb = len(graph.edges) / sumdis

    print("zero:", zero)
    print("one:", one)
    print("two:", two)
    print("three:", thr)
    print("three+:", thrp)

    print("sum of distance:", sumdis)
    print("average of distance:", avgdis)
    print("max degree:", dmax)
    print("min degree:", dmin)
    print("gridlock bound:", gb)
    print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t"
          .format(zero, one, two, thr, thrp, sumdis, round(avgdis, 4), dmax, dmin, round(gb, 2)))


def drawgraph(graph):
    nodeoptions = {
        'node_color': 'black',
        'node_size': 5,
    }
    edgeoptions = {
        'edge_color': 'black',
        'width': 1,
        'alpha': 0.1
    }
    pos = dict(nx.get_node_attributes(graph, 'pos'))
    nx.draw_networkx_nodes(graph, pos, **nodeoptions)
    nx.draw_networkx_edges(graph, pos, **edgeoptions)
    plt.axis('off')
    plt.show()


def drawsubgraph(graph, path, pointnum):
    nodeoptions = {
        'node_color': 'black',
        'node_size': 10,
        'alpha': 0.8
    }
    edgeoptions = {
        'edge_color': 'black',
        'width': 1,
        'alpha': 0.1
    }
    plt.close('all')
    fig, ax = plt.subplots(figsize=(15, 8))
    img = plt.imread("map.png")
    ax.imshow(img, extent=[0, 1200, 0, 800])
    pos = dict(nx.get_node_attributes(graph, 'pos'))

    # pointnum = 0
    nx.draw_networkx_nodes(graph, pos, **nodeoptions)
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=[pointnum],
                           node_color='red',
                           node_size=60)
    onelist = list()
    twolist = list()
    thrlist = list()
    edges = path[pointnum]
    for nextp, dis in edges.items():
        if dis == 1:
            onelist.append(nextp)
        elif dis == 2:
            twolist.append(nextp)
        elif dis == 3:
            thrlist.append(nextp)
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=onelist,
                           node_color='magenta',
                           node_size=30)
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=twolist,
                           node_color='yellow',
                           node_size=10)
    nx.draw_networkx_nodes(graph, pos,
                           nodelist=thrlist,
                           node_color='cyan',
                           node_size=10)
    nx.draw_networkx_edges(graph, pos, **edgeoptions)
    plt.axis('off')
    fig.canvas.draw()


def dyndraw(graph, path):
    start = 0
    plt.ion()
    while True:
        start = start + 1
        start = start % len(graph.nodes)
        # print(start)
        drawsubgraph(graph, path, start)
        plt.waitforbuttonpress()


def main():
    num = 1000
    pro = 0.9
    # g = gengraph(num, pro)
    g = nx.gnp_random_graph(num, pro)
    genposition(g)
    path = dict(nx.all_pairs_dijkstra_path_length(g))
    # print(path)
    report(g, path)
    # drawgraph(g)
    # dyndraw(g, path)


if __name__ == "__main__":
    main()
