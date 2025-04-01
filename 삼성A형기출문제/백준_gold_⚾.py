"""17281
9명으로 이루어진 두 팀
n이닝 동안 게임
한 이닝에 3아웃 발생 시 이닝 종료, 이후 두 팀이 공격 수비 전환

경기 전 타순을 정해야 함.
경기 중에는 타순 변경 불가
9번 타자까지 쳤는데 3아웃 발생하지 않은 상태면 1번 타자가 다시 타석에 서며,
타순은 이닝이 변경되어도 순서 유지

공격
이닝이 시작될 때 주자 X
1루, 2루, 3루, 홈 도착 시 1득점(1, 2, 3루에 머물러 있을 수 있음)
공을 쳐서 얻을 수 있는 결과: 안타, 2루타, 3루타, 홈런, 아웃

조건 :
4번 타자 - 1번 선수로 고정
1~3번, 5~9번 타자를 정해야 하고 각 선수가 각 이닝에서 어떤 결과를 얻는지 알고 있음.
가장 많은 득점을 하는 타순 찾기
각 이닝에는 아웃을 기록하는 타자가 적어도 한 명 존재

입력 :
첫째 줄에 이닝 수 N(2<=N<=50)
둘째 줄부터 N개의 줄에 1~9번 선수가 각 이닝에서 얻는 결과가 1번 이닝부터 N번 이닝까지 순서대로 주어짐
ex.
2
4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0
안타 1, 2루타 2, 3루타 3, 홈런 4, 아웃 0을 의미

아이디어 :
9명의 선수를 배치하는 순열
모든 경우의 수 중에서 max값을 찾는 것 -> dp
모든 분기를 순서대로 전부 탐색 -> dfs

- 4점마다 1득점
- 0이 합해서 세번 나오면 이닝 종료
"""
inning = int(input())
batting_result = [list(map(int, input().split())) for _ in range (inning)]

# 1번 선수(0)은 4번 타자로 고정되므로 제외
player = [1, 2, 3, 4, 5, 6, 7, 8]
visited = [0] * 8
current_order = [0] * 9
batting_order = []

# 타순 경우의 수
def permutation(level):
    if level >= 9:
        batting_order.append(current_order.copy())
        return

    # 4번 타자는 1번 선수(index 0)로 고정
    if level == 3:
        current_order[level] = 0
        permutation(level + 1)
        return

    for i in range(8):
        if visited[i] == 1:
            continue

        visited[i] = 1
        current_order[level] = player[i]

        permutation(level + 1)

        visited[i] = 0

# 한 경기의 점수 계산
def calculate_score(order, start_player):
    j = start_player
    total_score = 0

    for i in range(inning):
        out_count = 0
        inning_score = 0

        while out_count < 3:
            if j >= 9:
                j = 0

            player_result = batting_result[i][order[j]]
            print(f"{i}이닝 선수와 결과 : {order[j]}번 선수, {player_result}점")
            print(f"{i}이닝 아웃카운트 : {out_count}")
            print(f"{i}이닝 진루 : {inning_score}")
            if player_result == 0:
                out_count += 1
                j += 1
                print(f"{i}이닝 아웃 카운트가 올라갑니다.")
                if out_count == 3:
                    inning_score = inning_score//4
                    total_score += inning_score
                    print(f"{i}이닝 최종 점수 : {total_score}점")
                    break
            else:
                j += 1
                inning_score += player_result
                print(f"{i}이닝 진루합니다.")

    return total_score

def main():
    permutation(0)
    # print(batting_order)
    # print(len(batting_order))
    max_score = 0

    for i in range(len(batting_order)):
        print(f"현재 계산 중인 타순 : {batting_order[i]}")
        score = calculate_score(batting_order[i], 0)

        print(f"최종 점수 : {score}")
        if max_score <= score:
            max_score = score

    print(max_score)

if __name__ == '__main__':
    main()