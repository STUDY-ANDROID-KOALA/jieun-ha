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
brute force
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

def bf(paper, complete, own_paper):
    for i in range(10):
        for j in range(10):
            if paper[i][j] == 1 and complete[i][j] == 0:
                paper_test(i, j, paper, complete, own_paper)
                # print(f"({i}, {j}) 탐색 후 남은 색종이 수 : {own_paper}")

    use = 25 - sum(own_paper)
    print(use)

def paper_test(i, j, paper, complete, own_paper):
    if paper_valid_test(i, j, paper, 5): # 5x5 자리 있는지 확인
        if own_paper[4] >= 1: # 5x5 1장 필요
            own_paper[4] -= 1
            fill_complete(i, j, complete, 5)
        elif own_paper[0] >= 4 and own_paper[1] >= 3 and own_paper[2] >= 1: # 1x1 4개, 2x2 3개, 3x3 1개 필요
            own_paper[0] -= 4
            own_paper[1] -= 3
            own_paper[2] -= 1
            fill_complete(i, j, complete,5)
        else:
            print(-1)
            exit()
    elif paper_valid_test(i, j, paper, 4): # 4x4 자리 있는지 확인
        if own_paper[3] >= 1:
            own_paper[3] -= 1
            fill_complete(i, j, complete,4)
        elif own_paper[1] >= 4:
            own_paper[1] -= 4
            fill_complete(i, j, complete,4)
        elif own_paper[0] >= 4 and own_paper[1] >= 3:
            own_paper[0] -= 4
            own_paper[1] -= 3
            fill_complete(i, j, complete,4)
        else:
            print(-1)
            exit()
    elif paper_valid_test(i, j, paper, 3): # 3x3 자리 있는지 확인
        if own_paper[2] >= 1:
            own_paper[2] -= 1
            fill_complete(i, j, complete,3)
        elif own_paper[0] >= 5 and own_paper[1] >= 1:
            own_paper[0] -= 5
            own_paper[1] -= 1
            fill_complete(i, j, complete,3)
        else:
            print(-1)
            exit()
    elif paper_valid_test(i, j, paper, 2): # 2x2 자리 있는지 확인
        if own_paper[1] >= 1:
            own_paper[1] -= 1
            fill_complete(i, j, complete,2)
        elif own_paper[0] >= 4:
            own_paper[0] -= 4
            fill_complete(i, j, complete,2)
        else:
            print(-1)
            exit()
    elif paper_valid_test(i, j, paper, 1): # 1x1 자리 있는지 확인
        if own_paper[0] >= 1:
            own_paper[0] -= 1
            fill_complete(i, j, complete, 1)
        else:
            print(-1)
            exit()

def paper_valid_test(i, j, paper, n):
    if i + n > 10 or j + n > 10:
        return 0

    for col in range(i, i + n):
        for row in range(j, j + n):
            if paper[col][row] == 0:
                return 0
    return 1

def fill_complete(top_start_col, top_start_row, complete, n):
    for col in range(top_start_col, top_start_col + n):
        for row in range(top_start_row, top_start_row + n):
            complete[col][row] = 1

def main():
    paper = [list(map(int, input().split())) for _ in range(10)]
    complete = [[0 for row in range(10)] for col in range(10)]
    own_paper = [5 for _ in range(5)]

    bf(paper, complete, own_paper)

if __name__ == "__main__":
    main()