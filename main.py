from sistema import SistemaTreinos
from datetime import datetime

def pedir_data(mensagem):
    while True:
        data = input(mensagem).strip()
        try:
            datetime.strptime(data, '%d/%m/%Y')
            return data
        except ValueError:
            print("Data inválida. Use o formato dd/mm/yyyy.")

def menu():
    print("\n" + "=" * 50)
    print("TrainingLog ".center(50))
    print("=" * 50)
    print("""
[1] - Adicionar treino
[2] - Listar treinos
[3] - Buscar treino
[4] - Remover treino
[5] - Ver resumo
[6] - Editar treino
[0] - Sair
""")

def main():
    sistema = SistemaTreinos()
    while True:
        menu()
        opcao = input("Digite uma opção: ")

        if opcao == "1":
            print("\n" + "=" * 50)
            print("ADICIONAR TREINO".center(50))
            print("=" * 50)
            print()

            while True:
                tipo = input("Tipo de treino: ").strip()
                if tipo:
                    break
                else:
                    print("O campo não pode ser vazio.")
                
            data = pedir_data("Data (dd/mm/yyyy): ")

            while True:
                try:
                    duracao = int(input("Duração (minutos): "))
                    if duracao > 0:
                        break
                    else:
                        print("Duração deve ser maior que 0")
                except ValueError:
                    print("Digite um número válido")

            intensidades = ["baixa", "média", "alta"]
            while True:
                intensidade = input("Intensidade do treino (baixa/média/alta): ").lower()
                if intensidade in intensidades:
                    break
                else:
                    print("Intensidade inválida. Digite: baixa, média ou alta.")

            sistema.adicionar_treino(tipo, data, duracao, intensidade)
            input("Pressione ENTER para continuar...")

        elif opcao == "2":
            sistema.listar_treinos()
            input("Pressione ENTER para continuar...")

        elif opcao == "3":
            while True:
                tipo = input("Digite o nome do treino para buscar: ").strip()
                if tipo:
                    break
                else:
                    print("O campo não pode ser vazio.")
            sistema.buscar_treino(tipo)
            input("Pressione ENTER para continuar...")

        elif opcao == "4":
            print("\n" + "=" * 50)
            print("REMOVER TREINO".center(50))
            print("=" * 50)
            tipo = input("Digite o nome do treino para remover: ")

            data = pedir_data("Digite a data do treino (dd/mm/yyyy) que deseja remover: ")

            sistema.remover_treino(tipo, data)
            input("Pressione ENTER para continuar...")

        elif opcao == "5":
            print("\n" + "=" * 50)
            print("RESUMO DOS TREINOS".center(50))
            print("=" * 50)
            sistema.ver_resumo()
            input("Pressione ENTER para continuar...") 

        elif opcao == "6":
            print("\n" + "=" * 50)
            print("EDITAR TREINO".center(50))
            print("=" * 50)
            print("\nIdentifique o treino que deseja editar:")

            while True:
                tipo = input("Tipo do treino atual: ").strip()
                if tipo:
                    break
                else:
                    print("O campo não pode ser vazio.")

            data = pedir_data("Data do treino atual (dd/mm/yyyy): ")

            print("\nDigite os novos dados:")
            while True:
                novo_tipo = input("Novo tipo de treino: ").strip()
                if novo_tipo:
                    break
                else:
                    print("O campo não pode ser vazio.")
            nova_data = pedir_data("Nova data (dd/mm/yyyy): ")

            while True:
                try:
                    nova_duracao = int(input("Nova duração (minutos): "))
                    if nova_duracao > 0:
                        break
                    else:
                        print("Duração deve ser maior que 0.")
                except ValueError:
                    print("Digite um número válido.")

            intensidades = ["baixa", "média", "alta"]
            
            while True:
                nova_intensidade = input("Nova intensidade (baixa/média/alta): ").lower()
                if nova_intensidade in intensidades:
                    break
                else:
                    print("Intensidade inválida. Digite: baixa, média ou alta.")

            sistema.editar_treino(tipo, data, novo_tipo, nova_data, nova_duracao, nova_intensidade)
            input("Pressione ENTER para continuar...")

        elif opcao == "0":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")
            input("Pressione ENTER para continuar...")

if __name__ == "__main__":
    main()