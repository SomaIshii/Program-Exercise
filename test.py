# coding: utf-8
class Unko(object):
    def __init__(self):
        self.keben = 8

    def unchi(self, geri):
        geri = geri + 1
        return geri

    def gero(self):
        b = self.unchi(self.keben)


a = Unko()
a.gero()
print(a.keben)
