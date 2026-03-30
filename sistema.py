from treino import Treino
from database import conectar
from datetime import datetime

class SistemaTreinos:
    def adicionar_treino(self, tipo, data_str, duracao, intensidade):
        conn = conectar()
        if not conn:
            return     

        try:
            data = datetime.strptime(data_str, '%d/%m/%Y').date()
        except ValueError:
            print("Data inválida. Use o formato dd/mm/yyyy.")
            conn.close()
            return
        
        cursor = conn.cursor()
        tipo = tipo.capitalize()
        cursor.execute("""
            INSERT INTO treinos (tipo, data, duracao, intensidade)
            VALUES (%s, %s, %s, %s)
        """, (tipo, data, duracao, intensidade) )

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
        finally:
            cursor.close()
            conn.close()

    def remover_treino(self, tipo, data_str):
        conn = conectar()
        if not conn:
            return

        cursor = conn.cursor()

        data = datetime.strptime(data_str, "%d/%m/%Y").date()

        cursor.execute("""
            DELETE FROM treinos 
            WHERE LOWER(tipo) = %s AND data = %s
        """, (tipo.lower(), data))

        if cursor.rowcount == 0:
            print(f"Nenhum treino do tipo '{tipo}' encontrado na data {data_str}.")
        else:
            print(f"Treino do tipo '{tipo}' na data {data_str} removido com sucesso!")

        conn.commit()
        cursor.close()
        conn.close()

    def ver_resumo(self):
        conn = conectar()
        if not conn:
            return
        
        cursor = conn.cursor()

        #geral
        cursor.execute("SELECT COUNT(*), COALESCE(SUM(duracao), 0) FROM treinos")
        total_treinos, total_minutos = cursor.fetchone()
        total_minutos = int(total_minutos) 

        print("\n" + "=" * 50)
        print("RESUMO GERAL".center(50))
        print("=" * 50)

        print(f"Total de treinos: {total_treinos}")
        print(f"Total de minutos: {total_minutos}")

        #tipo
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