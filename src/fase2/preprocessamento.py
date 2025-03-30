import pandas as pd
import numpy as np
import re
from datetime import datetime

def preprocess_data(df):
    """
    Pré-processa o conjunto de dados de jogos da Steam.
    
    Args:
        df: DataFrame pandas com os dados brutos
        
    Returns:
        DataFrame pandas pré-processado
    """
    # Crie uma cópia para não modificar o original
    processed_df = df.copy()
    
    # Tratamento de valores ausentes no Metacritic
    processed_df['metacritic_score'] = pd.to_numeric(processed_df['metacritic_score'], errors='coerce')
    
    # Conversão da data de lançamento para datetime
    processed_df['release_date'] = pd.to_datetime(processed_df['release_date'], errors='coerce')
    
    # Extração do ano de lançamento
    processed_df['release_year'] = processed_df['release_date'].dt.year
    
    # Tratamento de campos numéricos
    numeric_columns = ['positive', 'negative', 'price', 'dlc_count']
    for col in numeric_columns:
        if col in processed_df.columns:
            processed_df[col] = pd.to_numeric(processed_df[col], errors='coerce')
    
    # Processamento dos sistemas operacionais suportados
    processed_df['supports_windows'] = processed_df['platforms'].str.contains('windows', case=False, na=False)
    processed_df['supports_mac'] = processed_df['platforms'].str.contains('mac', case=False, na=False)
    processed_df['supports_linux'] = processed_df['platforms'].str.contains('linux', case=False, na=False)
    
    # Processamento de categorias e gêneros (convertendo para listas)
    processed_df['categories_list'] = processed_df['categories'].str.split(';').fillna('').apply(lambda x: [item.strip() for item in x if item])
    processed_df['genres_list'] = processed_df['genres'].str.split(';').fillna('').apply(lambda x: [item.strip() for item in x if item])
    
    # Cálculo do material de demonstração (screenshots + movies)
    if 'screenshots' in processed_df.columns and 'movies' in processed_df.columns:
        processed_df['demo_material'] = processed_df['screenshots'].fillna(0) + processed_df['movies'].fillna(0)
    
    # Indicador de jogo pago
    processed_df['is_paid'] = processed_df['price'] > 0
    
    return processed_df

def save_processed_data(df, output_path='data/processed/steam_games_processed.csv'):
    """Salva os dados processados em CSV"""
    df.to_csv(output_path, index=False)
    print(f"Dados processados salvos em {output_path}")