n = int(input())
a = list(map(int, input().split()))
ans = 0
j = 0
for i in range(n):
    while j < n and a[j] - a[i] <= 5:
        j += 1
        ans = max(ans, j - i)
print(ans)




# n = int(input())
# a = [list(map(int, input().split())) for _ in range(n)]
#
# mx = max(set(a[-1]))
# inds = [i for i in range(n) if a[-1][i] == mx]
# for ind in inds:
#     dp = [0] * n
#     dp[0] = mx
#     for i in range(n - 1, 0, -1):
#         if a[i][ind] > a[i][ind - 1]:
#             dp[i] = dp[i - 1] + a[i][ind]
#         else:
#             dp[i] = dp[i - 1] + a[i][ind - 1]
#             ind -= 1
#     print(dp[-1])



# dp[0] = a[0][0]
# ind = 0
# for i in range(1, n):
#     if a[i][ind] > a[i][ind + 1]:
#         dp[i] = dp[i - 1] + a[i][ind]
#     else:
#         dp[i] = dp[i - 1] + a[i][ind + 1]
#         ind += 1
# print(dp[-1])
