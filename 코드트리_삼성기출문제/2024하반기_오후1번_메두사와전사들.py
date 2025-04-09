"""
NxN 크기의 마을(도로는 0, 도로가 아닌 곳 1)
메두사 집 (S_r, S_c)
공원 (E_r, E_c)

집에서 공원까지 산책
오직 도로만을 따라 최단 경로로 공원까지 이동
- 메두사의 집과 공원은 항상 도로 위에 있음
- 집과 공원의 좌표는 항상 다름

M명의 전사들이 메두사를 잡기 위해 마을에 도착
전사 초기 위치(r_i, c_i)
메두사를 향해 최단 경로로 이동
- 도로와 비도로를 구분하지 않고 어느 칸이든 이동 가능
- 메두사의 집과 전사의 초기 위치가 같은 경우 없음

[1] 메두사의 이동
- 도로(0)를 따라 한 칸 이동, 공원까지 최단 경로 따르기
- 메두사가 이동한 칸에 전사가 있는 경우 전사 사라짐
- 집으로부터 공원까지 최단경로가 여러개라면 "상 -> 하 -> 좌 -> 우"의 우선순위
- 메두사의 집에서 공원까지 도달하는 경로가 없을 수 있음

[2] 메두사의 시선
- 상, 하, 좌, 우 하나의 방향을 선택해 바라봄
- 바라보는 방향으로 90도 시야각(범위 내 전사들 바라볼 수 있음)
- 다른 전사에 가려진 경우 메두사에게 보이지 않음
    ex. 상하좌우 대각선 8방향 나눴을 때 메두사로부터 8방향 중 한 방향에 전사가 위치한 경우,
        그 전사가 메두사와 동일한 방향으로 바라본 범위에 포함된 모든 칸은 보이지 않음
- 메두사가 본 전사들은 모두 돌로 변해 움직일 수 없음
- 해당 턴에서 움직이지 못하고 다음 턴에 돌에서 풀려남
- 상, 하, 좌, 우 중 가장 전사를 많이 볼 수 있는 방향을 바라봄
- 같은 수의 전사를 바라볼 수 있는 방향이 여러개인 경우 상->하->좌->우의 우선순위로 방향 결정

[3] 전사들의 이동
- 돌로 변하지 않은 경우 최대 두 칸 이동
- 전사들끼리 같은 칸에 있을 수 있음
- 격자 바깥으로 못 감
- 메두사 시야에 있는 곳으로 못감
1. 메두사와의 거리를 줄일 수 있는 방향(우선순위 상하좌우)
2. 메두사와 거리를 줄일 수 있는 방향으로 한칸 더(우선순위 좌우상하)

[4] 전사의 공격
- 메두사와 같은 칸에 도달한 전사는 사라짐
- 최단경로 게산할 때 맨해튼 거리

입력 :
마을의 크기 N, 전사의 수 M
메두사의 집의 위치 정보 s_r, s_c와 공원의 위치 정보 e_r, e_c
다음 줄에 M명의 전사들의 좌표 a1_r, a1_c, a2_r, a2_c, ... am_r, am_c
N줄에 마을 도로 정보

출력 :
4단계 반복하며 메두사가 공원에 도달할 때까지 매 턴마다,
1. 해당 턴에서 모든 전사가 이동한 거리의 합
2. 메두사로 인해 돌이 된 전사의 수
3. 메두사를 공격한 전사의 수
공백 두고 차례대로 출력
메두사가 공원에 도착하는 턴에는 0 출력
메두사의 집으로부터 공원까지 이어지는 도로가 존재하지 않는 경우 -1 출력

아이디어 :
최단 경로 -> dfs
"""
from collections import deque

# 상, 우상, 우, 우하, 하, 좌하, 좌, 좌상
di = [-1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, 1, 1, 1, 0, -1, -1, -1]

# 메두사가 가는 길 dfs로 탐색
def find_route(si, sj, ei, ej):
    q = deque()
    visited = [[0] * n for _ in range(n)]

    q.append((si, sj))
    visited[si][sj] = (si, sj) # 직전 위치 저장

    while q:
        ci, cj = q.popleft()

        if (ci, cj) == (ei, ej): # 목적지 도착 시 경로 저장
            route = []
            ci, cj = visited[ci][cj]
            while (ci, cj) != (si, sj):
                route.append((ci, cj))
                ci, cj = visited[ci][cj]

            return route[::-1]

        for dx, dy in (-1,0),(1,0),(0,-1),(0,1):
            ni = ci + dx
            nj = cj + dy

            # 경계를 넘어가지 않고, 직전 위치가 저장되어 있지 않으면서, 도로(0)인 곳
            if 0 <= ni < n and 0 <= nj < n and visited[ni][nj] == 0 and town[ni][nj] == 0:
                visited[ni][nj] = (ci, cj)
                q.append((ni, nj))

    return -1


