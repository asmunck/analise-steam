from src.fase1.analisador_jogos import AnalisadorJogos

def main():
    """
    Função principal que cria uma amostra de 20 jogos.
    """
    try:
        # Substitua pelo caminho do seu arquivo de dados
        arquivo_dados = 'steam_games.csv'
        arquivo_amostra = 'amostra_jogos.csv'
        
        # Cria o analisador e gera a amostra
        analisador = AnalisadorJogos(arquivo_dados)
        analisador.criar_amostra(20, arquivo_amostra)
        
        print(f"Amostra de 20 jogos criada com sucesso no arquivo '{arquivo_amostra}'.")
        print("Use esta amostra para validar manualmente os resultados e criar os testes.")
        
    except Exception as e:
        print(f"Erro ao criar amostra: {str(e)}")

if __name__ == "__main__":
    main()