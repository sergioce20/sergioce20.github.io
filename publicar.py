#!/usr/bin/env python3
"""
Publica o site sergiocardoso.pro.br.

REGRA DE OURO: só é publicado o que tem "_ALUNO" no nome do arquivo,
mais a pasta de dados congelados. Gabarito, prova e lista de presença
nunca têm "_ALUNO" no nome, então nunca sobem. Pastas "arquivos_antigos"
são sempre ignoradas.

Uso:  python3 publicar.py            (monta e envia)
      python3 publicar.py --so-montar (monta e não envia)
"""
import html, shutil, subprocess, sys
from pathlib import Path

SITE = Path(__file__).resolve().parent
UFC = Path.home() / "Documents/UFC/disciplinas"

DISCIPLINAS = {
    "financas-corporativas": {
        "titulo": "Finanças Corporativas (ED0139)",
        "subtitulo": "Ciências Atuariais · UFC · 2026.2",
        "origem": UFC / "financas_corporativas/2026-2",
    },
}

ROTULO = {".html": "página", ".pdf": "PDF", ".xlsx": "Excel", ".docx": "Word",
          ".ipynb": "notebook", ".zip": "pacote", ".csv": "CSV"}


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
    return nome.replace("_", " ")


def pagina(titulo, subtitulo, corpo, voltar="/"):
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
  <p class="papel"><a href="{voltar}">Sérgio Cardoso</a></p>
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

def coletar_aula(origem, destino_disc, slug):
    """Copia os arquivos _ALUNO de cada aula e cápsula. Devolve o índice."""
    grupos = []
    fontes = sorted(
        [d for d in (origem / "aulas").glob("*") if d.is_dir()] +
        [d for d in (origem / "capsulas").glob("*") if d.is_dir()]
    )
    for pasta in fontes:
        arquivos = [
            f for f in pasta.rglob("*_ALUNO*")
            if f.is_file() and "arquivos_antigos" not in f.parts
        ]
        if not arquivos:
            continue
        destino = destino_disc / pasta.name
        destino.mkdir(parents=True, exist_ok=True)
        itens = []
        for f in sorted(arquivos):
            shutil.copy2(f, destino / f.name)
            itens.append((f.name, f.suffix.lower(), tamanho(f)))
        grupos.append((titulo_aula(pasta.name), pasta.name, itens))
    return grupos


def indice_aulas(grupos, slug, info):
    linhas = []
    for titulo, pasta, itens in grupos:
        links = " · ".join(
            f'<a href="/aulas/{slug}/{pasta}/{html.escape(n)}">'
            f'{ROTULO.get(ext, ext.lstrip("."))}</a> <span class="detalhe-inline">{t}</span>'
            for n, ext, t in itens
        )
        linhas.append(
            f'<li><span class="item-titulo">{html.escape(titulo)}</span>'
            f'<span class="detalhe">{links}</span></li>'
        )
    corpo = ('<section><p class="nota">Versões para o aluno. Os arquivos de apoio do professor '
             'não são publicados.</p><ul class="lista">' + "".join(linhas) + "</ul></section>")
    return pagina(info["titulo"], info["subtitulo"], corpo)


def indice_dados(destino_dados, slug, info):
    secoes = []
    for sub in sorted([p for p in destino_dados.iterdir() if p.is_dir()]) + [destino_dados]:
        arquivos = sorted(f for f in sub.glob("*") if f.is_file() and f.name != "index.html")
        if not arquivos:
            continue
        rel = "" if sub == destino_dados else sub.name + "/"
        nome = "raiz" if sub == destino_dados else sub.name
        linhas = "".join(
            f'<tr><td><a href="/dados/{slug}/{rel}{html.escape(f.name)}">'
            f'{html.escape(f.name)}</a></td><td>{tamanho(f)}</td></tr>'
            for f in arquivos
        )
        secoes.append(f"<h2>{html.escape(nome)}</h2>"
                      f"<table><tr><th>arquivo</th><th>tamanho</th></tr>{linhas}</table>")
    corpo = ('<section><p class="nota">Bases congeladas na data indicada no nome do arquivo. '
             'Para ler direto no Python, use o endereço completo do arquivo como caminho.</p>'
             + "".join(secoes) + "</section>")
    return pagina("Dados · " + info["titulo"], info["subtitulo"], corpo)


def main():
    for slug, info in DISCIPLINAS.items():
        origem = info["origem"]
        if not origem.exists():
            print(f"  ! origem não encontrada: {origem}")
            continue
        destino_aulas = SITE / "aulas" / slug
        destino_dados = SITE / "dados" / slug
        for d in (destino_aulas, destino_dados):
            if d.exists():
                shutil.rmtree(d)
            d.mkdir(parents=True)

        grupos = coletar_aula(origem, destino_aulas, slug)
        (destino_aulas / "index.html").write_text(indice_aulas(grupos, slug, info), encoding="utf-8")
        print(f"  aulas/{slug}: {sum(len(g[2]) for g in grupos)} arquivos em {len(grupos)} aulas")

        shutil.copytree(origem / "dados", destino_dados, dirs_exist_ok=True,
                        ignore=shutil.ignore_patterns(".DS_Store"))
        (destino_dados / "index.html").write_text(indice_dados(destino_dados, slug, info), encoding="utf-8")
        print(f"  dados/{slug}: {sum(1 for _ in destino_dados.rglob('*') if _.is_file())} arquivos")

    if "--so-montar" in sys.argv:
        print("montado (envio desligado)")
        return
    subprocess.run(["git", "add", "-A"], cwd=SITE, check=True)
    r = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=SITE)
    if r.returncode == 0:
        print("nada mudou, nada a enviar")
        return
    subprocess.run(["git", "commit", "-m", "atualiza publicação"], cwd=SITE, check=True)
    subprocess.run(["git", "push"], cwd=SITE, check=True)
    print("enviado. o site atualiza em cerca de um minuto")


if __name__ == "__main__":
    main()
