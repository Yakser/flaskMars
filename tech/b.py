a, b, k = map(int, input().split())
used = [0] * (b + 1)
total_cnt = 0
for i in range(2, b + 1):
    if not used[i]:
        j = i * i
        while j < b + 1:
            if j % i == 0:
                used[j] = 1
            j += i
ans = -1
used[1] = 1
p = [0] * (b + 1)
for i in range(a, b + 1):
    d = 0
    if not used[i]:
        d = 1
    p[i] += p[i - 1] + d
print()
for l in range(1, b - a + 2):
    if p[b - l + 1] == k:
        print(l)
        break
