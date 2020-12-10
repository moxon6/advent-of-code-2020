from collections import deque

q = deque()
target = 22477624

with open("inputs/day9.txt") as f:
    digits = list(map(int, f.readlines()))

    for digit in digits:
        if digit != target:
            q.append(digit)
            while sum(q) > target:
                q.popleft()
                        
            if sum(q) == target:
                print( min(q) + max(q) )