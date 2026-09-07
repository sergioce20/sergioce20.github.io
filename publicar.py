#!/usr/bin/env python3
"""
Publica o site sergiocardoso.pro.br.

DUAS TRAVAS, e as duas precisam passar para um arquivo ir para o ar:

  1. NOME: o arquivo precisa ter "_ALUNO" no nome (ou estar em dados/).
  2. LIBERAÇÃO: a pasta da aula precisa estar listada no PUBLICAR.txt da
     disciplina, sem o "#" na frente.

Aula nova, semestre novo ou disciplina nova NÃO vão para o ar sozinhos.
O padrão é não publicar. Publicar é um ato deliberado.

Uso:  python3 publicar.py             (monta e envia)
      python3 publicar.py --so-montar (monta e mostra o relatório, sem enviar)
"""
import html, shutil, subprocess, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
UFC = Path.home() / "Documents/UFC/disciplinas"
REPO = "sergioce20/sergioce20.github.io"
RAMO = "main"

INSTITUICOES = {"ufc": "Universidade Federal do Ceará"}

# chave: (instituicao, disciplina, periodo)
DISCIPLINAS = {
    ("ufc", "financas-corporativas", "2026-2"): {
        "titulo": "Finanças Corporativas",
        "codigo": "ED0139",
        "curso": "Ciências Atuariais",
        "origem": UFC / "financas_corporativas/2026-2",
    },
}

ROTULO = {".html": "slides", ".pdf": "PDF", ".xlsx": "Excel", ".docx": "Word",
          ".zip": "pacote", ".csv": "CSV"}

CABECA_MANIFESTO = """\
# QUAIS AULAS ESTÃO PUBLICADAS NO SITE
#
# Uma pasta por linha. Linha com "#" na frente NÃO é publicada.
# Pasta que não estiver aqui também NÃO é publicada, mesmo que tenha
# arquivos _ALUNO. Aula nova nasce fechada: para liberar, tire o "#"
# (ou acrescente a linha) e rode  python3 publicar.py
#
# A pasta dados/ é publicada sempre, junto com a disciplina.
"""


def tamanho(p):
    n = p.stat().st_size
    for u in ("B", "KB", "MB"):
        if n < 1024 or u == "MB":
            return f"{n:.1f} {u}".replace(".0 ", " ")
        n /= 1024


def titulo_aula(nome):
    partes = nome.split("_")
    if partes[0].isdigit():
        resto = " ".join(partes[1:]).replace("-", " ")
        return f"Aula {partes[0]} · {resto[:1].upper() + resto[1:]}"
    return nome.replace("_", " ").capitalize()


def pastas_de_aula(origem):
    return sorted(
        [d for d in (origem / "aulas").glob("*") if d.is_dir()] +
        [d for d in (origem / "capsulas").glob("*") if d.is_dir()],
        key=lambda d: d.name
    )


def ler_manifesto(origem):
    """Devolve (liberadas, existentes). Cria o arquivo na primeira vez."""
    arq = origem / "PUBLICAR.txt"
    existentes = [d.name for d in pastas_de_aula(origem)]
    if not arq.exists():
        arq.write_text(CABECA_MANIFESTO + "\n" +
                       "\n".join(f"# {n}" for n in existentes) + "\n",
                       encoding="utf-8")
        print(f"  ! criei {arq} com TUDO fechado. Libere o que for público e rode de novo.")
        return set(), existentes
    liberadas = {
        linha.strip() for linha in arq.read_text(encoding="utf-8").splitlines()
        if linha.strip() and not linha.strip().startswith("#")
    }
    return liberadas, existentes


def pagina(titulo, subtitulo, corpo, voltar, rotulo_voltar):
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(titulo)} · Sérgio Cardoso</title>
<link rel="stylesheet" href="/assets/estilo.css">
</head>
<body>
<header class="capa">
  <p class="papel"><a href="{voltar}">← {html.escape(rotulo_voltar)}</a></p>
  <h1>{html.escape(titulo)}</h1>
  <p class="papel">{html.escape(subtitulo)}</p>
