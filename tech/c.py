n = int(input())
a = set(map(int, input().split()))
if 1 in a:
    print(1)
else:
    num = int(1e6) + 1
    used = set()
    mx = mn = max(a) + 1
    for i in range(2, num):
        if i not in used:
            j = i * i
            while j < num:
                if j % i == 0:
                    used.add(j)
                j += i
    for i in a:
        if i not in used:
            num = min(num, i)
        mn = min(i, mn)

    if num == 1e9 + 1:
        num = mn
    for i in a:
        if i % num != 0:
            print(-1)
            break
    else:
        print(num)
