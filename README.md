# analise-steam

Projeto de análise de dados de jogos da plataforma Steam.

## Descrição

Este projeto realiza uma análise dos dados de jogos disponíveis na Steam, explorando diferentes aspectos do mercado de jogos digitais como distribuição de preços, anos de lançamento e categorização por gêneros. A implementação foi feita utilizando apenas bibliotecas básicas do Python, com foco em programação orientada a objetos e manipulação eficiente de dados.

## Estrutura do Projeto

- dados_jogos.py: Classes para carregamento e manipulação dos dados de jogos
- analisador_jogos.py: Implementação das análises e processamento dos dados
- criar_amostra.py: Script para criar uma amostra aleatória do conjunto de dados
- teste_analisador_jogos.py: Testes unitários para validar as funcionalidades
- analise_jogos.ipynb: Notebook Jupyter com demonstração das análises
- steam_games.csv: Conjunto de dados completo (gerenciado com Git LFS)
- amostra_jogos.csv: Amostra reduzida para testes e validação

## Funcionalidades

O projeto implementa análises como:

1. Percentual de jogos gratuitos versus pagos na plataforma
2. Identificação do ano com maior número de lançamentos
3. Análise de gêneros de jogos por faixa de preço
4. Estatísticas de preço por gênero

## Como Executar

Para criar uma amostra do conjunto de dados:
```
python criar_amostra.py
```

Para executar os testes:
```
python -m unittest teste_analisador_jogos.py
```

Para explorar as análises, abra o notebook Jupyter:
```
jupyter notebook analise_jogos.ipynb
```

## Requisitos

- Python 3.6+
- Bibliotecas padrão do Python (csv, random, datetime)
- Jupyter Notebook (opcional, para explorar o notebook de análise)

## Autores

Desenvolvido para a disciplina de Programação para Dados da PUC.
