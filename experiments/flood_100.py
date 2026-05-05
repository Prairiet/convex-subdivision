from polygenerator import random_polygon, random_convex_polygon
import matplotlib.pyplot as plt
import numpy as np
import time

total_edges = 0
for _ in range(100):
    poly = random_polygon(100) # generated in counterclockwise order
    edges = []
    removed_edges = []

    def orient(a, b, p):
        a = np.array(a)
        b = np.array(b)
        p = np.array(p)
        det = np.linalg.det([b - a, p - a])
        if det > 0:
            return 1 # ccw
        elif det < 0:
            return -1 # cw
        else:
            return 0
    def intersect(a, b, x, y):
        if a == x or a == y or b == x or b == y: # consider shared points as non-intersecting
            return False
        else:
            return orient(a, b, x) != orient(a, b, y) and orient(x, y, a) != orient(x, y, b)

    def render():
        try:
            while True:
                removed_edges.remove("placeholder")
        except ValueError:
            pass
        es = []
        for t in edges: es.append((poly[t[0]], poly[t[1]]))

        rs = []
        for t in removed_edges: rs.append((poly[t[0]], poly[t[1]]))

        poly_copy = poly.copy()
        poly_copy.append(poly[0])
        xs, ys = zip(*(poly_copy))

        plt.gca().set_aspect("equal")
        plt.plot(xs, ys, "o-")
        for e in es:
            exs, eys = zip(*(e))
            plt.plot(exs, eys, "c-")
        for r in rs:
            rxs, rys = zip(*(r))
            plt.plot(rxs, rys, "c:")
        plt.plot(xs[0], ys[0], "w.")
        plt.plot([xs[0], xs[1]], [ys[0], ys[1]], "w:")
        plt.show()

    # ear clipping algorithm
    status = np.zeros(len(poly), dtype=int) # 0 / 1 / 2 / 3 = concave / convex / ear / clipped
    neighbours = np.zeros((len(poly), 2), dtype=int)
    for i in range(len(poly)):
        neighbours[i][0] = (i + 1) % len(poly) # ccw neighbour, aka next
        neighbours[i][1] = (i - 1) % len(poly) # cw neighbour, aka prev

    def update_status(index):
        next_i = neighbours[index][0] # get ccw neighbour
        prev_i = neighbours[index][1] # get cw neighbour
        if orient(poly[prev_i], poly[index], poly[next_i]) == 1: # check if it's convex
            status[index] = 1
            if ((orient(poly[prev_i], poly[next_i], poly[neighbours[prev_i][1]]) == -1 or orient(poly[prev_i], poly[next_i], poly[neighbours[prev_i][0]]) == 1) 
            and (orient(poly[prev_i], poly[next_i], poly[neighbours[next_i][1]]) == 1 or orient(poly[prev_i], poly[next_i], poly[neighbours[next_i][0]]) == -1)):
                return # if both are offside, diagonal isnt internal
            edge_i = index
            while edge_i != prev_i: # iterate through all edges, except the two connecting our index and its neighbours
                edge_i = neighbours[edge_i][0]
                if intersect(poly[prev_i], poly[next_i], poly[edge_i], poly[neighbours[edge_i][0]]): # if an edge intersects, it's not an ear
                    return
            status[index] = 2
        else:
            status[index] = 0

    for i in range(len(poly)):
        update_status(i)

    clipped_count = 0

    def clip_ear(ear_i):
        next_i = neighbours[ear_i][0]
        prev_i = neighbours[ear_i][1]
        # clip the ear
        status[ear_i] = 3
        removed_edges.append(edges.pop())
        edges.append((prev_i, next_i))
        # connect neighbours
        neighbours[prev_i][0] = next_i
        neighbours[next_i][1] = prev_i
        # update status
        update_status(next_i)
        update_status(prev_i)

    while True:
        # find an ear
        ear_i = 0
        try:
            while status[ear_i] != 2:
                ear_i += 1
        except IndexError:
            break
        next_i = neighbours[ear_i][0]
        prev_i = neighbours[ear_i][1]
        edges.append("placeholder")
        clip_ear(ear_i)
        # if neighbours are ears and onside, clip them too
        iterate = True
        next_two = [ear_i, next_i]
        prev_two = [ear_i, prev_i]
        while iterate:
            iterate = False
            if (status[prev_i] == 2
            and orient(poly[prev_two[-2]], poly[prev_two[-1]], poly[neighbours[prev_i][1]]) == -1 # make sure it's still onside
            and orient(poly[neighbours[prev_i][1]], poly[next_two[1]], poly[next_two[0]]) == -1): # make sure we can still come back around
                clip_ear(prev_i)
                prev_i = neighbours[prev_i][1]
                prev_two.pop(0)
                prev_two.append(prev_i)
                iterate = True
            if (status[next_i] == 2
            and orient(poly[next_two[-2]], poly[next_two[-1]], poly[neighbours[next_i][0]]) == 1 # ditto above
            and orient(poly[neighbours[next_i][0]], poly[prev_two[1]], poly[prev_two[0]]) == 1):
                clip_ear(next_i)
                next_i = neighbours[next_i][0]
                next_two.pop(0)
                next_two.append(next_i)
                iterate = True
    # remove edges that are on the polygon's edge
    for i in range(len(edges) - 1, -1, -1):
        index_first = (edges[i][0] + len(poly)) % len(poly)
        index_second = (edges[i][1] + len(poly)) % len(poly)
        if index_first == index_second + 1 or index_second == index_first + 1:
            edges.pop(i)
    # remove duplicate edges
    # sort each edge
    for i in range(len(edges)):
        if edges[i][0] > edges[i][1]:
            edges[i] = (edges[i][1], edges[i][0])
    edges = np.unique(edges, axis=0)

    total_edges += len(edges)

print("runtime:", time.process_time())
print("average edges:", total_edges / 100)