"""
Módulo para carregamento e manipulação de dados de jogos da Steam.

Este módulo fornece classes e funções para carregar, processar e analisar
dados de jogos da plataforma Steam.
"""

import csv
import random
from datetime import datetime
from typing import List, Dict, Optional, Union, Set, Tuple, Any


class ErroDadosJogos(Exception):
    """Exceção personalizada para erros relacionados aos dados dos jogos."""
    pass


class Jogo:
    """
    Representa um jogo com seus atributos.

    Esta classe encapsula os dados de um jogo da plataforma Steam,
    fornecendo métodos para acessar e manipular suas propriedades.

    Atributos:
        app_id (str): Identificador único do jogo na plataforma.
        nome (str): Nome do jogo.
        data_lancamento (str): Data de lançamento do jogo.
        donos_estimados (str): Número estimado de proprietários.
        preco (float): Preço do jogo em dólares.
        gratuito (bool): Indica se o jogo é gratuito.
        desenvolvedores (List[str]): Lista de desenvolvedores do jogo.
        publicadores (List[str]): Lista de publicadoras do jogo.
        generos (List[str]): Lista de gêneros do jogo.
    """

    def __init__(self, dados_jogo: Dict[str, Any]):
        """
        Inicializa um objeto Jogo com os dados fornecidos.

        Args:
            dados_jogo: Dicionário contendo os dados do jogo.
        
        Raises:
            ErroDadosJogos: Se houver um erro ao processar os dados do jogo.
        """
        try:
            self.app_id = dados_jogo.get('AppID', '')
            self.nome = dados_jogo.get('Name', '')
            self.data_lancamento = dados_jogo.get('Release date', '')
            self.donos_estimados = dados_jogo.get('Estimated owners', '')
            
            # Converte preço para float
            preco_str = dados_jogo.get('Price', '0')
            self.preco = float(preco_str) if preco_str else 0.0
            
            # Determina se o jogo é gratuito com base no preço
            self.gratuito = self.preco == 0.0
            
            # Processa listas separadas por vírgulas ou ponto e vírgula
            desenvolvedores = dados_jogo.get('Developers', '')
            self.desenvolvedores = [d.strip() for d in desenvolvedores.split(';')] if desenvolvedores else []
            
            publicadores = dados_jogo.get('Publishers', '')
            self.publicadores = [p.strip() for p in publicadores.split(';')] if publicadores else []
            
            generos = dados_jogo.get('Genres', '')
            self.generos = [g.strip() for g in generos.split(',')] if generos else []
            
        except Exception as e:
            raise ErroDadosJogos(f"Erro ao processar dados do jogo {dados_jogo.get('Name', 'desconhecido')}: {str(e)}")
    
    def __str__(self) -> str:
        """Retorna uma representação em string do jogo."""
        return f"{self.nome} (ID: {self.app_id})"
    
    def ano_lancamento(self) -> Optional[int]:
        """
        Extrai o ano de lançamento da data de lançamento.
        
        Returns:
            int ou None: O ano de lançamento se disponível, None caso contrário.
        """
        try:
            if not self.data_lancamento:
                return None
            
            # Tenta diferentes formatos de data
            formatos = ["%b %d, %Y", "%B %d, %Y", "%d %b, %Y", "%Y-%m-%d"]
            for formato in formatos:
                try:
                    data = datetime.strptime(self.data_lancamento, formato)
                    return data.year
                except ValueError:
                    continue
            
            # Tenta extrair o ano diretamente da string
            for parte in self.data_lancamento.split():
                parte = parte.strip(',.')
                if parte.isdigit() and len(parte) == 4:
                    return int(parte)
            
            return None
        except Exception:
            return None


