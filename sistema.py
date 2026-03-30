from treino import Treino # importa a classe treino pra criar objetos
from database import conectar # importa a função que concta ao banco
from datetime import datetime # converter pra datas

class SistemaTreinos:
    def adicionar_treino(self, tipo, data_str, duracao, intensidade):
        conn = conectar() # abre conexão com o banco
        if not conn: # se nao conseguir conectar, encerra
            return     

        # tenta converter a data para o formato correto
        try:
            data = datetime.strptime(data_str, '%d/%m/%Y').date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/yyyy.")
            conn.close()
            return
        
        cursor = conn.cursor() # cria o cursor, ele que envia os comando SQL
        tipo = tipo.capitalize()

        # executa o INSERT no banco com as informações do treino
        cursor.execute("""
            INSERT INTO treinos (tipo, data, duracao, intensidade)
            VALUES (%s, %s, %s, %s)
        """, (tipo, data, duracao, intensidade) )

        # fecha o cursor
        conn.commit()
        cursor.close()
        conn.close()
        print("Treino adicionado com sucesso")

    def listar_treinos(self):
        conn = conectar()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            # busca os treinos selecionados por data
            cursor.execute("SELECT tipo, data, duracao, intensidade FROM treinos ORDER BY data")
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum treino encontrado")

            else:
                print("=" * 50)
                print("LISTA DE TREINOS".center(50))
                print("=" * 50)
                for t in resultados:
                    treino = Treino(t[0], t[1], t[2], t[3])
                    print(treino)
        except Exception as e:
            print("Erro ao listar treinos:", e)
        finally:
            cursor.close()
            conn.close()

    def buscar_treino(self, tipo_busca):
        conn = conectar()
        if not conn:
            return
        
        cursor = conn.cursor()
        try:
            # busca o treino no banco com SELECT de acordo com oque o usuario digitar com o
            cursor.execute(
                "SELECT tipo, data, duracao, intensidade FROM treinos WHERE LOWER(tipo) = LOWER(%s)",
                (tipo_busca,)
            )
            resultados = cursor.fetchall()

            if not resultados:
                print("Nenhum treino encontrado para: ", tipo_busca)
            else:
                print("=" * 50)
                print(f"RESULTADOS PARA '{tipo_busca}'".center(50))
                print("=" * 50)
                for t in resultados:
                    treino = Treino(t[0], t[1], t[2], t[3])
                    print(treino)

        except Exception as e:
            print("Erro ao buscar treino:", e)
        # se der erro ou nao, fecha o cursor
        finally:
            cursor.close()
            conn.close()

    def remover_treino(self, tipo, data_str):
        conn = conectar()
        if not conn:
            return

        cursor = conn.cursor()

        data = datetime.strptime(data_str, "%d/%m/%Y").date()

        # executa o DELETE no banco para o treino que irá ser excluido
        cursor.execute("""
            DELETE FROM treinos 
            WHERE LOWER(tipo) = %s AND data = %s
        """, (tipo.lower(), data))

        if cursor.rowcount == 0:
            print(f"Nenhum treino do tipo '{tipo}' encontrado na data {data_str}.")
        else:
            print(f"Treino do tipo '{tipo}' na data {data_str} removido com sucesso!")

        # fecha cursor
        conn.commit()
        cursor.close()
        conn.close()

    def ver_resumo(self):
        conn = conectar()
        if not conn:
            return
        
        cursor = conn.cursor()

        # resumo de todos os treinos 
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(duracao), 0) FROM treinos") # vai somar no SQL o total de treinos e minutos com SELECT
        total_treinos, total_minutos = cursor.fetchone()
        total_minutos = int(total_minutos) 

        print("\n" + "=" * 50)
        print("RESUMO GERAL".center(50))
        print("=" * 50)

        print(f"Total de treinos: {total_treinos}")
        print(f"Total de minutos: {total_minutos}")

        # resumo por tipo, para cada tipo um resumo
        cursor.execute("""
            SELECT tipo, COUNT(*), SUM(duracao)
            FROM treinos
            GROUP BY tipo
            ORDER BY tipo""")
        resultados = cursor.fetchall()

        print("\n" + "=" * 50)
        print("RESUMO POR TIPO".center(50))
        print("=" * 50)

        for tipo, quantidade, minutos in resultados:
            print(f"{tipo}: {quantidade} treino(s) - {minutos} min")

        cursor.close()
        conn.close()

    def editar_treino(self, tipo, data_str, novo_tipo, nova_data_str, nova_duracao, nova_intensidade):
        conn = conectar()
        if not conn:
            return

        try:
            data = datetime.strptime(data_str, '%d/%m/%Y').date()
            nova_data = datetime.strptime(nova_data_str, '%d/%m/%Y').date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/yyyy.")
            conn.close()
            return

        cursor = conn.cursor()
        try:
            # atualiza os treinos com UPDATE
            cursor.execute("""
                UPDATE treinos
                SET tipo = %s, data = %s, duracao = %s, intensidade = %s
                WHERE LOWER(tipo) = %s AND data = %s
            """, (novo_tipo.capitalize(), nova_data, nova_duracao, nova_intensidade, tipo.lower(), data))

            if cursor.rowcount == 0:
                print(f"Nenhum treino do tipo '{tipo}' encontrado na data {data_str}.")
            else:
                conn.commit()
                print(f"Treino atualizado com sucesso!")

        except Exception as e:
            conn.rollback()
            print("Erro ao editar treino:", e)
        finally:
            cursor.close()
            conn.close()