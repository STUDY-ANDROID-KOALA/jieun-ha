"""
RxC (1행~R행)
동/서/남쪽은 벽으로 막혀 있음
정령 - 숲의 북쪽을 통해서만 숲에 들어올 수 있음

K명의 정령이 각자 골렘을 타고 숲을 탐색
- 골렘 : 중앙 칸 + 상하좌우 5칸 차지
- 중앙 제외 4칸 중 1칸은 골렘의 출구
- 정령은 어느 방향에서든 탑승 가능 but 하차는 정해진 출구에서만 가능

i번째로 숲 탐색하는 골렘은 숲의 가장 북쪽에서부터
골렘의 중앙이 ci열이 되도록 하는 위치에서 내려오기 시작
초기 골렘의 출구는 di의 방향에 위치

숲 탐색 우선순위
1. 남쪽으로 한 칸 내려감
2. 비어있지 않은 경우 서쪽 방향으로 회전하며 내려감(출구가 반시계 방향으로 이동)
3. 두 방법 다 안되는 경우 동쪽 방향으로 회전하며 내려감(출구가 시계 방향으로 이동)

골렘이 이동할 수 있는 가장 남쪽에 도달한 경우
- 정령이 골렘 내에서 상하좌우 인접 칸으로 이동
- 현재 위치한 골렘의 출구가 다른 골렘과 인접한 경우 출구를 통해 다른 골렘으로 이동 가능
- 정령은 갈 수 있는 모든 칸 중 가장 남쪽의 칸으로 이동 후 종료
- 정령의 위치 = 해당 정령의 최종 위치

정령 최종 위치의 행 번호의 합 구해야 함 -> 각 정령이 도달하게 되는 최종 위치 누적

골렘이 최대한 남쪽으로 이동했지만 몸 일부가 숲 밖인 경우
- 모든 골렘들은 숲을 빠져나간 뒤 다음 골렘부터 새롭게 숲 탐색
-> 정령이 도달하는 최종 위치를 답에 포함시키지 않음

숲이 다시 텅 비게 돼도 행의 총합은 누적되는 것에 유의
"""
# 골렘 출구 방향 변화
def change_exit(direction, id):
    if direction == "r": # 시계 방향
        if golem_exit[id] == 3:
            golem_exit[id] = 0
        else:
            golem_exit[id] += 1

    elif direction == "l": # 반시계 방향
        if golem_exit[id] == 0:
            golem_exit[id] = 3
        else:
            golem_exit[id] -= 1

# 골렘 위치 표시
def mark_golem_location(arr, x, y):
    for direction in range(4):
        nx = x + dx[direction]
        ny = y + dy[direction]
        arr[nx][ny] = 1

# 정령 dfs
def dfs():
    return

############################################################################
############################################################################

# 숲의 크기 r x c, 정령 수 k, 골렘 (출발하는 중앙 열, 출구 방향 정보)
# 출구 방향 정보 d [0, 1, 2, 3] = [북, 동, 남, 서]
r, c, k = map(int, input().split())
golem = [list(map(int, input().split())) for _ in range(k)]

forest = [[0] * (c+1) for _ in range(r+1)]
golem_exit = []
total_row = 0

# 골렘의 출구 방향 저장
for gi in range(k):
    golem_exit.append(golem[gi][1])

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]
# [1] 정령의 개수만큼 반복
for golem_id in range(k):
    # [2] 골렘의 이동(최대한 남쪽으로)

    i = 1
    j = golem[golem_id][0]

    while True:
        if forest[i+2][j] == 0 and forest[i+1][j-1] == 0 and forest[i+1][j+1] == 0:
            forest[i][j] = 0
            # 정령 위치 갱신(골렘의 중앙) 및 골렘 위치 표시
            forest[i+1][j] = 2
            i += 1
            print(f"남쪽 현재 정령 ({i}, {j})")
        elif forest[i][j-2] == 0 and forest[i-1][j-1] == 0 and forest[i+1][j-1] == 0 and forest[i+1][j-2] == 0 and forest[i+2][j-2] == 0:
            forest[i][j] = 0
            forest[i+1][j-1] = 2
            i += 1
            j -= 1
            print(f"서쪽 현재 정령 ({i}, {j})")
            # 출구 방향 갱신
            change_exit("l", golem_id)
        elif forest[i-1][j+1] == 0 and forest[i][j+2] == 0 and forest[i+1][j+1] == 0 and forest[i+1][j+2] == 0 and forest[i+2][j+1] == 0:
            forest[i][j] = 0
            forest[i+1][j+1] = 2
            i += 1
            j += 1
            print(f"동쪽 현재 정령 ({i}, {j})")
            # 출구 방향 갱신
            change_exit("r", golem_id)
        else: # 이동할 공간 없는 경우
            mark_golem_location(forest, i, j)
            # [3] 정령의 이동

            break

    print("격자 넘어갔는지 여부 확인 전")
    print(forest)

    # 골렘의 일부가 격자 바깥에 있는 경우
    if not(1 <= i-1 <= r and 1 <= i+1 <= r and 1 <= j-1 <= c and 1 <= j+1 <= c):
        print("초기화 실행")
        for fi in range(r+1):
            for fj in range(c+1):
                forest[fi][fj] = 0
        continue

    print(f"{golem_id}번째 골렘 이동 완료 후 숲")
    print(forest)


print("골렘 총 이동 완료 후 골렘의 출구 방향")
print(golem_exit)