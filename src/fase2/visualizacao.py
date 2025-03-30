import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

def set_custom_style():
    """Define um estilo personalizado para todos os gráficos do projeto"""
    # Cores da Steam em tons de azul e cinza
    colors = ['#1b2838', '#2a475e', '#66c0f4', '#c7d5e0', '#b8b6b4']
    
    # Configurações de estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    
    # Definições personalizadas
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.titlesize'] = 16
    plt.rcParams['axes.titleweight'] = 'bold'
    plt.rcParams['axes.labelsize'] = 14
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 12
    plt.rcParams['ytick.labelsize'] = 12
    plt.rcParams['legend.fontsize'] = 12
    plt.rcParams['figure.titlesize'] = 20
    
    # Retorna a paleta de cores para uso em gráficos
    return colors

def plot_os_support(df):
    """
    Cria o gráfico de suporte aos sistemas operacionais (Gráfico 1)
    
    Args:
        df: DataFrame pré-processado
    """
    colors = set_custom_style()
    
    # Calcular o total de "votos" para cada SO
    total_games = len(df)
    windows_count = df['supports_windows'].sum()
    mac_count = df['supports_mac'].sum()
    linux_count = df['supports_linux'].sum()
    
    # Calcular percentuais
    windows_pct = (windows_count / total_games) * 100
    mac_pct = (mac_count / total_games) * 100
    linux_pct = (linux_count / total_games) * 100
    
    # Criar gráfico
    os_names = ['Windows', 'macOS', 'Linux']
    os_values = [windows_pct, mac_pct, linux_pct]
    
    plt.figure(figsize=(10, 8))
    bars = plt.bar(os_names, os_values, color=colors[:3])
    
    # Adicionar rótulos nas barras
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height + 1,
                 f'{height:.1f}%', ha='center', va='bottom')
    
    plt.title('Percentual de Jogos por Sistema Operacional Suportado')
    plt.ylabel('Percentual de Jogos (%)')
    plt.ylim(0, 100)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    
    return plt.gcf()  # retorna a figura atual