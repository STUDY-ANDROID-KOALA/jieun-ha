""" itertools 활용한 버전
from itertools import permutations

def solution(dots):
    for a, b, c, d in permutations(dots, 4):

        dx1 = b[0] - a[0]
        dy1 = b[1] - a[1]
        dx2 = d[0] - c[0]
        dy2 = d[1] - c[1]

        if dx1 * dy2 == dx2 * dy1:
            return 1
    return 0
"""

def solution(dots):
    n = len(dots)
    r = 4
    path = [0] * r
    visit = [0] * n
    path_list = []

    def permutation(depth):
        if depth == r:
            path_list.append(path.copy())
            return
        for i in range(n):
            if visit[i]:
                continue
            visit[i] = 1
            path[depth] = i
            permutation(depth + 1)
            visit[i] = 0

    permutation(0)

    for j in path_list:
        a, b, c, d = j
        x1, y1 = dots[a]
        x2, y2 = dots[b]
        x3, y3 = dots[c]
        x4, y4 = dots[d]

        if (y2 - y1) * (x4 - x3) == (y4 - y3) * (x2 - x1):
            return 1
    return 0
