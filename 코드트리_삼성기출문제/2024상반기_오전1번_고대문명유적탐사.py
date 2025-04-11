import copy

from collections import deque

def rotate_90(start_top_i, start_top_j, end_bottom_i, end_bottom_j, arr):
    result = [row[:] for row in arr]

    size = end_bottom_i - start_top_i + 1

    for i in range(size):
        for j in range(size):
            result[start_top_i + j][start_top_j + size - 1 - i] = arr[start_top_i + i][start_top_j + j]

    print(f"({start_top_i}, {start_top_j})를 기준으로 90도 회전" + str(result))
    return result

def rotate_180(start_top_i, start_top_j, end_bottom_i, end_bottom_j, arr):
    result = [row[:] for row in arr]

    size = end_bottom_i - start_top_i + 1

    for i in range(size):
        for j in range(size):
            result[start_top_i + size - 1 - i][start_top_j + size - 1 - j] = arr[start_top_i + i][start_top_j + j]

    return result

def rotate_270(start_top_i, start_top_j, end_bottom_i, end_bottom_j, arr):
    result = [row[:] for row in arr]
    size = end_bottom_i - start_top_i + 1

    for i in range(size):
        for j in range(size):
            result[start_top_i + size - 1 - j][start_top_j + i] = land[start_top_i + i][start_top_j + j]

    return result

def find_first_treasure_type(treasure_type, arr):
    for i in range(0, 5, 1):
        for j in range(0, 5, 1):
            if arr[i][j] == treasure_type:
                return i, j
    return -1, -1

direction_x = [-1, 1, 0, 0]
direction_y = [0, 0, -1, 1]

def find_treasure_bfs(treasure_type, arr):
    print("아래 배열에 대한 bfs 실행됨!")
    print(arr)

    q = deque()
    si, sj = find_first_treasure_type(treasure_type, arr)
    if si == -1 or sj == -1:
        return 0

    q.append((si, sj))
    v = [[0] * 5 for _ in range(5)]
    result = []

    v[si][sj] = 1
    arr[si][sj] = 0
    result.append((si, sj))

    while q:
        i, j = q.popleft()

        # 상하좌우 탐색
        for direction in range(4):
            nx = i + direction_x[direction]
            ny = j + direction_y[direction]

            if 0 <= nx < 5 and 0 <= ny < 5 and v[nx][ny] == 0 and arr[nx][ny] == treasure_type:
                q.append((nx, ny))
                v[nx][ny] = 1 # 방문 표시
                arr[nx][ny] = 0 # 조각 회수
                result.append((nx, ny))

    if len(result) < 3:
        return 0
    else:
        return len(result)

###############################################################
###############################################################
repeat, piece = map(int, input().split())
land = [list(map(int, input().split())) for _ in range(5)]
wall = list(map(int, input().split()))

total_score = 0

# 선택한 3x3 격자에 따른 회전 각도(90도 0, 180도 1, 270도 2) 3차원 배열에 1차 유적 가치 저장
first_treasure_value = [[[0] * 3 for s in range(3)] for rotate_num in range(3)]

for _ in range(repeat):
    max_score = -1
    best_ai, best_aj, best_rot = -1, -1, -1
    best_map = []

    # [1] 3x3 격자 선택 (왼쪽 위 좌표 기준 9가지)
    for ai in range(3):
        for aj in range(3):
            # [2] 선택한 격자마다 90도, 180도, 270도 회전(3가지)
            array_90 = rotate_90(ai, aj, ai + 2, aj + 2, land)
            array_180 = rotate_180(ai, aj, ai + 2, aj + 2, land)
            array_270 = rotate_270(ai, aj, ai + 2, aj + 2, land)

            # [3] 회전한 5x5 유적지에 대해 유물 획득되지 않을 때까지 bfs
            for rot_idx, arr in enumerate([array_90, array_180, array_270]):
                temp = [arr[:] for _ in arr]
                score = 0
                for treasure_type in range(1, piece + 1):
                    while True:
                        got = find_treasure_bfs(treasure_type, temp)
                        if got == 0:
                            break
                        score += got

                if score > max_score:
                    max_score = score
                    best_ai, best_aj, best_rot = ai, aj, rot_idx
                    best_map = [row[:] for row in arr]

    total_score += max_score
    land = best_map

    if total_score == 0:
        break

    # [4] 연쇄 획득
    while True:
        total = 0
        for i in range(1, 8):
            while True:
                r = find_treasure_bfs(i, land)
                if r == 0:
                    break
                total += r

        if total == 0:
            break

        for i in range(5):
            for j in range(5):
                if land[i][j] == 0:
                    land[i][j] = wall[i]

print(total_score)
print(*land)