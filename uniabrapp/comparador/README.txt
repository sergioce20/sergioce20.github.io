Comparador de Tábuas Biométricas — v5 MG

Como usar:
1. Abra index.html no navegador.
2. Coloque os arquivos institucionais em assets/:
   - logo-uniabrapp.svg
   - hashtag-azul-eletrico.gif
3. A página usa Plotly via CDN, portanto precisa de internet para renderizar os gráficos.

Edição rápida dos padrões:
No index.html, procure o bloco:
   // Configurações fáceis de alterar

Ali você pode alterar:
- DEFAULT_SELECTION: códigos das tábuas abertas inicialmente;
- DEFAULT_SUMMARY_AGES: idades da tabela comparativa;
- DEFAULT_HIGHLIGHT_AGE: idade do destaque;
- DEFAULT_HIGHLIGHT_METRIC: indicador do destaque;
- DEFAULT_CHART_METRIC: indicador inicial do gráfico;
- DEFAULT_TABLE_METRIC: indicador inicial da tabela.

Observação sobre IBGE 2020:
Na base usada, código 100 = IBGE 2020 Mulheres e código 101 = IBGE 2020 Homens.

Esta versão permite adicionar a mesma tábua mais de uma vez. Use isso para comparar, por exemplo, fator qx = 1,00 contra fator qx = 1,20 na mesma tábua.

Atualização v6 — exportação
- Incluídos botões de exportação em bloco recolhível "Exportação".
- Exporta gráfico atual em PNG.
- Exporta Excel completo com parâmetros, tábuas selecionadas e fatores qx, tabela resumo, detalhes da idade destaque, dados do gráfico e séries completas recalculadas.
- Exporta tabela resumo e detalhes da idade destaque em CSV.
- O Excel usa SheetJS via CDN; precisa de internet para carregar a biblioteca. Os CSVs e PNG dependem apenas da página carregada e do Plotly para o gráfico.
