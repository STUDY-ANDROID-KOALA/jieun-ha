""" 17471
n개의 백준시 구역(1~N번까지 번호 매겨져있음)
-> 0 based index로 변환 위해 -1해줄 것

n개의 구역을 2개의 선거구로 빠짐없이 나눌 것
선거구는 구역을 적어도 하나 포함해야 함
한 선거구에 포함되어 있는 구역은 모두 연결되어 있어야 함

구역 A에서 인접한 구역을 통해 구역 B로 갈 수 있을 때 두 구역은 연결되어 있다고 함
중간에 통하는 인접 구역은 0개 이상이어야 하고, 모두 같은 선거구에 포함된 구역이어야 함

아이디어 :
bfs (큐로 구현)
큐에서 하나의 노드를 방문할 때마다 거기까지가 A구역, 나머지를 B구역으로 해서 계산
min = A구역 인구 계산 - B구역 인구 계산 << 계속 갱신해 나가기

입력 :
첫째 줄 - 구역의 개수 N
둘째 줄 - 구역별 인구 (1번부터 N번 구역까지 순서대로)
셋째 줄부터 N개의 줄 - 인접한 구역의 수 + 인접한 구역의 번호

출력 :
인구 차이의 최솟값
두 선거구로 나눌 수 없는 경우 -1 출력
"""
from collections import deque

section_sum = int(input())
section_population = list(map(int, input().split()))
section_graph = [list(map(int, input().split()))[1:] for _ in range(section_sum)]

visited = [False] * section_sum
section_a = [] # A구역
section_b = list(range(section_sum)) # 1번부터 section_sum번 구역까지 index 값 집어넣기
print(f"초기 A구역 : {section_a}")
print(f"초기 B구역 : {section_b}")

min_diff = 1000

def bfs(graph, start, visit):
    queue = deque([start])
    visit[start] = True

    while len(queue) >= 1:
        v = queue.popleft()
        section_a.append(v)
        print(f"A구역 : {section_a}")

        global section_b
        section_b = [x for x in section_b if x != v]
        print(f"B구역 : {section_b}")

        calculate(section_a, section_b)

        for i in graph[v]:
            if not visit[i]:
                queue.append(i)
                visit[i] = True

def calculate(a, b):
    sum_a = 0
    sum_b = 0
    global min_diff

    for i in a:
        print(f"현재 A구역의 {i} 인구 수 : {section_population[i]}")
        sum_a += section_population[i]
    print(f"A구역 인구 합계: {sum_a}")

    for i in b:
        print(f"현재 B구역의 {i} 인구 수 : {section_population[i]}")
        sum_b += section_population[i]
    print(f"B구역 인구 합계 : {sum_b}")

    diff = abs(int(sum_a - sum_b))
    print(f"인구 차: {diff}")

    if diff < min_diff:
        min_diff = diff

bfs(section_graph, 0, visited)
print(min_diff)