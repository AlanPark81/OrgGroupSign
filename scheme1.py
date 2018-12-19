import random
from Crypto.PublicKey import RSA
from Crypto import Random


class TrustedPublicDirectory:
    def __init__(self, public_key_list):
        self.public_key_list = public_key_list
        random.shuffle(self.public_key_list)

    def __getitem__(self, item):
        return self.public_key_list[item]

    def verify(self, msg, signature):
        for key in self.public_key_list:
            if key.verify(msg, signature):
                return True
        return False


class Z:
    def __init__(self, num_of_members):
        self.key_list = [None] * num_of_members

        for i in range(num_of_members):
            self.key_list[i] = RSA.generate(1024)

    def __getitem__(self, item):
        return self.key_list[item]

    def get_trusted_public_directory(self):
        public_key_list = []
        for key in self.key_list:
            public_key_list.append(key.publickey())
        return TrustedPublicDirectory(public_key_list)

    def open_member(self, msg, signature):
        for i in range(len(self.key_list)):
            if self.key_list[i].sign(msg, 0) == signature:
                return i
        return -1


z = Z(40)
sign = z[13].sign(12379587193847134, 0)
tpd = z.get_trusted_public_directory()
assert tpd.verify(12379587193847134, sign) is True
assert z.open_member(12379587193847134, sign) == 13
