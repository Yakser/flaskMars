mod = 1e9 + 7


# рекурсивно
# def binpow(a, n):
#     if n == 0:
#         return 1
#     if n % 2 == 1:
#         return a * binpow(a, n - 1)
#     ans = binpow(a, n // 2)
#     return ans * ans
#
#
# print(binpow(5, 2))

# res = 1
# while n > 0:
#     if n % 2 != 0:
#         res *= a
#         n -= 1
#     a *= a
#     n //= 2
#
# print(res)

def binmul(a, n):
    if n == 0:
        return 0
    if n % 2 == 1:
        return a + binmul(a, n - 1)
    ans = binmul(a, n // 2)
    return ans + ans

print(binmul(5, 3))

# binpow
# # Created by Sergey Yaksanov at 09.12.2020
# Copyright © 2020 Yakser. All rights reserved.