class DadosJogos:
    """
    Classe para carregar e analisar dados de jogos da Steam.
    
    Esta classe fornece métodos para carregar dados de jogos de um arquivo CSV,
    criar amostras aleatórias e realizar análises nos dados.
    
    Atributos:
        jogos (List[Jogo]): Lista de objetos Jogo carregados.
        caminho_arquivo (str): Caminho para o arquivo CSV contendo os dados dos jogos.
    """
    
    def __init__(self, caminho_arquivo: str = None):
        """
        Inicializa um objeto DadosJogos.
        
        Args:
            caminho_arquivo (str, opcional): Caminho para o arquivo CSV. Se fornecido,
                                           os dados são carregados imediatamente.
        """
        self.jogos = []
        self.caminho_arquivo = caminho_arquivo
        if caminho_arquivo:
            self.carregar_dados(caminho_arquivo)
    
    def carregar_dados(self, caminho_arquivo: str) -> None:
        """
        Carrega dados de jogos de um arquivo CSV.
        
        Args:
            caminho_arquivo (str): Caminho para o arquivo CSV.
            
        Raises:
            ErroDadosJogos: Se houver um erro ao carregar os dados.
        """
        try:
            self.jogos = []
            self.caminho_arquivo = caminho_arquivo
            
            with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                leitor = csv.DictReader(arquivo)
                for linha in leitor:
                    try:
                        # Cria um objeto Jogo para cada linha do CSV
                        jogo = Jogo(linha)
                        self.jogos.append(jogo)
                    except Exception as e:
                        print(f"Aviso: Não foi possível processar a linha: {linha}. Erro: {e}")
                        
            if not self.jogos:
                raise ErroDadosJogos(f"Nenhum jogo foi carregado de {caminho_arquivo}")
                
        except Exception as e:
            raise ErroDadosJogos(f"Erro ao carregar dados de {caminho_arquivo}: {str(e)}")
    
    def criar_amostra(self, tamanho_amostra: int, arquivo_saida: str) -> None:
        """
        Cria uma amostra aleatória de jogos e a salva em um arquivo CSV.
        
        Args:
            tamanho_amostra (int): O número de jogos a serem incluídos na amostra.
            arquivo_saida (str): Caminho para salvar o arquivo CSV da amostra.
            
        Raises:
            ErroDadosJogos: Se houver um erro ao criar a amostra.
        """
        try:
            if not self.jogos:
                raise ErroDadosJogos("Nenhum dado de jogo carregado.")
            
            if tamanho_amostra > len(self.jogos):
                tamanho_amostra = len(self.jogos)
            
            # Seleciona jogos aleatórios para a amostra
            jogos_amostra = random.sample(self.jogos, tamanho_amostra)
            
            # Obtém os nomes dos campos do CSV original
            with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo:
                nomes_campos = csv.DictReader(arquivo).fieldnames
            
            # Cria o arquivo CSV da amostra
            with open(arquivo_saida, 'w', newline='', encoding='utf-8') as arquivo:
                escritor = csv.DictWriter(arquivo, fieldnames=nomes_campos)
                escritor.writeheader()
                
                # Abre o arquivo original para ler as linhas correspondentes aos jogos da amostra
                with open(self.caminho_arquivo, 'r', encoding='utf-8') as arquivo_original:
                    leitor = csv.DictReader(arquivo_original)
                    for linha in leitor:
                        if linha['AppID'] in [jogo.app_id for jogo in jogos_amostra]:
                            escritor.writerow(linha)
            
            print(f"Amostra de {tamanho_amostra} jogos salva em {arquivo_saida}")
        except Exception as e:
            raise ErroDadosJogos(f"Erro ao criar amostra: {str(e)}")
    
    def obter_contagem_jogos(self) -> int:
        """
        Retorna o número total de jogos carregados.
        
        Returns:
            int: Número de jogos.
        """
        return len(self.jogos)
    
    def calcular_percentual_gratuitos_vs_pagos(self) -> Dict[str, float]:
        """
        Calcula o percentual de jogos gratuitos versus pagos.
        
        Returns:
            Dict[str, float]: Dicionário com as porcentagens de jogos 'gratuitos' e 'pagos'.
            
        Raises:
            ErroDadosJogos: Se houver um erro no cálculo.
        """
        try:
            if not self.jogos:
                raise ErroDadosJogos("Nenhum dado de jogo carregado.")
            
            total_jogos = len(self.jogos)
            jogos_gratuitos = sum(1 for jogo in self.jogos if jogo.gratuito)
            jogos_pagos = total_jogos - jogos_gratuitos
            
            percentual_gratuitos = (jogos_gratuitos / total_jogos) * 100 if total_jogos > 0 else 0
            percentual_pagos = (jogos_pagos / total_jogos) * 100 if total_jogos > 0 else 0
            
            return {
                'gratuitos': round(percentual_gratuitos, 2),
                'pagos': round(percentual_pagos, 2)
            }
        except Exception as e:
            raise ErroDadosJogos(f"Erro ao calcular percentuais de jogos gratuitos vs pagos: {str(e)}")
    
    def obter_ano_com_mais_lancamentos(self) -> Union[int, List[int]]:
        """
        Encontra o ano(s) com o maior número de lançamentos de jogos.
        
        Returns:
            int ou List[int]: O ano com mais lançamentos, ou uma lista de anos em caso de empate.
            
        Raises:
            ErroDadosJogos: Se houver um erro no cálculo.
        """
        try:
            if not self.jogos:
                raise ErroDadosJogos("Nenhum dado de jogo carregado.")
            
            # Conta lançamentos por ano
            contagem_anos = {}
            for jogo in self.jogos:
                ano = jogo.ano_lancamento()
                if ano:
                    contagem_anos[ano] = contagem_anos.get(ano, 0) + 1
            
            if not contagem_anos:
                raise ErroDadosJogos("Nenhum ano de lançamento válido encontrado nos dados.")
            
            # Encontra o número máximo de lançamentos
            max_lancamentos = max(contagem_anos.values())
            
            # Encontra todos os anos com o número máximo de lançamentos
            anos_principais = [ano for ano, contagem in contagem_anos.items() if contagem == max_lancamentos]
            
            # Retorna um único ano ou uma lista de anos em caso de empate
            return anos_principais[0] if len(anos_principais) == 1 else sorted(anos_principais)
        except Exception as e:
            raise ErroDadosJogos(f"Erro ao encontrar ano com mais lançamentos: {str(e)}")