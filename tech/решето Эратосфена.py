from math import gcd
n = 15  # до какого числа

used = [0] * n
for i in range(2, n):
    if not used[i]:
        j = i * i
        while j < n:
            if j % i == 0:
                used[j] = 1
            j += i
print(used)

