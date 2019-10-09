class Question(object):
    def __init__(self):
        self.DEBUG = None

    def debug_mode(self):
        while True:
            q = input('Deseja rodar o programa de forma automática? [S/N] ')
            q = str(q).upper()

            if q == 'S' or q == 'N': break
            else: print('Opção inválida! \n')

        if q == 'S': self.DEBUG = True
        elif q == 'N': self.DEBUG = False
        else: raise ValueError