</header>
<main>
{corpo}
</main>
<footer><p>Material didático sob licença
<a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br">CC BY 4.0</a>,
salvo indicação em contrário no próprio arquivo.</p></footer>
</body>
</html>
"""


def link_arquivo(base_url, caminho_repo, nome, ext):
    """Notebook vira botão do Colab; o resto vira link para o arquivo."""
    if ext == ".ipynb":
        colab = (f"https://colab.research.google.com/github/{REPO}/blob/{RAMO}/"
                 f"{caminho_repo}/{nome}")
        return (f'<a class="colab" href="{colab}" target="_blank" rel="noopener">'
                f'Abrir no Colab</a>'
                f' <a class="secundario" href="{base_url}/{nome}">baixar .ipynb</a>')
    return f'<a href="{base_url}/{nome}">{ROTULO.get(ext, ext.lstrip("."))}</a>'


def montar_disciplina(chave, info):
    inst, disc, periodo = chave
    origem = info["origem"]
    raiz_url = f"/{inst}/{disc}/{periodo}"
    raiz_dir = SITE / inst / disc / periodo
    if raiz_dir.exists():
        shutil.rmtree(raiz_dir)
    (raiz_dir / "aulas").mkdir(parents=True)

    liberadas, existentes = ler_manifesto(origem)
    publicadas, retidas = [], []

    for pasta in pastas_de_aula(origem):
        arquivos = [f for f in pasta.rglob("*_ALUNO*")
                    if f.is_file() and "arquivos_antigos" not in f.parts]
        if pasta.name not in liberadas:
            if arquivos:
                retidas.append((pasta.name, len(arquivos)))
            continue
        if not arquivos:
            retidas.append((pasta.name, 0))
            continue
        destino = raiz_dir / "aulas" / pasta.name
        destino.mkdir(parents=True, exist_ok=True)
        itens = []
        for f in sorted(arquivos):
            shutil.copy2(f, destino / f.name)
            itens.append((f.name, f.suffix.lower()))
        publicadas.append((titulo_aula(pasta.name), pasta.name, itens))

    for nome in liberadas - set(existentes):
        print(f"  ! {origem.name}/PUBLICAR.txt cita '{nome}', que não existe")

    # índice das aulas
    linhas = []
    for titulo, pasta, itens in publicadas:
        base = f"{raiz_url}/aulas/{pasta}"
        repo_rel = f"{inst}/{disc}/{periodo}/aulas/{pasta}"
        links = " · ".join(link_arquivo(base, repo_rel, n, e) for n, e in itens)
        linhas.append(f'<li><span class="item-titulo">{html.escape(titulo)}</span>'
                      f'<span class="detalhe">{links}</span></li>')
    corpo = ('<section><p class="nota">Material do aluno. Os arquivos de apoio do '
             'professor não são publicados.</p><ul class="lista">' + "".join(linhas) +
             '</ul></section>'
             f'<section><h2>Dados</h2><p class="nota">Bases congeladas usadas nas '
             f'atividades.</p><ul class="lista"><li>'
             f'<a href="{raiz_url}/dados/">Pacote de dados {periodo}</a>'
             f'<span class="detalhe">DFP, preços da B3 e séries do Banco Central</span>'
             f'</li></ul></section>')
    sub = f'{info["codigo"]} · {info["curso"]} · {INSTITUICOES[inst]} · {periodo}'
    (raiz_dir / "index.html").write_text(
        pagina(info["titulo"], sub, corpo, "/", "Sérgio Cardoso"), encoding="utf-8")

    # dados
    destino_dados = raiz_dir / "dados"
    shutil.copytree(origem / "dados", destino_dados,
                    ignore=shutil.ignore_patterns(".DS_Store"))
    secoes = []
    for sub_dir in sorted([p for p in destino_dados.iterdir() if p.is_dir()]) + [destino_dados]:
        arqs = sorted(f for f in sub_dir.glob("*") if f.is_file() and f.name != "index.html")
        if not arqs:
            continue
        rel = "" if sub_dir == destino_dados else sub_dir.name + "/"
        nome = "raiz" if sub_dir == destino_dados else sub_dir.name
        tr = "".join(f'<tr><td><a href="{raiz_url}/dados/{rel}{html.escape(f.name)}">'
                     f'{html.escape(f.name)}</a></td><td>{tamanho(f)}</td></tr>' for f in arqs)
        secoes.append(f"<h2>{html.escape(nome)}</h2>"
                      f"<table><tr><th>arquivo</th><th>tamanho</th></tr>{tr}</table>")
    corpo_d = ('<section><p class="nota">Bases congeladas na data indicada no nome do '
               'arquivo. No Python, use o endereço completo do arquivo como caminho. '
               'Os CSV da DFP usam ponto e vírgula como separador '
               '(<code>sep=";"</code>).</p>' + "".join(secoes) + "</section>")
    (destino_dados / "index.html").write_text(
        pagina(f'Dados · {info["titulo"]}', sub, corpo_d, raiz_url, info["titulo"]),
        encoding="utf-8")

    return publicadas, retidas, raiz_url, sub


def indice_geral(entradas):
    por_inst = {}
    for (inst, disc, periodo), info, url, sub in entradas:
        por_inst.setdefault(inst, []).append((info, url, periodo))
    secoes = []
    for inst, itens in por_inst.items():
        linhas = "".join(
            f'<li><a href="{url}">{html.escape(i["titulo"])}</a>'
            f'<span class="detalhe">{html.escape(i["codigo"])} · '
            f'{html.escape(i["curso"])} · {periodo}</span></li>'
            for i, url, periodo in sorted(itens, key=lambda t: t[2], reverse=True))
        secoes.append(f'<section><h2>{html.escape(INSTITUICOES[inst])}</h2>'
                      f'<ul class="lista">{linhas}</ul></section>')
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sérgio Cardoso</title>
<link rel="stylesheet" href="/assets/estilo.css">
</head>
<body>
<header class="capa">
  <h1>Sérgio Cardoso</h1>
  <p class="papel">Atuário (MIBA 2.285) · Professor de Ciências Atuariais</p>
</header>
<main>
<p class="nota">Material didático das disciplinas em andamento: slides, roteiros de
atividade e bases de dados congeladas.</p>
{"".join(secoes)}
</main>
<footer><p>Material didático sob licença
<a href="https://creativecommons.org/licenses/by/4.0/deed.pt-br">CC BY 4.0</a>,
salvo indicação em contrário no próprio arquivo.</p></footer>
</body>
</html>
"""


