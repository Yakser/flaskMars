def divs(n):
    i = 2
    r = []
    while i * i <= n:
        if n % i == 0:
            r += [i]
            k = n // i
            if i != k:
                r += [k]
        i += 1
    return r