# tv, tstone = make_stone(warrior_arr, mi, mj, direction)
def make_stone(warrior_count_arr, medusa_i, medusa_j, dr):
    v = [[0] * n for _ in range(n)] # 메두사 시선 1, 전사에 가려진 곳 2, 빈 땅 0
    cnt = 0  # 시야에 걸리는 전사 수

    # [1] direction 방향으로 전사가 1명 이상인 곳을 만날 때까지 1 표시, 이후 좌표 2 표시
    ni = medusa_i + di[dr]
    nj = medusa_j + dj[dr]
    while 0 <= ni < n and 0 <= nj < n:
        v[ni][nj] = 1  # 메두사 시선

        if warrior_count_arr[ni][nj] > 0:  # 전사가 있는 경우
            cnt += warrior_count_arr[ni][nj]
            ni = ni + di[dr]
            nj = nj + dj[dr]
            mark_line(v, ni, nj, dr)  # 전사에 가려진 곳 표시
            break

        ni = ni + di[dr]
        nj = nj + dj[dr]

    # [2] dr-1, dr+1 방향으로 동일 처리, 대각선 원점 잡고 dr 방향 처리
    for org_dr in ((dr - 1) % 8, (dr + 1) % 8): # dr = 0(상)인 경우, 좌상은 7, 우상은 1 나옴
        si, sj = mi + di[org_dr], mj + dj[org_dr] # 첫 대각선 위치부터 체크

        while 0 <= si < n and 0 <= sj < n:
            if v[si][sj] == 0 and warrior_count_arr[si][sj] > 0: # 첫번째에서 전사 만난 경우
                v[si][sj] = 1
                cnt += warrior_count_arr[si][sj] # 돌로 만든 전사 수 합
                mark_safe(v, si, sj, dr, org_dr) # 전사가 바라보는 방향 org_dr로 시야 확장
                break

            # 첫번째에서 전사 만나지 않은 경우 - 직선 탐색
            ci, cj = si, sj
            while 0 <= ci < n and 0 <= cj < n:
                if v[ci][cj] == 0: # 처음 계산하는 빈 땅인 경우
                    v[ci][cj] = 1
                    if warrior_count_arr[ci][cj] > 0: # 전사 만난 경우
                        cnt += warrior_count_arr[ci][cj]
                        mark_safe(v, ci, cj, dr, org_dr) # 전사가 바라보는 방향 org_dr로 시야 확장
                        break
                else: # 빈 땅이 아닌 경우 다른 방향에서 이미 처리된 곳이므로 중지
                    break
                ci, cj = ci+di[dr], cj+dj[dr]

            si, sj = si + di[org_dr], sj + dj[org_dr]

    return v, cnt

# mark_line(v, ni, nj, dr)
def mark_line(v, ci, cj, dr):
    while 0 <= ci < n and 0 <= cj < n:
        v[ci][cj] = 2  # 전사에 가려진 곳
        ci, cj = ci + di[dr], cj + dj[dr]  # 해당 방향으로 한 칸 이동

# 전사를 기준으로 시야 확장. 대각선 + 직선 형태로 퍼져 나감
def mark_safe(v, si, sj, dr, org_dr):
    # [1] 직선 방향
    ci, cj = si + di[dr], sj + dj[dr]
    mark_line(v, ci, cj, dr)

    # [2] 바라보는 방향으로 한줄씩 표시
    ci, cj = si + di[org_dr], sj + dj[org_dr]
    while 0 <= ci < n and 0 <= cj < n:
        mark_line(v, ci, cj, dr)
        ci, cj = ci + di[org_dr], cj + dj[org_dr]

def move_men(v, me_i, me_j):
    # (상하좌우), (좌우상하) 메두사 시야가 아니면 (!=1)
    move, attk = 0, 0

    for dirs in (((-1,0),(1,0),(0,-1),(0,1)), ((0,-1),(0,1),(-1,0),(1,0))):
        for idx in range(len(men)-1,-1,-1):
            ci,cj = men[idx]
            if v[ci][cj]==1:                # 메두사 시야면 얼음!
                continue

            dist = abs(me_i-ci) + abs(me_j-cj)    # 현재 거리
            for dii,djj in dirs:
                ni,nj = ci + dii, cj + djj
                # 범위내 메두사 시야 아니고 현재보다 줄어드는 방향이면 (상하좌우 우선순위로 이동)
                if 0<=ni<n and 0<=nj<n and v[ni][nj]!=1 and dist>abs(me_i-ni)+abs(me_j-nj):
                    if (ni,nj)==(me_i,mj): # 메두사 만나면 공격하고 사망
                        attk+=1
                        men.pop(idx)
                    else:
                        men[idx]=[ni,nj]
                    move+=1
                    break
    return move, attk

##################################################################
##################################################################

n, m = map(int, input().split())
home_r, home_c, park_r, park_c = map(int, input().split())
men_list = list(map(int, input().split()))
town = [list(map(int, input().split())) for _ in range(n)]

men = []
for i in range(0, m*2, 2):
    men.append([men_list[i], men_list[i+1]])

route = find_route(home_r, home_c, park_r, park_c)

if route == -1:
    print(-1)
else:
    # [1] 메두사의 이동 : 지정된 최단거리로 한 칸씩 이동
    for mi, mj in route:
        move_count = 0
        attack_count = 0

        for i in range (len(men) - 1, -1, -1): # 삭제 시 역순으로 접근
            if men[i] == [mi, mj]:  # 메두사와 같은 좌표일 때
                men.pop(i)

        #  [2] 메두사의 시선 : 상하좌우 네 방향 가장 많이 돌로 만들 수 있는 방향
        # => sight[]에 표시해서 이동 시 참조(메두사 시선 1, 전사에 가려진 곳 2, 빈 땅 = 0)
        # warrior_arr[][] : 지도에 있는 전사 수 표시

        warrior_arr = [[0] * n for _ in range(n)]
        for ti, tj in men:
            warrior_arr[ti][tj] += 1

        max_stone = -1
        sight = []

        for direction in (0, 4, 6, 2): # 상하좌우 순서로 처리
            tv, tstone = make_stone(warrior_arr, mi, mj, direction)
            if max_stone < tstone:
                max_stone = tstone
                sight = tv

        # [3] 전사들의 이동(한 칸씩 두번) : 메두사 있는 경우 공격
        move_count, attack_count = move_men(sight, mi, mj)

        print(move_count, max_stone, attack_count)
    print(0)

