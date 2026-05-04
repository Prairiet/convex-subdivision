from polygenerator import random_polygon
import matplotlib.pyplot as plt
import numpy as np

poly = random_polygon(12) # generated in counterclockwise order
edges = []

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
    if a == x or a == y or b == x or b == y:
        return False
    else:
        return orient(a, b, x) != orient(a, b, y) and orient(x, y, a) != orient(x, y, b)

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
        if ((orient(poly[prev_i], poly[next_i], poly[neighbours[prev_i][1]]) != 1 or orient(poly[prev_i], poly[next_i], poly[neighbours[prev_i][0]]) != -1) 
        and (orient(poly[prev_i], poly[next_i], poly[neighbours[next_i][1]]) != -1 or orient(poly[prev_i], poly[next_i], poly[neighbours[next_i][0]]) != 1)):
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

for i in range(len(poly) - 3):
    # find an ear
    ear_i = 0
    try:
        while status[ear_i] != 2:
            ear_i += 1
    except IndexError:
        print("index err. force quit!")
        print("orientation test:")
        for i in range(len(poly)):
            print(orient(poly[i - 1], poly[i], poly[(i + 1) % len(poly)]))
        break
    # get its neighbours
    next_i = neighbours[ear_i][0]
    prev_i = neighbours[ear_i][1]
    # clip the ear
    status[ear_i] = 3
    edges.append((prev_i, next_i))
    # connect neighbours
    neighbours[prev_i][0] = next_i
    neighbours[next_i][1] = prev_i
    # update status
    update_status(next_i)
    update_status(prev_i)

# clean up 100% unneeded edges
orientations = []
removed_edges = []
for i in range(len(poly)):
    orientations.append(orient(poly[i - 1], poly[i], poly[(i + 1) % len(poly)]))
for i in range(len(edges) - 1, -1, -1):
    if orientations[edges[i][0]] == 1 and orientations[edges[i][1]] == 1:
        removed_edges.append(edges.pop(i))

es = []
for t in edges: es.append((poly[t[0]], poly[t[1]]))

poly.append(poly[0])

xs, ys = zip(*(poly))

plt.gca().set_aspect("equal")
plt.plot(xs, ys, "o-")
for e in es:
    exs, eys = zip(*(e))
    plt.plot(exs, eys, "c-")
plt.plot(xs[0], ys[0], "ro")
plt.show()
