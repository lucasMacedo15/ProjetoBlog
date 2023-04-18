class POO:

    def __init__(self, **kwargs):
        """
        Constructor. Called in the URLconf; can contain helpful extra
        keyword arguments, and other things.
        """
        self.var = None
        # Go through keyword arguments, and either save their values to our
        # instance, or raise an error.
        for key, value in kwargs.items():
            setattr(self, key, value)

    def setup(self, request, *args, **kwargs):

        self.request = request
        self.args = args
        self.kwargs = kwargs
        self.var = kwargs.get('post')


p1 = POO(request='get', post='Post comentario')

print(p1.post)
p1.setup('post', post='Conteudo do meu post')

print(p1.var)
