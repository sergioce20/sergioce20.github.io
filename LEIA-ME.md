# Site sergiocardoso.pro.br

Esta pasta **é** o site. O que está aqui vai ao ar; o que não está, não vai.
Não é resultado de build: você arruma a pasta com a mão e depois publica.

Os arquivos continuam nascendo e sendo editados nas pastas das disciplinas.
Aqui entram apenas cópias, trazidas pelo comando `sincronizar`.

---

## Como publicar

**Duplo clique em `Publicar site.command`.** Abre um menu no Terminal:

```
  1  Sincronizar        trazer de fora dados e atividades que mudaram
  2  Conferir           ver o que está (ou iria) no ar
  3  Publicar           enviar o que está na pasta
  4  Sincronizar e publicar     (o caminho mais comum)

  5  Abrir a pasta do site no Finder
  6  Abrir o site no navegador
  0  Sair
```

No dia a dia é a opção **4**.

Pelo Terminal, se preferir, a partir de `~/Documents/site`:

```
python3 publicar.py sincronizar
python3 publicar.py conferir
python3 publicar.py
```

**Publicar não sincroniza, de propósito.** Você traz as cópias novas, olha,
ajusta a pasta, e só então manda. Se publicar sincronizasse, ele desfaria os
seus ajustes.

O site atualiza cerca de um minuto depois do envio.

---

## As três regras

**1. Está na pasta, está publicado.** Não há lista, marcação nem cadastro.
A pasta é a resposta. Para tirar algo do ar, tire da pasta.

**2. Nome começando com `_` some de verdade.** Arquivo ou pasta, em qualquer
nível. Não vai ao site **nem ao GitHub**, porque está no `.gitignore`.
Use `_oculto/` para tirar algo do ar sem apagar.

**3. Nome suspeito trava a publicação.** Arquivo cujo nome contenha
*gabarito*, *prova*, *presenc*, *notas_*, *conceito* ou *matricula* faz a
publicação **parar**, sem enviar nada, com a lista na tela. Não é aviso, é
bloqueio. Renomeie ou mova para uma pasta `_`.

---

## Índice automático

Uma pasta só ganha um `index.html` gerado se tiver dentro dela um arquivo
vazio chamado **`_gerar_indice`**. O título da página vem de **`_titulo.txt`**.

Sem esse marcador, a página é sua e o script nunca encosta nela. É isso que
permite escrever páginas à mão sem medo de perdê-las na próxima publicação.

---

## O que fica aqui e o que vai para o SIGAA

**Só fica no site o que o SIGAA não consegue entregar:**

- **os dados**, porque o notebook precisa lê-los por URL, e
- **os notebooks**, porque o Colab só abre a partir de repositório público.

Slides, textos, planilhas, prazos e avisos vão para o SIGAA. Publicar nos dois
lugares cria duas versões do mesmo arquivo, e uma delas envelhece sem avisar.

Uma consequência que vale lembrar: **o repositório é público.** Estrutura de
pastas não esconde nada, e arquivo publicado por engano fica no histórico do
git para sempre. A proteção real é não publicar.

---

## Estrutura das pastas

```
site/
  index.html                    página inicial (escrita à mão)
  assets/estilo.css             o desenho do site inteiro
  publicar.py                   o script
  Publicar site.command         o menu de duplo clique
  LEIA-ME.md                    este arquivo
  CNAME                         o domínio (não apagar)
  .nojekyll                     não apagar

  ufc/<disciplina>/<periodo>/   uma pasta por disciplina e semestre
      index.html                página da disciplina (à mão)
      atividades/               notebooks; índice gerado
      dados/                    bases congeladas; índice gerado

  colab/<disciplina>/<NN>/      endereço curto que abre o notebook no Colab
      index.html

  _oculto/                      nada daqui vai ao ar nem ao GitHub
```

O endereço segue a pasta. `ufc/financas-corporativas/2026-2/dados/` no disco é
`sergiocardoso.pro.br/ufc/financas-corporativas/2026-2/dados/` no ar.

---

## Exemplo completo: acrescentar ED0145

**Práticas Simuladas em Atuária · ED0145 · 2026.2**

Essa disciplina já tem convenção própria, declarada no `LEIA-ME.md` dela:
a pasta **`publicar/`** é o "espelho do Google Drive da turma" e vai inteira.
É o mesmo modelo desta pasta aqui, então o encaixe é direto: sincronizamos
`publicar/` e pronto. Não é preciso `_ALUNO` no nome.

