from dados_jogos import DadosJogos, ErroDadosJogos, Jogo
from typing import Dict, List, Tuple, Union, Optional, Any


class AnalisadorJogos:
    """
    Classe para realizar análises em dados de jogos.
    
    Esta classe usa um objeto DadosJogos para realizar análises mais complexas
    e responder perguntas sobre o conjunto de dados de jogos.
    
    Atributos:
        dados (DadosJogos): Objeto contendo os dados dos jogos.
    """
    
    def __init__(self, arquivo_dados: str = None):
        """
        Inicializa um objeto AnalisadorJogos.
        
        Args:
            arquivo_dados (str, opcional): Caminho para o arquivo CSV com dados de jogos.
                                         Se fornecido, os dados são carregados imediatamente.
        """
        self.dados = DadosJogos(arquivo_dados) if arquivo_dados else DadosJogos()
    
    def carregar_dados(self, caminho_arquivo: str) -> None:
        """
        Carrega dados de jogos de um arquivo CSV.
        
        Args:
            caminho_arquivo (str): Caminho para o arquivo CSV.
        """
        self.dados.carregar_dados(caminho_arquivo)
    
    def criar_amostra(self, tamanho_amostra: int, arquivo_saida: str) -> None:
        """
        Cria uma amostra aleatória de jogos e a salva em um arquivo CSV.
        
        Args:
            tamanho_amostra (int): O número de jogos a serem incluídos na amostra.
            arquivo_saida (str): Caminho para salvar o arquivo CSV da amostra.
        """
        self.dados.criar_amostra(tamanho_amostra, arquivo_saida)
    
    def analisar_gratuitos_vs_pagos(self) -> Dict[str, float]:
        """
        Analisa o percentual de jogos gratuitos versus pagos.
        
        Returns:
            Dict[str, float]: Dicionário com as porcentagens de jogos gratuitos e pagos.
        """
        return self.dados.calcular_percentual_gratuitos_vs_pagos()
    
    def analisar_ano_com_mais_lancamentos(self) -> Tuple[Union[int, List[int]], int]:
        """
        Analisa qual ano teve mais lançamentos de jogos.
        
        Returns:
            Tuple[Union[int, List[int]], int]: Uma tupla contendo:
                - O ano ou lista de anos com mais lançamentos
                - O número de lançamentos nesse(s) ano(s)
        """
        anos_principais = self.dados.obter_ano_com_mais_lancamentos()
        
        # Contabiliza o número de lançamentos no(s) ano(s) de pico
        if isinstance(anos_principais, list):
            contagem_lancamentos = sum(1 for jogo in self.dados.jogos 
                                if jogo.ano_lancamento() == anos_principais[0])
        else:
            contagem_lancamentos = sum(1 for jogo in self.dados.jogos 
                                if jogo.ano_lancamento() == anos_principais)
        
        return anos_principais, contagem_lancamentos
    
    def analisar_generos_por_faixa_preco(self) -> Dict[str, Dict[str, int]]:
        """
        Analisa a distribuição de gêneros por faixa de preço.
        
        Esta é uma implementação para a terceira pergunta:
        "Qual a distribuição de gêneros de jogos por faixa de preço?"
        
        Returns:
            Dict[str, Dict[str, int]]: Um dicionário onde:
                - As chaves são faixas de preço (ex: "Gratuito", "Até R$10", etc.)
                - Os valores são dicionários com contagens de gêneros nessa faixa
        """
        if not self.dados.jogos:
            raise ErroDadosJogos("Nenhum dado de jogo carregado.")
        
        # Definição das faixas de preço
        faixas = {
            "Gratuito": (0, 0),
            "Até R$10": (0.01, 10),
            "R$10-30": (10.01, 30),
            "R$30-60": (30.01, 60),
            "Acima de R$60": (60.01, float('inf'))
        }
        
        # Inicializa o resultado
        resultado = {faixa: {} for faixa in faixas}
        
        # Analisa cada jogo
        for jogo in self.dados.jogos:
            # Determina a faixa de preço do jogo
            faixa_jogo = None
            for faixa, (preco_min, preco_max) in faixas.items():
                if preco_min <= jogo.preco <= preco_max:
                    faixa_jogo = faixa
                    break
            
            if faixa_jogo is None:
                continue  # Ignora jogos sem preço válido
            
            # Contabiliza gêneros do jogo na faixa de preço correspondente
            for genero in jogo.generos:
                if genero:  # Ignora gêneros vazios
                    if genero in resultado[faixa_jogo]:
                        resultado[faixa_jogo][genero] += 1
                    else:
                        resultado[faixa_jogo][genero] = 1
        
        # Ordena os gêneros por frequência em cada faixa de preço
        for faixa in resultado:
            resultado[faixa] = dict(sorted(
                resultado[faixa].items(), 
                key=lambda x: x[1], 
                reverse=True
            ))
        
        return resultado
    
    def obter_estatisticas_preco_por_genero(self) -> Dict[str, Dict[str, float]]:
        """
        Calcula estatísticas de preço por gênero.
        
        Esta é outra possível implementação para a terceira pergunta:
        "Quais gêneros de jogos têm o maior e menor preço médio?"
        
        Returns:
            Dict[str, Dict[str, float]]: Um dicionário onde:
                - As chaves são gêneros de jogos
                - Os valores são dicionários com estatísticas como:
                  'preco_medio', 'preco_maximo', 'preco_minimo', 'total_jogos'
        """
        if not self.dados.jogos:
            raise ErroDadosJogos("Nenhum dado de jogo carregado.")
        
        # Inicializa estruturas para armazenar dados por gênero
        precos_por_genero = {}
        
        # Coleta dados de preço por gênero
        for jogo in self.dados.jogos:
            if jogo.preco is None:
                continue  # Ignora jogos sem preço

            for genero in jogo.generos:
                if not genero:
                    continue  # Ignora gêneros vazios
                
                if genero not in precos_por_genero:
                    precos_por_genero[genero] = {
                        'precos': [],
                        'total_jogos': 0
                    }
                
                precos_por_genero[genero]['precos'].append(jogo.preco)
                precos_por_genero[genero]['total_jogos'] += 1
        
        # Calcula estatísticas para cada gênero
        resultado = {}
        for genero, dados in precos_por_genero.items():
            precos = dados['precos']
            if precos:
                resultado[genero] = {
                    'preco_medio': round(sum(precos) / len(precos), 2),
                    'preco_maximo': max(precos),
                    'preco_minimo': min(p for p in precos if p > 0) if any(p > 0 for p in precos) else 0,
                    'total_jogos': dados['total_jogos']
                }
        
        # Ordena os gêneros por preço médio (decrescente)
        resultado = dict(sorted(
            resultado.items(),
            key=lambda x: x[1]['preco_medio'],
            reverse=True
        ))
        
        return resultado

    def analisar_generos_por_faixa_preco(self) -> Dict[str, Dict[str, int]]:
        """
        Analisa a distribuição de gêneros de jogos por faixa de preço.
        
        Returns:
            Dict[str, Dict[str, int]]: Dicionário com faixas de preço como chaves e
                                    dicionários de gêneros e suas contagens como valores.
        """
        try:
            if not self.dados.jogos:
                raise ErroDadosJogos("Nenhum dado de jogo carregado.")
            
            # Define faixas de preço
            faixas = {
                "Gratuito": (0, 0),
                "Até R$10": (0.01, 10),
                "R$10-30": (10.01, 30),
                "R$30-60": (30.01, 60),
                "Acima de R$60": (60.01, float('inf'))
            }
            
            # Inicializa contadores por faixa de preço e gênero
            contagem_generos = {faixa: {} for faixa in faixas}
            
            # Analisa cada jogo
            for jogo in self.dados.jogos:
                # Determina a faixa de preço do jogo
                faixa_jogo = None
                for faixa, (min_preco, max_preco) in faixas.items():
                    if jogo.gratuito and faixa == "Gratuito":
                        faixa_jogo = faixa
                        break
                    elif min_preco <= jogo.preco <= max_preco:
                        faixa_jogo = faixa
                        break
                
                if not faixa_jogo:  # Se não encontrar faixa (improvável, mas por segurança)
                    continue
                
                # Conta os gêneros para este jogo
                for genero in jogo.generos:
                    if not genero:  # Ignora gêneros vazios
                        continue
                    contagem_generos[faixa_jogo][genero] = contagem_generos[faixa_jogo].get(genero, 0) + 1
            
            # Ordena os gêneros por contagem (decrescente) em cada faixa
            for faixa, generos in contagem_generos.items():
                contagem_generos[faixa] = dict(sorted(
                    generos.items(), 
                    key=lambda item: item[1], 
                    reverse=True
                ))
            
            return contagem_generos
        except Exception as e:
            raise ErroDadosJogos(f"Erro ao analisar gêneros por faixa de preço: {str(e)}")