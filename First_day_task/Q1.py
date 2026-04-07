def series(n):
    count = -1
    num = 2
    mcount = 0
    if n == 0:
        print(num)
    for i in range(n+1):
        for i in range(3):
            count += 1
            num = num + 2
            if count == n:
                print(num)
        mcount += 1
        count += 1
        num += 10*(mcount)
        if count == n:
            print(num)
series(0)
series(1)
series(2)
series(3)
series(4)
series(5)
series(6)
series(7)
series(8)
series(9)
series(10)
series(11)
series(12)
series(13)
series(14)
series(15)