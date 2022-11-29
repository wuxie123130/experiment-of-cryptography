from random import randint


def factorization(n):
    i = 2
    ret = []
    while i * i <= n:
        while n % i == 0:
            ret.append(i)
            n //= i
        i += 1
    if n > 1:
        ret.append(n)
    return ret


if __name__ == "__main__":
    rand = randint(10 ** 13, 10 ** 14)
    print(rand, factorization(rand))
