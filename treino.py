from datetime import datetime

class Treino:
    def __init__(self, tipo, data, duracao, intensidade):
        self.tipo = tipo
        self.data = data
        self.duracao = duracao
        self.intensidade = intensidade

    def __str__(self):
        return f"[{self.tipo.capitalize()}]  {self.data.strftime('%d/%m/%Y')} - {self.duracao}min ({self.intensidade})"