import pandas as pd
import numpy as np
from datetime import datetime

def preprocess_data(df):
    # Pré-processa o conjunto de dados de jogos da Steam.
    processed_df = df.copy()
    
    # Tratamento do Metacritic score
    processed_df['metacritic_score'] = pd.to_numeric(processed_df['Metacritic score'], errors='coerce')
    
    # Conversão da data de lançamento para datetime
    processed_df['release_date'] = pd.to_datetime(processed_df['Release date'], errors='coerce')
    processed_df['release_year'] = processed_df['release_date'].dt.year
    
    # Tratamento de campos numéricos
    processed_df['positive'] = pd.to_numeric(processed_df['Positive'], errors='coerce')
    processed_df['negative'] = pd.to_numeric(processed_df['Negative'], errors='coerce')
    processed_df['price'] = pd.to_numeric(processed_df['Price'], errors='coerce')
    processed_df['dlc_count'] = pd.to_numeric(processed_df['DLC count'], errors='coerce')
    
    # Usar as colunas de plataforma que já existem
    processed_df['supports_windows'] = processed_df['Windows'].astype(bool)
    processed_df['supports_mac'] = processed_df['Mac'].astype(bool)
    processed_df['supports_linux'] = processed_df['Linux'].astype(bool)
    
    # Processamento de categorias e gêneros
    processed_df['categories_list'] = processed_df['Categories'].str.split(';').fillna('').apply(lambda x: [item.strip() for item in x if item])
    processed_df['genres_list'] = processed_df['Genres'].str.split(';').fillna('').apply(lambda x: [item.strip() for item in x if item])
    
    # Cálculo do material de demonstração (screenshots + movies)
    processed_df['screenshots'] = pd.to_numeric(processed_df['Screenshots'], errors='coerce').fillna(0)
    processed_df['movies'] = pd.to_numeric(processed_df['Movies'], errors='coerce').fillna(0)
    processed_df['demo_material'] = processed_df['screenshots'] + processed_df['movies']
    
    # Indicador de jogo pago
    processed_df['is_paid'] = processed_df['price'] > 0
    
    # Manter colunas originais importantes
    processed_df['name'] = processed_df['Name']
    processed_df['publisher'] = processed_df['Publishers']
    processed_df['developer'] = processed_df['Developers']
    
    return processed_df

def save_processed_data(df, output_path='../../data/processed/steam_games_processed.csv'):
    """Salva os dados processados em CSV"""
    import os
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    df.to_csv(output_path, index=False)
    print(f"Dados processados salvos em {output_path}")