def main():
    # limpa a estrutura antiga
    for velho in ("aulas", "dados"):
        p = SITE / velho
        if p.exists():
            shutil.rmtree(p)

    entradas, total_ret = [], 0
    for chave, info in DISCIPLINAS.items():
        if not info["origem"].exists():
            print(f"  ! origem não encontrada: {info['origem']}")
            continue
        pub, ret, url, sub = montar_disciplina(chave, info)
        entradas.append((chave, info, url, sub))
        print(f"\n  {'/'.join(chave)}")
        for titulo, pasta, itens in pub:
            print(f"    PUBLICADA  {pasta}  ({len(itens)} arquivos)")
        for pasta, n in ret:
            motivo = "fechada no PUBLICAR.txt" if n else "sem arquivo _ALUNO"
            print(f"    retida     {pasta}  ({n} arquivos, {motivo})")
        total_ret += len(ret)

    (SITE / "index.html").write_text(indice_geral(entradas), encoding="utf-8")
    print(f"\n  {len(entradas)} disciplina(s) no ar, {total_ret} pasta(s) retida(s)")

    if "--so-montar" in sys.argv:
        print("  (envio desligado)")
        return
    subprocess.run(["git", "add", "-A"], cwd=SITE, check=True)
    if subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=SITE).returncode == 0:
        print("  nada mudou, nada a enviar")
        return
    subprocess.run(["git", "commit", "-m", "atualiza publicação"], cwd=SITE, check=True)
    subprocess.run(["git", "push"], cwd=SITE, check=True)
    print("  enviado. o site atualiza em cerca de um minuto")


if __name__ == "__main__":
    main()
