from datetime import datetime

# classe que representa um treino - é o molde pra criar objetos de treinos
class Treino:
    # método construtor — é chamado automaticamente ao criar um treino
    # recebe os 4 dados do treino e os salva no objeto
    def __init__(self, tipo, data, duracao, intensidade):
        self.tipo = tipo
        self.data = data
        self.duracao = duracao
        self.intensidade = intensidade

     # método que define como o treino é exibido quando impresso com print()
    def __str__(self):
        return f"[{self.tipo.capitalize()}]  {self.data.strftime('%d/%m/%Y')} - {self.duracao}min ({self.intensidade})"