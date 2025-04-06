"""17136
색종이 5개씩 5종 가지고 있음(1x1 .. 5x5)
10x10 종이 위에 색종이 붙이기(1x1 크기 칸으로 100칸 으로 나뉨)
- 각 칸에 0 또는 1이 적혀져 있음
- 1이 적힌 칸은 모두 색종이로 덮여져야 함
- 0이 적힌 칸에 색종이가 있으면 안됨
-경계를 나가거나 겹치면 안됨

입력 :
10줄에 종이의 각 칸에 적힌 수

출력 :
모든 1을 덮는 데 필요한 색종이의 최소 개수
* 1을 모두 덮는 것이 불가능한 경우 -1 출력

아이디어 :
dfs
이차원 배열 활용 -> 인덱스 하나하나 싹 돌면서 if~elif~else 조건 분기
가진 색종이 개수 카운트 [5] 다 5로 초기화하고 쓸 때마다 개수 -1 해줌
입력받을 이차원 배열 arr_paper[10][10]
색종이 붙이기 완료 여부 기록할 이차원 배열 arr_complete[10][10]
- 탐색 중인 인덱스가 색종이의 왼쪽 최상단 위치가 된다고 가정
- 1 1 1 1 1 인 경우 5x5 색종이를 해당 위치에 넣고, 남은 개수 카운트 -1
  1 1 1 1 1
  1 1 1 1 1
  1 1 1 1 1
  1 1 1 1 1
  5x5 색종이가 안 남아 있는 경우 3x3 1개, 2x2 3개, 1x1 4개 필요
  부족 시 바로 -1
  색종이 집어넣은 경우에는 가진 색종이 개수 카운트 배열에 집어넣기
"""
result = float('inf')

def dfs(paper, own_paper, used, x):
    global result

    if used > result:
        return

    for i in range(x, 10):
        for j in range(10):
            if paper[i][j] == 1:
                for size in range(5, 0, -1):
                    if own_paper[size-1] > 0 and paper_valid(i, j, paper, size):
                        fill_complete(i, j, paper, size, 0)
                        own_paper[size-1] -= 1

                        dfs(paper, own_paper, used + 1, i)

                        fill_complete(i, j, paper, size, 1)
                        own_paper[size-1] += 1
                return

    result = min(result, used)

def paper_valid(i, j, paper, n):
    if i + n > 10 or j + n > 10:
        return False

    for col in range(i, i + n):
        for row in range(j, j + n):
            if paper[col][row] == 0:
                return False
    return True

def fill_complete(top_start_col, top_start_row, paper, n, fill):
    for col in range(top_start_col, top_start_col + n):
        for row in range(top_start_row, top_start_row + n):
            paper[col][row] = fill

def main():
    global result

    paper = [list(map(int, input().split())) for _ in range(10)]
    own_paper = [5 for _ in range(5)]

    dfs(paper, own_paper, 0, 0)

    if result != float('inf'):
        print(result)
    else:
        print(-1)

if __name__ == "__main__":
    main()