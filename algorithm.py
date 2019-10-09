from time import sleep


class Solver(object):
    def __init__(self):
        # descrição das hastes
        self.hastes = ['inicial', 'auxiliar', 'final']

        # intervalo de pausa em segundos
        self.pausa = 0.05

        # lista de movimentos 
        self.all_moves = []

        # lista de comandos
        self.all_commands = []

    def command_disk(self):
        for count in range(len(self.all_moves)):
            try:
                if count % 2 == 0:
                    i = self.all_moves[count]
                    f = self.all_moves[count+1]
                    direction = (f - i)

                    # comando para cima
                    self.all_commands.append('up')

                    if direction == 0:
                            continue

                    # comando para direita
                    elif direction > 0:
                            for c in range(direction):
                                    self.all_commands.append('right')                

                    # comando para esquerda
                    elif direction < 0:
                            for c in range(-direction):
                                    self.all_commands.append('left')
                    
                    # comando para baixo
                    self.all_commands.append('down')

                else:
                    i = self.all_moves[count]
                    f = self.all_moves[count+1]
                    direction = (f - i)

                    # comando para direita
                    if direction > 0:
                            for c in range(direction):
                                    self.all_commands.append('right')                

                    # comando para esquerda
                    elif direction < 0:
                            for c in range(-direction):
                                    self.all_commands.append('left')

            except IndexError:
                Exception

    # algoritmo de resolução do puzzle
    def tower(self, n, inicio=1, fim=3):
        if n:
            # move o disco n - 1 do inicio para o auxiliar
            self.tower(n - 1, inicio, 6-inicio-fim)

            # mostra o progresso
            print(f'O disco {n} será movido da torre {self.hastes[inicio-1]} para a torre {self.hastes[fim-1]}')
    
            # cria uma lista com os comandos para mover os discos
            self.all_moves.append(inicio)
            self.all_moves.append(fim)

            # diminui a velocidade de excução da função
            sleep(self.pausa)

            # move o disco n - 1 do auxiliar para o fim
            self.tower(n - 1, 6-inicio-fim, fim)
            
