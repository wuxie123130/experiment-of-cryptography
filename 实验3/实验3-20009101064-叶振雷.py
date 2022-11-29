import random
import sys
from math import prod, gcd


# 检查列表互素函数
def mutual_prime_check(m: list):
    # 互素校验
    size = len(m)
    for i in range(size):
        for j in range(i + 1, size):
            if gcd(m[i], m[j]) != 1:
                return False
    return True


# 扩展欧几里得算法求模逆
def find_mod_reverse(a: int, m: int):
    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3

    return u1 % m


# 中国剩余定律
def crt(equation_num: int, a_list: list, m_list: list):
    for i in range(len(a_list)):
        print("a", i, ":", a_list[i])
    for i in range(len(m_list)):
        print("m", i, ":", m_list[i])
    if not mutual_prime_check(m_list):  # 互素检查
        print("不能直接利用中国剩余定理")
        print()
        return
    # 求乘积
    m = prod(m_list)
    # 求Mj
    mj = [m // _m for _m in m_list]
    # 求Mj的逆
    inv_mj = [find_mod_reverse(m // _m, _m) for _m in m_list]
    xj = [(mj[j] * inv_mj[j] * a_list[j]) % m for j in range(equation_num)]
    res = sum(xj) % m
    return res


# 根据选取的n和t 生成d数组
def find_d1(n, t):
    d = []  # 初始化d数组
    x = 0
    for i in range(500):
        if (i * t > 502) & (i * (t - 1) < 502):
            x = i
            break
    print("x:", x)
    temp = random.randint(pow(10, x), pow(10, x+1))
    d.append(temp)
    i = 1
    while i < n:
        temp = random.randint(pow(10, x), pow(10, x+1))
        tem = d.copy()
        tem.append(temp)
        if mutual_prime_check(tem):  # judge1是判断是否互素的函数
            d.append(temp)
            i = i + 1
    return d


# 加密算法
def encrypt(k, t, n):
    # 前t组相乘计算N
    d_seq = find_d1(n, t)
    n_sum = prod(d_seq[0:t])
    print(f"N: {n_sum}")
    print()
    # 后t-1组相乘计算N
    m_sum = prod(d_seq[n - t + 1:n])
    print(f"M: {m_sum}")
    print()
    # 需要满足n_sum > k > m_sum
    # 轮流求模得到一系列ki值
    ki = [k % d_seq[i] for i in range(n)]
    # 把生成的ki和di打包成对返回
    res = list(zip(ki, d_seq))
    return res


# 解密算法
def decrypt(t, k_d: list):
    if len(k_d) < t:
        print(f"数据少于{t}组，无法解密")
        sys.exit()
    # 送入中国剩余定理求解函数拿到返回值就是秘密k
    return crt(t, [k_d[i][0] for i in range(t)], [k_d[j][1] for j in range(t)])


def main():
    t = int(input("请输入t："))
    n = int(input("请输入n："))
    d_seq = find_d1(n, t)
    for d_idx in range(n):
        print(f"d{d_idx + 1} = {d_seq[d_idx]}")
        print()

    for case_i in range(2):
        print(f"{'#' * 36} 测试样例【{case_i + 1}】{'#' * 36}")
        with open(f"./secret{case_i + 1}.txt", "r") as f:
            k = int(f.read())
            print("[+]测试加密：", end="\n\n")
            print("k = ", k)
            res_enc = encrypt(k, t, n)
            for i in range(n):
                print(f"(k{i + 1}, d{i + 1})：{res_enc[i]}")
                print()
            print("[-]测试解密：", end="\n\n")
            # 取前t组用于解密（从res_enc中任取t组均可）
            res_dec = decrypt(t, random.sample(res_enc, t))
            print("正确秘密k：", k)
            print("还原秘密k：", res_dec)
            if res_dec == k:
                print("秘密还原正确！")
            else:
                print("秘密还原错误！")


if __name__ == "__main__":
    main()
