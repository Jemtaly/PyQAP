def network(n, j = 0):
    if n == 1:
        return []
    if n == 2:
        return [(j, j + 1)]
    k = n // 2
    lbitn = n // 2
    rbitn = n // 2 + n % 2 - 1
    net = []
    for i in range(lbitn):
        net.append((j + i, j + i + k))
    net += network(k, j)
    net += network(n - k, j + k)
    for i in range(rbitn):
        net.append((j + i, j + i + k))
    return net
def genbits(lft, rgt):
    n = min(len(lft), len(rgt))
    if n == 1:
        return []
    if n == 2:
        return [lft[0] != rgt[0]]
    k = n // 2
    lbitn = n // 2
    rbitn = n // 2 + n % 2 - 1
    # generate lookup tables
    ls = sorted(range(n), key = lft.__getitem__)
    rs = sorted(range(n), key = rgt.__getitem__)
    l2r = [None] * n
    r2l = [None] * n
    for l, r in zip(ls, rs):
        l2r[r] = l
        r2l[l] = r
    # left and right bits
    lbits = [None] * lbitn
    rbits = [None] * rbitn
    # counter for the remaining bits to be generated
    c = lbitn + rbitn
    # generate bits
    if n % 2 == 0:
        l = n - 1
        r = l2r[l]
        while True:
            lbits[r % k] = r // k == 0
            r = r + k if r // k == 0 else r - k
            l = r2l[r]
            c -= 1
            if l == k - 1:
                break
            rbits[l % k] = l // k == 1
            l = l + k if l // k == 0 else l - k
            r = l2r[l]
            c -= 1
    else:
        l = n - 1
        r = l2r[l]
        while True:
            if r == n - 1:
                break
            lbits[r % k] = r // k == 0
            r = r + k if r // k == 0 else r - k
            l = r2l[r]
            c -= 1
            rbits[l % k] = l // k == 1
            l = l + k if l // k == 0 else l - k
            r = l2r[l]
            c -= 1
    # generate remaining bits
    t = rbitn - 1
    while c > 0:
        while rbits[t] is not None:
            t -= 1
        l = t + k
        r = l2r[l]
        while True:
            lbits[r % k] = r // k == 0
            r = r + k if r // k == 0 else r - k
            l = r2l[r]
            c -= 1
            rbits[l % k] = l // k == 1
            l = l + k if l // k == 0 else l - k
            r = l2r[l]
            c -= 1
            if l == t + k:
                break
    # apply swaps to the left and right inputs
    ulft, dlft = lft[:k], lft[k:]
    for i in range(lbitn):
        if lbits[i]:
            ulft[i], dlft[i] = dlft[i], ulft[i]
    urgt, drgt = rgt[:k], rgt[k:]
    for i in range(rbitn):
        if rbits[i]:
            urgt[i], drgt[i] = drgt[i], urgt[i]
    # generate bits for the upper and lower halves
    ubits = genbits(ulft, urgt)
    dbits = genbits(dlft, drgt)
    # concatenate and return the bits
    return lbits + ubits + dbits + rbits
def apply(src, net, bits):
    for bit, (i, j) in zip(bits, net):
        if bit:
            src[i], src[j] = src[j], src[i]
