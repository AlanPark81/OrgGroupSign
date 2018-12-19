from decimal import *
from Crypto.Util import number
import math

context = Context(prec=10000)


def generate_n_p_q_f():
    p = Decimal(number.getPrime(1024))
    q = Decimal(number.getPrime(1024))
    n = context.multiply(p, q)

    def f():
        x = Decimal(number.getPrime(1024))
        y = Decimal(number.getPrime(1024))
        while x == p or x == q or y == p or y == q:
            x = Decimal(number.getPrime(1024))
            y = Decimal(number.getPrime(1024))
        return context.multiply(x, y)

    return p, q, n, f


def generate_s_list(n_val, number_of_members):
    range_begin = math.ceil(context.sqrt(n_val)) // 1
    range_end = math.floor(context.multiply(2, context.sqrt(n_val))) // 1
    s = []
    num = range_begin
    while num < range_end and len(s) < number_of_members:
        if number.isPrime(num):
            s.append(num)
        num += 1

    v_val = Decimal(1)
    for i in range(number_of_members):
        v_val = context.multiply(v_val, s[i])
    return s, v_val


class Z:
    def __init__(self, num_of_members):
        self.n, self.p, self.q, self.f = generate_n_p_q_f()
        self.s, self.v = generate_s_list(self.n, num_of_members)

    def publish(self):
        return self.n, self.v, self.f

    def __getitem__(self, item):
        return self.s[item]


def sign(msg, f, s, n):
    _, remainder = context.divmod(context.power(f(msg), s), n)
    return remainder


z = Z(40)
n, v, f = z.publish()
private_s = z[13]

assert context.divmod(v, private_s)[1] == 0
minimum = math.ceil(context.sqrt(n)) // 1
limit = math.floor(context.multiply(2, context.sqrt(n))) // 1
assert minimum <= private_s < limit