Ela já vem organizada por dentro, com `publicar/dados/` e `publicar/material/`,
então basta espelhar a pasta toda e a estrutura se mantém.

> ### ATENÇÃO, e isto não é detalhe
>
> A disciplina tem também uma pasta **`publicar_alunos/`**, com uma subpasta por
> aluno (`aluno_1`, `aluno_2`, …). **Ela nunca pode entrar aqui.** Material
> individualizado num site público expõe o trabalho de cada aluno para qualquer
> pessoa, e o histórico do git não esquece.
>
> Sincronize **`publicar/`**, nunca `publicar_alunos/`. Se um dia precisar
> entregar material individual, o canal é o SIGAA ou o Drive, com acesso
> restrito, não este site.

### 1. Ensinar o script a trazer os arquivos

Abra `publicar.py` e, logo abaixo das linhas do Finanças Corporativas,
acrescente:

```python
PS = UFC / "praticas_simuladas/2026-2"
DESTINO_PS = "ufc/praticas-simuladas/2026-2"
```

e, dentro da lista `SINCRONIZAR`, mais uma entrada, espelhando a pasta inteira:

```python
    {"de": PS / "publicar", "para": DESTINO_PS, "glob": "**/*",
     "descricao": "material da turma de Práticas Simuladas"},
```

Isso traz `publicar/dados/` e `publicar/material/` já na estrutura certa.

### 2. Criar as pastas e ligar o índice automático

No Terminal:

```
cd ~/Documents/site
mkdir -p ufc/praticas-simuladas/2026-2/dados
touch    ufc/praticas-simuladas/2026-2/dados/_gerar_indice
echo "Dados · Práticas Simuladas 2026.2" > ufc/praticas-simuladas/2026-2/dados/_titulo.txt
```

Repita para `material/` se quiser índice gerado também nessa pasta.

### 3. Escrever a página da disciplina

Copie `ufc/financas-corporativas/2026-2/index.html` para
`ufc/praticas-simuladas/2026-2/index.html` e troque o título, o código da
disciplina e os links. É HTML simples; se preferir, me peça.

### 4. Pôr a disciplina na página inicial

No `index.html` da raiz, dentro da lista de disciplinas:

```html
    <li>
      <a href="/ufc/praticas-simuladas/2026-2/">Práticas Simuladas em Atuária</a>
      <span class="detalhe">ED0145 · Ciências Atuariais · UFC · 2026.2</span>
    </li>
```

### 5. Criar o endereço curto do Colab, se houver notebook

```
mkdir -p colab/praticas/01
```

e dentro, um `index.html` copiado de `colab/fincorp/04/index.html`, trocando
apenas o caminho do notebook no `meta refresh` e no link.

### 6. Sincronizar, conferir e publicar

Duplo clique em `Publicar site.command`, opção **1**, depois **2** para olhar
o que veio, e **3** para publicar.

### Antes de fazer isso, duas decisões

**As amostras de ED0145 não estão congeladas como as de Finanças Corporativas.**
Elas são geradas por `base/scripts/`. Se os alunos forem ler dados por URL, a
data de congelamento precisa estar no nome do arquivo, como em
`amostra_g3_congelada_2026-09-01.csv`. Sem isso, um resultado deixa de ser
reproduzível no dia em que a base for regerada, e a disciplina inteira perde a
rastreabilidade que Finanças Corporativas tem.

**Hoje o material dela vai para o Google Drive.** Trazer para o site só faz
sentido se substituir o Drive, não se conviver com ele: material em dois
lugares é a mesma armadilha das duas versões. Decida qual dos dois é o canal.

---

## Quando algo dá errado

**A publicação parou dizendo BLOQUEADO.** Um arquivo tem nome suspeito. Ele
aparece na lista. Renomeie ou mova para `_oculto/`. Nada foi enviado.

**"Updates were rejected" ou erro de git.** O GitHub também escreve neste
repositório sozinho. O script já integra antes de enviar; se ainda assim der
erro, me chame em vez de forçar.

**Mudei uma página e o site continua igual.** Espere um minuto e recarregue.
A folha de estilo é carimbada com a versão a cada publicação, então cache de
CSS não é mais um problema.

**O link do Colab não abre.** O notebook precisa estar no site (é o que o
publica no repositório público). Confira com a opção **2** do menu.

**Apaguei algo sem querer.** Tudo que já foi publicado está no histórico do
GitHub. Me diga o que era e a data, que eu recupero. O que estava em `_oculto/`
nunca foi para lá, então esse não tem volta.
