import sys

input = sys.stdin.readline
n, k = map(int, input().split())
a = list(map(int, input().split()))
s = []
m = 0
l = 0
r = 1
rind = lind = 1
for i in range(n):
    if m < k:
        s.append((a[i], i))
        rind = i
        m += 1
    else:
        if a[i] in s:
            s.append((a[i], i))
            rind = i
        else:
            
            del s[0]
            lind = s[0][1]
            s.append((a[i], i))
            rind = i
    print(s)

print(lind, rind)




# streak = mx_str = rind = 0
# for i in range(n - 1):
#     if a[i] == a[i + 1]:
#         streak += 1
#     else:
#         if mx_str <= streak:
#             rind = i - 1
#             mx_str = streak
#         streak = 0
# if not mx_str:
#     print(1, k)
# else:
#     l = rind - mx_str + 1
#     r = rind
#     print(l, r + k - (r - l))
# l = 0
# r = n - 1
# cnt = 0
# while l < r:
#     if n - cnt
#     if a[l + 1] != a[l]:
#         l += 1
#         cnt += 1
#     elif a[r - 1] != a[r]:
#         r -= 1
#         cnt += 1
# print(cnt)



