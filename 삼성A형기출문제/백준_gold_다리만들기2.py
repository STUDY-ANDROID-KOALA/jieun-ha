""" 17472
모든 섬을 다리로 연결
NxM 크기의 지도
섬 : 연결된 땅이 붙어있는 덩어리
색칠되어 있는 칸 : 땅
색칠 안되어 있는 칸 : 바다
다리
- 바다에만 건설 가능
- 다리의 길이는 격자에서 차지하는 칸의 수
- 다리를 연결해 모든 섬을 연결
- 다리의 방향은 바뀔 수 없음
- 다리의 길이는 2 이상이어야 함
- 교차하는 다리의 경우 각 칸이 다리 길이에 모두 포함되어야 함

입력 :
첫째 줄 - 세로 크기 n, 가로 크기 m
둘째 줄 - n개의 줄에 지도 정보(0은 바다, 1은 땅)

출력 :
모든 섬을 연결하는 다리 길이의 최솟값
모든 섬을 연결하는 것이 불가능하면 -1

아이디어 :
1. 연결되어 있는 땅을 찾아 섬으로 저장
- (0, 0)부터 순서대로 탐색
- 기준 좌표에 대해 (i+1,j), (i,j+1), (i, j-1), (i-1,j)에 1(땅)이 있는 경우 해당 좌표에 값 넣기
    첫번째 섬이라면 10, 두번째 섬이라면 11, 세번째 섬이라면 12.. 이런 식으로(땅이 원래 1이니까 10부터 시작하는 걸로)
    or
    그래프를 만들자
- 재귀적으로 찾자 지도 외곽선을 넘지 않는 선에서(재귀 종료 조건) + 이미 10이면 종료
2. 재귀적으로..
- 다리는 서로 다른 섬의 땅이 같은 행 or 같은 열에 있어야 연결 가능
- if 10인 좌표인 경우 같은 행이나 열에 0과 10이 아닌 수가 있다면 다리 연결
    - 연결된 다리 없는 경우
    - 연결된 경우 그 다음 좌표 탐색. 10인 좌표이면 return

** 정답 아이디어 :
1. bfs로 섬의 영역별 좌표 구하기
2. 간선 제작 : 좌표를 순환하며 상하좌우로 다리를 쭉 뻗는 방식의 다리 제작(자기 자신or지도밖으로 벗어나면 다음 다리 제작)
3. MST(크루스칼)로 다리 길이의 최솟값 계산
"""
from collections import deque
dx = [0, 1, 0, -1]
dy = [1, 0, -1, 0]

n, m = map(int, input().split())
country_map = [list(map(int, input().split())) for _ in range(n)]
visited = [[False] * m for _ in range(n)]

# 인접한 애들끼리 분리
def bfs_land(i, j, mark):
    q = deque()
    q.append((i, j))

    visited[i][j] = True
    country_map[i][j] = mark

    while q:
        x, y = q.popleft()
        for direction in range(4):
            nx = x + dx[direction]
            ny = y + dy[direction]
            if 0 <= nx < n and 0 <= ny < m and not visited[nx][ny] and country_map[nx][ny] == 1:
                country_map[nx][ny] = mark
                q.append((nx, ny))
                visited[nx][ny] = True

# 인접한 애들에게 섬 이름 지어주기(1부터 섬 개수 k까지)
def mark_land():
    mark = 1
    for i in range(n):
        for j in range(m):
            if country_map[i][j] and visited[i][j] == False:
                bfs_land(i, j, mark)
                mark += 1

edges = [] # 거리, 시작 섬, 종료 섬

# 지도에서 섬 만나면 상하좌우로 bfs 돌려서 바다 0을 따라가다가 다른 섬 만나면 다리로 저장
# 다리 길이 최소 2
def find_bridges():
    for i in range(n):
        for j in range(m):
            if country_map[i][j] > 0: # 섬인 경우
                start_island = country_map[i][j]
                for direction in range(4):
                    q = deque()
                    q.append((i, j, 0)) # 시작 위치, 거리
                    visited_bridge = [[False] * m for _ in range(n)]
                    visited_bridge[i][j] = True

                    while q:
                        x, y, dist = q.popleft()
                        nx = x + dx[direction]
                        ny = y + dy[direction]

                        if not (0 <= nx < n and 0 <= ny < m):
                            continue
                        if visited_bridge[nx][ny]:
                            continue
                        visited_bridge[nx][ny] = True

                        if country_map[nx][ny] == 0: # 바다를 만난 경우
                            q.append((nx, ny, dist + 1))
                        elif country_map[nx][ny] != start_island:
                            if dist >= 2:
                                end_island = country_map[nx][ny]
                                edges.append((dist, start_island, end_island))
                            break # 다른 섬 만났으니 종료
                        else:
                            break # 자기 섬 만났으니 종료

parent = [i for i in range(7)] # 섬 최대 6개, 섬 이름은 1부터 시작

def find(x):
    if parent[x] == x:
        return x
    else:
        parent[x] = find(parent[x])
        return parent[x]

def union(x, y):
    root_x = find(x)
    root_y = find(y)

    if root_x == root_y: return False
    else:
        parent[root_y] = root_x
        return True

# 길이 오름차순으로 정렬
# 유니온-파인드(Disjoint Set) 자료구조로 섬들이 연결되어 있는지 확인(사이클 생성 여부 확인)
# 서로 다른 섬이라면 연결하고 다리 길이 더함
# 섬의 수 - 1개의 다리가 연결되면 종료
def kruskal():
    total_cost = 0
    edge_count = 0
    edges.sort()

    for cost, a, b in edges:
        if union(a, b):
            total_cost += cost
            edge_count += 1

    num_island = max(max(row) for row in country_map)

    # 다리 수가 섬 수 - 1이 아니면 MST 만들 수 없음
    if edge_count == num_island - 1:
        print(total_cost)
    else:
        print(-1)

mark_land()
find_bridges()
kruskal()