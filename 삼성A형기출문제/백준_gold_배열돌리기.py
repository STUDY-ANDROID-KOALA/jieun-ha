""" 17406
NxM 크기의 배열
배열 A의 값 = 각 행에 있는 모든 수의 합 중 최솟값

회전 연산 (r, c, s)
가장 왼쪽 윗칸이 (r-s,c-s), 가장 오른쪽 아랫칸이 (r+s, c+s)인 정사각형을
시계 방향으로 한 칸씩 돌린다는 의미
배열의 칸 (r,c)는 r행 c열을 의미

서로 다른 회전 연산 K개의 순서를 조합해서 경우의 수를 다 따져 봐야 함 -> 순열 활용

입력 :
1 - 배열의 크기 N, M, 회전 연산의 개수 K
2 - N개의 줄에 배열 A에 들어 있는 수 A[i][j]
3 - K개의 줄에 회전 연산의 정보 r, c, s

아이디어 :
1. 회전 연산 개수 K개의 순열(근데 이제 모든 걸 선택해야 하니 팩토리얼이랑 같은) 구하기
2.

"""
n, m, rotation = map(int, input().split())
array = [list(map(int, input().split())) for _ in range(n)]
calculate = [tuple(map(int, input().split())) for _ in range(rotation)]

# 순열 nPr
visited = [0] * rotation
current_permutation = [0] * rotation
permutation_list = []

def permutation(level):
    if level >= rotation:
        # print(current_permutation)
        permutation_list.append(current_permutation.copy())
        return

    for i in range(rotation):
        if visited[i] == 1:
            continue

        visited[i] = 1
        current_permutation[level] = calculate[i]
        permutation(level + 1)

        visited[i] = 0

# permutation(0)
# print(f"permutation list : {permutation_list}")
# output. [[(3, 4, 2), (4, 2, 1)], [(4, 2, 1), (3, 4, 2)]]

def rotation_array(arr, cal):
    # cal[i] = (r, c, s). 시작 칸이 (r-s, c-s), 마지막 칸이 (r+s, c+s)
    # print(cal)
    r, c, s = cal
    r, c = r - 1, c - 1 # (0,1)이 (1,2)임. 실제 배열에서 index -= 1 해줘야 함

    for level in range(1, s + 1):  # 바깥쪽부터 안쪽으로 한 층씩
        top, left = r - level, c - level
        bottom, right = r + level, c + level

        # 테두리 회전을 위한 값 저장
        prev = arr[top][left]

        # 왼쪽 세로 이동 (위로)
        for i in range(top, bottom):
            arr[i][left] = arr[i + 1][left]

        # 아래 가로 이동 (왼쪽으로)
        for i in range(left, right):
            arr[bottom][i] = arr[bottom][i + 1]

        # 오른쪽 세로 이동 (아래로)
        for i in range(bottom, top, -1):
            arr[i][right] = arr[i - 1][right]

        # 위 가로 이동 (오른쪽으로)
        for i in range(right, left, -1):
            arr[top][i] = arr[top][i - 1]

        # 저장했던 첫 번째 값 삽입
        arr[top][left + 1] = prev

def calculate_all(arr, cal):
    # rotation 순열 생성
    permutation(0)

    min_value = 5001

    # 모든 순열에 대해 회전 연산
    for i in range(len(permutation_list)):
        mock_arr = [row[:] for row in arr]

        for cal in permutation_list[i]:
            rotation_array(mock_arr, cal)
            # print(f"mock_arr: {mock_arr}")

        current_min = min_row(mock_arr)
        # print(f"current_min: {current_min}")
        if min_value > current_min:
            min_value = current_min

    print(min_value)

def min_row(arr):
    sum_row = 0
    min_array = 5001

    for i in range(n):
        for j in range(m):
            # print(f"sum_row와 array[i][j] : {sum_row}, {array[i][j]}")
            sum_row += arr[i][j]
        if min_array > sum_row:
            min_array = sum_row
        sum_row = 0

    return min_array

calculate_all(array, calculate)