from decimal import *
from Crypto.Util import number


def mod_pow(a, b, mod):
    if b > 0:
        return context.power(a, b, mod)
    else:
        # inverse the result based on a theorem from number theory
        sub_result = context.power(a, context.minus(b), mod)
        return context.power(sub_result, mod - 2, mod)


def mod_mul(a, b, mod):
    return context.divmod(context.multiply(a, b), mod)[1]


context = Context(prec=MAX_PREC)

N = number.getPrime(1024)
alpha = number.getRandomInteger(1024)
beta = number.getRandomInteger(1024)

c = number.getRandomRange(alpha, alpha + beta + 1)
r_chosen = Decimal(number.getRandomRange(0, beta + 1))

x = number.getRandomInteger(1024)
y = mod_pow(x, c, N)


cnt = 0

z1 = mod_pow(x, r_chosen, N)
z2 = mod_pow(x, context.subtract(r_chosen, beta), N)


assert mod_pow(x, r_chosen, N) == z1 or mod_pow(x, r_chosen, N) == z2
assert mod_pow(x, context.subtract(r_chosen, beta), N) == z2
assert alpha - beta <= c + r_chosen - beta <= alpha + beta
assert alpha <= c + r_chosen <= alpha + beta + beta
assert mod_mul(z1, y, N) == mod_pow(x, context.add(c, r_chosen), N)
rx = context.subtract(context.add(c, r_chosen), beta)
assert mod_mul(z2, y, N) == mod_pow(x, rx, N)
