class Caneca:

    peso = 2
    cor = 'branca'
    material = 'vidro'

    def __init__(self, cor, nome) -> None:
        self._cor = cor
        self.nome = nome

    @property
    def cor(self):
        return self._cor

    @cor.setter
    def cor(self, nova_cor):
        self._cor = nova_cor


c1 = Caneca('vermelha', 'lucas')
print(Caneca.cor)

print(c1.cor)
c1.cor = 'preta'
print(c1.cor)
