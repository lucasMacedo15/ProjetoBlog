from django.test import TestCase

# Create your tests here.


class Caneca:

    def __init__(self, nome, cor) -> None:
        self.nome = nome
        self.cor = cor

    def encher(self):

        return f'enchendo a {self.__class__.__name__} {self.nome}'


class CanecaMac(Caneca):

    def encher(self):
        print(super().encher())


c1 = CanecaMac('Lucas', 'preta')

c1.encher()
