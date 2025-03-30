import unittest
from src.fase1.analisador_jogos import AnalisadorJogos
from src.fase1.dados_jogos import ErroDadosJogos

class TesteAnalisadorJogos(unittest.TestCase):
    """Testes para a classe AnalisadorJogos."""
    
    def setUp(self):
        """Configura o ambiente de teste antes de cada teste."""
        # Carrega a amostra de jogos
        self.analisador = AnalisadorJogos("amostra_jogos.csv")
        
        # Resultados esperados baseados em cálculos manuais da amostra
        self.percentual_esperado = {
            'gratuitos': 20.0,
            'pagos': 80.0      
        }
        
        self.ano_esperado = 2022 
        self.lancamentos_esperados = 5  # Exemplo: número de lançamentos no ano de pico
    
    def test_analisar_gratuitos_vs_pagos(self):
        """Testa o cálculo de percentual de jogos gratuitos vs pagos."""
        resultado = self.analisador.analisar_gratuitos_vs_pagos()
        
        # Compara com os resultados esperados (calculados manualmente)
        self.assertAlmostEqual(resultado['gratuitos'], 
                              self.percentual_esperado['gratuitos'],
                              places=1)
        self.assertAlmostEqual(resultado['pagos'], 
                              self.percentual_esperado['pagos'],
                              places=1)
        
        # Verifica se os percentuais somam 100%
        self.assertAlmostEqual(resultado['gratuitos'] + resultado['pagos'], 
                              100.0, 
                              places=1)
    
    def test_analisar_ano_com_mais_lancamentos(self):
        """Testa a identificação do ano com mais lançamentos."""
        anos, contagem = self.analisador.analisar_ano_com_mais_lancamentos()
        
        # Lida com o caso de retorno único ou lista de anos
        if isinstance(anos, list):
            self.assertIn(self.ano_esperado, anos)
        else:
            self.assertEqual(anos, self.ano_esperado)
            
        # Verifica se a contagem está correta
        self.assertEqual(contagem, self.lancamentos_esperados)
    
    def test_analisar_generos_por_faixa_preco(self):
        """Testa a análise de gêneros por faixa de preço."""
        resultado = self.analisador.analisar_generos_por_faixa_preco()
        
        # Verifica se todas as faixas de preço estão presentes
        faixas_esperadas = ["Gratuito", "Até R$10", "R$10-30", "R$30-60", "Acima de R$60"]
        for faixa in faixas_esperadas:
            self.assertIn(faixa, resultado)
        
        # Verifica se há pelo menos um gênero em alguma faixa
        tem_generos = False
        for faixa, generos in resultado.items():
            if generos:
                tem_generos = True
                break
        
        self.assertTrue(tem_generos, "Não foram encontrados gêneros em nenhuma faixa de preço")


if __name__ == "__main__":
    unittest.main()