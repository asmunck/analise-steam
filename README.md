# Análise de Jogos da Steam

Projeto de análise de dados de jogos da plataforma Steam.

## Descrição

Este projeto realiza uma análise abrangente dos dados de jogos disponíveis na Steam, explorando diferentes aspectos do mercado de jogos digitais. Investigamos distribuição de preços, tendências de lançamento, categorização por gêneros, avaliações de usuários e suporte a diferentes sistemas operacionais. A análise foi dividida em fases incrementais, com foco em extração de insights valiosos para desenvolvedores e empresas do setor.

## Estrutura do Projeto

### Dados
- `data/raw/steam_games.csv`: Conjunto de dados original
- `data/processed/steam_games_processed.csv`: Dados processados e limpos para análise

### Notebooks de Análise
- `notebooks/fase1/analise_jogos-1.ipynb`: Análises iniciais e exploração de dados
- `notebooks/fase2/fun-corp.ipynb`: Análises avançadas para a empresa Fun Corp, incluindo:
    - Jogos mais bem avaliados pelo Metacritic
    - Estatísticas de jogos RPG
    - Análise de suporte a sistemas operacionais
    - Tendências de preços e avaliações

### Códigos-fonte
- `src/fase1/`: Scripts para processamento inicial dos dados
- `src/fase2/`: Scripts para análises avançadas
    - `preprocessamento.py`: Funções para limpeza e transformação dos dados
    - `visualizacao.py`: Funções para criação de visualizações personalizadas

## Funcionalidades e Insights

O projeto implementa análises como:

1. Identificação dos jogos mais bem avaliados pela crítica especializada
2. Percentual de jogos que possuem suporte para cada sistema operacional
3. Análise estatística de jogos de role-playing (DLCs, avaliações, material de demonstração)
4. Evolução anual do suporte a Linux na plataforma
5. Correlação entre preço e avaliações positivas
6. Identificação dos gêneros mais populares na plataforma
7. Análise de publicadoras com maior número de títulos e sua popularidade

## Como Executar

Para explorar as análises, você pode abrir qualquer um dos notebooks Jupyter:

```
jupyter notebook notebooks/fase2/fun-corp.ipynb
```

Para reprocessar os dados a partir do arquivo original:

```
python -m src.fase2.preprocessamento
```

## Requisitos

- Python 3.6+
- pandas
- numpy
- matplotlib
- seaborn
- jupyter notebook

## Visualizações

O projeto inclui diversas visualizações, como:
- Gráficos comparativos de sistemas operacionais
- Evolução temporal do suporte a Linux
- Distribuição de preços por gênero
- Correlação entre preço e avaliações positivas

## Autores

Desenvolvido para a disciplina de Programação para Dados da PUC.
