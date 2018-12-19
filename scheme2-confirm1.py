from decimal import *
from Crypto.Util import number
from Crypto import Random
import os, math

context = Context(prec=MAX_PREC)

N = number.getPrime(1024)

alpha = number.getRandomInteger(1024)
beta = number.getRandomInteger(1024)

c = number.getRandomRange(alpha, alpha + beta + 1)

r_chosen = Decimal(number.getRandomRange(0, beta + 1))

x = number.getRandomInteger(1024)
y = context.power(x, c, N)
z1 = z2 = 1

cnt = 0

z1 = context.power(x, r_chosen, N)

# To computer x pow r - beta,
# we should change the exponent from r - beta that is negative to beta - r and get the inverse of it
# get x pow beta - r
zx = context.power(x, beta - r_chosen, N)
# inverse the result based on a theorem from number theory
z2 = context.power(zx, N-2, N)


assert (context.power(x, r_chosen, N) == z1 or context.power(x, r_chosen, N) == z2)
assert (context.divmod(context.multiply(context.power(x, beta - r_chosen, N), z2), N)[1] == 1)
assert alpha - beta <= c + r_chosen - beta <= alpha + beta
assert alpha <= c + r_chosen <= alpha + beta + beta
assert context.divmod(context.multiply(z1, y), N)[1] == context.power(x, context.add(c, r_chosen), N) or context.divmod(context.multiply(z2, y), N)[1] == context.power(x, context.add(c, r_chosen), N)