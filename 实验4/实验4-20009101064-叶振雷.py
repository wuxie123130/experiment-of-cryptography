import random
from math import gcd
from gmpy2 import invert
from random import randint
from Crypto.Util.number import getStrongPrime


# 生成强素数
def large_prime(n_bits: int):
    prime = getStrongPrime(n_bits)
    # 强素数的判断 注意此处用int转化类型
    return prime


# 原根生成算法
def source_root(p: int):
    root = 0
    for i in range(2, p - 1):
        if pow(i, 2, p) != 1 and pow(i, int((p - 1) / 2), p) != 1:
            root = i
            break
    return root


# 密钥生成算法
def gen_key_pair():
    # 生成强素数
    p = large_prime(512)
    g = source_root(p)
    a = randint(2, p - 1)
    ga = pow(g, a, p)
    pub_key = p, g, ga
    sec_key = a
    return pub_key, sec_key


# 加密算法
def encrypt(m: int, pub_key: tuple):
    p, g, ga = pub_key
    k = random.randint(1, p - 2)
    c1 = pow(g, k, p)  # C1 = g^k(mod p)
    c2 = m * pow(ga, k, p)  # C2 = (m * (g^a)^k)(mod p)
    print("随机选择的K为：", k)
    return c1, c2


# 解密算法
def decrypt(c: tuple, pub_key: tuple, sec_key: int):
    c1, c2 = c
    p, g, ga = pub_key
    v = pow(c1, sec_key, p)
    inv_v = invert(v, p)
    m = c2 * inv_v % p
    return m


def main():
    with open("secret0.txt", "r") as f:
        m = int(f.read())
    print(f"消息长度: {len(str(m))}")
    pub_key, sec_key = gen_key_pair()
    print("p为：", pub_key[0])
    print("原根为：", pub_key[1])
    print("原根的a次方为：", pub_key[2])
    # 加密消息m，得到C1 C2
    c1, c2 = encrypt(m, pub_key)
    print(f"c1: {c1}")
    print(f"c2: {c2}")

    # 解密密文C1 C2得到消息m
    dec_m = decrypt((c1, c2), pub_key, sec_key)
    print(f"原明文消息: {m}")
    print(f"解密后消息: {dec_m}")
    print(f"校验结果(True/False): {m == dec_m}")


if __name__ == "__main__":
    main()
