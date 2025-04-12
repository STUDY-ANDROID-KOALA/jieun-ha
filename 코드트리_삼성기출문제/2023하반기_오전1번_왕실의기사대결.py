from collections import deque

################################################################################
################################################################################

L, N, Q = map(int, input().split())
# chess map 0이면 빈칸, 1 함정, 2 벽
chess_map = [list(map(int, input().split())) for _ in range(L)]
# 처음 위치 r, c 세로 길이 h, 가로 길이 w, 초기 체력 k (1번~N번 기사 = 0~N-1 index)
knight_info = {}
init_k = [0] * (N+1)
for kni in range(1, N+1):
    si, sj, h, w, k = map(int, input().split())
    knight_info[kni] = [si, sj, h, w, k]
    init_k[kni] = k # 체력 저장

command = [list(map(int, input().split())) for _ in range(Q)]

# command[0][0] = 몇번 기사, command[][1] = 방향으로 한 칸 이동
# 0, 1, 2, 3 각각 상/우/하/좌
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

# 바깥쪽을 벽으로 패딩 둔 배열 생성
""" 다음과 같이 표현 가능
chess = [[2] * (L + 2)] + \
        [[2] + row + [2] for row in chess_map] + \
        [[2] * (L + 2)]
"""
chess = [[2] * (L+2) for _ in range(L+2)]
for i in range(1, L+1):
    for j in range(1, L+1):
        chess[i][j] = chess_map[i-1][j-1]

def bfs(start, dire):
    q = deque() # 밀리는 후보를 저장
    pset = set() # 이동 기사 번호 저장
    damage = [0] * (N+1)

    q.append(start)
    pset.add(start)

    while q:
        current = q.popleft()
        ci, cj, h, w, k = knight_info[current]

        # [1] 현재 기사를 명령 받은 dire으로 이동
        # 벽인 경우 : 다음 이동 불가 판정, bfs 종료
        # 벽이 아닌 경우 : 이동 가능 or 함정 or 다른 기사
        ni, nj = ci + dx[dire], cj + dx[dire]
        for ai in range(ni, ni+h):
            for aj in range(nj, nj+w):
                if chess[ai][aj] == 2: # 벽인 경우
                    return # 밀 수 없음
                if chess[ai][aj] == 1: # 함정인 경우
                    damage[current] += 1

        # [2] 겹치는 다른 기사가 있는 지 검사 후 이동 기사 pset 및 후보 큐에 추가
        for kidx in knight_info:
            print("겹치는 기사 확인")
            print(kidx)
            print(f"현재 움직일 대상 : {pset}")
            if kidx in pset:
                print(f"이미 움직일 대상인 기사입니다 : {kidx}")
                continue

            # 겹치는 경우
            ti, tj, th, tw, tk = knight_info[kidx]
            if ni<=ti+th-1 and ni+h-1>=ti and nj<=tj+tw-1 and tj<=nj+w-1:
                q.append(kidx)
                pset.add(kidx)
                print(f"밀리는 후보에 저장 {kidx}")
                print(f"이동 기사 번호에 추가 {kidx}")

    damage[start] = 0

    # [3] 기사들 한번에 이동!
    # 데미지가 체력 이상인 경우
    for kidx in pset:
        si, sj, h, w, k = knight_info[kidx]

        if k <= damage[kidx]:  # 체력보다 더 큰 데미지면 삭제
            knight_info.pop(kidx)
        else:
            ni, nj = si + dx[dire], sj + dy[dire]
            knight_info[kidx] = [ni, nj, h, w, k - damage[kidx]]

for knight, direction in command:
    # 이미 사라진 기사가 주어질 수 있음
    if knight in knight_info:
        print(f"{knight}번 기사를 이동시킵니다...")
        bfs(knight, direction) # 명령 받은 기사 밀어내는 bfs 실행

# 정답 처리
ans = 0
for idx in knight_info:
    ans += init_k[idx] - knight_info[idx][4] # 초기 체력 - 남은 체력
print(ans)
