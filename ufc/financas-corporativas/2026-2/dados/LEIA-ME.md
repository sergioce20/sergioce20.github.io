# Pacote de dados do parecer · ED0139 Finanças Corporativas 2026-2

**Congelado em 24/08/2026 · data-base dos preços: 20/08/2026**
Prof. Sérgio Cardoso · UFC · Ciências Atuariais

Este é o pacote único de dados do trabalho em grupo (parecer). Todos os grupos
calculam sobre esta mesma base. As três regras valem o semestre inteiro:

1. **Dados congelados**: ninguém atualiza número. Parecer profissional tem
   data-base; o de vocês também.
2. **Excel e Python, o mesmo número duas vezes**: a planilha e o notebook têm
   de bater.
3. **Cotação ao vivo é proibida** no parecer: a fonte é este pacote, não o
   pregão de hoje.

## O que há em cada pasta

### `dfp2025/`

Demonstrações financeiras padronizadas (DFP) **consolidadas** do exercício
2025 das oito empresas, no padrão CVM, com os exercícios 2025 e 2024 lado a
lado. **Valores em R$ mil.**

* `por_empresa/`: um arquivo Excel por empresa, com quatro abas: Balanço
  (Ativo), Balanço (Passivo), DRE e Fluxo de Caixa (método indireto). É por
  aqui que o grupo começa.
* Os quatro CSV `dfp2025_*_con_8empresas_*.csv` trazem as oito empresas
  juntas, no formato bruto da CVM (separador `;`), para quem preferir carregar
  em Python (`pd.read_csv(..., sep=';')`).

Fonte: CVM, Dados Abertos, `dfp_cia_aberta_2025.zip`
(https://dados.cvm.gov.br/dados/CIA_ABERTA/DOC/DFP/DADOS/), acesso em 24/08/2026.

### `precos/`

Séries diárias de 5 anos (20/08/2021 a 20/08/2026, 1.248 pregões), fechamento
oficial da B3:

* `fechamentos_diarios_*.csv` / `.xlsx`: uma coluna por empresa, mais
  **BOVA11** (ETF de Ibovespa, proxy negociável do índice) e **IBOV** (o
  índice em pontos). Uso principal: retorno e beta, nas Unidades 2 e 3.
* `precos_diarios_b3_*.csv`: formato longo, com abertura, máxima, mínima,
  fechamento, negócios, quantidade e volume financeiro por dia.
* `ibovespa_diario_*.csv`: o índice isolado.

Fontes: B3, arquivos oficiais COTAHIST
(https://bvmf.bmfbovespa.com.br/InstDados/SerHist/), acesso em 24/08/2026;
Ibovespa: Ipeadata, série GM366_IBVSP366 (http://www.ipeadata.gov.br), acesso
em 24/08/2026.

**Atenção 1 · preços sem ajuste por proventos.** O fechamento é o oficial da
B3, sem ajuste por dividendos, JCP ou eventos societários. Para janelas curtas
de retorno diário isso é irrelevante; para comparações de nível de preço ao
longo dos anos, não é. O ajuste é conteúdo de aula na Unidade 2.

**Atenção 2 · evento societário no período.** A **Hapvida (HAPV3) fez
grupamento de ações 15:1**, com negociação agrupada a partir de **06/06/2025**
(InfoMoney, 2025: https://www.infomoney.com.br/mercados/hapvida-inicia-procedimentos-para-grupamento-de-acoes-na-porporcao-de-15-para-1/,
acesso em 24/08/2026). O salto de R$ 2,70 para R$ 39,91 nessa data **não é
retorno**: é mudança de unidade. Qualquer série de retornos da HAPV3 que
atravesse 06/06/2025 precisa tratar esse dia. Nenhuma das outras sete
empresas teve evento do tipo no período.

**Atenção 3 · quedas grandes que SÃO reais.** A HAPV3 teve quedas diárias
superiores a 30% em 01/03/2023, 09/03/2023, 13/11/2025 e 13/08/2026. Essas
são movimentos de mercado de verdade, não eventos societários: ficam na
série e contam no retorno e no risco. A diferença entre os dois tipos de
salto é, em si, material de aula.

### `macro/`

* `selic_diaria_sgs11_*.csv`: Selic diária (% ao dia), série SGS 11.
* `selic_meta_anual_sgs432_*.csv`: meta Selic (% ao ano), série SGS 432.
* `ipca_variacao_mensal_sgs433_*.csv`: IPCA, variação % mensal, série SGS 433.
* `macro_sgs_*.xlsx`: as três séries em um único Excel.

Fonte: Banco Central do Brasil, séries SGS (https://api.bcb.gov.br), acesso em
24/08/2026. Uso principal: proxy de taxa livre de risco e deflacionamento.

## Como citar no parecer

Indicar sempre: "Dados do pacote congelado da disciplina (24/08/2026);
fontes primárias: CVM, B3, Ipeadata e Banco Central do Brasil."
